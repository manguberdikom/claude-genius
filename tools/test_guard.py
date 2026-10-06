#!/usr/bin/env python3
"""guard.py uchun sinovlar.

    python3 tools/test_guard.py [-k matn] [--vaqt [ms]]

Sinov matnlari shu faylda turadi, Bash buyrug'ida emas: aks holda guard
o'z sinovini haqiqiy chaqiruv deb to'sib qo'yadi.
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GUARD = os.path.join(HERE, "guard.py")

# Hook faqat Java proyektida yoki klonning o'zida ishlaydi
# (hookio.active). Sinovlar vaqtinchalik papkada yuradi, shu yerda esa
# tekshirilayotgan narsa gating emas: ildiz klonga qo'yiladi. Gating ning
# o'z sinovlari tools/test_hookio.py da va shu fayldagi alohida
# holatlarda.
os.environ["CLAUDE_PROJECT_DIR"] = ROOT

# Sinov standart chegarani o'lchaydi: muhitdagi DOC_MAX_* uni o'zgartirib,
# o'nlab chalg'ituvchi XATO bermasin. guard subprocess i ham shu muhitni oladi.
for _key in [k for k in os.environ if k.startswith("DOC_MAX_")]:
    del os.environ[_key]
sys.path.insert(0, HERE)
import guard as G  # noqa: E402
import testkit  # noqa: E402

# Chegaradan ancha katta bob (guard.py MAX_BYTES).
BIG = "docs/patterns/25-anti-patternlar.md"
# Chegaradan katta, lekin satri kam bob: eski 1200 satr chegarasi uni
# to'liq o'qishga ruxsat berardi.
MID = "docs/patterns/23-testing-patternlari.md"
# Chegaradan kichik bob.
SMALL = "docs/clean-code/43-professional-masuliyat.md"
OTHER_CWD = tempfile.gettempdir()


def line_count(path):
    try:
        with open(os.path.join(ROOT, path), "rb") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0  # main() yo'q fixture ni alohida aytadi


def bash(command):
    return {"tool_name": "Bash", "tool_input": {"command": command}}


def sub(command):
    """Subagent ichidagi chaqiruv: payloadda agent_id bor."""
    return dict(bash(command), agent_id="a0637d1b6b9967aea")


# ask: pul va vaqt sarflaydigan amal, qarorni odam qiladi.
# deny: kontekstni himoya qiladi, arzon yo'l har doim bir xil.
DENY, ALLOW, ASK = "deny", "allow", "ask"

# (nom, kutilgan, payload [, cwd]). cwd berilmasa ROOT.
CASES = [
    ("katta bob, chegarasiz Read", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": BIG}}),
    ("katta bob, limit=60", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "limit": 60}}),
    ("katta bob, limit=9000", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "limit": 9000}}),
    # Satr emas, bayt: zich bobda 300 satr chegaradan oshadi.
    ("katta bob, limit=300", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "limit": 300}}),
    ("katta bob, offset=100 limit=40", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "offset": 100, "limit": 40}}),
    ("katta bob oxiri, limitsiz", ALLOW,
     {"tool_name": "Read", "tool_input":
      {"file_path": BIG, "offset": line_count(BIG) - 20}}),
    ("o'rta bob, chegarasiz Read", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": MID}}),
    ("o'rta bob, limit=100", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": MID, "limit": 100}}),
    ("o'rta bob, limit=400", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": MID, "limit": 400}}),
    ("kichik bob, chegarasiz Read", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": SMALL}}),
    # Read asbobi yo'lni doim mutlaq yuboradi.
    ("katta bob, mutlaq yo'l", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": os.path.join(ROOT, BIG)}}),
    ("katta bob, mutlaq yo'l, limit=60", ALLOW,
     {"tool_name": "Read", "tool_input":
      {"file_path": os.path.join(ROOT, BIG), "limit": 60}}),
    ("boshqa cwd, mutlaq yo'l", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": os.path.join(ROOT, BIG)}},
     OTHER_CWD),
    # watched_path() dagi ROOT zaxirasi: cwd boshqa bo'lsa ham nisbiy yo'l topiladi.
    ("boshqa cwd, nisbiy yo'l", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": BIG}}, OTHER_CWD),
    ("docs tashqarisidagi fayl", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": "README.md"}}),
    ("mavjud bo'lmagan fayl", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": "docs/yoq.md"}}),
    ("katta bobni cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat " + BIG}}),
    ("katta bobni cat, mutlaq yo'l", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat " + os.path.join(ROOT, BIG)}}),
    ("o'rta bobni cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat " + MID}}),
    ("kichik bobni cat", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "cat " + SMALL}}),
    ("less", DENY, {"tool_name": "Bash", "tool_input": {"command": "less " + BIG}}),
    ("tac", DENY, {"tool_name": "Bash", "tool_input": {"command": "tac " + BIG}}),
    ("quvur ichidagi cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "x; cat " + BIG + " | tail -3"}}),
    # Buyruqlar yangi satr bilan ajratilsa ham ko'rinadi.
    ("yangi satrdan keyingi cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "echo x\ncat " + BIG}}),
    ("qo'shtirnoqli yo'l", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat \"" + BIG + "\""}}),
    ("glob, bitta bob", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat docs/patterns/25-*.md"}}),
    # Har bob kichik bo'lsa ham, yig'indisi butun hujjat.
    ("glob, butun hujjat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat docs/clean-code/*.md"}}),
    ("sed oralig'i", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "sed -n 100,160p " + BIG}}),
    ("grep", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "grep -n God " + BIG}}),
    ("head -n", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "head -n 40 " + BIG}}),
    # Asosiy noto'g'ri-ijobiy holat: heredoc bilan YOZISH, matn ichida
    # tasodifan fayl nomi uchraydi.
    ("heredoc yozish, nom matnda", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > CLAUDE.md <<EOF\nqoida: " + BIG + " to'liq o'qilmaydi\nEOF"}}),
    ("cat > boshqa faylga", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > notes.md <<EOF\n" + BIG + "\nEOF"}}),
    # Heredoc tanasi matn: undagi buyruq ham, cat ham chaqiruv emas.
    ("heredoc tanasida konteyner va cat", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > notes <<'EOF'\ndocker run x\ncat " + BIG
                  + "\nEOF\necho ok"}}),
    ("heredoc tugagach konteyner", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > notes <<EOF\nmatn\nEOF\ndocker run x"}}),
    ("boshqa faylni cat", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "cat README.md"}}),
    ("Bash bo'lmagan asbob", ALLOW,
     {"tool_name": "Grep", "tool_input": {"pattern": "x", "path": BIG}}),
    ("buzuq JSON", ALLOW, None),

    # Pul va vaqt sarflaydigan amallar.
    ("docker compose up", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker compose up -d"}}),
    ("docker run", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker run -it pg:16"}}),
    ("docker build", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker build -t app ."}}),
    ("docker-compose up (eski)", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker-compose up"}}),
    ("psql uzoq hostga", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "psql -h db.local -U u app"}}),
    ("mongosh URI bilan", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "mongosh mongodb://localhost:27017/app"}}),
    # Amalda eng ko'p uchraydigan shakllar: bayroq, prefiks, yangi satr,
    # container/image kichik buyrug'i, konteyner ichidagi klient.
    ("compose -f bilan up", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "docker compose -f docker-compose.dev.yml up -d"}}),
    ("compose bir nechta -f bilan up", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "docker compose -f a.yml -f b.yml up --build"}}),
    ("compose --profile bilan up", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "docker compose --profile dev up -d"}}),
    ("eski compose -f bilan up", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker-compose -f x.yml up"}}),
    ("eski compose run", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker-compose run app"}}),
    ("sudo bilan run", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "sudo docker run -d pg:16"}}),
    ("sudo -E bilan run", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "sudo -E docker run x"}}),
    ("time bilan build", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "time docker build ."}}),
    ("VAR= bilan build", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "DOCKER_BUILDKIT=1 docker build ."}}),
    ("container run", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker container run pg"}}),
    ("image pull", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker image pull pg"}}),
    ("yangi satrdan keyingi compose up", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "cd /app\ndocker compose up -d"}}),
    ("subshell ichida compose up", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "(cd infra && docker compose up -d)"}}),
    ("backtick ichida run", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "echo `docker run x`"}}),
    ("VAR= bilan baza", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "PGPASSWORD=x psql -h db -U u"}}),
    ("env bilan baza", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "env PGPASSWORD=x psql -h db -U u"}}),
    ("konteyner ichidagi klient", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker exec -it db psql -U app"}}),
    # Tekshiruv keyingi buyruqqa o'tib ketmaydi.
    ("exec, keyingi buyruqda klient nomi", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "docker exec app ls; echo psql"}}),
    # Bayroq qiymatidagi fe'lga o'xshash so'z fe'l emas.
    ("compose logs -f", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "docker compose logs -f api"}}),
    ("compose -f bilan ps", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "docker compose -f x.yml ps"}}),
    ("compose -f build/... ps", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "docker compose -f build/compose.yml ps"}}),
    ("compose -f run-dev.yml logs", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "docker compose -f run-dev.yml logs -f"}}),
    ("psql --help", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "psql --help"}}),
    ("psql -V", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "psql -V"}}),
    # Lokal ulanish ham ulanish: host sharti endi yo'q.
    ("mongosh, hostsiz", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "mongosh"}}),
    ("redis-cli, hostsiz", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "redis-cli"}}),
    ("psql lokal baza", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "psql -U postgres shop"}}),
    # Qo'shtirnoq olib tashlansa ham klient nomi buyruq o'rnida qoladi.
    ("psql qo'shtirnoqli URI", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": 'psql "postgresql://u:p@db/shop"'}}),
    ("VAR= bilan lokal psql", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "PGPASSWORD=x psql -U u shop"}}),
    # Prefiks bayrog'ining qiymati ("postgres") buyruq emas.
    ("sudo -u postgres psql", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "sudo -u postgres psql"}}),
    ("docker exec ichida psql", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker exec -it pg psql -U postgres"}}),
    ("compose exec ichida psql", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "docker compose exec db psql -U u"}}),
    ("compose -f bilan exec", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "docker compose -f x.yml exec db psql -U u"}}),
    ("kubectl exec ichida psql", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "kubectl exec pod -- psql"}}),
    ("kubectl -n bilan exec", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "kubectl -n prod exec pod -- psql"}}),
    ("naqsh ichida klient nomlari", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "grep -rnE 'mongosh|redis-cli' ."}}),
    ("which psql", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "which psql"}}),
    # Regex qaytishi (backtracking) bilan osilib qolmasin.
    ("ko'p bayroqli compose logs", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "docker compose" + " --file x.yml" * 30 + " logs"}}),
    # Tashxis arzon, to'silmaydi.
    ("docker ps", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "docker ps -a"}}),
    ("docker logs", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "docker logs app --tail 50"}}),
    ("psql --version", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "psql --version"}}),
    ("mvn test to'silmaydi", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "mvn -q test -Dtest=OrderTest"}}),
    ("powershell", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "powershell -c ls"}}),
    ("pwsh", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "pwsh ./build.ps1"}}),
    (".ps1 skript", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "./deploy.ps1 -Env prod"}}),
    # "powershell" so'zi matn ichida: to'silmasligi kerak.
    ("matndagi powershell", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "grep -rn powershell docs/"}}),
    # Qidiruv naqshi ichidagi so'z chaqiruv emas. Bu holat amalda
    # uchradi: qo'riqchi shu repoda o'z sozlamalarini qidirgan grep ni
    # to'xtatib qo'ydi.
    ("naqsh ichida taqiqlangan so'zlar", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "grep -rnoiE " + chr(39) + "(" + "docker (run|build)"
                  + "|powershell)" + chr(39) + " .claude/"}}),
    ("naqsh ichida konteyner buyrug'i", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "grep -rn " + chr(39) + "docker " + "run" + chr(39) + " docs/"}}),
    ("matnga yozilgan ulanish", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "echo " + chr(39) + "psql -h localhost" + chr(39)
                  + " >> notes.txt"}}),
    # Skript nomini ATASH uni yurgizish emas. Bu holat amalda uchradi:
    # o'rnatuvchi faylni yozayotganda qo'riqchi o'z yozuvini to'xtatdi.
    ("ps1 nomi argument sifatida", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "wc -l install/manguberdi" + ".ps1"}}),
    ("ps1 ni git ga qo'shish", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "git add install/manguberdi" + ".ps1"}}),
    ("ps1 ni cat qilish", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "head -20 install/x" + ".ps1"}}),
    ("pwsh bilan yurgizish to'siladi", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "pwsh install/x" + ".ps1"}}),
    # COST_OK endi qochish yo'li emas: qarorni odam qiladi, shuning uchun
    # prefiks hech narsani o'zgartirmaydi.
    ("COST_OK prefiksi ham ask", ASK,
     {"tool_name": "Bash", "tool_input":
      {"command": "COST_OK=1 docker compose up -d"}}),

    # Windows da Git Bash bo'lmasa PowerShell asbobi yoqiladi: to'siqlar
    # unda ham ishlashi kerak.
    # Papkali yo'l: avval `[\w.-]*\.ps1` faqat joriy papkani ko'rardi.
    ("PowerShell: papkadagi .ps1", ASK,
     {"tool_name": "PowerShell", "tool_input":
      {"command": "& .\\install\\manguberdi" + ".ps1 -Update"}}),
    ("PowerShell: joriy papkadagi .ps1", ASK,
     {"tool_name": "PowerShell", "tool_input": {"command": ".\\build" + ".ps1 -Task test"}}),
    ("Bash: mutlaq yo'ldagi .ps1", ASK,
     {"tool_name": "Bash", "tool_input": {"command": "C:/src/tools/x" + ".ps1"}}),
    ("PowerShell: oddiy buyruq", ALLOW,
     {"tool_name": "PowerShell", "tool_input": {"command": "Get-ChildItem install"}}),
    ("PowerShell: compose up", ASK,
     {"tool_name": "PowerShell", "tool_input": {"command": "docker compose up -d"}}),
    ("PowerShell: lokal psql", ASK,
     {"tool_name": "PowerShell", "tool_input": {"command": "psql -U postgres shop"}}),
    ("PowerShell: Get-Content katta bob", DENY,
     {"tool_name": "PowerShell", "tool_input": {"command": "Get-Content " + BIG}}),
    ("PowerShell: Get-Content -TotalCount", ALLOW,
     {"tool_name": "PowerShell", "tool_input":
      {"command": "Get-Content -TotalCount 80 " + BIG}}),
    ("PowerShell: cat -Tail", ALLOW,
     {"tool_name": "PowerShell", "tool_input": {"command": "cat " + BIG + " -Tail 30"}}),
    ("PowerShell: gc, teskari slash", DENY,
     {"tool_name": "PowerShell", "tool_input":
      {"command": "gc " + BIG.replace("/", chr(92))}}),
    ("PowerShell: type, katta harf", DENY,
     {"tool_name": "PowerShell", "tool_input": {"command": "TYPE " + BIG}}),
    ("PowerShell: kichik bob", ALLOW,
     {"tool_name": "PowerShell", "tool_input": {"command": "Get-Content " + SMALL}}),
    # Bash da `type` faylni o'qimaydi: PowerShell fe'llari unga qo'llanmaydi.
    ("Bash: type", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "type " + BIG}}),
    # Test vaqti: to'liq suite, clean, --rerun-tasks, --no-daemon deny.
    # Arzon yo'l bir xil (run_tests.py), shuning uchun ask emas: ask
    # zanjirni odamni kutib to'xtatardi.
    ("gradle: filtrsiz test", DENY, bash("./gradlew test")),
    ("gradle: check", DENY, bash("./gradlew check")),
    ("gradle: integrationTest", DENY, bash("./gradlew integrationTest")),
    ("gradle: && dan keyin test", DENY, bash("cd app && ./gradlew test")),
    ("gradle: modulli --tests", ALLOW,
     bash("./gradlew :orders:test --tests 'shop.orders.OrderServiceTest'")),
    ("gradle: --console qiymati vazifa emas", ALLOW,
     bash("gradle --console plain :a:test --tests A")),
    ("gradle: build -x test", ALLOW, bash("./gradlew build -x test")),
    ("gradle: compileJava", ALLOW, bash("./gradlew compileJava compileTestJava")),
    ("gradle: clean", DENY, bash("./gradlew clean :a:test --tests A")),
    ("gradle: --rerun-tasks", DENY, bash("./gradlew :a:test --tests A --rerun-tasks")),
    ("gradle: --no-daemon", DENY, bash("./gradlew --no-daemon :a:test --tests A")),
    ("maven: filtrsiz test", DENY, bash("./mvnw -B test")),
    ("maven: verify", DENY, bash("cd app; mvn verify")),
    ("maven: clean install", DENY, bash("mvn clean install")),
    ("maven: -Dtest qo'shtirnoqda", ALLOW,
     bash("./mvnw -pl orders -am test -Dtest='A,B' "
          "-Dsurefire.failIfNoSpecifiedTests=false")),
    ("maven: -Dit.test", ALLOW, bash("mvn verify -Dit.test=OrderIT")),
    ("maven: -DskipTests", ALLOW, bash("mvn package -DskipTests")),
    ("maven: dependency:tree", ALLOW, bash("mvn -q dependency:tree")),
    ("grep ichidagi 'gradle test'", ALLOW, bash("grep -rn 'gradle test' .")),

    # Subagentda ask muddatsiz kutadi: u yerda deny, asosiy oqimda ask.
    ("subagent: psql deny", DENY, sub("psql -U postgres shop")),
    ("subagent: compose up deny", DENY, sub("docker compose up -d")),
    ("subagent: docker ps o'tadi", ALLOW, sub("docker ps -a")),
    ("asosiy oqim: psql ask", ASK, bash("psql -U postgres shop")),
    ("asosiy oqim: compose up ask", ASK, bash("docker compose up -d")),

    # Tabiiy prefikslar: timeout (bayroqlari bilan), command, sh/bash, subshell.
    ("timeout: gradle test", DENY, bash("timeout 900 ./gradlew test")),
    ("timeout -s KILL: gradle test", DENY, bash("timeout -s KILL 900 ./gradlew test")),
    ("timeout -k 5 --preserve-status", DENY,
     bash("timeout -k 5 --preserve-status 10m mvn verify")),
    ("timeout: docker run", ASK, bash("timeout 60 docker run postgres")),
    ("timeout: katta bobni cat", DENY, bash("timeout 5 cat " + BIG)),
    ("timeout: filtrli test o'tadi", ALLOW,
     bash("timeout 900 mvn -q test -Dtest=OrderTest")),
    ("cd && timeout mvn verify", DENY, bash("cd x && timeout 600 mvn verify")),
    ("command cat katta bob", DENY, bash("command cat " + BIG)),
    ("command docker run", ASK, bash("command docker run postgres")),
    ("command -v psql o'tadi", ALLOW, bash("command -v psql")),
    ("sh gradlew test", DENY, bash("sh gradlew test")),
    ("bash ./gradlew check", DENY, bash("bash ./gradlew check")),
    ("bash gradlew compileJava o'tadi", ALLOW, bash("bash gradlew compileJava")),
    ("subshell: cat katta bob", DENY, bash("(cat " + BIG + ")")),
    ("$(): cat katta bob", DENY, bash("x=$(cat " + BIG + ")")),
    ("subshell: kichik bob o'tadi", ALLOW, bash("(cat " + SMALL + ")")),
    ("subshell: gradle test", DENY, bash("(cd app && ./gradlew test)")),
    ("xargs qo'shilmagan", ALLOW, bash("xargs -a /dev/null ./gradlew test")),

    # .java ga Bash bilan yozish: check_code va rules_for undan o'tib ketardi.
    ("java: heredoc bilan yozish", DENY,
     bash("cat > src/main/java/Foo.java <<'EOF'\nclass Foo {}\nEOF")),
    ("java: qo'shtirnoqli nomga yozish", DENY,
     bash("cat > \"src/Foo.java\" <<EOF\nclass Foo {}\nEOF")),
    ("java: >> qo'shish", DENY, bash("echo '}' >> src/Foo.java")),
    ("java: tee", DENY, bash("printf x | tee src/Foo.java")),
    ("java: tee -a", DENY, bash("echo x | tee -a Foo.java > /dev/null")),
    ("java: sed -i", DENY, bash("sed -i 's/a/b/;s/c/d/' src/main/java/demo/Foo.java")),
    ("java: sed -i.bak", DENY, bash("sed -i.bak -e s/a/b/ Foo.java")),
    ("java: perl -pi", DENY, bash("perl -pi -e 's/a/b/' Foo.java")),
    ("java: grep o'tadi", ALLOW, bash("grep -n x Foo.java")),
    ("java: cat | head o'tadi", ALLOW, bash("cat Foo.java | head")),
    ("java: sed -n o'tadi", ALLOW, bash("sed -n 1,20p Foo.java")),
    ("java: perl -Mstrict o'tadi", ALLOW, bash("perl -Mstrict -ne 'print' Foo.java")),
    ("java: Foo.java.txt o'tadi", ALLOW, bash("git log > Foo.java.txt")),
    ("java: 2>&1 o'tadi", ALLOW, bash("javac Foo.java 2>&1 | head")),
    ("java: heredoc tanasidagi Java", ALLOW,
     bash("cat > notes.md <<'EOF'\nsed -i s/a/b/ Foo.java\necho x > Bar.java\nEOF")),
    ("java: qo'shtirnoq ichidagi >", ALLOW, bash("echo 'x > Foo.java' >> notes.txt")),

    # Jonli bazani o'chirish: Test vaqti emas, alohida sabab bilan ask.
    ("flyway:clean ask", ASK, bash("./mvnw flyway:clean")),
    ("flywayClean ask", ASK, bash("./gradlew flywayClean")),
    ("liquibase:dropAll ask", ASK, bash("mvn liquibase:dropAll")),
    ("subagent: flywayClean deny", DENY, sub("./gradlew flywayClean")),
    ("flyway:migrate o'tadi", ALLOW, bash("./mvnw flyway:migrate")),
    ("flyway:clean + to'liq suite deny", DENY, bash("mvn flyway:clean verify")),

    # index/ ham kuzatuvda: grep qilinadi, kontekstga olinmaydi.
    ("index: cat sections.tsv", DENY, bash("cat index/sections.tsv")),
    ("index: chegarasiz Read", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": "index/sections.tsv"}}),
    ("index: grep o'tadi", ALLOW, bash("grep -n circuit index/sections.tsv")),
    ("index: Read limit=20 o'tadi", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": "index/sections.tsv", "limit": 20}}),
]

# To'siq maslahatidagi `tools/` yo'llari va CLAUDE.md. Global o'rnatishda
# hook boshqa proyektda yuradi: nisbiy `tools/doc.sh` u yerda yo'q.
HINT_PAYLOADS = [
    {"tool_name": "Read", "tool_input": {"file_path": os.path.join(ROOT, BIG)}},
    {"tool_name": "Bash", "tool_input": {"command": "docker compose up -d"}},
    {"tool_name": "Bash", "tool_input": {"command": "psql -U u shop"}},
    {"tool_name": "Bash", "tool_input": {"command": "./gradlew test"}},
    {"tool_name": "Bash", "tool_input": {"command": "sed -i s/a/b/ Foo.java"}},
    {"tool_name": "Bash", "tool_input": {"command": "./gradlew flywayClean"}},
]
HINT_PATH_RE = re.compile(r'"([^"]*(?:tools/[\w.-]+|CLAUDE\.md))"'
                          r'|([^\s"]*(?:tools/[\w.-]+|CLAUDE\.md))')


# Jarayon chegarasini sinaydigan holatlar subprocess bilan yuradi, qolgani
# jarayon ichida (testkit.call_main): har holatga Python ishga tushirish
# suite vaqtining deyarli hammasi edi. Holat nomi -> uzatish usuli.
# Qator matni va natijasi jarayon ichidagi holatlar bilan bir xil.
E2E = {
    # Buzuq kirish: hook jim, chaqiruvni to'smaydi.
    "buzuq JSON": {},
    # To'siq va maslahat matni haqiqiy stdout orqali JSON bo'lib chiqadi.
    "katta bob, chegarasiz Read": {},
    # Nisbiy yo'l jarayonning o'z papkasidan, ROOT zaxirasi bilan topiladi.
    "boshqa cwd, nisbiy yo'l": {},
    # PowerShell 5.1 pipe boshiga BOM qo'yadi.
    "docker compose up": {"bom": True},
    # Windows da matnli stdin cp1252: hookio baytlarni o'qishi kerak.
    # U+014D ning UTF-8 baytida 0x8D bor, cp1252 uni o'qiy olmaydi.
    "docker run": {"env": {"PYTHONIOENCODING": "cp1252"},
                   "extra": {"description": "Konteyner ō"}},
    # CLAUDE_PROJECT_DIR berilmasa ildiz payload dagi cwd dan olinadi.
    "psql uzoq hostga": {"env": {"CLAUDE_PROJECT_DIR": None},
                         "extra": {"cwd": ROOT}},
}


def run_guard(payload, cwd, root=None, e2e=None):
    """`root` berilsa CLAUDE_PROJECT_DIR shunga qo'yiladi (hookio.active).

    `e2e` berilsa (E2E qiymati) guard alohida jarayonda yuradi.
    """
    env = {} if root is None else {"CLAUDE_PROJECT_DIR": root}
    if e2e is None:
        raw = "not json" if payload is None else json.dumps(payload)
        out = testkit.call_main(G.main, raw, cwd=cwd, env=env).stdout.strip()
        return json.loads(out)["hookSpecificOutput"] if out else {}
    if payload is not None:
        payload = dict(payload, **e2e.get("extra", {}))
    raw = (b"not json" if payload is None
           else json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    if e2e.get("bom"):
        raw = b"\xef\xbb\xbf" + raw
    environ = dict(os.environ, **env)
    for key, value in e2e.get("env", {}).items():
        if value is None:
            environ.pop(key, None)
        else:
            environ[key] = value
    out = subprocess.run(
        [sys.executable, GUARD], input=raw, capture_output=True,
        cwd=cwd, timeout=20, env=environ,
    ).stdout.decode("utf-8").strip()
    return json.loads(out)["hookSpecificOutput"] if out else {}


def verdict(payload, cwd=ROOT, e2e=None):
    return run_guard(payload, cwd, e2e=e2e).get("permissionDecision", ALLOW)


def hint_paths(cwd):
    """(topilgan yo'llar soni, shu cwd dan ochilmaydiganlari)."""
    seen, broken = 0, []
    for payload in HINT_PAYLOADS:
        reason = run_guard(payload, cwd).get("permissionDecisionReason", "")
        for quoted, bare in HINT_PATH_RE.findall(reason):
            seen += 1
            path = quoted or bare
            if not os.path.exists(os.path.join(cwd, path)):
                broken.append(path)
    return seen, broken


def verdict_line(name, want, got):
    return [("%-30s kutilgan=%-5s olingan=%s" % (name, want, got), got == want)]


def decision_case(name, want, payload, cwd=ROOT):
    return name, lambda: verdict_line(name, want, verdict(payload, cwd, E2E.get(name)))


# Qaror to'g'ri bo'lsa ham sabab noto'g'ri bo'lishi mumkin: flyway:clean
# avval 'Test vaqti: clean' bilan to'silardi.
REASONS = [
    ("subagent sababi", sub("psql shop"), G.SUBAGENT_NOTE, None),
    ("asosiy oqimda subagent sababi yo'q", bash("psql shop"), None, G.SUBAGENT_NOTE),
    ("flyway:clean sababi", bash("./mvnw flyway:clean"),
     "Jonli bazani o'chiradi", "Test vaqti"),
    ("java yozish sababi", bash("sed -i s/a/b/ Foo.java"),
     "Java faylni Edit yoki Write bilan yozing: check_code va rules_for "
     "faqat shu asboblarda ishlaydi", None),
]


def reason_case(name, payload, need, avoid):
    def run():
        reason = run_guard(payload, ROOT).get("permissionDecisionReason", "")
        ok = (need is None or need in reason) and (avoid is None or avoid not in reason)
        return [("%-30s %s" % (name, reason.split("\n")[0][:60]), ok)]
    return name, run


def hint_case(name, other):
    """Maslahatdagi har yo'l chaqiruvchi turgan papkadan ochilishi kerak."""
    def run():
        cwd = tempfile.mkdtemp() if other else ROOT
        try:
            seen, broken = hint_paths(cwd)
        finally:
            if other:
                shutil.rmtree(cwd, ignore_errors=True)
        return [("%-30s yo'l=%d ochilmaydi=%s" % (name, seen, ", ".join(broken) or "-"),
                 seen > 0 and not broken)]
    return name, run


# Global o'rnatishda hook har proyektda yuradi. Java bo'lmagan
# proyektda docker va psql to'sig'i o'rinsiz: qo'riqchi jim o'tadi.
GATING = [
    ("Java emas: docker run o'tadi", ALLOW, ("main.py",),
     {"tool_name": "Bash", "tool_input": {"command": "docker run x"}}),
    ("Java emas: psql o'tadi", ALLOW, ("main.py",),
     {"tool_name": "Bash", "tool_input": {"command": "psql db"}}),
    ("Java emas: katta bob ham o'tadi", ALLOW, ("main.py",),
     {"tool_name": "Read", "tool_input": {"file_path": BIG}}),
    ("pom.xml: docker run ask beradi", ASK, ("pom.xml",),
     {"tool_name": "Bash", "tool_input": {"command": "docker run x"}}),
    ("pom.xml: psql ask beradi", ASK, ("pom.xml",),
     {"tool_name": "Bash", "tool_input": {"command": "psql db"}}),
    ("backend/pom.xml: ask beradi", ASK, ("backend/pom.xml",),
     {"tool_name": "Bash", "tool_input": {"command": "docker run x"}}),
]


def gating_case(name, want, files, payload):
    def run():
        tmp = tempfile.mkdtemp(prefix="guard_gate_")
        try:
            for rel in files:
                full = os.path.join(tmp, rel.replace("/", os.sep))
                os.makedirs(os.path.dirname(full), exist_ok=True)
                io.open(full, "w", encoding="utf-8").write("")
            got = run_guard(payload, ROOT, root=tmp).get(
                "permissionDecision", ALLOW)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return verdict_line(name, want, got)
    return name, run


def case_hooks_off():
    """GENIUS_HOOKS=off: klonda ham jim. Muhit jarayonga meros o'tadi."""
    off = subprocess.run(
        [sys.executable, GUARD],
        input=json.dumps({"tool_name": "Bash",
                          "tool_input": {"command": "docker run x"}}),
        capture_output=True, text=True, cwd=ROOT, timeout=20,
        env=dict(os.environ, GENIUS_HOOKS="off")).stdout.strip()
    return [("%-30s kutilgan=%-5s olingan=%s"
             % ("GENIUS_HOOKS=off: jim", "bo'sh", off[:40] or "bo'sh"), off == "")]


ALL_CASES = (
    [decision_case(name, want, payload, *rest) for name, want, payload, *rest in CASES]
    + [reason_case(*row) for row in REASONS]
    + [hint_case("maslahat yo'llari, klon", False),
       hint_case("maslahat yo'llari, boshqa proyekt", True)]
    + [gating_case(*row) for row in GATING]
    + [("GENIUS_HOOKS=off: jim", case_hooks_off)]
)


def main(argv=()):
    missing = [p for p in (BIG, MID, SMALL) if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        print("sinov fayllari yo'q: %s" % ", ".join(missing))
        return 1
    # Fixture chegarani kesib o'tsa (bob ikkiga bo'linsa yoki kichigi
    # o'sib ketsa), o'nlab chalg'ituvchi XATO o'rniga sababi aytiladi.
    size = {p: os.path.getsize(os.path.join(ROOT, p)) for p in (BIG, MID, SMALL)}
    if size[BIG] <= G.MAX_BYTES or size[MID] <= G.MAX_BYTES or size[SMALL] > G.MAX_BYTES:
        print("sinov fayli chegaradan o'tdi (chegara %d bayt): %s" % (
            G.MAX_BYTES, ", ".join("%s=%d" % (p, n) for p, n in size.items())))
        return 1
    # index/ hosila va git da yo'q: toza klonda index holatlari uchun yasaladi.
    if not os.path.exists(os.path.join(ROOT, "index", "sections.tsv")):
        subprocess.run([sys.executable, os.path.join(HERE, "build_index.py")],
                       capture_output=True, timeout=300)
    return testkit.run_cases(ALL_CASES, argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
