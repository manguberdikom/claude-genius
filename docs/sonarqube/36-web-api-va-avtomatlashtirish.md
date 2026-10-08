<!-- doc: sonarqube | chapter: 36 | part: IX. Kengaytirish va integratsiya -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 36. Web API va avtomatlashtirish (Web API and Automation)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [36.1 Web API qayerda hujjatlashtirilgan va uni serverdan qanday ochish](#361-web-api-qayerda-hujjatlashtirilgan-va-uni-serverdan-qanday-ochish)
- [36.2 Autentifikatsiya: token bilan so'rov yuborish](#362-autentifikatsiya-token-bilan-sorov-yuborish)
- [36.3 Loyiha holatini olish va gate natijasini skript bilan tekshirish](#363-loyiha-holatini-olish-va-gate-natijasini-skript-bilan-tekshirish)
- [36.4 Issue larni ro'yxat sifatida olish va filtrlash](#364-issue-larni-royxat-sifatida-olish-va-filtrlash)
- [36.5 Metrikalarni o'qish va tarixiy qiymatlarni olish](#365-metrikalarni-oqish-va-tarixiy-qiymatlarni-olish)
- [36.6 Quality gate va profilni API orqali yaratish va tayinlash](#366-quality-gate-va-profilni-api-orqali-yaratish-va-tayinlash)
- [36.7 Yangi loyihani avtomatik yaratish va huquq shablonini qo'llash](#367-yangi-loyihani-avtomatik-yaratish-va-huquq-shablonini-qollash)
- [36.8 Natijalarni tashqi tizimga chiqarish: hisobot, dashboard, ogohlantirish](#368-natijalarni-tashqi-tizimga-chiqarish-hisobot-dashboard-ogohlantirish)
- [36.9 Sahifalash, chegaralar va ko'p so'rov yuborishda ehtiyotkorlik](#369-sahifalash-chegaralar-va-kop-sorov-yuborishda-ehtiyotkorlik)
- [36.10 API javobini CI da ishlatish: bloklash va hisobot yasash](#3610-api-javobini-ci-da-ishlatish-bloklash-va-hisobot-yasash)
- [36.11 API versiyasi o'zgarishi va skriptlarni himoyalash](#3611-api-versiyasi-ozgarishi-va-skriptlarni-himoyalash)
- [36.12 Sonar vazifasi kelganda tartib va mbabm serverining gate shartlari (Working a Sonar Task)](#3612-sonar-vazifasi-kelganda-tartib-va-mbabm-serverining-gate-shartlari-working-a-sonar-task)
- [36.13 Amalda qo'llash](#3613-amalda-qollash)

</details>



SonarQube ning UI si tahlil natijasini odam uchun ko'rsatadi, Web API esa aynan shu ma'lumotni mashina uchun beradi. Quality gate holatini CI da tekshirish, issue larni jamoaga tarqatish, metrikani o'z dashboard ingizga chiqarish va yangi loyihani sozlash bilan birga yaratish shu API orqali qilinadi. Muhim ogohlantirish: endpoint nomlari, parametrlar va javob shakli versiyalar orasida o'zgaradi, shuning uchun har bir skriptni yozishdan oldin aynan o'z serveringizning hujjatini ochish kerak. Quyida ishonchli va keng ishlatiladigan endpointlar nomi bilan, qolganlari esa "serverda topish" ko'rsatmasi bilan beriladi.

## 36.1 Web API qayerda hujjatlashtirilgan va uni serverdan qanday ochish

Eng ishonchli hujjat sizning serveringizning o'zida turadi. SonarQube ning har bir instansiyasi `/web_api` sahifasini beradi va u aynan o'rnatilgan versiyaning endpointlarini ko'rsatadi. Ya'ni `https://sonar.example.com/web_api` manzili sizdagi parametrlarni, majburiy maydonlarni va deprecated belgilarini aniq aytadi. Internetdagi eski blog postga emas, shu sahifaga ishoning.

Bu sahifada har bir endpoint yonida qaysi versiyada paydo bo'lgani va qaysi versiyada deprecated qilingani yoziladi. "Show Internal API" tugmasi bor, u UI ning o'zi ishlatadigan ichki endpointlarni ham ko'rsatadi. Ichki endpointni skriptda ishlatish mumkin, lekin u ogohlantirishsiz o'zgaradi, shuning uchun uni faqat vaqtinchalik yechim sifatida oling.

Yangi liniyalarda `/api/v2/...` ko'rinishidagi yangi API ham paydo bo'ldi. Eski `/api/...` endpointlari hali ishlaydi, lekin ularning bir qismi asta sekin v2 ga ko'chiriladi. Shu sababli skriptda bazaviy yo'lni o'zgaruvchi qilib saqlash foydali.

```bash
# Serverning o'z hujjatini brauzerda ochish uchun manzil
echo "https://sonar.example.com/web_api"

# Server tirikmi va versiyasi nima: eng oddiy tekshiruv
curl -s "https://sonar.example.com/api/server/version"

# Tizim holati: UP, DB_MIGRATION_NEEDED yoki boshqa holat
curl -s "https://sonar.example.com/api/system/status" | jq .

# Ba'zi versiyalarda hujjat ro'yxatini JSON sifatida ham olish mumkin,
# lekin bu yo'lning mavjudligi versiyaga qarab farq qiladi.
# Shuning uchun asosiy manba /web_api sahifasi bo'lib qoladi.
```

## 36.2 Autentifikatsiya: token bilan so'rov yuborish

Parol bilan emas, token bilan ishlang. Token ni UI da foydalanuvchi profilidagi "Security" bo'limida yoki `api/user_tokens/generate` endpointi orqali yaratasiz. Tokenning turi muhim: global analysis token, project analysis token va user token har xil huquq doirasiga ega. CI uchun eng kichik huquqli variantni tanlang.

Eski klassik usul: token ni HTTP Basic ning login qismiga qo'yish, parol qismini bo'sh qoldirish. Ya'ni `-u TOKEN:` ko'rinishi. Yangi versiyalarda `Authorization: Bearer TOKEN` sarlavhasi ham qo'llaniladi va u o'qishga osonroq. Ikkisi ham keng tarqalgan, lekin aynan sizning versiyangizda qaysi biri qo'llanishini `/web_api` dagi autentifikatsiya bo'limidan tekshiring.

Token ni hech qachon repozitoriyga yozmang. CI secret yoki vault dan o'qing. Skriptda uni `echo` qilmang, chunki CI log i saqlanadi.

```bash
# Token ni muhit o'zgaruvchisidan olish, skriptga yozmaslik
: "${SONAR_TOKEN:?SONAR_TOKEN belgilanmagan}"
SONAR_URL="https://sonar.example.com"

# 1-usul: Basic auth, parol bo'sh
curl -s -u "${SONAR_TOKEN}:" "${SONAR_URL}/api/authentication/validate"

# 2-usul: Bearer sarlavha (yangi versiyalarda)
curl -s -H "Authorization: Bearer ${SONAR_TOKEN}" \
  "${SONAR_URL}/api/authentication/validate"

# Javob {"valid":true} bo'lsa token ishlayapti.
# 401 qaytsa token xato, 403 qaytsa huquq yetishmaydi: ikkisi boshqa muammo.
```

Mahalliy tahlil uchun token ni `sonar-project.properties` ga yozish vasvasasi paydo bo'ladi. Bunga yo'l qo'ymang, chunki bu fayl repozitoriyda yotadi.

```properties
# sonar-project.properties: faqat sir bo'lmagan sozlamalar
sonar.projectKey=payments-service
sonar.projectName=Payments Service
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
# Coverage hisoboti JaCoCo 0.8.x dan keladi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
# Token va host bu yerda EMAS: ular CI secret va -D parametri orqali uzatiladi
# sonar.token=... <- bunday qatorni yozmang
```

## 36.3 Loyiha holatini olish va gate natijasini skript bilan tekshirish

Gate natijasini olishning eng to'g'ri yo'li `api/qualitygates/project_status` endpointi. U `projectKey` parametri bilan loyihaning oxirgi tahlil natijasini qaytaradi. Javobda umumiy `status` maydoni bor va u `OK`, `ERROR` yoki ba'zi holatlarda `NONE` bo'ladi. Shu bilan birga har bir shart alohida ro'yxatda keladi: metrika kaliti, taqqoslash operatori, chegara va haqiqiy qiymat.

Muhim nuqta: tahlil skaner tomonidan yuborilgandan keyin server uni navbatda qayta ishlaydi. Shu sababli skaner tugashi bilan darhol gate natijasini so'rash noto'g'ri javob berishi mumkin. Skaner `target/sonar/report-task.txt` faylini yozadi va unda `ceTaskId` hamda `dashboardUrl` bo'ladi. To'g'ri ketma ketlik: `api/ce/task` orqali vazifa `SUCCESS` bo'lishini kutish, keyin gate holatini so'rash.

Shuning uchun `analysisId` yoki `ceTaskId` bo'yicha so'rash branch bo'yicha so'rashdan ishonchliroq. Branch yoki pull request uchun so'ralganda `branch` va `pullRequest` parametrlari ishlatiladi, ularning aniq nomini `/web_api` dan tasdiqlang.

```bash
set -euo pipefail
SONAR_URL="https://sonar.example.com"
TASK_URL=$(awk -F= '/^ceTaskUrl=/{sub(/^ceTaskUrl=/,""); print}' target/sonar/report-task.txt)

# Vazifa tugashini kutish, cheksiz emas: 30 marta, har 5 sekundda
for i in $(seq 1 30); do
  STATUS=$(curl -s -u "${SONAR_TOKEN}:" "${TASK_URL}" | jq -r '.task.status')
  [ "${STATUS}" = "SUCCESS" ] && break
  [ "${STATUS}" = "FAILED" ] && { echo "Tahlil xato tugadi"; exit 1; }
  sleep 5
done

# Endi gate holatini so'rash xavfsiz
curl -s -u "${SONAR_TOKEN}:" \
  "${SONAR_URL}/api/qualitygates/project_status?projectKey=payments-service" \
  | jq -r '.projectStatus.status, (.projectStatus.conditions[]
      | "\(.metricKey) \(.comparator) \(.errorThreshold) actual=\(.actualValue) \(.status)")'
```

## 36.4 Issue larni ro'yxat sifatida olish va filtrlash

`api/issues/search` endpointi issue larni qidirish uchun ishlatiladi. U juda ko'p filtr qabul qiladi: loyiha kaliti, jiddiylik, turi, holat, tayinlangan odam, qoida kaliti, fayl va sana oralig'i. Filtr nomlari versiyalar orasida o'zgargan: eski liniyalarda `severities` va `types` ishlatilgan, yangi liniyalarda "clean code attribute" va "software quality" asosidagi yangi filtrlar qo'shilgan. Shuning uchun filtr nomini aynan o'z serveringizning hujjatidan oling.

Amaliy maslahat: butun ro'yxatni tortib olish o'rniga `ps=1` va faqat `total` maydonini o'qish bilan sanashni bajarish mumkin. Bu tarmoqqa ham, serverga ham yengil. Hisobot uchun esa kerakli maydonlarni `jq` bilan tanlab oling, chunki to'liq javob katta bo'ladi.

Yangi kod bo'yicha issue larni ajratish alohida qiymatga ega, chunki gate asosan yangi kodga qaraydi. Bunday filtr uchun "new code period" ga tegishli parametr bor, lekin uning nomi versiyaga qarab farq qiladi, shuning uchun uni hujjatdan tekshirib ishlating.

```bash
SONAR_URL="https://sonar.example.com"
PROJECT="payments-service"

# Ochiq issue larni faylga yozish, 100 tadan sahifa bilan
curl -s -u "${SONAR_TOKEN}:" -G "${SONAR_URL}/api/issues/search" \
  --data-urlencode "componentKeys=${PROJECT}" \
  --data-urlencode "statuses=OPEN,CONFIRMED" \
  --data-urlencode "ps=100" --data-urlencode "p=1" \
  | jq -r '.issues[] | [.rule, .severity, .component, (.line//0), .message] | @tsv' \
  > /tmp/sonar-issues.tsv

# Faqat sanash: eng yengil so'rov, ps=1 va total ni o'qish
curl -s -u "${SONAR_TOKEN}:" -G "${SONAR_URL}/api/issues/search" \
  --data-urlencode "componentKeys=${PROJECT}" \
  --data-urlencode "ps=1" | jq '.total'

# Bitta qoida bo'yicha: masalan murakkablik qoidasi
curl -s -u "${SONAR_TOKEN}:" -G "${SONAR_URL}/api/issues/search" \
  --data-urlencode "componentKeys=${PROJECT}" \
  --data-urlencode "rules=java:S3776" --data-urlencode "ps=1" | jq '.total'
```

Security hotspot lar issue lardan alohida ro'yxatda turadi. Ularni olish uchun hotspot larga tegishli qidiruv endpointi ishlatiladi, lekin uning parametrlari ancha o'zgargan, shuning uchun `/web_api` da "hotspots" bo'limini ochib tekshiring.

## 36.5 Metrikalarni o'qish va tarixiy qiymatlarni olish

Bir nuqtadagi qiymat uchun `api/measures/component` endpointi ishlatiladi. Unga `component` sifatida loyiha kaliti va `metricKeys` sifatida vergul bilan ajratilgan metrika kalitlari beriladi. Ishonchli va keng ishlatiladigan kalitlar: `coverage`, `new_coverage`, `bugs`, `vulnerabilities`, `code_smells`, `duplicated_lines_density`, `ncloc`. Boshqa kalitni o'ylab chiqarmang, mavjud kalitlar ro'yxatini metrikalar qidiruv endpointi yoki `/web_api` beradi.

Modul va paket darajasida bo'lish uchun `api/measures/component_tree` qulay. U daraxt bo'ylab yurib har bir komponent uchun qiymat qaytaradi, shu bilan "qaysi paketda coverage past" degan savolga javob beradi.

Tarix uchun `api/measures/search_history` ishlatiladi. U metrika kalitlari va sana oralig'i bo'yicha qiymatlar qatorini qaytaradi. Shu endpoint bilan "coverage oxirgi uch oyda qanday o'zgardi" grafigini o'zingizda yasashingiz mumkin. Tahlillar ro'yxati va ularning sanasi uchun esa loyiha tahlillari qidiruv endpointi bor, uning aniq nomini hujjatdan tasdiqlang.

```bash
SONAR_URL="https://sonar.example.com"
PROJECT="payments-service"

# Bir nuqtadagi asosiy metrikalar
curl -s -u "${SONAR_TOKEN}:" -G "${SONAR_URL}/api/measures/component" \
  --data-urlencode "component=${PROJECT}" \
  --data-urlencode "metricKeys=coverage,new_coverage,bugs,vulnerabilities,code_smells,duplicated_lines_density" \
  | jq -r '.component.measures[] | "\(.metric)=\(.value // .periods[0].value)"'

# Tarix: coverage va duplication oxirgi 90 kun
FROM=$(date -u -d '90 days ago' +%F)
curl -s -u "${SONAR_TOKEN}:" -G "${SONAR_URL}/api/measures/search_history" \
  --data-urlencode "component=${PROJECT}" \
  --data-urlencode "metrics=coverage,duplicated_lines_density" \
  --data-urlencode "from=${FROM}" --data-urlencode "ps=500" \
  | jq -r '.measures[] | .metric as $m | .history[] | "\($m)\t\(.date)\t\(.value)"'
```

Olingan tarixni o'z bazangizda saqlash foydali, chunki Sonar eski tahlillarni housekeeping sozlamasiga qarab siqadi va tafsilotni yo'qotadi. Kichik jadval yetarli.

```sql
-- Metrika suratlarini o'z bazamizda saqlash: trend uchun ishonchli manba
create table sonar_metric_snapshot (
    id            bigserial primary key,
    project_key   text        not null,
    metric_key    text        not null,
    measured_at   date        not null,
    metric_value  numeric(12,4) not null,
    -- Bitta kun, bitta loyiha, bitta metrika uchun bitta qator
    constraint uq_snapshot unique (project_key, metric_key, measured_at)
);

-- Trend savoli: coverage oxirgi 30 kunda qanchaga o'zgardi
select metric_value - lag(metric_value) over (order by measured_at) as delta,
       measured_at
from sonar_metric_snapshot
where project_key = 'payments-service'
  and metric_key = 'coverage'
  and measured_at >= current_date - 30
order by measured_at;
```

## 36.6 Quality gate va profilni API orqali yaratish va tayinlash

Gate va quality profile ni qo'lda UI da sozlash kichik tashkilotda ishlaydi. Loyihalar soni oshganda bu qo'lda ish xatoga aylanadi, chunki har bir yangi loyiha tasodifiy sozlama bilan boshlanadi. Yechim: gate va profilni kod sifatida saqlash va API orqali qo'llash.

Gate yaratish uchun `api/qualitygates/create` ishlatiladi, shartlarni qo'shish uchun shartga tegishli endpoint bor va u `gateName` yoki `gateId`, `metric`, `op`, `error` parametrlarini oladi. Parametr nomlari versiyalar orasida `gateId` dan `gateName` ga ko'chgan, shuning uchun bu yerda ayniqsa hujjatni tekshirish kerak. Gate ni loyihaga bog'lash endpointining nomi ham o'zgargan, uni `/web_api` da "qualitygates" bo'limidan toping.

Quality profile uchun `api/qualityprofiles/create` va `api/qualityprofiles/add_project` keng ishlatiladi. Profilni backup qilish va tiklash uchun ham endpoint bor, u profilni XML sifatida chiqaradi. Shu XML ni repozitoriyda saqlash eng amaliy yo'l, chunki u review qilinadi va tarixi ko'rinadi.

```bash
SONAR_URL="https://sonar.example.com"
GATE="Team Backend Gate"

# 1. Gate yaratish (bir marta)
curl -s -u "${SONAR_TOKEN}:" -X POST "${SONAR_URL}/api/qualitygates/create" \
  --data-urlencode "name=${GATE}"

# 2. Shart qo'shish: parametr nomlari versiyaga qarab gateId yoki gateName.
# Avval /web_api dagi "qualitygates" bo'limida aniq nomni tekshiring.
curl -s -u "${SONAR_TOKEN}:" -X POST \
  "${SONAR_URL}/api/qualitygates/create_condition" \
  --data-urlencode "gateName=${GATE}" \
  --data-urlencode "metric=new_coverage" \
  --data-urlencode "op=LT" --data-urlencode "error=80"

# 3. Profilni XML sifatida saqlab, git ga qo'yish
curl -s -u "${SONAR_TOKEN}:" -G "${SONAR_URL}/api/qualityprofiles/backup" \
  --data-urlencode "language=java" \
  --data-urlencode "qualityProfile=Backend Java" > profiles/backend-java.xml
```

## 36.7 Yangi loyihani avtomatik yaratish va huquq shablonini qo'llash

Yangi mikroservis paydo bo'lganda uch ish birga bajarilishi kerak: loyiha yaratish, kerakli quality profile ni bog'lash va huquqlarni berish. Qo'lda bajarilsa ulardan biri doimo esdan chiqadi. Natijada loyiha "default" profil bilan ishlaydi yoki jamoa unga kira olmaydi.

Loyiha yaratish uchun `api/projects/create` ishlatiladi, u `project` va `name` parametrlarini oladi. Mavjudligini tekshirish uchun `api/projects/search` qulay. Huquqlar uchun permission template tayinlanadi va buning endpointi `api/permissions/apply_template`. Bu uchtasini bitta skriptga yig'ish provizion vaqtini bir daqiqaga tushiradi.

Agar monorepo ichida bir nechta modul alohida loyiha sifatida ko'rilsa, kalitlash qoidasini oldindan belgilang. Masalan `org.company:service-payments` ko'rinishi. Kalit keyin o'zgarsa, barcha tarix va trend uziladi.

```bash
set -euo pipefail
SONAR_URL="https://sonar.example.com"
KEY="org.company:service-inventory"
NAME="Inventory Service"
TEMPLATE="Backend Services"

# Loyiha bormi: bo'lmasa yaratamiz (idempotent skript)
EXISTS=$(curl -s -u "${SONAR_TOKEN}:" -G "${SONAR_URL}/api/projects/search" \
  --data-urlencode "projects=${KEY}" | jq '.paging.total')

if [ "${EXISTS}" = "0" ]; then
  curl -s -u "${SONAR_TOKEN}:" -X POST "${SONAR_URL}/api/projects/create" \
    --data-urlencode "project=${KEY}" --data-urlencode "name=${NAME}"
fi

# Java profilini bog'lash
curl -s -u "${SONAR_TOKEN}:" -X POST "${SONAR_URL}/api/qualityprofiles/add_project" \
  --data-urlencode "project=${KEY}" --data-urlencode "language=java" \
  --data-urlencode "qualityProfile=Backend Java"

# Huquq shablonini qo'llash
curl -s -u "${SONAR_TOKEN}:" -X POST "${SONAR_URL}/api/permissions/apply_template" \
  --data-urlencode "projectKey=${KEY}" --data-urlencode "templateName=${TEMPLATE}"
```

## 36.8 Natijalarni tashqi tizimga chiqarish: hisobot, dashboard, ogohlantirish

Sonar ning UI si yaxshi, lekin u jamoaning kundalik oqimida emas. Shuning uchun uchta chiqish nuqtasi amalda qiymat beradi: haftalik hisobot, umumiy dashboard va darhol ogohlantirish. Uchtasi ham bir xil manbadan, ya'ni metrika va gate endpointlaridan oziqlanadi.

Ogohlantirishda tanlov muhim. Har bir yangi code smell uchun xabar yuborish shovqin yaratadi va jamoa uni o'chirib qo'yadi. Faqat ikki holatda xabar yuboring: gate `ERROR` ga o'tganda va yangi security issue paydo bo'lganda. Qolgani haftalik hisobotda ko'rinsa yetarli.

Java tarafida kichik Spring komponenti yozish qulay, chunki u scheduler, retry va o'z bazangizga yozishni bir joyda beradi. Quyidagi misol gate holatini o'qiydi va faqat buzilganda xabar yuboradi.

```java
// Gate holatini o'qiydigan kichik komponent: faqat buzilganda xabar yuboradi
@Component
class GateWatcher {
    private final RestClient client;   // bazaviy URL va token bilan sozlangan
    private final Notifier notifier;

    GateWatcher(RestClient client, Notifier notifier) {
        this.client = client; this.notifier = notifier;
    }

    @Scheduled(cron = "0 */15 * * * *")   // har 15 daqiqada, tez tez emas
    void check() {
        ProjectStatusResponse body = client.get()
                .uri(b -> b.path("/api/qualitygates/project_status")
                           .queryParam("projectKey", "payments-service").build())
                .retrieve().body(ProjectStatusResponse.class);

        // NONE holati "hali tahlil bo'lmagan" degani: bu xato emas
        if (body == null || !"ERROR".equals(body.projectStatus().status())) {
            return;
        }
        String buzilgan = body.projectStatus().conditions().stream()
                .filter(c -> "ERROR".equals(c.status()))
                .map(c -> c.metricKey() + "=" + c.actualValue())
                .collect(Collectors.joining(", "));
        notifier.send("Gate buzildi: " + buzilgan);
    }
}
```

Bu komponentning testi Sonar serveriga ulanmasligi kerak. HTTP javobini mock qilish usullari [testlash qo'llanmasidagi](../testing/README.md) tashqi servis mock mavzusida yoritilgan.

## 36.9 Sahifalash, chegaralar va ko'p so'rov yuborishda ehtiyotkorlik

Qidiruv endpointlari sahifalab javob beradi. `p` sahifa raqami, `ps` sahifadagi element soni. `ps` ning maksimumi odatda 500 atrofida va undan katta qiymat xato qaytaradi. Bundan muhimi: ko'plab qidiruv endpointlarida umumiy natija chuqurligi chegaralangan, ya'ni `p * ps` ma'lum sondan oshsa server xato beradi. Shu sababli "barcha issue larni tortib olaman" degan yondashuv katta loyihada ishlamaydi.

To'g'ri yechim: natijani kichik bo'laklarga bo'lish. Masalan har bir fayl yoki har bir qoida bo'yicha alohida so'rash, yoki sana oralig'ini kichraytirish. Yana bir yo'l: issue larni emas, agregat metrikalarni o'qish, chunki sanoq uchun `total` maydoni yetarli.

So'rovlar sonini ham cheklang. CI da yuzlab parallel job bitta Sonar serverga yopirilsa, server sekinlashadi va tahlil navbati o'sadi. Retry da eksponensial kutish ishlatish va 429 yoki 503 javobida darhol qayta urinmaslik kerak.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Skaner tugashi bilan gate so'raladi | Eski tahlil natijasi o'qiladi, CI yolg'on yashil | `report-task.txt` dagi `ceTaskUrl` ni `SUCCESS` bo'lgunicha kutish |
| `ps=1000` berish | Xato javob yoki kesilgan ro'yxat | `ps` ni 500 dan oshirmaslik, sahifalab yurish |
| Chuqur sahifalash, `p=200` | Server chegara xatosini qaytaradi | So'rovni qoida yoki fayl bo'yicha bo'lish |
| Token repozitoriyda | Sir tarqaydi, token ni almashtirish kerak | CI secret yoki vault, token ni log ga chiqarmaslik |
| Admin token CI da | Har qanday skript loyiha o'chirishi mumkin | Analysis token, eng kichik huquq doirasi |
| Ichki API ga tayanish | Versiya yangilanganda skript jim o'ladi | Faqat hujjatlangan endpointlar, smoke test bilan tekshirish |
| `jq` bo'lmasa grep bilan parsing | Javob shakli o'zgarsa noto'g'ri qiymat chiqadi | `jq` ni majburiy qilish, maydonni nomi bilan o'qish |
| Har 10 sekundda polling | Server yuklanadi, navbat o'sadi | Interval ni kattalashtirish, eksponensial kutish |
| Metrika kaliti o'ylab chiqarilgan | Javobda `null` keladi, hisobot bo'sh | Kalitni metrikalar qidiruvidan yoki `/web_api` dan olish |

## 36.10 API javobini CI da ishlatish: bloklash va hisobot yasash

CI da ikki xil qaror bor: bloklash va xabar berish. Maven plugin da `sonar.qualitygate.wait=true` parametri skanerni gate natijasini kutishga majbur qiladi va gate buzilsa build ni yiqitadi. Bu eng oddiy yo'l va ko'p holatda yetarli. Lekin u faqat "o'tdi yoki o'tmadi" deydi, qaysi shart buzilganini chiroyli ko'rsatmaydi.

Shuning uchun amaliy sxema: skaner `wait` bilan ishlaydi, keyin alohida qadam `api/qualitygates/project_status` dan tafsilotni olib PR izohiga yozadi. Bloklash skaner tomonida, tushuntirish API tomonida bo'ladi.

```xml
<!-- Maven: skaner gate natijasini kutadi va buzilsa build yiqiladi -->
<plugin>
  <groupId>org.sonarsource.scanner.maven</groupId>
  <artifactId>sonar-maven-plugin</artifactId>
  <!-- Versiyani o'z loyihangizdagi qiymat bilan belgilang -->
  <configuration>
    <!-- Gate natijasini kutish: CI ni bloklash uchun eng oddiy yo'l -->
    <sonar.qualitygate.wait>true</sonar.qualitygate.wait>
    <!-- Kutish chegarasi sekundda: cheksiz kutmaslik uchun -->
    <sonar.qualitygate.timeout>300</sonar.qualitygate.timeout>
  </configuration>
</plugin>
```

```yaml
# CI: avval coverage, keyin tahlil, keyin API dan tafsilot
steps:
  - name: Test va coverage
    run: ./mvnw -B verify   # JaCoCo 0.8.x xml hisobotini yozadi

  - name: Sonar tahlili
    env:
      SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    run: >
      ./mvnw -B sonar:sonar
      -Dsonar.host.url=https://sonar.example.com
      -Dsonar.qualitygate.wait=true

  - name: Gate tafsilotini PR ga yozish
    if: always()          # gate yiqilsa ham tafsilot kerak
    env:
      SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    run: ./ci/gate-report.sh payments-service
```

| Vazifa | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Gate natijasini bilish | UI ni ochib ko'z bilan qarash | `project_status` javobini CI da o'qib qaror qilish |
| Tahlil tugashini kutish | `sleep 60` qo'yish | `ceTaskUrl` ni `SUCCESS` bo'lgunicha polling qilish |
| Token saqlash | `pom.xml` yoki properties faylida | CI secret, analysis token, aylantirish jadvali bilan |
| Gate sozlamasi | UI da qo'lda, har loyihada boshqa | Gate va profil XML sifatida git da, API orqali qo'llanadi |
| Yangi loyiha | Qo'lda yaratish, profil esdan chiqadi | Idempotent provizion skripti: yaratish, profil, huquq |
| Issue larni tarqatish | Haftada bir UI dan eksport | Filtrlangan so'rov, faqat yangi kod, avtomatik izoh |
| Trend kuzatish | Oxirgi qiymatga qarash | `search_history` dan o'qib o'z bazada saqlash |
| Ogohlantirish | Har bir issue uchun xabar | Faqat gate `ERROR` va yangi security issue uchun |
| API o'zgarishi | Yangilanishdan keyin skript jim o'ladi | Smoke test, versiya tekshiruvi, bitta klient qatlami |
| Hisobot | Qo'lda skrinshot | Metrika endpointidan generatsiya qilingan hisobot |

## 36.11 API versiyasi o'zgarishi va skriptlarni himoyalash

Eng ko'p uchraydigan nosozlik: SonarQube yangilangandan keyin CI skripti xatoga tushadi yoki undan yomoni, jim jim noto'g'ri natija beradi. Sabab oddiy. Parametr nomi o'zgargan, endpoint deprecated bo'lgan yoki javobdagi maydon boshqa joyga ko'chgan. 9.9 LTA va 2025 LTA liniyalari orasida ayniqsa issue va jiddiylik modeli sezilarli o'zgargan.

Himoya uchun to'rt oddiy qoida bor. Birinchi: barcha API chaqiruvlarini bitta joyda saqlang, masalan bitta `sonar-api.sh` yoki bitta Java klient klassi. Shunda o'zgarish bitta faylga tegadi. Ikkinchi: javobdan maydonni nomi bilan oling va uning yo'qligini xato deb hisoblang. Agar `status` maydoni `null` bo'lsa, skript yashil qaytarmasligi kerak.

Uchinchi: serverning versiyasini `api/server/version` dan o'qib, kutilgan liniya bilan solishtiring va mos kelmasa ogohlantirish bering. To'rtinchi: kichik smoke test yozing va uni kunda bir marta ishlating. U faqat uch narsani tekshirsin: token ishlaydi, `project_status` javobida `status` bor, `measures/component` javobida kutilgan metrika bor.

```bash
#!/usr/bin/env bash
# sonar-smoke.sh: API shartnomasi hali amal qilayotganini tekshiradi
set -euo pipefail
SONAR_URL="https://sonar.example.com"; PROJECT="payments-service"
AUTH=(-u "${SONAR_TOKEN}:")

# 1. Token amal qiladi
curl -sf "${AUTH[@]}" "${SONAR_URL}/api/authentication/validate" | jq -e '.valid == true' >/dev/null

# 2. Gate javobida status maydoni bor va u kutilgan qiymatlardan biri
ST=$(curl -sf "${AUTH[@]}" -G "${SONAR_URL}/api/qualitygates/project_status" \
      --data-urlencode "projectKey=${PROJECT}" | jq -r '.projectStatus.status')
case "${ST}" in OK|ERROR|NONE) ;; *) echo "Kutilmagan status: ${ST}"; exit 1 ;; esac

# 3. Metrika kaliti hali mavjud
curl -sf "${AUTH[@]}" -G "${SONAR_URL}/api/measures/component" \
  --data-urlencode "component=${PROJECT}" --data-urlencode "metricKeys=coverage" \
  | jq -e '.component.measures | length > 0' >/dev/null

echo "Smoke test o'tdi"
```

Yana bir muhim nuqta: `curl` da `-f` flagini ishlatish. Usiz HTTP 404 yoki 500 javobi ham `exit 0` bilan tugaydi va skript xato javobni ma'lumot deb qabul qiladi. Bu aynan "yashil CI, buzilgan tekshiruv" holatiga olib keladi.

## 36.12 Sonar vazifasi kelganda tartib va mbabm serverining gate shartlari (Working a Sonar Task)

Sonar vazifasi kelganda issue larni qo'lda ko'chirmaslik uchun `tools/sonar_fetch.py` serverdan faqat o'qiydi: `issues` (ochiq issue lar TSV: kalit, daraja, tur, fayl, qator, xabar), `gate` (shartlar va qiymatlar), `coverage` (fayl bo'yicha `uncovered_lines` va `uncovered_conditions`), `hotspots` (`TO_REVIEW` holatdagilar). Token qiymati kodga, logga va chiqishga yozilmaydi: u `GENIUS_SONAR_TOKEN_FILE` ko'rsatgan fayldan (sukut `~/.sonar-token.txt`) o'qiladi va `-u token:` ko'rinishida yuboriladi. Server `GENIUS_SONAR_URL` (sukut `https://sonar.mbabm.uz`), project key `--loyiha` yoki `GENIUS_SONAR_PROJECT` dan olinadi (masalan `service-space-space-attendance-control-dev`).

```bash
python3 tools/sonar_fetch.py gate --loyiha service-space-space-attendance-control-dev
python3 tools/sonar_fetch.py issues --chiqish issues.tsv
python3 tools/sonar_fetch.py coverage
```

Tartib: 1) token fayli borligini tekshirish; 2) `gate` bilan yiqilgan shartni aniqlash; 3) `issues` ni `kalit` bo'yicha guruhlash, eng ko'pidan boshlash; 4) guruhlarni fayl bo'yicha kesishmaydigan to'plamlarga bo'lish, shunda parallel aktyorlar bir faylga tegmaydi; 5) tuzatish va `check_code.py` bilan qayta tekshirish. Serverda holatni o'zgartiradigan amallar tashqi ta'sir: hotspot ni `SAFE` deb belgilash va issue ni `Accept` yoki `won't fix` qilish faqat foydalanuvchi roziligi bilan bajariladi, asbob ularni bajarmaydi.

2026-10-08 holatida serverdagi quality gate shartlari (ERROR beradigan chegara):

| Metrika | Chegara |
| --- | --- |
| `new_coverage` | 60 dan kam |
| `coverage` | 50 dan kam |
| `new_duplicated_lines_density` | 10 dan ko'p |
| `duplicated_lines_density` | 20 dan ko'p |
| `new_security_hotspots_reviewed` | 70 dan kam |
| `security_hotspots_reviewed` | 60 dan kam |
| `new_violations` | 30 dan ko'p |
| `software_quality_reliability_rating` | 3 dan katta |
| `software_quality_security_rating` | 3 dan katta |

Coverage faqat `test` task ning JaCoCo hisobotidan keladi; integratsion testlar `integrationTest` da yuradi va coverage ga kirmaydi. Kotlin fayllar uchun "ABM Kotlin" profili ishlatiladi.

Yuzlab issue li katta tozalashda parallel andoza:

1. Issue lar paket bo'yicha kesishmaydigan guruhlarga bo'linadi, har guruh o'z worktree ida ishlaydi.
2. Ko'p paketga tegadigan qoidalar guruhga berilmaydi: deprecated API ni o'chirish (`java:S1874`, `java:S1133`, `java:S6355`, `java:S5738`, `java:S1123`) va restricted nomli metodni qayta nomlash (`java:S6213` method). Ular alohida "cross" worktree da, o'z branchida commit bilan bajariladi va oxirida haqiqiy `git merge` (3-way) bilan qo'shiladi.
3. Paket guruhlari patch sifatida qo'shiladi (`guruh.py birlashtir --3way`), guruh tugashi bilan darhol, oxirgisini kutmasdan.
4. Har birlashtirishdan keyin kompilyatsiya: guruhlar yozgan yangi kod o'chirilgan yoki qayta nomlangan API ga murojaat qilishi mumkin.
5. Sonar API ning `sources/lines` chaqiruvi fayl boshiga sekin va timeout siz osiladi, shuning uchun qatorma-qator coverage ni lokal JaCoCo XML dan oling. O'lchash uchun `run_tests.py --coverage`: maqsadli yurishda ham jacoco agenti va hisobot qoladi, hisobot yo'li chiqishda aytiladi.

## 36.13 Amalda qo'llash

- [ ] O'z serveringizning `/web_api` sahifasini ochib, skriptlarda ishlatayotgan har bir endpoint va parametr nomini tasdiqlang, deprecated belgisi borlarini ro'yxatga oling.
- [ ] CI dagi Sonar token ni tekshirib ko'ring: u admin huquqli bo'lmasin, faqat analysis doirasida bo'lsin, va `pom.xml` yoki properties fayllarida saqlanmasin.
- [ ] `report-task.txt` dagi `ceTaskUrl` ni kutadigan qadam qo'shing, `sleep` ga tayangan joylarni olib tashlang.
- [ ] `gate-report.sh` skriptini yozing: `api/qualitygates/project_status` javobidan buzilgan shartlarni chiqarib PR izohiga yozsin.
- [ ] Barcha API chaqiruvlarini bitta klient qatlamiga yig'ing, bir nechta joyda takrorlangan `curl` larni o'sha yerga ko'chiring.
- [ ] `sonar-smoke.sh` ni kunda bir marta ishlatadigan CI job yarating, u token, gate javobi va metrika kalitini tekshirsin.
- [ ] Yangi loyiha uchun idempotent provizion skripti yozing: `api/projects/create`, `api/qualityprofiles/add_project` va `api/permissions/apply_template` bitta qadamda bajarilsin.
- [ ] `api/measures/search_history` dan coverage va duplication qiymatlarini haftada bir o'qib o'z bazangizga yozadigan ish qo'shing, trend uchun ishonchli manba shu bo'ladi.
- [ ] Sonar vazifasida avval `python3 tools/sonar_fetch.py gate` bilan yiqilgan shartni aniqlang; hotspot va issue holatini o'zgartirish uchun foydalanuvchi roziligini oling.

---

[&larr; 35. Foydalanuvchi, guruh, huquqlar, token va SSO](35-foydalanuvchi-guruh-huquqlar-token-va-sso.md) · [Mundarija](README.md) · [37. Taint analysis mexanikasi: source, sink, sanitizer &rarr;](37-taint-analysis-mexanikasi-source-sink.md)
