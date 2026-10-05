#!/usr/bin/env python3
"""guard.py uchun sinovlar.

    python3 tools/test_guard.py

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
]

# To'siq maslahatidagi `tools/` yo'llari va CLAUDE.md. Global o'rnatishda
# hook boshqa proyektda yuradi: nisbiy `tools/doc.sh` u yerda yo'q.
HINT_PAYLOADS = [
    {"tool_name": "Read", "tool_input": {"file_path": os.path.join(ROOT, BIG)}},
    {"tool_name": "Bash", "tool_input": {"command": "docker compose up -d"}},
    {"tool_name": "Bash", "tool_input": {"command": "psql -U u shop"}},
]
HINT_PATH_RE = re.compile(r'"([^"]*(?:tools/[\w.-]+|CLAUDE\.md))"'
                          r'|([^\s"]*(?:tools/[\w.-]+|CLAUDE\.md))')


def run_guard(payload, cwd, root=None):
    """`root` berilsa CLAUDE_PROJECT_DIR shunga qo'yiladi (hookio.active)."""
    raw = "not json" if payload is None else json.dumps(payload)
    environ = os.environ if root is None else dict(os.environ,
                                                   CLAUDE_PROJECT_DIR=root)
    out = subprocess.run(
        [sys.executable, GUARD], input=raw, capture_output=True, text=True,
        cwd=cwd, timeout=20, env=environ,
    ).stdout.strip()
    return json.loads(out)["hookSpecificOutput"] if out else {}


def verdict(payload, cwd=ROOT):
    return run_guard(payload, cwd).get("permissionDecision", ALLOW)


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


def main():
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

    failures = 0
    for name, want, payload, *rest in CASES:
        got = verdict(payload, rest[0] if rest else ROOT)
        ok = got == want
        failures += not ok
        print("%-4s %-30s kutilgan=%-5s olingan=%s"
              % ("OK" if ok else "XATO", name, want, got))

    # Maslahatdagi har yo'l chaqiruvchi turgan papkadan ochilishi kerak.
    other = tempfile.mkdtemp()
    try:
        checks = [("maslahat yo'llari, klon", ROOT),
                  ("maslahat yo'llari, boshqa proyekt", other)]
        for name, cwd in checks:
            seen, broken = hint_paths(cwd)
            ok = seen > 0 and not broken
            failures += not ok
            print("%-4s %-30s yo'l=%d ochilmaydi=%s"
                  % ("OK" if ok else "XATO", name, seen, ", ".join(broken) or "-"))
    finally:
        shutil.rmtree(other, ignore_errors=True)

    # Global o'rnatishda hook har proyektda yuradi. Java bo'lmagan
    # proyektda docker va psql to'sig'i o'rinsiz: qo'riqchi jim o'tadi.
    gating = [
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
    for name, want, files, payload in gating:
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
        ok = got == want
        failures += not ok
        print("%-4s %-30s kutilgan=%-5s olingan=%s"
              % ("OK" if ok else "XATO", name, want, got))

    # GENIUS_HOOKS=off: klonda ham jim.
    off = subprocess.run(
        [sys.executable, GUARD],
        input=json.dumps({"tool_name": "Bash",
                          "tool_input": {"command": "docker run x"}}),
        capture_output=True, text=True, cwd=ROOT, timeout=20,
        env=dict(os.environ, GENIUS_HOOKS="off")).stdout.strip()
    ok = off == ""
    failures += not ok
    print("%-4s %-30s kutilgan=%-5s olingan=%s"
          % ("OK" if ok else "XATO", "GENIUS_HOOKS=off: jim", "bo'sh",
             off[:40] or "bo'sh"))

    total = len(CASES) + len(checks) + len(gating) + 1
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
