<!-- doc: sonarqube | chapter: 33 | part: VIII. Server va tashkilot -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 33. Serverni o'rnatish, sozlash va resurs rejalashtirish (Installing and Sizing the Server)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [33.1 Server tarkibi: web, compute engine, qidiruv indeksi va ma'lumotlar bazasi](#331-server-tarkibi-web-compute-engine-qidiruv-indeksi-va-malumotlar-bazasi)
- [33.2 Ma'lumotlar bazasi talablari va PostgreSQL ni tayyorlash](#332-malumotlar-bazasi-talablari-va-postgresql-ni-tayyorlash)
- [33.3 Docker va Docker Compose bilan ko'tarish](#333-docker-va-docker-compose-bilan-kotarish)
- [33.4 Kubernetes da ishga tushirish va doimiy saqlash](#334-kubernetes-da-ishga-tushirish-va-doimiy-saqlash)
- [33.5 Operatsion tizim talablari: `vm.max_map_count` va fayl deskriptorlari](#335-operatsion-tizim-talablari-vmmax_map_count-va-fayl-deskriptorlari)
- [33.6 Xotira taqsimoti: web, compute engine va qidiruv uchun alohida sozlash](#336-xotira-taqsimoti-web-compute-engine-va-qidiruv-uchun-alohida-sozlash)
- [33.7 Loyihalar soni va kod hajmiga qarab resurs rejalashtirish](#337-loyihalar-soni-va-kod-hajmiga-qarab-resurs-rejalashtirish)
- [33.8 Disk: ma'lumotlar bazasi, indeks va o'sish prognozi](#338-disk-malumotlar-bazasi-indeks-va-osish-prognozi)
- [33.9 Teskari proksi, HTTPS va tashqi manzil sozlash](#339-teskari-proksi-https-va-tashqi-manzil-sozlash)
- [33.10 Tahlil navbati uzayganda nima qilish](#3310-tahlil-navbati-uzayganda-nima-qilish)
- [33.11 Server loglarini o'qish va asosiy sog'liq tekshiruvlari](#3311-server-loglarini-oqish-va-asosiy-sogliq-tekshiruvlari)
- [33.12 Amalda qo'llash](#3312-amalda-qollash)

</details>



SonarQube server bitta jarayon emas. Uning ichida to'rtta mustaqil qism bor va ularning har biri boshqa resursni yeydi. Shuning uchun "serverni o'rnatish" aslida ikki ish: to'g'ri ko'tarish va to'g'ri o'lchamlash. Quyida versiyadan versiyaga o'zgarmaydigan mexanika, o'zgaradigan raqamlar esa aniq belgilangan holda beriladi.

## 33.1 Server tarkibi: web, compute engine, qidiruv indeksi va ma'lumotlar bazasi

SonarQube server bitta JVM jarayoni ichidan uchta bola jarayonni ko'taradi. Birinchisi web server: UI, REST API va scanner dan kelayotgan yuklamani qabul qiladi. Ikkinchisi compute engine (CE): scanner yuborgan tahlil hisobotini navbatdan olib, issue larni hisoblaydi, measure larni yozadi va quality gate ni baholaydi. Uchinchisi search: Elasticsearch asosidagi qidiruv indeksi, u issue va component larni tez filtrlash uchun ishlatiladi.

To'rtinchi qism server ichida emas, tashqarida turadi: relyatsion ma'lumotlar bazasi. Haqiqat manbai bazada yashaydi. Qidiruv indeksi esa keltirilgan (derived) ma'lumot, uni bazadan qayta qurish mumkin.

Bu taqsimotdan ikkita amaliy xulosa chiqadi. Birinchi: scanner tahlilni serverda bajarmaydi, u faqat hisobotni yuboradi, haqiqiy hisob CE da bo'ladi. Ikkinchi: zahira nusxa (backup) olishda ma'lumotlar bazasi va `extensions` katalogi majburiy, qidiruv indeksi esa shart emas.

| Jarayon | Nima qiladi | Nimaga sezgir | Agar yetmasa |
|---|---|---|---|
| Web | UI, API, hisobot qabul qilish | CPU va JVM heap | UI sekinlashadi, 503 javob |
| Compute engine | Hisobotni qayta ishlash, quality gate | CPU va heap | Navbat uzayadi, natija kechikadi |
| Search | Issue va component qidiruvi | RAM va disk I/O | Qidiruv timeout, indeks qizil |
| Ma'lumotlar bazasi | Haqiqat manbai | Disk IOPS va ulanishlar | Hamma joy sekinlashadi |

## 33.2 Ma'lumotlar bazasi talablari va PostgreSQL ni tayyorlash

PostgreSQL qo'llab-quvvatlanadigan versiyalar oynasi SonarQube versiyasiga qarab o'zgaradi va har yangi relizda eski PostgreSQL versiyalari ro'yxatdan chiqarib tashlanadi. Shuning uchun aniq raqamni bu yerdan emas, o'zingiz o'rnatayotgan versiyaning rasmiy talablar sahifasidan oling. Umumiy qoida: 9.9 LTA liniyasi uchun PostgreSQL 11 dan yuqori, 2025 LTA liniyasi uchun esa ancha yangi minimal versiya talab qilinadi. MySQL qo'llab-quvvatlanmaydi va bu qaytmaydigan qaror.

Muhim nozik joy: bazani to'g'ri collation va encoding bilan yaratish kerak. UTF8 bo'lmasa, tahlil paytida matnli maydonlarda xato chiqadi. Sxema uchun alohida foydalanuvchi yarating va unga faqat o'z sxemasiga egalik bering.

```sql
-- Alohida rol va baza: SonarQube migratsiya uchun DDL huquqiga muhtoj
CREATE ROLE sonarqube WITH LOGIN PASSWORD 'kuchli_parol_env_dan';

CREATE DATABASE sonarqube
  WITH OWNER = sonarqube
       ENCODING = 'UTF8'
       TEMPLATE = template0;

\c sonarqube

-- public sxemani ishlatmaslik tavsiya etiladi
CREATE SCHEMA IF NOT EXISTS sonarqube AUTHORIZATION sonarqube;
ALTER ROLE sonarqube SET search_path TO sonarqube;

-- SonarQube o'z jadvallarini o'zi yaratadi, qo'lda DDL yozmang
```

Bazaga ulanishni `sonar.properties` da yoki muhit o'zgaruvchisi bilan beradi. Parolni fayl ichida ochiq saqlamang, uni secret manager yoki Kubernetes Secret dan oling. Baza bilan server bir xil ma'lumot markazida bo'lsin, chunki CE va web juda ko'p mayda so'rov yuboradi va kechikish (latency) to'g'ridan to'g'ri tahlil tezligiga ta'sir qiladi.

## 33.3 Docker va Docker Compose bilan ko'tarish

Docker eng tez yo'l, lekin ikkita xato ko'p uchraydi. Birinchi: volume ulanmagan holda ko'tarish, natijada konteyner yangilanganda plugin va indeks yo'qoladi. Ikkinchi: ichki (embedded) bazada ishlatish, u faqat sinov uchun va yangilanishni (upgrade) qo'llab-quvvatlamaydi.

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: sonarqube
      POSTGRES_PASSWORD: kuchli_parol
      POSTGRES_DB: sonarqube
    volumes:
      - pg_data:/var/lib/postgresql/data

  sonarqube:
    # Teg ni aniq qotirib qo'ying, "latest" ishlatmang
    image: sonarqube:2025.1-community
    depends_on: [db]
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonarqube
      SONAR_JDBC_USERNAME: sonarqube
      SONAR_JDBC_PASSWORD: kuchli_parol
    volumes:
      - sq_data:/opt/sonarqube/data
      - sq_extensions:/opt/sonarqube/extensions
    ports:
      - "9000:9000"

volumes:
  pg_data:
  sq_data:
  sq_extensions:
```

Image nomi va teg sxemasi vaqt o'tishi bilan o'zgargan: eski liniyada `sonarqube:9.9-community` ko'rinishida, yangi liniyada yil asosidagi teglar ishlatiladi va Community nashri "Community Build" deb nomlanadi. Shuning uchun teg nomini registry dan tekshirib oling, xotiradan yozmang. Konteyner ichida jarayon root bo'lmagan foydalanuvchi sifatida ishlaydi, demak volume lar egaligi to'g'ri bo'lishi kerak.

## 33.4 Kubernetes da ishga tushirish va doimiy saqlash

Kubernetes da SonarQube Deployment emas, StatefulSet sifatida yashashi qulay, chunki unga barqaror identifikator va doimiy disk kerak. Qidiruv indeksi `data` katalogida yashaydi va u yo'qolsa server ko'tarilishda indeksni qayta quradi, bu katta instansiyada uzoq vaqt oladi.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: sonarqube
spec:
  serviceName: sonarqube
  replicas: 1          # Community va Developer da bitta replika
  template:
    spec:
      securityContext:
        fsGroup: 1000  # volume egaligi konteyner foydalanuvchisiga tegsin
      initContainers:
        - name: sysctl       # tugunda sysctl sozlanmagan bo'lsa
          image: busybox:1.36
          command: ["sh","-c","sysctl -w vm.max_map_count=524288"]
          securityContext: { privileged: true }
      containers:
        - name: sonarqube
          image: sonarqube:2025.1-community
          readinessProbe:
            httpGet: { path: /api/system/status, port: 9000 }
            initialDelaySeconds: 60
          volumeMounts:
            - { name: data, mountPath: /opt/sonarqube/data }
            - { name: ext,  mountPath: /opt/sonarqube/extensions }
```

Replikani ko'paytirish faqat Data Center nashrida ma'noga ega. Oddiy nashrda ikkinchi pod ko'tarilsa, ikkita CE bir xil navbatga va bir xil indeksga tegib buzilish keltiradi. Horizontal Pod Autoscaler ni bu ish yuklamasiga ulamang.

## 33.5 Operatsion tizim talablari: `vm.max_map_count` va fayl deskriptorlari

Eng ko'p uchraydigan "server ko'tarilmaydi" muammosi aslida OS sozlamasi. Elasticsearch mmap ishlatadi va yadroning xarita limiti kichik bo'lsa jarayon darhol o'ladi. Loglarda bu `max virtual memory areas vm.max_map_count ... is too low` ko'rinishida chiqadi. Fayl deskriptorlari limiti ham shunday: indeks ko'p fayl ochadi.

```bash
# Joriy qiymatlarni ko'rish
sysctl vm.max_map_count fs.file-max
ulimit -n && ulimit -u

# Vaqtinchalik (restart dan keyin yo'qoladi)
sudo sysctl -w vm.max_map_count=524288
sudo sysctl -w fs.file-max=131072

# Doimiy qilish
echo 'vm.max_map_count=524288' | sudo tee /etc/sysctl.d/99-sonarqube.conf
echo 'fs.file-max=131072'     | sudo tee -a /etc/sysctl.d/99-sonarqube.conf
sudo sysctl --system

# Foydalanuvchi limitlari: nofile va nproc
printf 'sonarqube - nofile 131072\nsonarqube - nproc 8192\n' \
  | sudo tee /etc/security/limits.d/99-sonarqube.conf
```

Yana ikki talab. Birinchi: SonarQube jarayoni root sifatida ishlamasligi kerak, aks holda ichki Elasticsearch ishga tushishni rad etadi. Ikkinchi: Java versiyasi. Har bir SonarQube liniyasi o'ziga xos minimal JDK talab qiladi va bu talab relizlar bilan oshib boradi, shuning uchun o'rnatishdan oldin aynan o'z versiyangiz uchun tekshiring. Scanner tomonidagi JDK talabi serverdan alohida va ko'pincha undan pastroq bo'ladi.

## 33.6 Xotira taqsimoti: web, compute engine va qidiruv uchun alohida sozlash

Bu bobning eng muhim joyi. Uchta jarayonning har biriga alohida JVM parametri beriladi va ularni birga "server xotirasi" deb o'ylash xato. Standart qiymatlar kichik va faqat kichik instansiya uchun mos, aniq standart raqam versiyaga qarab farq qiladi.

```properties
# $SONARQUBE_HOME/conf/sonar.properties
# Web server: foydalanuvchi soni va API yuklamasiga bog'liq
sonar.web.javaOpts=-Xmx2G -Xms1G -XX:+HeapDumpOnOutOfMemoryError

# Compute engine: eng katta loyihaning hisobot hajmiga bog'liq
sonar.ce.javaOpts=-Xmx4G -Xms1G -XX:+HeapDumpOnOutOfMemoryError

# Search: Xms va Xmx TENG bo'lishi kerak, swap ni oldini oladi
sonar.search.javaOpts=-Xmx4G -Xms4G -XX:MaxDirectMemorySize=256m

# Search uchun OS da shuncha bo'sh RAM qoldiring: fayl keshi indeksni tezlashtiradi
# Qoida: jami RAM ning yarmidan ko'pini bitta JVM ga bermang
```

Uch qoidani eslab qoling. Search uchun `Xms` va `Xmx` teng bo'lsin. CE heap i eng katta monorepo hisobotini sig'dirishi kerak, chunki `OutOfMemoryError` eng ko'p shu jarayonda chiqadi. Web heap i foydalanuvchi soniga qarab o'sadi, lekin odatda CE dan kichik qoladi.

CE da parallel ishchi (worker) sonini oshirish `sonar.ce.workerCount` orqali bo'ladi, lekin bu imkoniyat tijorat nashrlarida mavjud. Community Build da navbat ketma-ket ishlanadi va uni tezlashtirish yo'li faqat CPU va heap ni oshirish.

## 33.7 Loyihalar soni va kod hajmiga qarab resurs rejalashtirish

Quyidagi raqamlar taxminiy va boshlang'ich nuqta sifatida beriladi. Haqiqiy ehtiyoj til soniga, test coverage hisobot hajmiga va kuniga necha marta tahlil ishga tushishiga bog'liq. Shuning uchun birinchi oyda monitoring yig'ing va keyin tuzating.

| Hajm | Loyiha / LOC (taxminan) | RAM (taxminan) | vCPU (taxminan) |
|---|---|---|---|
| Kichik | 20 loyiha, 500k LOC gacha | 8 GB | 4 |
| O'rta | 100 loyiha, 5M LOC gacha | 16 GB | 8 |
| Katta | 300+ loyiha, 20M LOC gacha | 32 GB va yuqori | 16 |

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| O'lchamlash | "8 GB yetadi" deb boshlash | Eng katta loyihaning hisobot hajmini o'lchab CE heap ni tanlash |
| Xotira | Bitta `JAVA_OPTS` ga hamma narsani berish | Web, CE va search ga alohida profil berish |
| Baza | Server bilan bir xil diskda PostgreSQL | Alohida managed baza, IOPS kafolati bilan |
| Yangilanish | Image tegini `latest` qoldirish | Tegni qotirib qo'yish, LTA liniyasida qolish |
| Zahira | Faqat VM snapshot | Baza dump plus `extensions` katalogi, tiklanishni sinab ko'rish |
| Indeks | Qidiruv indeksini ham backup qilish | Indeksni keltirilgan ma'lumot deb bilib, qayta qurishga tayanish |
| Kuzatish | UI sekinlashganda qarash | CE navbat uzunligi va heap foydalanishiga alert qo'yish |
| O'sish | Disk to'lganda kengaytirish | Housekeeping ni sozlab o'sish tezligini pasaytirish |
| Masshtab | Replikani ikkiga chiqarish | Faqat Data Center nashrida klaster, aks holda vertikal o'sish |

## 33.8 Disk: ma'lumotlar bazasi, indeks va o'sish prognozi

Disk uch joyda sarflanadi: ma'lumotlar bazasi, qidiruv indeksi (`data` katalogi) va loglar. Bazada eng ko'p joy o'lchov tarixi va tahlil hisobotlari tomonidan egallanadi. Shuning uchun o'sishni boshqarishning asosiy vositasi housekeeping sozlamasi: eski snapshot larni qanchalik tez siqish va o'chirish.

```sql
-- Eng katta jadvallarni topish: o'sish manbaini ko'rish uchun
SELECT relname AS jadval,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS hajm
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r' AND n.nspname NOT IN ('pg_catalog','information_schema')
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 10;

-- Butun bazaning hajmi
SELECT pg_size_pretty(pg_database_size('sonarqube')) AS baza_hajmi;

-- Tahlil navbati tarixidagi muvaffaqiyatsizliklar nisbati
SELECT status, count(*) FROM ce_activity GROUP BY status;
```

Odatda `project_measures`, `issues` va hisobot bilan bog'liq jadvallar ro'yxatning boshida turadi. Agar `project_measures` nomutanosib katta bo'lsa, demak tarix saqlash siyosati juda yumshoq yoki juda ko'p custom metrika yoziladi. Boshlang'ich disk sifatida o'rta instansiya uchun baza ostiga taxminan 50 GB, indeks ostiga taxminan 20 GB ajratish mantiqiy, lekin bu raqamlar faqat taxmin va birinchi chorakda real o'sish bo'yicha qayta ko'rilishi kerak.

Loglarni rotatsiya qilishni yoqing. Aks holda `ce.log` va `es.log` oylar davomida o'sib diskni to'ldiradi va bu butun serverni to'xtatadi.

## 33.9 Teskari proksi, HTTPS va tashqi manzil sozlash

SonarQube ni to'g'ridan to'g'ri 9000 portda ochib qo'ymaslik kerak. Oldiga teskari proksi qo'yiladi va TLS shu yerda tugatiladi. Bunda ikkita sozlama majburiy bo'ladi.

```properties
# Tashqi manzil: UI havolalari, PR dekoratsiyasi va webhook shu manzilni ishlatadi
sonar.core.serverBaseURL=https://sonar.kompaniya.uz

# Agar ildiz yo'lida emas, subpath da turadigan bo'lsa
# sonar.web.context=/sonar

# Proksi orqasida ishlayotganini bildirish
sonar.web.port=9000
sonar.web.host=127.0.0.1
```

```bash
# Proksi sozlamasini tekshirish: ikki narsa to'g'ri bo'lishi kerak
curl -sI https://sonar.kompaniya.uz/ | head -5

# Katta hisobotlar uchun proksi da yuklama limiti yetarli bo'lsin
# (nginx: client_max_body_size, timeout: proxy_read_timeout)

# Scanner tomonidan ulanishni tekshirish
curl -s -u "$SONAR_TOKEN:" \
  https://sonar.kompaniya.uz/api/system/status

# Agar 413 yoki 504 chiqsa, muammo SonarQube da emas, proksida
```

`sonar.core.serverBaseURL` noto'g'ri bo'lsa, quality gate natijasi CI ga qaytadi, lekin pull request dagi havolalar ichki IP ga ketadi. Bu eng tez sezilmaydigan va eng ko'p vaqt yeydigan noto'g'ri sozlamalardan biri. Webhook va PR dekoratsiyasi CI bilan bog'langan joy, u haqida [testlash qo'llanmasidagi](../testing/README.md) CI/CD test pipeline mavzusiga qarang.

## 33.10 Tahlil navbati uzayganda nima qilish

CE navbati uzayishi deyarli har doim bitta sabab bilan bo'ladi: CE bitta hisobotni juda uzoq ishlayotgani yoki hisobotlar ketma-ket tez kelayotgani. Birinchi qadam diagnostika: UI dagi Administration bo'limida Background Tasks sahifasi har bir vazifaning davomiyligini ko'rsatadi. Eng uzoq vazifani topib, qaysi loyiha ekanini aniqlang.

| Tuzoq | Belgisi | Yechim |
|---|---|---|
| CE heap kichik | `ce.log` da `OutOfMemoryError` | `sonar.ce.javaOpts` dagi `Xmx` ni oshirish |
| Monorepo bitta loyiha sifatida | Bitta vazifa soatlab ishlaydi | Modullarga bo'lib alohida loyiha qilish |
| Tahlil juda tez-tez | Navbat hech bo'shamaydi | Har push emas, PR va asosiy branch da ishga tushirish |
| Generatsiya qilingan kod skanerlanadi | LOC sun'iy katta | `sonar.exclusions` bilan chiqarib tashlash |
| Baza sekin | Vazifa CPU emas, I/O kutadi | Baza diskini IOPS bo'yicha kuchaytirish |
| Indeks qizil | Qidiruv xato beradi | Disk bo'shatib server restart, indeks qayta qurilsin |
| Housekeeping o'chirilgan | Baza va navbat sekinlashadi | Tarix saqlash siyosatini qisqartirish |
| Bitta CE worker | Parallel ishlamaydi | CPU oshirish, yoki tijorat nashrida worker sonini ko'paytirish |

Eng arzon g'alaba ko'pincha hisobot hajmini kamaytirish bo'ladi, ya'ni skanerlanadigan fayllarni toraytirish. Serverga RAM qo'shish keyingi qadam, birinchi qadam emas.

## 33.11 Server loglarini o'qish va asosiy sog'liq tekshiruvlari

Loglar `$SONARQUBE_HOME/logs` ichida va har jarayon o'z fayliga yozadi. `sonar.log` umumiy ko'tarilish jarayoni, `web.log` web server, `ce.log` compute engine, `es.log` qidiruv indeksi. Muammoni izlashda birinchi qaraladigan fayl aynan muammo chiqqan jarayonning fayli, `sonar.log` emas.

```bash
# Ko'tarilish muvaffaqiyatli tugaganini tasdiqlash
grep -i "SonarQube is operational" logs/sonar.log

# Autentifikatsiya talab qilmaydigan holat tekshiruvi
curl -s http://localhost:9000/api/system/status
# Kutilgan javob: {"status":"UP", ...}
# STARTING yoki DB_MIGRATION_NEEDED bo'lsa hali tayyor emas

# Batafsil sog'liq: admin token yoki system passcode kerak
curl -s -u "$ADMIN_TOKEN:" http://localhost:9000/api/system/health

# Konteynerda loglarni kuzatish
docker compose logs -f sonarqube | grep -iE "error|warn|oom"

# CE da uzoq ishlagan vazifalarni log dan ko'rish
grep -i "executed task" logs/ce.log | tail -20
```

`/api/system/status` yengil va monitoring probe uchun mos. `/api/system/health` esa batafsil, lekin autentifikatsiya talab qiladi. Kubernetes readiness probe uchun birinchisini ishlatish amaliy. Alert qo'yishda uchta signal yetarli boshlanish beradi: `status` UP emasligi, CE navbat uzunligi ostonadan oshishi va disk bandligi 80 foizdan oshishi.

## 33.12 Amalda qo'llash

- [ ] O'rnatayotgan aniq SonarQube versiyasi uchun rasmiy talablar sahifasidan JDK va PostgreSQL minimal versiyasini tekshirib yozib qo'ying, xotiradan ishonmang.
- [ ] PostgreSQL bazasini UTF8 encoding va alohida rol bilan yarating, parolni secret manager dan oling.
- [ ] Image tegini aniq versiyaga qotirib qo'ying va `latest` dan voz kechib, volume larni `data`, `extensions`, `logs` uchun ulang.
- [ ] Tugunda `vm.max_map_count=524288` va `nofile` limitini doimiy qilib qo'ying, keyin restart dan keyin qiymatlarni qayta tekshiring.
- [ ] `sonar.web.javaOpts`, `sonar.ce.javaOpts` va `sonar.search.javaOpts` ni alohida sozlang, search da `Xms` va `Xmx` ni teng qiling.
- [ ] `sonar.core.serverBaseURL` ni tashqi HTTPS manzilga qo'yib, PR dagi havolaning to'g'ri ochilishini bitta real PR da sinab ko'ring.
- [ ] Baza hajmi bo'yicha so'rovni oyda bir marta ishlatib o'sish tezligini yozib boring va housekeeping siyosatini shunga qarab qisqartiring.
- [ ] `/api/system/status`, CE navbat uzunligi va disk bandligi uchun uchta alert qo'ying, keyin baza dump dan tiklanishni sinov muhitida bir marta bajarib ko'ring.

---

[&larr; 32. SonarQube nashrlari va ularning farqi](32-sonarqube-nashrlari-va-ularning-farqi.md) · [Mundarija](README.md) · [34. Yangilash, LTA migratsiyasi, zaxira va housekeeping &rarr;](34-yangilash-lta-migratsiyasi-zaxira-va.md)
