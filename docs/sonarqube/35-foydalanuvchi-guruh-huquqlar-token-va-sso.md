<!-- doc: sonarqube | chapter: 35 | part: VIII. Server va tashkilot -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 35. Foydalanuvchi, guruh, huquqlar, token va SSO (Users, Permissions and Tokens)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [35.1 Huquqlar modeli: global huquqlar va loyiha huquqlari](#351-huquqlar-modeli-global-huquqlar-va-loyiha-huquqlari)
- [35.2 Asosiy loyiha huquqlari: ko'rish, tahlil yuritish, issue boshqarish, sozlash](#352-asosiy-loyiha-huquqlari-korish-tahlil-yuritish-issue-boshqarish-sozlash)
- [35.3 Guruhlar bilan ishlash va shaxsiy huquq bermaslik qoidasi](#353-guruhlar-bilan-ishlash-va-shaxsiy-huquq-bermaslik-qoidasi)
- [35.4 Huquq shabloni (permission template) va yangi loyihaga avtomatik qo'llash](#354-huquq-shabloni-permission-template-va-yangi-loyihaga-avtomatik-qollash)
- [35.5 Loyiha ko'rinuvchanligi: ochiq va yopiq loyihalar](#355-loyiha-korinuvchanligi-ochiq-va-yopiq-loyihalar)
- [35.6 Token turlari: foydalanuvchi, global tahlil, loyiha tahlili](#356-token-turlari-foydalanuvchi-global-tahlil-loyiha-tahlili)
- [35.7 Token ni CI da saqlash, aylantirish va muddatini belgilash](#357-token-ni-ci-da-saqlash-aylantirish-va-muddatini-belgilash)
- [35.8 LDAP, SAML va OAuth orqali kirishni ulash](#358-ldap-saml-va-oauth-orqali-kirishni-ulash)
- [35.9 Kim quality gate va profilni o'zgartira olishi kerak](#359-kim-quality-gate-va-profilni-ozgartira-olishi-kerak)
- [35.10 Audit: kim nimani o'zgartirganini kuzatish](#3510-audit-kim-nimani-ozgartirganini-kuzatish)
- [35.11 Xavfsizlik bo'yicha tez-tez uchraydigan xatolar: ochiq server, umumiy token](#3511-xavfsizlik-boyicha-tez-tez-uchraydigan-xatolar-ochiq-server-umumiy-token)
- [35.12 Amalda qo'llash](#3512-amalda-qollash)

</details>



Sonar serveri kodni o'lchaydi, lekin o'zi ham ishlab chiqarish tizimi: unda hisob, guruh, token va sozlama bor. Kim quality gate shartini o'zgartira oladi va kim tahlil yuborishi mumkin degan savol texnik savol emas, boshqaruv savoli. Bu bo'limda huquqlar modeli, guruhlar, huquq shabloni, token turlari va tashqi autentifikatsiya mexanikasi ko'rsatiladi. Darhol bir ogohlantirish: huquqlarning interfeysdagi nomlari SonarQube versiyasiga qarab biroz farq qiladi, shuning uchun quyida har bir huquqning nomi bilan birga ma'nosi ham yoziladi, siz esa o'z serveringizdagi aniq yozuvni tekshirib oling.

## 35.1 Huquqlar modeli: global huquqlar va loyiha huquqlari

Sonar da huquqlar ikki qatlamga bo'linadi. Global huquqlar butun serverga tegishli: tizim sozlamalari, quality profile va quality gate ni tahrirlash, yangi loyiha yaratish, global darajada tahlil yuritish. Loyiha huquqlari esa faqat bitta loyiha yoki uning portfeliga tegishli: loyihani ko'rish, manba kodini ko'rish, tahlil yuborish, issue bilan ishlash va loyiha sozlamalarini o'zgartirish.

Bu ajratishning amaliy ma'nosi bor. Developer ga global `Administer System` bermaslik kerak, chunki u bilan birga serverning hamma sozlamasi ochiladi. Aksincha, CI ga faqat tahlil yuritish huquqi kerak, boshqa hech narsa kerak emas. Huquqni eng kichik to'plamdan boshlab berish, keyin kamligi aniqlansa qo'shish, teskarisidan ancha xavfsiz.

| Rol | Global huquqlar | Loyiha huquqlari | Nega shunday |
| --- | --- | --- | --- |
| Tashqi kuzatuvchi (menejer) | hech qanday | Browse | faqat natijani ko'rishi kerak |
| Developer | hech qanday | Browse, See Source Code, Administer Issues | issue ni false positive deb belgilashi kerak |
| Texnik yetakchi | Administer Quality Profiles (ixtiyoriy) | yuqoridagi va Administer (loyiha) | profil va gate muhokamasini olib boradi |
| CI servis hisobi | Execute Analysis (yoki Create Projects) | Execute Analysis | faqat tahlil yuboradi, hech narsani ko'rmaydi |
| Xavfsizlik mas'uli | hech qanday | Browse, Administer Security Hotspots | hotspot ni ko'rib chiqadi va yopadi |
| Platforma admini | Administer System, Administer Quality Gates | kerak bo'lsa hammasiga | server va integratsiyani boshqaradi |
| Audit o'quvchisi | nashrga qarab alohida huquq | Browse | o'zgarishlar jurnalini o'qiydi |

Jadvaldagi nomlar interfeysda biroz boshqacha yozilishi mumkin, masalan bir versiyada "Execute Analysis", boshqasida "Run Analysis" ko'rinishida. Ma'nosi bir xil qoladi: shu hisob scanner natijasini serverga yuborishi mumkinmi yoki yo'qmi.

## 35.2 Asosiy loyiha huquqlari: ko'rish, tahlil yuritish, issue boshqarish, sozlash

Browse huquqi loyihani ro'yxatda ko'rish va o'lchovlarni ochish imkonini beradi. Uning yonida alohida See Source Code huquqi turadi. Bu ikkisi ajratilgani tasodif emas: ba'zi jamoalarda tashqi auditor metrikani ko'rishi kerak, lekin manba kodini ko'rmasligi kerak. Browse ni olib qo'ysangiz, foydalanuvchi uchun loyiha umuman yo'q bo'lib ko'rinadi.

Execute Analysis huquqi faqat CI uchun. Shaxsga berilsa, odam o'z mashinasidan tahlil yuborib, serverdagi natijani CI dagi natijadan farqli qilib qo'yadi.

Administer Issues huquqi issue ni "Won't fix" yoki "False positive" deb belgilash, jiddiylikni o'zgartirish va boshqa odamga tayinlash imkonini beradi. Bu huquq xavfli, chunki u bilan quality gate ni kodni tuzatmasdan ham yashil qilish mumkin. Shuning uchun uni developer larga berish mumkin, lekin issue ni yopish qarorini code review da muhokama qilish qoidasi bo'lishi kerak.

Administer (loyiha darajasida) huquqi loyiha sozlamalari, uning quality gate tanlovi va exclusion ro'yxatini o'zgartirishga ruxsat beradi. Eng ko'p suiiste'mol shu yerda sodir bo'ladi: kod tuzatilmaydi, `sonar.exclusions` ga katalog qo'shiladi va gate yashil bo'ladi. Bu huquqni loyihada ikki yoki uch odamda qoldirish kifoya.

## 35.3 Guruhlar bilan ishlash va shaxsiy huquq bermaslik qoidasi

Sonar huquqni ham foydalanuvchiga, ham guruhga berish imkonini beradi. Amalda faqat guruhga berish kerak. Sababi oddiy: odam jamoadan ketganda yoki boshqa loyihaga o'tganda uni bitta guruhdan chiqarish yetarli, aks holda o'nlab loyihaning huquq ro'yxatini qo'lda tozalash kerak bo'ladi.

Serverda ikki sukutdagi guruh bor: hamma autentifikatsiya qilgan foydalanuvchini o'z ichiga oladigan `sonar-users` va administratorlar guruhi `sonar-administrators`. `sonar-users` ga keng huquq bermang, chunki unga LDAP dan kelgan har bir yangi xodim avtomatik tushadi. O'z guruhlaringizni loyiha yoki jamoa nomi bilan yarating, masalan `payment-dev`, `payment-lead`, `ci-scanner`.

```bash
# Guruh yaratish va unga loyiha huquqini berish (Web API orqali).
# $SONAR_HOST va $SONAR_ADMIN_TOKEN oldindan muhit o'zgaruvchisida bo'lsin.
curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
  "$SONAR_HOST/api/user_groups/create" \
  -d "name=payment-dev" -d "description=To'lov servisi developerlari"

# Developer guruhiga ko'rish va issue boshqarish huquqi.
for P in user codeviewer issueadmin; do
  curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
    "$SONAR_HOST/api/permissions/add_group" \
    -d "groupName=payment-dev" \
    -d "projectKey=com.example:payment-service" \
    -d "permission=$P"
done

# CI guruhiga faqat tahlil yuritish huquqi.
curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
  "$SONAR_HOST/api/permissions/add_group" \
  -d "groupName=ci-scanner" \
  -d "projectKey=com.example:payment-service" \
  -d "permission=scan"
```

E'tibor bering: API da huquqlar `user`, `codeviewer`, `issueadmin`, `scan`, `admin` kabi kalitlar bilan yuritiladi, interfeysda esa odamga tushunarli nom bilan ko'rsatiladi. Kalitlar ro'yxati versiyaga qarab to'ldirilgan, masalan security hotspot uchun alohida kalit keyinchalik qo'shilgan. Shuning uchun skript yozishdan oldin o'z serveringizdagi `api/permissions/*` javobini bir marta tekshirib ko'ring.

## 35.4 Huquq shabloni (permission template) va yangi loyihaga avtomatik qo'llash

Yangi loyiha birinchi tahlildan keyin avtomatik yaratiladi. Agar huquqlar qo'lda beriladigan bo'lsa, o'nta mikroservis bo'lgan tizimda admin har hafta bir xil ishni qiladi. Huquq shabloni shu muammoni yechadi: shablonda guruhlar va ularning huquqlari yozib qo'yiladi, keyin shablon loyiha kalitining namunasiga bog'lanadi.

Masalan `com.example.payment:.*` namunasiga `payment-template` bog'langan bo'lsa, shu kalit bilan kelgan har bir yangi loyiha darhol to'g'ri guruhlarni oladi. Bu loyiha kaliti nomlash qoidasini talab qiladi, ya'ni kalitni tasodifiy emas, domen bo'yicha berish kerak.

```bash
# Shablon yaratish, unga guruh huquqlarini qo'shish va kalit namunasini bog'lash.
curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
  "$SONAR_HOST/api/permissions/create_template" \
  -d "name=payment-template" \
  -d "projectKeyPattern=com\.example\.payment:.*"

curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
  "$SONAR_HOST/api/permissions/add_group_to_template" \
  -d "templateName=payment-template" \
  -d "groupName=payment-dev" -d "permission=user"

# Mavjud loyihaga shablonni majburan qo'llash (huquqlar qayta yoziladi).
curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
  "$SONAR_HOST/api/permissions/apply_template" \
  -d "templateName=payment-template" \
  -d "projectKey=com.example.payment:order-api"
```

Shablonni mavjud loyihaga qo'llash avvalgi huquqlarni almashtiradi. Shuning uchun bu buyruqni avval sinov loyihasida ishga tushiring. Shablonlarning o'zini ham versiyaga qo'shib o'zgartiring, ya'ni yuqoridagi buyruqlarni infratuzilma repozitoriyasida skript sifatida saqlang.

## 35.5 Loyiha ko'rinuvchanligi: ochiq va yopiq loyihalar

Har bir loyihaning ko'rinuvchanligi bor: public yoki private. Ochiq loyihani serverga kirgan har bir foydalanuvchi ko'radi, ba'zi sozlamalarda esa autentifikatsiyasiz mehmon ham ko'rishi mumkin. Yopiq loyihani faqat huquq berilgan guruhlar ko'radi.

Ichki korporativ serverda sukutdagi ko'rinuvchanlikni private qilib qo'yish to'g'ri qaror. Buni global sozlamada bir marta o'zgartirsangiz, keyin yaratilgan har bir loyiha yopiq bo'lib tug'iladi. Mavjud loyihalarning ko'rinuvchanligi avtomatik o'zgarmaydi, ularni alohida ko'rib chiqish kerak.

Ochiq loyiha ba'zan kerak bo'ladi, masalan ichki open source kutubxona uchun. Lekin u manba kodini ham ochadi, shuning uchun to'lov yoki shaxsiy ma'lumot bilan ishlaydigan servisni ochiq qoldirmang.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Huquq berish | har bir odamga alohida beriladi | faqat guruhga beriladi, odam guruhga qo'shiladi |
| Yangi loyiha | admin qo'lda huquq yozadi | kalit namunasiga bog'langan huquq shabloni ishlaydi |
| Ko'rinuvchanlik | sukutdagi holat o'zgartirilmaydi | sukut private, ochiqlik alohida qarorga qo'yiladi |
| Tahlil tokeni | developer o'z tokenini CI ga qo'yadi | alohida servis hisobi va project analysis token |
| Token muddati | muddatsiz token yaratiladi | muddat belgilanadi va aylantirish taqvimi bor |
| Quality gate | har jamoa o'zi uchun gate yaratadi | bitta umumiy gate, chetga chiqish yozilib qo'yiladi |
| Kirish | lokal hisoblar qo'lda yaratiladi | LDAP yoki SAML, guruh mapping bilan |
| Issue yopish | kim xohlasa "Won't fix" qiladi | huquq cheklangan, qaror review da qoladi |
| Server kirishi | server hammaga ochiq turadi | force authentication yoqilgan, tarmoq cheklangan |
| O'zgarish izi | hech kim kuzatmaydi | audit yoki kamida konfiguratsiya tarixi saqlanadi |

## 35.6 Token turlari: foydalanuvchi, global tahlil, loyiha tahlili

Sonar ga parol bilan emas, token bilan ulanish kerak. Tokenlarning bir nechta turi bor va ular bir xil emas. Foydalanuvchi tokeni (user token) o'z egasining hamma huquqini oladi, shuning uchun CI da ishlatilmaydi. Global tahlil tokeni (global analysis token) har qanday loyihaga tahlil yuborishi mumkin, u ko'p loyihali umumiy pipeline uchun qulay. Loyiha tahlil tokeni (project analysis token) faqat bitta loyihaga tahlil yuboradi va eng xavfsiz variant.

Global va loyiha tahlil tokenlari SonarQube ning yangi liniyalarida paydo bo'lgan, eski o'rnatmalarda faqat user token bo'lishi mumkin. Agar interfeysda token turini tanlash maydoni ko'rinmasa, demak versiyangiz uni qo'llamaydi va siz servis hisobi ochib, unga faqat `scan` huquqini berib, uning user tokenini ishlatishingiz kerak.

```bash
# Loyiha tahlili uchun token yaratish (turni qo'llaydigan versiyalarda).
curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
  "$SONAR_HOST/api/user_tokens/generate" \
  -d "name=ci-payment-2026Q1" \
  -d "type=PROJECT_ANALYSIS_TOKEN" \
  -d "projectKey=com.example.payment:order-api" \
  -d "expirationDate=2026-07-01"

# Tokenlar ro'yxati: muddati tugaganini topish uchun.
curl -sS -u "$SONAR_ADMIN_TOKEN:" \
  "$SONAR_HOST/api/user_tokens/search?login=svc-ci" | head -c 2000

# Eski tokenni o'chirish (yangisini sinovdan o'tkazgandan keyin).
curl -sS -u "$SONAR_ADMIN_TOKEN:" -X POST \
  "$SONAR_HOST/api/user_tokens/revoke" -d "name=ci-payment-2025Q4"
```

Token nomiga maqsad va davrni yozish kichik, lekin foydali odat: `ci-payment-2026Q1` dan kim va nima uchun yaratganini tushunish mumkin, `token1` dan esa hech narsa tushunilmaydi.

## 35.7 Token ni CI da saqlash, aylantirish va muddatini belgilash

Token hech qachon repozitoriyaga, `pom.xml` ga yoki `sonar-project.properties` ga yozilmaydi. U CI tizimining secret omborida saqlanadi va muhit o'zgaruvchisi sifatida beriladi. Scanner yangi versiyalarda `sonar.token` xususiyatini va `SONAR_TOKEN` o'zgaruvchisini o'qiydi, eski versiyalarda `sonar.login` ishlatilgan va u endi tavsiya etilmaydi.

```yaml
# GitHub Actions: token secret dan keladi, log ga tushmaydi.
name: sonar
on:
  push:
    branches: [ main ]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0        # new code uchun tarix kerak
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - name: Test va tahlil
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        run: >
          ./mvnw -B verify sonar:sonar
          -Dsonar.host.url=$SONAR_HOST_URL
          -Dsonar.projectKey=com.example.payment:order-api
```

Lokal mashinada esa tokenni Maven ning `settings.xml` fayliga profil sifatida qo'yish mumkin, lekin fayl foydalanuvchi uy katalogida qolishi kerak va repozitoriyaga tushmasligi kerak.

```xml
<!-- ~/.m2/settings.xml: token repozitoriyada emas, uy katalogida turadi -->
<settings>
  <profiles>
    <profile>
      <id>sonar-local</id>
      <properties>
        <!-- qiymatni fayldan emas, muhit o'zgaruvchisidan olish ham mumkin -->
        <sonar.host.url>https://sonar.internal.example.com</sonar.host.url>
        <sonar.token>${env.SONAR_TOKEN}</sonar.token>
      </properties>
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>sonar-local</activeProfile>
  </activeProfiles>
</settings>
```

Tokenga muddat qo'yish majburiy odat bo'lishi kerak. Muddat yo'q token yillar davomida yashaydi va kim ishlatayotgani esdan chiqadi. Choraklik muddat qulay: aylantirish taqvimga tushadi, yangi token yaratilib, pipeline bir marta o'tgandan keyin eskisi bekor qilinadi.

Kod ichida ham xuddi shu qoida ishlaydi va Sonar buni o'zi tekshiradi. Qo'lda yozilgan parol yoki token security hotspot yoki vulnerability sifatida belgilanadi, chunki u manba kodda qoladi.

```java
// Yomon: sir kodda qoldi, Sonar bunga darhol shikoyat qiladi.
class ReportUploader {
    private static final String TOKEN = "sqa_8f21c0b4e9d1"; // sir kodda
    void upload(String body) { send(TOKEN, body); }
}

// Sonar o'tadigan variant: sir tashqaridan keladi, kodda yo'q.
@Component
class ReportUploaderFixed {
    private final String token;

    ReportUploaderFixed(@Value("${report.api.token}") String token) {
        // konfiguratsiya muhit o'zgaruvchisidan to'ldiriladi
        if (token == null || token.isBlank()) {
            throw new IllegalStateException("report.api.token berilmagan");
        }
        this.token = token;
    }

    void upload(String body) { send(token, body); }
}
```

Testda esa haqiqiy token kerak emas. Konfiguratsiyaga sinov qiymatini bering, shunda test ham o'tadi, kodda ham sir qolmaydi. Testni qanday tuzish texnikasi [testlash qo'llanmasidagi](../testing/README.md) test konfiguratsiyasi mavzusida batafsil yozilgan.

## 35.8 LDAP, SAML va OAuth orqali kirishni ulash

Lokal hisoblarni qo'lda yaratish kichik serverda ishlaydi, lekin xodim ketganda uni o'chirishni hech kim eslamaydi. Shuning uchun kirishni korporativ katalogga ulash kerak. SonarQube LDAP ni server xususiyatlari orqali, SAML va OAuth provayderlarini esa yangi versiyalarda ko'proq interfeys orqali sozlaydi. Qaysi sozlama fayldan, qaysi biri interfeysdan kelishi versiyaga qarab farq qiladi, shuning uchun o'z versiyangiz hujjatidagi maydon nomlarini tekshiring.

```properties
# sonar.properties: LDAP orqali kirish va guruh mapping.
sonar.security.realm=LDAP
sonar.security.savePassword=false

ldap.url=ldaps://ldap.internal.example.com:636
ldap.bindDn=cn=sonar-bind,ou=service,dc=example,dc=com
ldap.bindPassword=${env:LDAP_BIND_PASSWORD}

# Foydalanuvchini qidirish
ldap.user.baseDn=ou=people,dc=example,dc=com
ldap.user.request=(&(objectClass=inetOrgPerson)(uid={login}))
ldap.user.realNameAttribute=cn
ldap.user.emailAttribute=mail

# Guruhlarni olish: Sonar guruh nomi LDAP guruh nomiga mos bo'lishi kerak
ldap.group.baseDn=ou=groups,dc=example,dc=com
ldap.group.request=(&(objectClass=groupOfNames)(member={dn}))

# Mehmon kirishini yopish: ichki serverda bu yoqilgan bo'lishi kerak
sonar.forceAuthentication=true
```

`sonar.forceAuthentication` sozlamasi anonim ko'rishni butunlay yopadi. Yangi versiyalarda u sukut bo'yicha yoqilgan, eski versiyalarda esa o'chirilgan bo'lishi mumkin, shuning uchun uni ochiq yozib qo'yish xavfsizroq.

Guruh mapping ning ma'nosi shu: LDAP yoki SAML dan kelgan guruh nomi Sonar dagi guruh nomi bilan bir xil bo'lsa, foydalanuvchi kirgan paytda avtomatik shu guruhga tushadi. Shunda huquq boshqarish katalogga ko'chadi va Sonar da qo'lda ish qolmaydi. Guruh nomlarini oldindan kelishib oling, aks holda LDAP da `PaymentDev`, Sonar da `payment-dev` bo'lib, mapping ishlamaydi.

SAML da service provider va identity provider sertifikatlari muddati bor. Bu muddat tugaganda kirish to'liq to'xtaydi, shuning uchun sertifikat muddatini token aylantirish taqvimiga qo'shib qo'ying.

## 35.9 Kim quality gate va profilni o'zgartira olishi kerak

Quality gate va quality profile ni o'zgartirish huquqi global huquq. Bu to'g'ri, chunki gate shartini bir odam o'zgartirsa, u hamma loyihaga ta'sir qiladi. Amalda bu huquq platforma jamoasida va bir yoki ikki texnik yetakchida qolishi kerak.

Sababi oddiy. Gate ni bo'shatish eng tez "yechim" bo'lib ko'rinadi: coverage shartini 80 dan 60 ga tushirsang, pipeline darhol yashil bo'ladi. Shu qarorni bosim ostida turgan odam qabul qilsa, standart sekin yemiriladi. Agar o'zgartirish faqat umumiy muhokamadan o'tsa, bosim gate ga emas, kodga boradi.

Profil uchun ham xuddi shunday. Qoidani olib tashlashdan oldin uning nima uchun ishga tushganini aniqlash kerak, ba'zan qoida haqiqatan mos emas, lekin sababi yozilgan bo'lishi kerak. Qoidalar va gate shartlari mexanikasi quality gate va profil mavzularida alohida ko'rilgan.

Amaliy tartib oddiy: umumiy gate bitta bo'ladi va uni platforma jamoasi saqlaydi. Loyiha chetga chiqishni so'rasa, so'rov repozitoriyadagi faylda yozilib ko'rib chiqiladi va muddat bilan beriladi.

## 35.10 Audit: kim nimani o'zgartirganini kuzatish

Huquq, token va gate o'zgarishini kuzatish kerak. To'liq audit jurnali, ya'ni kim qachon qaysi sozlamani o'zgartirganini ko'rsatadigan alohida bo'lim, nashrga qarab mavjud bo'ladi va bepul nashrda bo'lmasligi mumkin. Agar sizning serveringizda bu bo'lim yo'q bo'lsa, taslim bo'lish shart emas, bir nechta amaliy o'rinbosar bor.

Birinchisi, huquqlarni qo'lda emas, skript bilan boshqarish: `curl` buyruqlari repozitoriyada tursa, har bir o'zgarish git tarixiga tushadi. Ikkinchisi, davriy snapshot, ya'ni huquq va token ro'yxatini API dan olib versiyalash. Uchinchisi, server loglarini markaziy log tizimiga yuborish.

```sql
-- Ma'lumotlar bazasiga to'g'ridan to'g'ri so'rov qo'yish QO'LLANMAYDI:
-- sxema versiya orasida o'zgaradi va yangilanishda buziladi.
-- Shuning uchun inventarizatsiyani API javobini saqlagan o'z jadvalingizda yuritish.
CREATE TABLE sonar_access_snapshot (
    taken_at     timestamptz NOT NULL DEFAULT now(),
    subject_kind text        NOT NULL,   -- 'group' yoki 'user' yoki 'token'
    subject_name text        NOT NULL,
    project_key  text,                   -- global huquq uchun NULL
    permission   text        NOT NULL,
    expires_at   date                    -- token uchun muddat
);

-- Muddati yaqinlashgan tokenlar: aylantirish ro'yxati.
SELECT subject_name, project_key, expires_at
FROM sonar_access_snapshot
WHERE subject_kind = 'token'
  AND expires_at IS NOT NULL
  AND expires_at < current_date + INTERVAL '30 days'
ORDER BY expires_at;
```

Bu yondashuvning foydasi shundaki, u nashrdan mustaqil ishlaydi. Zarari shundaki, u faqat snapshot oralig'idagi holatni ko'rsatadi, ya'ni ikki snapshot orasida qilingan va qaytarilgan o'zgarish ko'rinmaydi. Shuning uchun imkoni bo'lsa, haqiqiy audit jurnalidan foydalanish afzal.

## 35.11 Xavfsizlik bo'yicha tez-tez uchraydigan xatolar: ochiq server, umumiy token

Eng ko'p uchraydigan xato: Sonar serveri ichki tarmoqda deb o'ylanadi, lekin aslida u internetdan ochiq turadi. Ikkinchi xato: bitta "umumiy" token yaratiladi va u hamma pipeline da, hamma loyihada ishlatiladi. Uchinchisi: admin paroli sukutdagi holatda qoladi.

Oqibatlari bir xil emas. Ochiq server manba kodni oshkor qiladi, umumiy token esa bitta pipeline buzilganda hamma loyihaga tahlil yuborish imkonini beradi va izlanishni imkonsiz qiladi.

| Tuzoq | Nega xavfli | Yechim |
| --- | --- | --- |
| Server internetdan ochiq | manba kod va metrikalar oshkor bo'ladi | tarmoq cheklovi va reverse proxy, faqat VPN dan kirish |
| Sukutdagi admin paroli | serverni to'liq egallash mumkin | o'rnatishdan keyin darhol almashtirish, yangi admin hisob |
| Bitta umumiy token | izlanish imkonsiz, ta'sir doirasi keng | loyiha yoki pipeline uchun alohida token |
| Muddatsiz token | eski token yillar yashaydi | muddat belgilash va choraklik aylantirish |
| Token log ga tushadi | log o'quvchi hamma sirni ko'radi | secret ni muhit o'zgaruvchisiga berish, `set -x` ni o'chirish |
| Token repozitoriyada | tarixdan o'chirish qiyin | CI secret omboridan foydalanish, pre-commit scan |
| `sonar-users` ga admin huquqi | har bir yangi xodim admin bo'ladi | huquqni alohida guruhlarga berish |
| Shaxsiy token CI da | odam ketganda pipeline o'ladi | servis hisobi va uning tokeni |
| HTTP orqali ulanish | token tarmoqda ochiq ketadi | faqat HTTPS, sertifikatni tekshirish |
| Anonim ko'rish yoqilgan | autentifikatsiyasiz kirish mumkin | `sonar.forceAuthentication=true` |

Alohida eslatma: `sonar.token` yoki parolni buyruq qatorida `-D` bilan uzatish xavfli, chunki u jarayonlar ro'yxatida va CI logida ko'rinib qolishi mumkin. Muhit o'zgaruvchisi bu jihatdan yaxshiroq. Agar scanner ni debug rejimida ishga tushirsangiz, chiqishni jamoatchi log ga yubormang.

## 35.12 Amalda qo'llash

- [ ] Loyihangizdagi hamma shaxsiy huquqni ko'rib chiqing va ularni guruh huquqiga ko'chiring, keyin shaxsiy huquqlarni olib tashlang.
- [ ] `sonar-users` guruhida qanday huquq borligini tekshiring va keng huquqlarni undan olib, alohida guruhlarga bering.
- [ ] Kalit namunasiga bog'langan huquq shabloni yaratib, sinov loyihasida tekshiring, keyin yangi loyihalar uchun yoqib qo'ying.
- [ ] Global sukutdagi ko'rinuvchanlikni private qiling va mavjud ochiq loyihalar ro'yxatini ko'rib chiqing.
- [ ] CI uchun alohida servis hisobi ochib, unga faqat tahlil yuritish huquqini bering, developer tokenini pipeline dan olib tashlang.
- [ ] Hamma tokenni ro'yxatlab, muddatsizlarini muddatli yangisiga almashtiring va aylantirish sanasini taqvimga qo'ying.
- [ ] Kirishni LDAP yoki SAML ga ulab, guruh nomlarini mapping uchun kelishib oling va anonim kirishni yopganingizni tasdiqlang.
- [ ] Huquq va token inventarizatsiyasini API dan oladigan skript yozib, uning natijasini versiyalanadigan faylga yozishni avtomatlashtiring.

---

[&larr; 34. Yangilash, LTA migratsiyasi, zaxira va housekeeping](34-yangilash-lta-migratsiyasi-zaxira-va.md) · [Mundarija](README.md) · [36. Web API va avtomatlashtirish &rarr;](36-web-api-va-avtomatlashtirish.md)
