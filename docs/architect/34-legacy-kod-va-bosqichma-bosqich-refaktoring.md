<!-- doc: architect | chapter: 34 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 34. Legacy kod va bosqichma-bosqich refaktoring (Legacy Code and Refactoring)

<details>
<summary>Bu bobdagi 22 bo'lim</summary>

- [34.1 Legacy kodga birinchi kun: o'qish, o'lchash, hech narsani o'zgartirmaslik](#341-legacy-kodga-birinchi-kun-oqish-olchash-hech-narsani-ozgartirmaslik)
- [34.2 Tizimni tushunish usullari: kirish nuqtalari, ma'lumot oqimi, eng ko'p o'zgargan fayllar](#342-tizimni-tushunish-usullari-kirish-nuqtalari-malumot-oqimi-eng-kop-ozgargan-fayllar)
- [34.3 Xavfsizlik to'ri qurish: xatti-harakatni qayd etuvchi test](#343-xavfsizlik-tori-qurish-xatti-harakatni-qayd-etuvchi-test)
- [34.4 Chok (seam) topish: o'zgarishni kiritish mumkin bo'lgan nuqta](#344-chok-seam-topish-ozgarishni-kiritish-mumkin-bolgan-nuqta)
- [34.5 Kichik qadamlar: har bir qadamdan keyin ishlaydigan tizim](#345-kichik-qadamlar-har-bir-qadamdan-keyin-ishlaydigan-tizim)
- [34.6 Katta qayta yozish nega deyarli har doim muvaffaqiyatsiz bo'ladi](#346-katta-qayta-yozish-nega-deyarli-har-doim-muvaffaqiyatsiz-boladi)
- [34.7 Bo'g'uvchi anjir (strangler) usuli bilan bosqichma-bosqich almashtirish](#347-boguvchi-anjir-strangler-usuli-bilan-bosqichma-bosqich-almashtirish)
- [34.8 Ma'lumotlar bazasini ajratish: eng qiyin qism va uning tartibi](#348-malumotlar-bazasini-ajratish-eng-qiyin-qism-va-uning-tartibi)
- [34.9 Refaktoringni biznes bilan kelishish: qiymat tilida tushuntirish](#349-refaktoringni-biznes-bilan-kelishish-qiymat-tilida-tushuntirish)
- [34.10 O'lchov: refaktoring ishladimi yoki yo'qligini qanday bilish](#3410-olchov-refaktoring-ishladimi-yoki-yoqligini-qanday-bilish)
- [34.11 Qachon tegmaslik kerak: ishlayotgan, o'zgarmaydigan kod](#3411-qachon-tegmaslik-kerak-ishlayotgan-ozgarmaydigan-kod)
- [34.12 Bosqichma-bosqich reja namunasi: to'lov moduli misolida](#3412-bosqichma-bosqich-reja-namunasi-tolov-moduli-misolida)
- [34.13 O'zgarishning to'rt sababi va xavfni uch savol bilan chegaralash](#3413-ozgarishning-tort-sababi-va-xavfni-uch-savol-bilan-chegaralash)
- [34.14 Ta'sir qanday tarqaladi: uch yo'l va inkapsulyatsiyaning foydasi](#3414-tasir-qanday-tarqaladi-uch-yol-va-inkapsulyatsiyaning-foydasi)
- [34.15 Vaqtincha qoplama test: yuqori darajada yozib, keyin pastga tushirish](#3415-vaqtincha-qoplama-test-yuqori-darajada-yozib-keyin-pastga-tushirish)
- [34.16 Metod ichidagi `new` ni testda almashtirish: Extract and Override uchligi](#3416-metod-ichidagi-new-ni-testda-almashtirish-extract-and-override-uchligi)
- [34.17 Statik chaqiruv va singleton: instance delegator va static setter](#3417-statik-chaqiruv-va-singleton-instance-delegator-va-static-setter)
- [34.18 Interface ajratish ishlamaganda: Adapt Parameter va Extract Implementer](#3418-interface-ajratish-ishlamaganda-adapt-parameter-va-extract-implementer)
- [34.19 Nimadan boshlash: qiymat va qiyinlik kvadranti](#3419-nimadan-boshlash-qiymat-va-qiyinlik-kvadranti)
- [34.20 Bazani ajratishning besh qadami va ma'lumot suvereniteti narxi](#3420-bazani-ajratishning-besh-qadami-va-malumot-suvereniteti-narxi)
- [34.21 Deprecation ni jarayon sifatida yuritish: ega, almashtirish va orqaga qaytishni to'sish](#3421-deprecation-ni-jarayon-sifatida-yuritish-ega-almashtirish-va-orqaga-qaytishni-tosish)
- [34.22 Amalda qo'llash](#3422-amalda-qollash)

</details>



Legacy kod degani eski kod emas va uni kim yozgani ham ahamiyatsiz. Michael
Feathers ta'rifi bo'yicha legacy kod - testlari yo'q kod; kod qanchalik yaxshi
yozilgani, qanchalik obyektga yo'naltirilgan yoki inkapsulyatsiya qilingani bu
ta'rifni o'zgartirmaydi (*Working Effectively with Legacy Code*, Preface,
xvi-bet). Sababi oddiy: testlar bo'lsa kodning xatti-harakatini tez va
tekshirib bo'ladigan tarzda o'zgartirish mumkin, testlar bo'lmasa kod
yaxshilanayotganini yoki buzilayotganini bilish imkoni yo'q. Shu ta'rifdan
amaliy xulosa chiqadi: refaktoring kodni o'zgartirishdan emas, kodning hozirgi
xatti-harakatini qayd etishdan boshlanadi. Bu bobda arxitektor legacy tizimga
kirib, uni to'xtatmasdan bosqichma-bosqich almashtirish ketma-ketligi ko'rib
chiqiladi.

## 34.1 Legacy kodga birinchi kun: o'qish, o'lchash, hech narsani o'zgartirmaslik

Birinchi kunning maqsadi bitta: tizimni ishlab turgan holda ko'rish. "Kichik
tozalash" qilinmaydi, chunki siz hali qaysi g'alati kod atayin yozilganini
bilmaysiz. `OrderService` ichidagi tushunarsiz `if (status == 7 && legacyFlag)`
sharti ko'pincha eski incident'ning yechimi bo'lib chiqadi.

Tartib o'ylab topilmaydi, u kitobda bor. Feathers legacy kodga o'zgarish
kiritishning besh qadamli algoritmini beradi: o'zgarish nuqtalarini aniqlash,
test nuqtalarini topish, bog'liqliklarni uzish, test yozish, keyin o'zgartirish
va refaktoring (*Working Effectively with Legacy Code*, 2-bob, 18-bet). Kod
mantiqining o'zgarishi beshinchi qadamda turadi, birinchida emas. Birinchi kun
shu algoritmning birinchi va ikkinchi qadamiga tegishli.

Birinchi kunda uchta narsa yig'iladi: build qanday ishlaydi, ilova qanday
ko'tariladi, va production'da qaysi kod aslida chaqiriladi. Uchinchisi eng
qimmatli. Spring Boot'da bu `actuator` metrikalari va log'lar orqali ko'rinadi.

```bash
# Build va ishga tushish vaqtini o'lchaymiz, keyin taqqoslash uchun asos bo'ladi
./mvnw -q -DskipTests package
# Bean'lar soni: konteyner kattaligi haqida birinchi raqam
curl -s localhost:8080/actuator/beans | jq '[.contexts[].beans | keys[]] | length'
# Eng sekin endpoint'lar: bu refaktoring uchun birinchi nomzodlar ro'yxati
curl -s localhost:8080/actuator/metrics/http.server.requests \
  | jq '.availableTags[] | select(.tag=="uri") | .values'
```

Birinchi kun oxirida sizda o'zgarish emas, o'lchov bo'lishi kerak: startup
vaqti, bean soni, eng ko'p chaqirilgan endpoint'lar, eng sekin so'rovlar. Bu
raqamlarning "normal" qiymati yo'q, ularning qiymati taqqoslashda: keyinchalik
"yaxshilandi" degan gapni dalilga aylantiradigan boshlang'ich nuqta.

O'qishning o'zida bitta tuzoq bor va u birinchi kunning oxirida paydo bo'ladi:
kod arxitektura abstraksiyalariga mos kelmaydi. Fairbanks buni muqarrar deb
ataydi, chunki kitoblardagi arxitektura abstraksiyalari dasturlash tilida,
freymvorkda va eski kodda mavjud bo'lgan abstraksiyalar bilan ustma-ust
tushmaydi; shuning uchun modelni kodga tushirishda yoki kodning arxitekturasini
o'qishda ishqalanish bo'ladi. Vasvasa ham oldindan ma'lum: kodni aniq modul va
komponentlarga refaktoring qilib moslashtirish. Kitobning javobi qat'iy, bu
odatda juda qimmat; amaliyroq yo'l mavjud tizimni yirik modul yoki
komponentlar to'plami deb qarash va ularning ichki quyi komponentlarini
modellashtirmaslik. Birinchi kunda bu shunday ko'rinadi: `legacy-core` ni bitta
qora quti deb belgilab, uning tashqi qirralarini (endpoint, jadval, navbat,
cron) ro'yxatga olasiz, ichidagi paketlar ierarxiyasini qayta chizmaysiz.
Moslikni oldindan oson qilish esa faqat yangi kodda mumkin, va u
[5.20](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md#520-cheklov-yonaltiruvchi-sifatida-foydasi-va-kiritish-tartibi)
dagi cheklov tartibi bilan boradi.

## 34.2 Tizimni tushunish usullari: kirish nuqtalari, ma'lumot oqimi, eng ko'p o'zgargan fayllar

Legacy tizimni to'liq o'qib chiqish mumkin emas. Katta monolitda o'qish tartibi
kerak: kirish nuqtalari, ma'lumot oqimi va o'zgarish tarixi.

Kirish nuqtalari deganda HTTP controller'lar, Kafka listener'lar, `@Scheduled`
job'lar va JMS consumer'lar tushuniladi. Ular kod bazasining kichik qismi bo'lsa
ham, tizim tashqi dunyo uchun nima qilishini to'liq belgilaydi.

```bash
# Kirish nuqtalari xaritasi: tizim tashqi dunyo bilan qayerda gaplashadi
grep -rln --include=*.java -E '@(RestController|Controller)' src/main/java | wc -l
grep -rn --include=*.java -E '@(KafkaListener|RabbitListener|JmsListener)' src/main/java
grep -rn --include=*.java '@Scheduled' src/main/java

# O'zgarish tarixi: oxirgi 2 yilda eng ko'p tegilgan fayllar
git log --since="2 years ago" --name-only --pretty=format: \
  | grep '\.java$' | sort | uniq -c | sort -rn | head -30
```

Oxirgi buyruq eng muhim ro'yxatni beradi. Tez-tez o'zgaradigan va katta fayl,
ya'ni yuqori churn va yuqori murakkablik kesishgan joy, refaktoringdan foyda
chiqadigan nuqta. Feathers shu holatga ikki alohida bob bag'ishlaydi: bitta
joyda ko'p o'zgarish kiritish kerak bo'lgan holat (12-bob) va bir xil kodni
hamma yerda o'zgartirish holati (21-bob). Kamdan kam tegiladigan katta fayl esa
odatda tinch qoldiriladi.

Kodni tushunish uchun Feathers o'qishning o'zini yetarli deb hisoblamaydi va
uchta usul beradi. Notes/Sketching: o'qiyotganda qog'ozda sinflar va chaqiruvlar
sxemasini chizish, sxema rasmiy notatsiya bo'lishi shart emas (16-bob,
210-bet). Scratch refactoring: kodni tushunish uchun qo'rqmasdan refaktoring
qilish, lekin natijani commit qilmaslik, oxirida hammasini tashlab yuborish
(212-bet). Delete unused code: ishlatilmayotgan kodni o'chirish, chunki u
o'qishni qiyinlashtiradi va boshqa hech narsa bermaydi (213-bet). O'zgarish
ta'siri qayerga yetib borishini kuzatish uchun esa effect sketch ishlatiladi:
o'zgargan narsadan boshlab unga bog'liq narsalarga strelka chiziladi (11-bob,
155-bet).

Uzun metod uchun Feathers to'rtinchi usulni beradi: listing markup, ya'ni
kodni chop etib qog'ozda belgilash (16-bob, 211-bet). Belgilash shakli
maqsadga qarab o'zgaradi. Mas'uliyatlarni ajratish uchun bir-biriga tegishli
qatorlar bitta belgi bilan guruhlanadi. Uzun metodning tuzilishini ko'rish
uchun blok boshi va oxiri chiziq bilan tutashtiriladi, va bu ichkaridan
tashqariga qarab bajariladi: birinchi yopiluvchi qavs topiladi, keyin unga
mos ochiluvchi qavs belgilanadi. Ajratishga nomzod bo'lak aylana bilan
belgilanib, yoniga bog'liqlik soni yoziladi. O'zgarish ta'sirini ko'rish
uchun esa effect sketch o'rniga o'zgaradigan qator belgilanadi, keyin
qiymati shundan o'zgaradigan har bir o'zgaruvchi va ta'sirlanadigan har bir
chaqiruv ketma-ket belgilanib boriladi, va shu bilan nimani test qilish
kerakligi ko'rinadi (212-bet). ESLATMA: chop etish o'rniga faylning
vaqtinchalik nusxasini izohlar bilan belgilash shu korpusning
moslashtirishi, kitob qog'ozni nazarda tutadi.

Modul chegarasi qayerda ekanini jamoa bilan tekshirish uchun Feathers "tizim
haqida hikoya aytib berish" usulini beradi: tizimni bir necha gapda, sanoqli
tushuncha bilan tushuntirib ko'rish; tushuntirish qiyin bo'lsa yoki
tushuntirishdagi tuzilish koddagi tuzilishga mos kelmasa, shu farqning o'zi
refaktoring yo'nalishini ko'rsatadi (17-bob, 216-bet). Shu bobda dizayn
suhbatining ikkinchi usuli ham bor: Naked CRC, ya'ni yozilmagan kartochkalar
(220-223-bet). Klassik CRC da kartochkaga sinf nomi, mas'uliyatlari va
hamkorlari yoziladi; Naked CRC da kartochkalar bo'sh qoladi, so'zlovchi
ularni stolga birma-bir qo'yib, ko'rsatib va harakatlantirib ssenariyni
aytib beradi, va shu harakat bilan obyektlar orasidagi muloqotni
ko'rsatadi. Ikki qoidasi bor: kartochka sinfni emas, nusxani bildiradi, va
ustma-ust qo'yilgan kartochkalar to'plamni bildiradi (223-bet). Legacy
tizimda bu usul UML diagrammasidan arzon va hikoya usulining tabiiy
davomi: jamoa ssenariyni kartochkalarda ko'rsata olmasa, modul chegarasi
hali tushunilmagan.

Ma'lumot oqimini tushunish uchun jadval darajasiga tushish kerak. PostgreSQL'da
qaysi jadval haqiqatan ishlatilayotgani statistikadan ko'rinadi.

```sql
-- Jadvallar bo'yicha haqiqiy yuklama: o'qish va yozish nisbati
SELECT relname,
       seq_scan, idx_scan,
       n_tup_ins AS qoshildi,
       n_tup_upd AS ozgardi,
       n_tup_del AS ochirildi,
       pg_size_pretty(pg_total_relation_size(relid)) AS hajm
FROM pg_stat_user_tables
ORDER BY (coalesce(idx_scan,0) + seq_scan) DESC
LIMIT 20;

-- Umuman ishlatilmayotgan index'lar: ortiqcha yozish narxi
SELECT relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

Agar `pg_stat_statements` extension yoqilgan bo'lsa, `total_exec_time` bo'yicha
tartiblangan birinchi so'rovlar tizimning haqiqiy og'irlik markazini
ko'rsatadi.

## 34.3 Xavfsizlik to'ri qurish: xatti-harakatni qayd etuvchi test

Characterization test oddiy testdan maqsadi bilan farq qiladi. Oddiy test "kod
to'g'ri ishlashini" tekshiradi. Characterization test kod bo'lagining hozirgi,
haqiqiy xatti-harakatini hujjatlashtiradi: "shunday bo'lishi kerak" yoki
"menimcha shunday qiladi" degan gap yo'q (Feathers, *Working Effectively with
Legacy Code*, 13-bob, 186-bet). Bu farq muhim, chunki legacy tizimda
Feathers'ning so'zi bilan tizim nima qilayotgani uning nima qilishi kerakligidan
muhimroq: noto'g'ri xatti-harakat ham ko'pincha mijoz ishonib qolgan
xatti-harakatdir.

Feathers buning uchun aniq algoritm beradi (186-bet):

1. Kod bo'lagini test harness ichida ishga tushirish.
2. Yiqilishini bilgan assert yozish.
3. Yiqilish xabari xatti-harakatni aytib berishini kutish.
4. Testni kod chiqargan natijani kutadigan qilib o'zgartirish.
5. Shu tartibni takrorlash.

Ya'ni kutilgan natija o'ylab topilmaydi, u koddan o'qib olinadi. Keyin shu
qayddan chetga chiqish regressiya hisoblanadi. Masalan to'lov komissiyasini
hisoblash uchun real buyurtma ID'lari olinadi, eski kod natijasi fayl sifatida
saqlanadi, refaktoringdan keyin natija aynan shu fayl bilan taqqoslanadi.
Texnikaning katalog yozuvi [patternlar hujjatidagi xarakterizatsiya
testlari](../patterns/23-testing-patternlari.md#2324-xarakterizatsiya-testlari-characterization-tests)
bo'limida, test yozish mexanikasi [testlash
qo'llanmasida](../testing/README.md), bu yerda faqat tartib muhim.

Arxitektor uchun qoida: characterization test production trafigidan olingan
ma'lumotga asoslansin. Sun'iy ma'lumot legacy tizimning eng qiziq holatlarini
qamramaydi, chunki legacy tizimning qiymati aynan o'sha g'alati holatlarda
yashaydi. Masalan eski valyuta kursi bilan yozilgan buyurtmalar yoki `NULL`
yetkazib berish manzili bilan yopilgan to'lovlar.

## 34.4 Chok (seam) topish: o'zgarishni kiritish mumkin bo'lgan nuqta

Seam tushunchasiga Feathers kodga qarashni o'zgartirishdan kelib chiqadi.
Avval odatiy qarash ta'riflanadi: programma - bitta katta matn varag'i,
listing; unda bitta qatorni o'zgartirish butun hujjatning ma'nosini
o'zgartirishi mumkin, shuning uchun unga ehtiyotkorlik bilan tegiladi
(Feathers, *Working Effectively with Legacy Code*, 4-bob, 29-30-bet). Bu
qarash kod o'qish uchun yetarli, lekin bitta sinfni test harness ichiga
olib kirishga urinilganda yetmaydi: matn varag'ida "shu qatorni bu safar
ishlatmaslik kerak" degan joy yo'q, uni faqat tahrirlab o'chirish mumkin, va
Feathers misolida o'chirish mumkin bo'lmaydi, chunki qator production'da
kerak (30-31-bet). Shuning uchun ikkinchi qarash kiritiladi: programma
bir-biriga ulangan bo'laklar va ularning ulanish joylari. Shu nuqtadan
ko'rilgan ulanish joyi seam deb ataladi.

Seam deganda programmada xatti-harakatni o'sha joyni tahrirlamasdan
o'zgartirish mumkin bo'lgan nuqta tushuniladi (Feathers, *Working Effectively
with Legacy Code*, 4-bob, 31-bet). Ta'rifning ikkinchi yarmi muhim: manba kod
production'da va testda bir xil qolishi kerak, shuning uchun o'zgarish boshqa
joydan kiritiladi.

Shundan ikkinchi tushuncha chiqadi: har bir seam'ning enabling point'i bor,
ya'ni ikki xatti-harakatdan birini tanlash qarori qabul qilinadigan joy
(36-bet). Enabling point bo'lmasa seam ham yo'q. Shuning uchun seam izlashda
ikki savol birga beriladi: xatti-harakatni qayerda almashtirish mumkin, va
o'sha tanlov qayerdan boshqariladi.

Feathers seam turlarini programma matnini ishlaydigan kodga aylantirish
qadamlari bo'yicha ajratadi va uchta tur sanaydi.

| Seam turi | Qaysi qadam | Enabling point | Java va Spring'da |
|---|---|---|---|
| Preprocessing seam (33-bet) | kompilyatsiyadan oldin matn almashtirish | preprocessor makrosi, `#define` | yo'q: Java'da makro preprocessor yo'q |
| Link seam (36-bet) | linking, chaqiruvlarni hal qilish | classpath yoki build konfiguratsiyasi | bor: classpath, alohida kutubxona |
| Object seam (40-bet) | ishga tushish, obyekt chaqiruvi | obyekt yaratilgan joy yoki argument ro'yxati | asosiy tur: interface, konstruktor, Spring konfiguratsiyasi |

Preprocessing seam faqat C va C++ da uchraydi, chunki ularda kompilyatsiyadan
oldin makro preprocessor yuradi. Java'da amalda ikki tur qoladi va kundalik ish
object seam ustida boradi: chaqirilgan metodni, chaqiruvchi metodni
tahrirlamasdan almashtirish.

```java
// OLDIN: object seam yo'q, chunki enabling point yo'q.
// gateway shu metod ichida yaratiladi, tashqaridan boshqarib bo'lmaydi
public class PaymentService {
    public Receipt charge(Order order) {
        var gateway = new AcquirerGateway("https://acq.example.com"); // qotib qolgan
        return gateway.charge(order.total());
    }
}

// KEYIN: object seam bor, enabling point - konstruktor argumenti
public class PaymentService {
    private final AcquirerClient client; // interface, almashtirish mumkin

    public PaymentService(AcquirerClient client) { this.client = client; }

    public Receipt charge(Order order) {
        return client.charge(order.total()); // xatti-harakat aynan o'sha
    }
}
```

Bu o'zgarishda mantiq bir qatorga ham tegilmadi, faqat bog'lanish ko'chirildi.
Feathers shu qadamni Extract Interface deb nomlaydi va uni eng xavfsiz
bog'liqlik uzish usullaridan biri deb sanaydi: qadam xato bajarilsa kompilyator
darhol aytadi, shuning uchun xato kiritish ehtimoli juda kichik (25-bob,
362-bet). Spring'da bu seam'ning enabling point'i konstruktor argumenti bo'lib
qoladi, konteyner uni testda ham, production'da ham o'zi to'ldiradi.

Seam topilgandan keyin test qayerga yoziladi degan savol qoladi, va Feathers
buning uchun ham ikki atama beradi. Interception point - o'zgarishning ta'sirini
sezish mumkin bo'lgan nuqta (12-bob, 174-bet). Pinch point - katta kod
bo'lagining barcha ta'siri o'tadigan tor interception point, ya'ni tabiiy
inkapsulyatsiya chegarasi: uning ichidagi tafsilotni bilish kerak emas, ichiga
qaraganda esa tashqarini bilish kerak emas (182-bet). Pinch point'da yozilgan
bitta test ko'p sinfni qamrab oladi, va pinch point'ning o'zi modul chegarasini
qayerga chizish kerakligini ko'rsatadi. Eng yomon holat esa `new
PaymentGateway()` yoki `static` utility chaqiruvi: u yerda seam yo'q va avval
uni yaratish kerak.

## 34.5 Kichik qadamlar: har bir qadamdan keyin ishlaydigan tizim

Refaktoringning asosiy intizomi shu: har bir commit'dan keyin tizim deploy
qilinishi mumkin bo'lsin. Bu "yarim ishlangan" holatni umuman yo'q qiladi. Agar
qadam shunday bo'lishi mumkin bo'lmasa, qadam juda katta.

Shundan oldingi shartni Fowler "ikki shlyapa" metaforasi bilan beradi (Kent
Beck metaforasi): funksiya qo'shish va refaktoring - ikki alohida ish. Funksiya
qo'shilganda mavjud kod o'zgartirilmaydi, faqat yangi imkoniyat qo'shiladi va
natija test bilan o'lchanadi; refaktoring qilinganda esa funksiya qo'shilmaydi,
faqat tuzilish o'zgaradi va yangi test yozilmaydi (*Refactoring*, 2-bob,
"The Two Hats"). Ta'rif bo'yicha refaktoring kuzatiladigan xatti-harakatni
o'zgartirmaydi. Shundan amaliy qoida: refaktoring commit'i va mantiq commit'i
aralashmaydi, diff o'qiganda qaysi biri xatti-harakatni o'zgartirgani
ko'rinishi kerak.

Katta o'zgarishni kichiklarga bo'lishning kitobdan olingan ikki usuli bor.
Birinchisi branch by abstraction, besh qadam: almashtirilayotgan funksionallik
uchun abstraksiya yaratish, mijozlarni shu abstraksiyaga o'tkazish, abstraksiya
ortida yangi implementatsiya yozish, abstraksiyani yangi implementatsiyaga
o'tkazish, keyin abstraksiyani tozalab eski implementatsiyani o'chirish
(Newman, *Monolith to Microservices*, 3-bob, 104-105-bet). Newman birinchi
qadamni ko'pincha IDE'ning Extract Interface refaktoringi bajaradi, kod yomon
bo'lsa esa avval seam ajratish kerak bo'ladi deb yozadi. U bu usulni uzoq
yashaydigan branch'dan deyarli har qanday holatda afzal deb hisoblaydi
(112-bet).

Ikkinchi usul parallel run: eski yoki yangi implementatsiyadan birini chaqirish
o'rniga ikkisi ham chaqiriladi va natijalar taqqoslanadi, lekin haqiqat manbasi
sifatida har bir paytda faqat bittasi hisoblanadi - odatda eskisi, toki
tekshiruv yangisiga ishonish mumkinligini ko'rsatmaguncha (113-bet). Parallel
run natijani emas, nofunksional ko'rsatkichni ham tekshiradi: yangi servis
yetarlicha tez javob beradimi, timeout ko'paydimi.

```java
@Service
public class FeeCalculationFacade {   // parallel run: ikki implementatsiya ham chaqiriladi
    private final LegacyFeeCalculator legacy;
    private final NewFeeCalculator fresh;
    private final boolean compare;    // taqqoslash yoqilganmi
    private final boolean useNew;     // javob qaysi koddan qaytadi

    public Money fee(Order order) {
        Money old = legacy.fee(order);   // hozircha haqiqat manbasi
        if (compare) {
            try {
                Money neu = fresh.fee(order);
                if (!neu.equals(old)) {
                    log.warn("fee farqi order={} eski={} yangi={}",
                             order.id(), old, neu); // farqlar metrikaga ham chiqadi
                }
                if (useNew) return neu;
            } catch (RuntimeException e) {
                log.error("yangi hisob xato berdi, eski javob qaytadi", e);
            }
        }
        return old;
    }
}
```

Farqlar soni nolga tushib, bir muddat shunday turgandan keyin `useNew`
yoqiladi. Bu yerda muhim detal: yangi kodning exception'i mijozga chiqmasligi
kerak, aks holda taqqoslashning o'zi incident manbasiga aylanadi. Newman
parallel run'ning narxini ham aytadi: uni amalga oshirish arzon emas, shuning
uchun odatda faqat xavfi yuqori o'zgarishlar uchun ishlatiladi; kod darajasida
shu ishni osonlashtiradigan kutubxonalar bor, masalan GitHub Scientist
(117-bet).

| Qadam | Hajmi | Deploy mumkinmi | Qaytarish yo'li |
|---|---|---|---|
| Interface ajratish (Extract Interface) | kichik, bir necha fayl | Ha | revert |
| Metodni ko'chirish | kichik | Ha | revert |
| Parallel run qo'shish | kichik | Ha | flag o'chirish, deploy kerak emas |
| Trafikni yangiga o'tkazish | kod o'zgarmaydi | Ha | flag o'chirish, deploy kerak emas |
| Eski kodni o'chirish | o'rta | Ha | revert |
| Jadvalni ikkiga bo'lish (split table) | migratsiya | Shartli | backfill qayta ishlatiladi, tez emas |
| Butun modulni qayta yozish | butun modul | Yo'q | yo'q, 34.6 ga qarang |

Kichik qadam o'z-o'zidan ishlamaydi, u uchlik bilan keladi. Fairbanks
evolyutsion dizaynning kamchiliklarini aynan uch amaliyot yopadi deb yozadi:
refaktoring (xatti-harakatni saqlaydigan o'zgarish) mahalliy va
muvofiqlashtirilmagan dizaynlarni tozalaydi, test-driven dizayn o'zgarish
mavjud funksionallikni buzmaganini ta'minlaydi, continuous integration esa
butun jamoani bitta kod bazasida ushlaydi. Uchtadan refaktoring asosiy ish
hayvoni: u eski va mahalliy muammoni yechgan dizaynni hozirgi va global
muammoni yechadigan dizaynga almashtiradi.

Shu yerda ikki chegara ham ochiq aytilgan va ikkisi ham bu bobga tegishli.
Birinchisi, refaktoring arxitektura miqyosidagi o'zgarish uchun kam yo'l-yo'riq
beradi: Amazon ning qatlamli va bitta bazali arxitekturadan servisga o'tishini
sinf va metod darajasidagi kichik refaktoring qadamlaridan chiqqan deb
tasavvur qilish qiyin. Ikkinchisi, legacy kodda odatda ishonch bilan
refaktoring qilish uchun test yetarli emas, holbuki deyarli har tizimda legacy
kod bor. Ya'ni bu bobning tartibi tasodifiy emas: avval
[34.3](#343-xavfsizlik-tori-qurish-xatti-harakatni-qayd-etuvchi-test) dagi
xavfsizlik to'ri, keyin kichik qadamlar, va arxitektura miqyosidagi o'zgarish
uchun refaktoring emas, [34.7](#347-boguvchi-anjir-strangler-usuli-bilan-bosqichma-bosqich-almashtirish)
dagi strangler kabi alohida apparat.

## 34.6 Katta qayta yozish nega deyarli har doim muvaffaqiyatsiz bo'ladi

Noldan qayta yozish amalda kam muvaffaqiyat qiladi. Fowler'ning Newman keltirgan
gapi buni qisqa qilib aytadi: katta portlashli qayta yozishdan kafolatlangan
yagona natija - portlash (*Monolith to Microservices*, 2-bob, 53-bet). Newman
shu yerda monolitni marmar blokiga o'xshatadi: uni butunligicha portlatish
o'rniga bo'lak-bo'lak kesish kerak, chunki bosqichma-bosqich borish har bir
xatoning hajmini kichraytiradi va har qadamdan xulosa chiqarish imkonini
beradi.

Birinchi sabab aniq: eski tizim turib qolmaydi. Siz yangi versiyani yozganda
eski tizimga o'zgarish kirishda davom etadi va maqsad harakatlanadi.

Ikkinchi sabab bilimning taqsimlanishi. Legacy kodning qiymati arxitekturasida
emas, yillar davomida yig'ilgan mayda shartlarida, va ular hujjatlashtirilmagan.
Qayta yozishda ularning bir qismi yo'qoladi va har biri alohida incident bo'lib
qaytadi.

Uchinchi sabab iqtisodiy. Newman teskari tomondan ko'rsatadi: servislarni
bittalab ajratish ularning qiymatini bosqichma-bosqich ochadi, katta bitta
deploy'ni kutish kerak emas (53-bet). Demak qayta yozish davomida biznes qiymat
olmaydi, va yangi funksiya so'rovi kelganda jamoa ikki joyda ishlashga majbur
bo'ladi.

To'rtinchi xavf chegarani noto'g'ri chizish. Newman ThoughtWorks'ning SnapCI
jamoasi misolini keltiradi: uzluksiz integratsiya domenini yaxshi bilgan jamoa
ham birinchi urinishda servis chegaralarini noto'g'ri qo'ydi, o'zgarish va
egalik narxi oshdi, va jamoa bir necha oy kurashgandan keyin servislarni qaytib
bitta katta ilovaga qo'shishga qaror qildi; funksionallik barqarorlashgach
chegaralarni topish osonlashdi va keyingi ajratish muvaffaqiyatli bo'ldi
(43-bet). Newman shu yerdan xulosa chiqaradi: mavjud kod bazasini ajratish
noldan microservice'dan boshlashdan osonroq.

Qayta yozish asosli bo'lgan kam holatlar bor: platforma umuman
qo'llab-quvvatlanmaydi, masalan Java 6 va EJB 2 ustidagi tizim; yoki modul juda
kichik va chiqish nuqtalari aniq, masalan bitta hisobot generatori. Ikkinchi
holatda bu qayta yozish emas, modul almashtirish.

## 34.7 Bo'g'uvchi anjir (strangler) usuli bilan bosqichma-bosqich almashtirish

Strangler fig yondashuvining mohiyati: yangi tizim eski tizim atrofida o'sadi
va trafikni asta-sekin o'ziga tortadi. Nomi anjir turidan olingan: urug' daraxt
shoxida unib chiqadi, pastga tushib ildiz otadi va asl daraxtni o'rab oladi;
asl daraxt boshida tayanch bo'ladi, oxirida chirib ketadi va faqat o'zini
tutib turadigan yangi anjir qoladi. Patternni birinchi bo'lib Martin Fowler
yozib qoldirgan (Newman, *Monolith to Microservices*, 3-bob, 79-bet). Katalog
yozuvi [patternlar hujjatidagi strangler fig
application](../patterns/27-monolitdan-microservicega-migratsiya.md#271-boguvchi-anjir-ilovasi-strangler-fig-application)
bo'limida.

Newman uchta qadamni sanaydi: ko'chirilishi kerak qismni aniqlash, uni yangi
servisda amalga oshirish, keyin chaqiruvlarni monolitdan yangi servisga qayta
yo'naltirish (79-bet). Uchinchi qadamgacha yangi funksionallik production'ga
deploy qilingan bo'lsa ham hali tirik emas. Bu foydali: kodni shoshmasdan
tayyorlash, deploy va ekspluatatsiya jihatlarini trafiksiz holda tinch sinab
ko'rish mumkin (80-bet).

Patternning asosiy foydasi bosqichma-bosqich ko'chish va har qadamning oson
qaytarilishi. Yana bir foydasi kamroq aytiladi: ko'chishni to'xtatib yoki
butunlay tashlab qo'yish mumkin, shu paytgacha yetkazilgan yangi tizimdan
foyda esa qoladi (79-bet).

Pattern ishlamaydigan holat ham bor: ko'chirilishi kerak funksionallik monolit
ichidagi chaqiruvlar o'rtasida chuqur joylashgan va chetdan ushlab qolishning
iloji bo'lmasa, strangler fig o'rniga branch by abstraction kerak bo'ladi
(81-82 va 104-bet).

Texnik asosi routing qatlami. Spring Cloud Gateway yoki oddiy nginx yetarli.
Qoida yo'l bo'yicha emas, imkon qadar mijoz segmenti bo'yicha ham yozilsin,
shunda yangi kod avval kichik trafikni ko'radi.

```yaml
# Gateway: /api/v1/payments faqat belgilangan header bilan yangi servisga ketadi
spring:
  cloud:
    gateway:
      routes:
        - id: payments-new
          uri: http://payment-service:8080
          predicates:
            - Path=/api/v1/payments/**
            - Header=X-Canary, true        # boshida kichik ulush
          filters:
            - name: CircuitBreaker
              args:
                name: paymentsCb
                fallbackUri: forward:/legacy/payments  # xato bo'lsa eskiga qaytadi
        - id: payments-legacy
          uri: http://monolith:8080
          predicates:
            - Path=/api/v1/payments/**     # qolgan hamma trafik
```

Trafikni bosqichlab oshirish Newman'da canary release deb ataladi:
foydalanuvchilarning bir qismi yangi funksionallikka yo'naltiriladi, qolgani
eskisini ko'radi, shunda muammo chiqsa faqat so'rovlarning bir qismi
ta'sirlanadi (118-bet). Canary release parallel run bilan bir narsa emas:
parallel run'da ikki implementatsiya ham chaqiriladi, canary'da esa har bir
so'rov uchun faqat bittasi. Ikkisi ham, dark launching bilan birga, progressive
delivery deb atalgan guruhga kiradi (118-bet).

Har bosqichda error rate va p99 latency taqqoslanadi. Kitobdan keladigan talab
bitta: oldingi bosqichga qaytish bitta konfiguratsiya o'zgarishi bo'lib
qolsin.

Qachon "tugadi" deyish mumkin degan savolga Newman qat'iy javob beradi: servis
ajratish production da ishlab turmaguncha va haqiqatan ishlatilmaguncha
tugallangan hisoblanmaydi (53-bet). Sabab bosqichma-bosqich ajratishning
maqsadi bilan bir xil: darslarning aksariyati faqat production da ko'rinadi.
Kitob ularni sanaydi ham, nosozlikni izlash va oqimni kuzatish qiyinlashishi,
latency, referential integrity va cascading failure. Shundan amaliy qoida
chiqadi: birinchi ajratilgan servislar imkon qadar tez production ga
chiqariladi, hatto funksionallik kichik bo'lsa ham, chunki maqsad qiymat
yetkazish bilan birga o'rganish. Bu [34.5](#345-kichik-qadamlar-har-bir-qadamdan-keyin-ishlaydigan-tizim)
dagi kichik qadam qoidasining davomi: kichik o'zgarishda muammoni ko'rish ham,
tuzatish ham osonroq.

## 34.8 Ma'lumotlar bazasini ajratish: eng qiyin qism va uning tartibi

Kodni bo'lish oson, bazani bo'lish qiyin. Sababi aniq: monolitda `orders` va
`payments` jadvallari bitta tranzaksiyada yangilanadi va bitta `JOIN` bilan
o'qiladi. Ajratilgandan keyin ikkalasi ham yo'qoladi.

Birinchi qaror: nimani avval ajratish. Newman ikkisini bir vaqtda, bitta katta
qadamda ajratishdan voz kechishni maslahat beradi, chunki qadam juda katta
bo'ladi va qaror natijasini baholash uzoqqa cho'ziladi; u sxemani yoki ilova
qatlamini avval ajratishni qat'iy afzal ko'radi (*Monolith to Microservices*,
4-bob, 169-170-bet).

Qolgan ikki variant orasidagi tanlov esa shartli, universal tartib yo'q.
Newman o'z tanlovini ikki shart bilan bayon qiladi: agar monolitni o'zgartirish
imkoni bo'lsa va ishlash yoki ma'lumot izchilligiga mumkin bo'lgan ta'sirdan
xavotir bo'lsa, u avval sxemani ajratadi; aks holda avval kodni ajratadi va shu
orqali bu ma'lumot egaligiga qanday ta'sir qilishini tushunadi (170-bet). Ya'ni
"avval kod" degan qoida shartsiz berilmaydi: u ikkinchi shoxdan biri.

Amalda bu shunday ko'rinadi. Avval kod ajratilsa: har bir jadvalga faqat bitta
modul yozadi, boshqalar API orqali so'raydi, keyin `JOIN`'lar yo'qoladi, keyin
schema ajratiladi va faqat oxirida alohida baza instance'i. Avval sxema
ajratilsa, kod bir muddat ikki schema bilan ishlashga majbur bo'ladi; Newman
buning uchun multischema storage patternini beradi: yangi ma'lumot o'z
schema'sida yashaydi, eski ma'lumot esa hali monolit schema'sida o'qiladi
(169-bet).

```sql
-- 1-qadam: mantiqiy ajratish, baza hali bitta
CREATE SCHEMA payment;
ALTER TABLE public.payments SET SCHEMA payment;

-- 2-qadam: faqat payment moduli yozish huquqiga ega bo'ladi
REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA payment FROM monolith_app;
GRANT  SELECT ON payment.payments TO monolith_app;  -- vaqtinchalik o'qish

-- 3-qadam: o'qish ham API orqali bo'lganda ruxsat umuman olinadi
REVOKE SELECT ON payment.payments FROM monolith_app;
```

Newman ma'lumotni ko'chirish uchun nomlangan patternlar beradi, va ular shu
bosqichlarga mos tushadi.

| Pattern | Bet | Nima qiladi |
|---|---|---|
| Database view | 128 | monolit schema'si ustiga faqat kerakli ustunlarni ko'rsatadigan view qo'yadi, mijoz ko'radigan yuzani kichraytiradi |
| Change data ownership | 141 | ma'lumot egaligini yangi servisga o'tkazadi, monolit unga API orqali murojaat qiladi |
| Synchronize data in application | 145 | ilovaning o'zi ikki bazani sinxron ushlaydi: avval bulk ko'chirish, keyin ikki tomonga yozib eski joydan o'qish |
| Tracer write | 149 | ko'chish davomida ikki manba ham haqiqat manbasi bo'lishiga toqat qiladi va ulushni asta oshiradi |
| Split table | 171 | ikki chegara aralashgan bitta jadvalni ikkiga bo'ladi |

Tranzaksiya chegarasi buzilgan joyda ikkita yozishni bitta `@Transactional`
ushlab turolmaydi. Bu yerda outbox orqali ishonchli xabar yuborish kerak
bo'ladi, mexanikasi dizayn [patternlar hujjatidagi](../patterns/README.md)
outbox pattern bo'limida bor. Arxitektorning qarori esa boshqa: qaysi joy
eventual consistency'ga chidaydi. Newman nomuvofiqlik oynasining uzunligi
sinxronizatsiya mexanizmiga bog'liq deb yozadi: kechasi bir marta ishlaydigan
batch bilan ko'chirilsa, ikkinchi manba bir kungacha eskirgan bo'lishi mumkin;
change data capture bilan uzluksiz oqim bo'lsa, oyna sekundlar yoki undan kam
bo'ladi (153-bet). Qaysi oyna qabul qilinishi mumkinligini biznes qoidasi
aytadi, kitob emas, va shu javob sinxronizatsiya mexanizmini tanlaydi.

| Tuzoq | Natijasi | Yechim |
|---|---|---|
| Kod va bazani bitta katta qadamda birga ajratish | qadam juda katta, natijani baholash cho'ziladi | Newman: avval yo sxemani, yo ilova qatlamini ajrat (169-170-bet) |
| Tartibni shartsiz, odat bo'yicha tanlash | ishlash yoki izchillik muammosi keyin, qimmat joyda chiqadi | ikki shartni tekshir: monolit o'zgartiriladimi, ishlash va izchillikdan xavotir bormi (170-bet) |
| Backfill'ni bir marta katta `UPDATE` bilan qilish | jadval lock, uzoq kutish | batch bilan ko'chirish, har batchdan keyin commit |
| Ikki tomonga yozib, hech qachon tekshirmaslik | jim ketadigan ma'lumot tafovuti | reconciliation jarayoni: ikki bazaga bir nechta SQL so'rov, farq ko'rinsin (153-bet) |
| Eski ustunni darhol `DROP` qilish | rollback imkonsiz | avval ishlatishni to'xtatish, bir muddat kutish, keyin drop |
| Yangi kodda eski jadvalga to'g'ridan-to'g'ri yozish | egalik chegarasi buzildi | baza darajasida `REVOKE`, qoida kodga tayanmasin |
| `Flyway` migratsiyasini orqaga qaytarishga umid qilish | qaytarish skripti sinovdan o'tmagan | faqat oldinga mos migratsiya: ustun qo'shish, to'ldirish, o'tish |
| Parallel run'ni muddatsiz ushlab turish | ikki marta xarajat va chalkashlik | har flag uchun o'chirish muddati va egasi belgilansin |

Migratsiyani to'xtashsiz o'tkazish mexanikasi (ustun qo'shish, backfill, ikki
tomonlama yozish, o'tish) [33-bob, Sxema migratsiyasi va to'xtashsiz
reliz](33-sxema-migratsiyasi-va-toxtashsiz-reliz.md) da.

## 34.9 Refaktoringni biznes bilan kelishish: qiymat tilida tushuntirish

"Kod iflos" degan dalil byudjet ochmaydi. Robert C. Martin buni boshqa
tomondan qo'yadi: xatti-harakat shoshilinch, lekin har doim muhim emas;
arxitektura esa muhim, lekin hech qachon shoshilinch emas. Biznes menejeri
arxitekturaning muhimligini baholashga jihozlanmagan, shuning uchun uni
shoshilinch funksiyalar oldida himoya qilish ishlab chiqish jamoasining
javobgarligi (*Clean Architecture*, 2-bob, "Fight for the Architecture"). Ya'ni
bu suhbat texnik emas, kelishuv suhbati, va unga tayyorlanib kirish kerak.

Martin bu da'voni Eisenhower matritsasi bilan asoslaydi: shoshilinch ishlar
kamdan kam muhim, muhim ishlar esa kamdan kam shoshilinch. Shundan to'rt
kvadrant va ularning tartibi chiqadi: shoshilinch va muhim; shoshilinch
emas lekin muhim; shoshilinch lekin muhim emas; na shoshilinch na muhim.
Arxitektura ro'yxatning birinchi ikki o'rnida turadi, xatti-harakat esa
birinchi va uchinchi o'rinda. Odatiy xato ham shu yerda: uchinchi toifadagi
ishni birinchi toifaga ko'tarib qo'yish, ya'ni shoshilinch lekin muhim
bo'lmagan funksiyani haqiqatan shoshilinch va muhim funksiyadan ajratmaslik;
natijada tizimning arxitekturasi muhim bo'lmagan funksiya uchun qurbon
qilinadi (*Clean Architecture*, 2-bob, "Eisenhower's Matrix"). Kelishuvda
bundan aniq savol chiqadi: refaktoring "muhim lekin shoshilinch emas"
qutisida turadi, shuning uchun uni surib qo'yayotgan ishning birinchi
toifadanmi yoki uchinchisidanmi ekani so'raladi.

Newman kelishuvni maqsaddan boshlashni talab qiladi: microservice yoki
refaktoringning o'zi maqsad emas, siz mavjud arxitektura bilan erisha
olmayotgan biror natijaga erishish uchun borasiz; maqsad aniq bo'lmasa qaysi
variantni tanlashni ham hal qilib bo'lmaydi (*Monolith to Microservices*,
2-bob, 33-bet).

Amalda bu vaqt va xavf tilida yozilgan dalil degani. Shaklni misol bilan
ko'rsatish mumkin: "to'lov modulidagi har bir o'zgarish hozir N kun oladi,
shundan M kuni qo'lda regressiya tekshiruvi; chok ajratilgandan keyin bu K
kunga tushishi kutiladi; yiliga shuncha o'zgarish bo'lsa, shuncha ish kuni
tejaladi". N, M va K kitobdan emas, sizning o'lchovingizdan keladi va ularni
olish usuli 34.10 da.

Ikkinchi ishonchli dalil incident statistikasi. Agar oxirgi 12 oyda production
incident'larining katta qismi bitta modulda to'plangan bo'lsa, bu modul
refaktoringi xavfni kamaytirish loyihasi sifatida tushuntiriladi.

Kelishuvning shakli ham muhim. Newman o'zgarishni doimiy yaxshilash
madaniyatiga aylantirishni, uni alohida ish oqimlariga ajratmaslikni maslahat
beradi: aks holda o'zgarish bir martalik tranzaksiya sifatida ko'riladi, ish
tugadi, boshqa o'zgarish yo'q (73-bet). Shundan amaliy xulosa: alohida
"refaktoring sprint'i" so'ralmaydi, tizimni ishlashga yaroqli saqlash har
sprintning doimiy ulushi bo'ladi. Bitta katta so'rov bir marta rad etiladi,
kichik doimiy ulush esa odatga aylanadi.

Newman tashkiliy o'zgarish uchun John Kotter'ning sakkiz qadamli modelini ham
keltiradi (2-bob, 47-52-bet). Undan ikki qadam refaktoringda bevosita ishlaydi:
shoshilinchlik hissini yaratish, buning uchun incident kabi "o'rganish
momenti"dan foydalanish (48-bet); va qisqa muddatli g'alabalarni ishlab chiqish,
chunki odamlar natijani uzoq ko'rmasa ishonchni yo'qotadi, shuning uchun
monolitdan oson ajraladigan funksionallik ro'yxatning boshida turadi (51-bet).

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| "Bu kod juda yomon, qayta yozamiz" | "Bu modul o'zgarish narxini shuncha oshiradi, o'lchovi shu, bosqichma-bosqich almashtiramiz" |
| Refaktoringni mantiq o'zgarishi bilan birga commit qiladi | Xatti-harakat o'zgarmaydigan commit va mantiq commit'i ajratiladi (ikki shlyapa) |
| Avval tozalaydi, keyin o'lchaydi | Avval o'lchaydi, keyin faqat o'lchov ko'rsatgan joyni tozalaydi |
| Butun kod bazasini bir xil darajada yaxshilaydi | Yuqori churn joyga kuch beradi, tinch joyga tegmaydi |
| Kod va bazani ajratish tartibini odat bo'yicha tanlaydi | Newman'ning ikki shartini tekshirib tanlaydi, 34.8 ga qarang |
| Yangi kodni darhol production javobiga qo'yadi | Parallel run'da taqqoslaydi, farq nolga tushgach o'tadi |
| Flag'larni cheksiz qoldiradi | Har flag uchun o'chirish muddati va egasi bo'ladi |
| "Yaxshilandi" deb his bilan aytadi | Cycle time, change failure rate va p99 latency raqamini ko'rsatadi |
| Eski kodni "ehtimol kerak bo'ladi" deb saqlaydi | Trafik nolga tushganini metrikada ko'rib, o'chiradi |

Suhbatni boshlashdan oldin bajarilishi kerak bitta ish bor va u ko'pincha
o'tkazib yuboriladi: g'oyadan production gacha yo'lni modellash. Newman buni
time to market sekin bo'lgan har holatda tavsiya qiladi va o'z misolini
keltiradi (37-bet). Yirik investitsiya bankidagi loyihada "dasturchilar
production ga chiqarishga juda uzoq vaqt sarflaydi" deb aytilgan; hamkasbi
yetkazib berishning hamma bosqichini product owner g'oya o'ylab topgan
paytdan to production gacha xaritaga tushirgan. Dasturchi ish boshlaganidan
deploy gacha o'rtacha olti hafta ketgan va avtomatlashtirish bilan bundan ikki
hafta qisqartirish mumkin edi. Lekin haqiqiy to'siq boshqa joyda chiqdi: g'oya
product owner dan dasturchilar ish boshlay oladigan nuqtaga yetib kelishiga
ko'pincha 40 haftadan oshiq ketgan.

Amaliy natija aniq: har bosqichni va uning davomiyligini (o'tgan vaqt va
haqiqiy band vaqt alohida) yozib chiqing, keyin og'riq nuqtalarini belgilang.
Shundan keyin mikroservis yoki refaktoring yechimning bir qismi bo'lishi
mumkin, lekin yonida bir vaqtda sinab ko'rish mumkin bo'lgan boshqa ko'p narsa
ham ko'rinadi. Biznes bilan suhbatda bu xarita eng kuchli dalil: u
"arxitekturani tuzatamiz" degan taklifni "yo'lning qaysi bosqichi qancha vaqt
oladi" degan o'lchovga aylantiradi.

## 34.10 O'lchov: refaktoring ishladimi yoki yo'qligini qanday bilish

Refaktoring natijasi kod chiroyliligi bilan o'lchanmaydi. Newman o'lchovni
maqsaddan chiqarishni talab qiladi: time to market yaxshilanishi maqsad bo'lsa
cycle time, deploy soni va failure rate o'lchanadi; ilovani ko'proq yuklamaga
moslash maqsad bo'lsa performance test natijasi o'lchanadi (*Monolith to
Microservices*, 2-bob, 72-bet).

Newman shu yerda ikki ogohlantirish beradi. Birinchisi: metrikani o'ynash
mumkin, "nimani o'lchasang, shuni olasan"; u yopilgan ticket soni bo'yicha
to'lov olgan yetkazib beruvchining muammo hal qilinmagan bo'lsa ham ticketni
yopib qo'yishini misol qilib keltiradi. Ikkinchisi muhimroq: ko'chishning
birinchi oylarida cycle time'ning yaxshilanishini kutmaslik kerak, hatto
boshida yomonlashishi ehtimoli bor, chunki ishlash usulining o'zgarishi qisqa
muddatda unumdorlikni tushiradi (72-bet). Shuning uchun "refaktoringdan keyin
lead time shuncha kunga tushadi" degan oldindan aytilgan raqam dalil emas: u
o'lchanadi, aytib qo'yilmaydi. Shundan yana bir xulosa: qadam kichik bo'lsa,
bu vaqtinchalik tushish ham kichik bo'ladi.

Raqamning o'zi yetarli emas. Newman kvantitativ o'lchov yonida kvalitativ
fikrni ham talab qiladi: jamoa ishni yoqtiryaptimi, o'zini kuchli his
qiladimi, yoki bosilib qolganmi, yangi javobgarlikni olish uchun kerakli
yordamni olayotganmi. Faqat raqamga tayanib odamlar aytayotganini e'tiborsiz
qoldirish muammoga olib boradi (72-bet).

Ikkisi ham muntazam checkpoint'da ko'riladi. Newman checkpoint'da to'rt narsani
qilishni aytadi: ko'chishdan nima kutilganini qayta aytib berish va biznes
yo'nalishi o'zgargan bo'lsa to'xtash, kvantitativ o'lchovni ko'rib chiqish,
kvalitativ fikr so'rash, keyin nimani o'zgartirishni hal qilish (71-bet).
Checkpoint'ning yana bir vazifasi sunk cost tuzog'idan chiqish: odam avvalgi
yondashuvga shunchalik yopishib qoladiki, ishlamayotgani ko'rinib turganda ham
davom etadi; qadamlar kichik bo'lsa yo'nalishni o'zgartirish osonlashadi
(73-bet).

```bash
# Modul bo'yicha o'zgarish zichligi: refaktoringdan oldin va keyin taqqoslanadi
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '^src/main/java/com/shop/payment/' | sort -u | wc -l

# Modulga tegadigan commit'lar soni va o'rtacha diff hajmi
git log --since="6 months ago" --numstat --pretty='C' -- src/main/java/com/shop/payment/ \
  | awk '/^C/{c++} /^[0-9]/{a+=$1; d+=$2} END{printf "commit=%d +%d -%d ortacha=%.1f\n", c, a, d, (a+d)/c}'
```

Ishlash tomonidan `http.server.requests` p99 va baza so'rovlari soni
kuzatiladi. Kod tozalangani so'rov sonini oshirib qo'yishi mumkin: [N+1 so'rov
muammosi](18-spring-data-jpa-va-hibernate-chuqur.md#184-n1-sorov-muammosi-topish-usuli-va-tort-xil-yechim)
paydo bo'lsa p99 o'sadi, kod esa diffda chiroyli ko'rinadi. Shuning uchun har
bosqichda so'rov soni ham o'lchanadi.

Kod sifati metrikalaridan ikkitasi foydali: modullar orasidagi bog'liqlik
yo'nalishi va aylanma bog'liqliklar soni. Ikkisini ham ArchUnit qoidalari bilan
qulflash mumkin, batafsili [testlash qo'llanmasidagi ArchUnit
asoslari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari)
bo'limida.

Bitta o'lchov esa ro'yxatga umuman kirmaydi va uni maqsad qilib qo'yish
ko'pincha xato bo'ladi: qayta foydalanish. Newman buni ochiq aytadi, reuse
odamlarning haqiqiy maqsadi emas, u boshqa natijaga olib borishi kutilgan
vosita; agar maqsad tezroq yetkazish yoki xarajatni kamaytirish bo'lsa, aynan
shu narsalarni o'lchash kerak, aks holda noto'g'ri narsa optimallashtiriladi
(42-bet). Kitobning misoli tanish: mijozlarga xizmat jamoasiga hisob-faktura
uchun PDF kerak, tizimda PDF yasash qobiliyati allaqachon bor, lekin u boshqa
tashkilot qismidagi boshqa jamoa qo'lida. Reuse maqsadiga amal qilinsa, endi
o'sha jamoa bilan muvofiqlashish kerak: ishni ular bajaradi yoki o'zgarishni
o'zingiz yozib pull request yuborasiz. Hisob shuni ko'rsatishi mumkin, o'z
implementatsiyasini yozish muvofiqlashishdan tezroq. Agar haqiqiy maqsad time
to market bo'lsa, bu to'g'ri tanlov; reuse uchun optimallashtirish esa aynan
shu maqsadni sekinlashtiradi. Shu sababli refaktoring hisobotida "n modul
qayta ishlatildi" qatori o'lchov emas: o'lchov [34.9](#349-refaktoringni-biznes-bilan-kelishish-qiymat-tilida-tushuntirish)
da yozilgan maqsaddan chiqadi.

## 34.11 Qachon tegmaslik kerak: ishlayotgan, o'zgarmaydigan kod

Refaktoring qilmaslik ham qaror. Newman buni to'g'ridan-to'g'ri aytadi:
microservice maqsad emas, undan "g'alaba qilib" bo'lmaydi, va o'tish ongli,
asosli qaror bo'lishi kerak (*Monolith to Microservices*, 2-bob, 33-bet). U
microservice yomon g'oya bo'lgan holatlarni alohida sanaydi, va ularning
oxirgisi shunchaki "yaxshi sabab yo'q" deb nomlanadi (42-45-bet). Birinchisi
esa domen noaniq bo'lishi: chegarani noto'g'ri qo'yish qimmat, servislar
orasidagi o'zgarishlar ko'payadi, komponentlar ortiqcha bog'lanadi va natija
bitta monolitdan ham yomon bo'lishi mumkin (43-bet).

Modul darajasida tegmaslik mezonlari aniq bo'lishi kerak: past churn, nol
incident, latency byudjet ichida, yaqin yo'l xaritasida o'zgarish yo'q. Shu
to'rt shart bajarilsa, modul "muzlatilgan" deb belgilanadi va faqat xavfsizlik
yangilanishlari oladi. Mezonlarni yozib qo'yish muhim: aks holda "tegmaymiz"
qarori har safar his bilan qabul qilinadi.

Alohida holat: kod yomon, lekin uni o'rab olish mumkin. Feathers buning uchun
to'rtta nomlangan usul beradi (*Working Effectively with Legacy Code*, 6-bob).
Sprout Method: yangi mantiq eski metod ichiga qo'shilmaydi, u alohida yangi
metodga ajratiladi va eski metoddan chaqiriladi, shunda yangi kod test bilan
yoziladi va eski kod bilan aralashmaydi (59-bet). Sprout Class: bog'liqliklar
shunchalik yomon bo'lsa, sinfni test harness ichida yaratishning iloji
bo'lmasa, yangi mantiq butunlay yangi sinfga chiqariladi (63-bet). Wrap Method:
eski metod boshqa nom bilan private qilinadi, uning nomi bilan yangi metod
yaratiladi, yangi metod qo'shimcha xatti-harakatni bajarib keyin eskisini
chaqiradi; mijozlar o'zgarishni sezmaydi (67-bet). Feathers bu usulning
chegarasini ham aytadi: yangi xatti-harakat eski mantiq ichiga kirib
ketmasligi, undan oldin yoki keyin turishi kerak. Wrap Class: xuddi shu
g'oyaning sinf darajasidagi hamkori, yangi xatti-harakat o'sha metodni
ishlatadigan boshqa sinfga joylashtiriladi; Feathers bu usulni Decorator
patterniga bog'laydi (71-bet).

Qora qutini o'rash uchun esa Extract Interface ishlatiladi: sinfdan kerakli
metodlar uchun interface ajratiladi, atrofdagi kod shu interface'ga tayanadi,
ichi tegilmay qoladi (25-bob, 362-bet). Masalan katta hisobot generatorini
qayta yozish o'rniga oldiga interface qo'yiladi; kelgusida uni almashtirish
kerak bo'lsa, faqat bitta implementatsiya yoziladi.

Kod deyarli butunlay tashqi API chaqiruvlaridan iborat bo'lsa, o'rash usuli
bitta emas: Feathers ikki yo'lni ajratadi (15-bob, 205-bet). Skin and Wrap
the API: API ni iloji boricha aynan takrorlaydigan interface yasab,
kutubxona sinflari atrofiga wrapper qo'yiladi, va shunda production kodda
tashqi API ga bog'liqlik faqat yupqa delegatsiya qatlamida qoladi, qolgan
hamma narsa test ostiga tushadi. Responsibility-Based Extraction: koddagi
mas'uliyatlar aniqlanib, har biri uchun metod ajratiladi, ya'ni kod past
darajali API chaqiruvlariga emas, yuqori darajali nomlarga tayanadi.

| Shart | Tanlov |
|---|---|
| API kichik; tashqi kutubxonadan to'liq ajralmoqchisiz; API orqali test yozib bo'lmaydi | Skin and Wrap the API (206-bet) |
| API murakkab; ishonchli Extract Method asbobi bor yoki ajratishni qo'lda xavfsiz bajarasiz | Responsibility-Based Extraction (207-bet) |

Narxini Feathers yashirmaydi: Skin and Wrap the API ko'proq ish, lekin
uchinchi tomon kutubxonasidan ajralish kerak bo'lganda u to'g'ri tanlov;
Responsibility-Based Extraction'da esa ajratilgan metodga yuqori darajali
nom berish uchun o'z mantiqingizning bir qismi API kodi bilan birga tushib
qolishi mumkin, va o'sha qism testdan tashqarida qolishi mumkin. Jamoalar
ko'pincha ikkisini birga ishlatadi: test uchun yupqa wrapper va ilovaga
yaxshi interface beradigan yuqori darajali wrapper (207-bet).

Bunday yarim chegarani Robert C. Martin qisman chegara deb ataydi: to'liq
arxitektura chegarasi qimmat, lekin keyin kerak bo'lishi mumkin bo'lgan joyda
uning o'rni band qilib qo'yiladi. Eng oddiy shakli bir o'lchovli chegara, ya'ni
mijoz interface'ga tayanadi, implementatsiya shu interface ortida turadi
(*Clean Architecture*, 24-bob, "Skip the Last Step" va "One-Dimensional
Boundaries"). Martin ogohlantirishini ham yozib qo'yish kerak: qisman chegara
o'z-o'zidan buziladi, bog'liqlik noto'g'ri yo'nalishda chiziqni kesib o'tishni
boshlaydi; shuning uchun chegara ArchUnit kabi qoida bilan qulflanmasa uzoq
yashamaydi.

## 34.12 Bosqichma-bosqich reja namunasi: to'lov moduli misolida

Quyida monolitdagi to'lov modulini alohida servisga chiqarish bosqichlarining
ketma-ketligi. Tartib Feathers'ning legacy kodga o'zgarish kiritish
algoritmiga va Newman'ning migratsiya patternlariga tayanadi; bosqichlarga
bo'linish, ularning soni va nomi esa shu korpusning namunasi, kitobdagi reja
emas. Har bosqich oxirida tizim ishlaydi va orqaga qaytish yo'li bor.

Birinchi bosqich, o'lchov. To'lov bilan bog'liq endpoint'lar, Kafka
listener'lar va `@Scheduled` job'lar ro'yxati; `payments` jadvaliga kim
yozayotganini `grep` va baza grant'lari bo'yicha aniqlash; p99 va kunlik hajm
raqamlari. Bu Feathers algoritmining o'zgarish nuqtalarini aniqlash qadami.

Ikkinchi bosqich, characterization testlar. Production'dan olingan to'lov
holatlari uchun hozirgi natija qayd etiladi, shu qatorda rad etilgan va
qaytarilgan to'lovlar. Har qayd 34.3 dagi tartib bilan olinadi: yiqilishini
bilgan assert'dan boshlanadi va kod chiqargan natija bilan to'ldiriladi.

Uchinchi bosqich, modul chegarasini monolit ichida chizish. Barcha to'lov
mantiqi bitta paketga ko'chiriladi, tashqi kod faqat `PaymentFacade` orqali
murojaat qiladi, bazaga to'g'ridan-to'g'ri murojaatlar yo'qotiladi. Bu Martin
aytgan qisman chegara: komponentni ajratish uchun kerak bo'lgan ish qilinadi,
lekin deploy hali bitta.

```java
// Modul chegarasi: tashqi dunyo faqat shu interface'ni ko'radi
public interface PaymentFacade {
    PaymentResult authorize(OrderId orderId, Money amount);
    void capture(PaymentId paymentId);
    void refund(PaymentId paymentId, Money amount, String reason);
    Optional<PaymentView> find(PaymentId paymentId);
}
// ArchUnit qoidasi: payment.internal paketiga tashqaridan murojaat taqiqlanadi.
// Shu qoida buzilmasa, keyingi bosqichda servisga chiqarish mexanik ish bo'ladi.
```

To'rtinchi bosqich, 34.8 dagi tanlov. Monolitni o'zgartirish imkoni bor va
ishlash yoki izchillikdan xavotir bo'lsa, sxema shu yerda ajratiladi va
grant'lar qo'yiladi; aks holda kod ajratish davom etadi va schema keyinroq
ko'chadi.

Beshinchi bosqich: yangi servis ko'tariladi, `PaymentFacade` implementatsiyasi
HTTP client bo'ladi va parallel run'da ishlaydi. Oltinchi bosqich: canary
release bilan trafik asta-sekin o'tkaziladi. Yettinchi bosqich: monolitdagi
eski kod va grant'lar o'chiriladi.

Muhimi muddat emas, balki har bosqich oxirida tizim ishlashi va rollback bitta
flag yoki bitta revert bo'lib qolishi.

## 34.13 O'zgarishning to'rt sababi va xavfni uch savol bilan chegaralash

Legacy kodda birinchi savol "kod yaxshimi" emas, "nima uchun tegyapmiz".
Feathers o'zgarishning to'rt sababini sanaydi: funksiya qo'shish, xatoni
tuzatish, dizaynni yaxshilash va resurs sarfini optimallashtirish (Feathers,
*Working Effectively with Legacy Code*, 1-bob, 3-bet). Taksonomiya bo'sh
emas: har bir sabab boshqa narsani o'zgarmas deb saqlaydi, demak har biriga
boshqa xavfsizlik to'ri kerak. Kitob buni jadval bilan ko'rsatadi (6-bet).

| O'zgarish | Tuzilish | Yangi funksionallik | Mavjud funksionallik | Resurs sarfi |
|---|---|---|---|---|
| Funksiya qo'shish | o'zgaradi | o'zgaradi | o'zgarmaydi | o'zgarmaydi |
| Xatoni tuzatish | o'zgaradi | o'zgarmaydi | o'zgaradi | o'zgarmaydi |
| Refaktoring | o'zgaradi | o'zgarmaydi | o'zgarmaydi | o'zgarmaydi |
| Optimallashtirish | o'zgarmaydi | o'zgarmaydi | o'zgarmaydi | o'zgaradi |

Jadvalning xulosasi shu: to'rt holatning hammasida mavjud xatti-harakatning
katta qismi saqlanishi kerak, va aynan xatti-harakat foydalanuvchi tayangan
narsa. Yangi xatti-harakat qo'shilsa odamlar xursand bo'ladi, tayangan
xatti-harakat o'zgarsa yoki yo'qolsa ishonch yo'qoladi (4-bet). Shundan
amaliy farq chiqadi: metod qo'shilishining o'zi xatti-harakatni
o'zgartirmaydi, toki u chaqirilmaguncha (5-bet).

```java
// Yangi metod qo'shildi: hali hech narsa o'zgarmadi, chunki chaqiruv yo'q
public class OrderService {
    public void addItem(OrderLine line) { /* mavjud mantiq */ }

    public void replaceItem(String sku, OrderLine line) { /* yangi mantiq */ }
}

// Xatti-harakat aynan shu qatorda o'zgaradi: yangi yo'l ulandi
@PostMapping("/orders/{id}/items")
ResponseEntity<Void> replace(@PathVariable String id,
                             @RequestBody OrderLine line) {
    orderService.replaceItem(line.sku(), line);
    return ResponseEntity.noContent().build();
}
```

Misol kitobdagi `CDPlayer` namunasining Spring MVC kontekstiga
o'tkazilgan shakli: g'oya bir xil, metod va ulanish qatori ikki alohida
qadam. Shuning uchun diffda yangi metod va uni ulagan qator ajratib
ko'rinadi, va [refaktoringni mantiq o'zgarishidan
ajratish](../clean-code/38-refaktoringni-xavfsiz-bajarish.md#384-refaktoringni-mantiq-ozgarishidan-ajratish)
qoidasi shu yerda kuchga kiradi.

Xavfni Feathers uchta savolga qisqartiradi (1-bob, 8-bet):

1. Qanday o'zgarish kiritishimiz kerak?
2. Buni to'g'ri bajarganimizni qanday bilamiz?
3. Boshqa hech narsani buzmaganimizni qanday bilamiz?

Birinchi savolga odatda javob bor, ikkinchisiga test yoziladi, uchinchisi
esa legacy kodda eng qimmat va eng ko'p tashlab ketiladigan savol. Feathers
ko'p jamoalar tanlagan javobni rad etadi: "buzilmagan narsaga tegmaslik"
siyosati o'zgarish sonini kamaytiradi, lekin mavjud sinf va metodlarni
kattalashtiradi, sinfni bo'lish ko'nikmasini zanglatadi va oxirida
o'zgarishdan qo'rqish madaniyatini qoldiradi (8-bet). Ya'ni xavfni
kamaytirish yo'li o'zgarishni kamaytirish emas, feedback qo'shish.

## 34.14 Ta'sir qanday tarqaladi: uch yo'l va inkapsulyatsiyaning foydasi

Qaysi metodni test qilish kerakligini aniqlash uchun o'zgarishning ta'siri
qayerga yetib borishini bilish kerak. Feathers ta'sir tarqalishining uch
yo'lini sanaydi (Feathers, *Working Effectively with Legacy Code*, 11-bob,
165-bet): chaqiruvchi ishlatadigan qaytish qiymati; parametr sifatida
uzatilgan obyektning holatini o'zgartirish, agar o'sha obyekt keyin
ishlatilsa; va statik yoki global ma'lumotni o'zgartirish, agar u keyin
ishlatilsa. Uchinchisi eng yashirin, chunki metod imzosida ko'rinmaydi:
Feathers buni "ma'lumotni yashirish yaxshi, lekin bizga kerak bo'lgan
ma'lumot yashirilmasa" deb izohlaydi (164-bet).

```java
// Uchta yo'l bitta metodda birga uchraydi
public class InvoiceBatch {
    private static int processed;                 // 3-yo'l: statik holat

    public BigDecimal post(List<Invoice> invoices) {
        invoices.removeIf(Invoice::isVoid);       // 2-yo'l: parametrni o'zgartirish
        processed += invoices.size();
        return invoices.stream().map(Invoice::total)
                .reduce(BigDecimal.ZERO, BigDecimal::add); // 1-yo'l: qaytish qiymati
    }
}

// Ta'sir yuzasi toraytirilgan shakl: parametr tegilmaydi, statik holat yo'q
public class InvoiceBatch {
    private final BatchCounter counter;           // bog'liqlik ko'rinib turadi

    public InvoiceBatch(BatchCounter counter) { this.counter = counter; }

    public BigDecimal post(List<Invoice> invoices) {
        var payable = invoices.stream().filter(i -> !i.isVoid()).toList();
        counter.add(payable.size());
        return payable.stream().map(Invoice::total)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

Izlash tartibi ham kitobdan olinadi: o'zgaradigan metodni belgilash;
qaytish qiymati bo'lsa chaqiruvchilarni ko'rish; metod qanday qiymatlarni
o'zgartirsa, o'sha qiymatlarni ishlatadigan metodlarni va ularni
ishlatadigan metodlarni ko'rish; superclass va subclass larni ham tekshirish,
chunki ular ham o'sha maydon va metodlarni ishlatishi mumkin; parametrlarni
va ular qaytargan obyektlarni ko'rish; oxirida statik va global
o'zgaruvchilarni ko'rish (165-bet).

Shu qadamlar sonini kamaytiradigan narsa inkapsulyatsiya. Feathers ikki
`Coordinate` sinfini yonma-yon qo'yadi: maydonlar `private` bo'lsa, ularni
o'zgartirish mijozlarga faqat bitta metod orqali yetib boradi, demak sinf
chegarasidan tashqariga qaramaslik mumkin; maydonlar package darajasida
ko'rinsa, paketdagi kod va subclass lar ham ularga tegishi mumkin, demak
izlash yuzasi kattalashadi (166-167-bet). Xulosa Feathers da to'g'ridan
yozilgan: tilning qoidalarini bilish kerak, chunki tilda ta'sirni
to'xtatadigan "devorlar" bor va ularni bilgan odam ulardan ortiga
qaramaydi (167-bet).

Ta'sir tahlilining uzoq muddatli foydasi esa boshqa: tahlilni takrorlagan
odam kod bazasining o'z qoidalarini topadi. Feathers buni "lekin bu
ahmoqlik bo'lardi" qoidasi deb ataydi: masalan konstruktorga uzatilgan
ro'yxat keyin tashqaridan o'zgartirilmaydi degan qoida bo'lsa, tahlil
qisqaradi; qoidalar yo'q yoki ular istisnolarga to'la bo'lsa, har safar
hammasini tekshirishga to'g'ri keladi (167-168-bet). Shuning uchun
inkapsulyatsiya va o'zgarmas obyekt refaktoringdan oldin ham foyda beradi:
ular keyingi har bir ta'sir tahlilini arzonlashtiradi. Ta'sirni qog'ozda
kuzatish usuli, effect sketch, [tizimni tushunish
usullari](#342-tizimni-tushunish-usullari-kirish-nuqtalari-malumot-oqimi-eng-kop-ozgargan-fayllar)
bo'limida.

## 34.15 Vaqtincha qoplama test: yuqori darajada yozib, keyin pastga tushirish

Feathers o'zgarish kiritishning ikki uslubini qarama-qarshi qo'yadi: Edit
and Pray, ya'ni ehtiyotkorlik bilan tahrirlab keyin tizimni qo'lda
tekshirish, va Cover and Modify, ya'ni kodni test bilan qoplab, keyin
o'zgartirish (Feathers, *Working Effectively with Legacy Code*, 2-bob,
9-bet). Qoplama metafora emas: o'zgarish kiritilayotgan joy test bilan
yopilgan bo'lsa, yomon o'zgarish shu joydan tashqariga chiqmaydi.

Qoplama testning darajasi birdan sinf darajasi bo'lishi shart emas.
Feathers yuqori darajali testning o'z o'rni borligini aytadi: ular bir
vaqtda bir necha sinfning xatti-harakatini qotirib qo'yadi, va shundan
keyin alohida sinflar uchun test yozish osonlashadi (14-bet). Bu legacy
kodda tartibni teskari qiladi: avval tor unit test emas, avval keng
qoplama test.

```java
// Qoplama test: pinch point'da turadi va bir nechta sinfni birga qamraydi
class PaymentPinchPointTest {

    @Test
    @DisplayName("komissiya qaydi production namunasida saqlanadi")
    void komissiyaQaydiSaqlanadi() {
        var facade = new PaymentFacade(new FeeTable(), new AcquirerStub());

        var receipt = facade.charge(order("ORD-1042"));

        // kutilgan qiymat o'ylab topilmagan, eski koddan o'qib olingan
        assertThat(receipt.fee()).isEqualTo(Money.of("3.47"));
    }
}
```

Shu bosqichda bog'liqlikni uzish uchun testsiz refaktoring qilishga to'g'ri
keladi, va Feathers buning xavfsiz chegarasini aytadi: Primitivize Parameter
va Extract Interface kabi qadamlarni test yo'q joyda ham bajarish mumkin,
agar ular juda konservativ bajarilsa (17-bet). Natija chiroyli bo'lmasligi
mumkin: production kodga faqat test uchun kerak bo'lgan parametr qo'shilishi
yoki sinf g'alati joydan bo'linishi mumkin. Feathers buni jarrohlikdagi
kesish joyiga o'xshatadi: kodda chandiq qoladi, lekin uning ostidagi hamma
narsa yaxshilanishi mumkin, va keyin o'sha joy test bilan qoplangach
chandiq ham tuzatiladi (18-bet).

Qoplama testning tuzog'i ham bor. Pinch point'da yozilgan test vaqt o'tib
katta integratsion testga aylanadi: yangi kod uchun unit test yozganda
hamkorlarni birga yaratish odat bo'lib qoladi va test to'plami sekinlashadi
(12-bob, 184-bet). Feathers ikki yo'nalishni ajratadi. Yangi kod uchun:
test kattalashayotganini sezsangiz, sinfni kichikroq mustaqil bo'laklarga
bo'ling va hamkorlarni fake bilan almashtiring. Mavjud kod uchun: aksincha,
avval bir bo'lakni pinch point testi bilan o'rab oling, keyin tegayotgan
har bir sinf uchun tor test yozing, va oxirida pinch point'dagi testlarni
o'chirib tashlang (184-bet). Feathers buni o'rmonga bir necha qadam kirib
chiziq chizishga o'xshatadi: chiziq ichidagi yer sizning, uni test va
refaktoring bilan o'zlashtirasiz.

ESLATMA: qoplama testni vaqtincha ekanini kodda belgilash shu korpusning
amaliy tavsiyasi: test sinfining nomida yoki `@DisplayName` da uning
pinch point testi ekani va qaysi shart bajarilganda o'chirilishi yozib
qo'yiladi, aks holda u doimiy sekin integratsion testga aylanadi. Qayd
etuvchi testning o'z mexanikasi [xavfsizlik to'ri
qurish](#343-xavfsizlik-tori-qurish-xatti-harakatni-qayd-etuvchi-test)
bo'limida, pinch point ta'rifi esa [chok
topish](#344-chok-seam-topish-ozgarishni-kiritish-mumkin-bolgan-nuqta)
bo'limida.

## 34.16 Metod ichidagi `new` ni testda almashtirish: Extract and Override uchligi

Metod ichidagi `new` uchun maqsad holati [chok
topish](#344-chok-seam-topish-ozgarishni-kiritish-mumkin-bolgan-nuqta)
bo'limida yozilgan: bog'liqlikni konstruktor argumentiga chiqarish va
to'ldirishni konteynerga qoldirish. Bu
to'g'ri maqsad, lekin u bitta qadamda bajarilsa, testi yo'q sinfning
konstruktori o'zgaradi va o'zgarish o'sha sinfni yaratadigan hamma joyga
tegadi. Feathers shu vaziyat uchun oraliq qadam beradi: yaratishni yoki
muammoli chaqiruvni `protected` metodga chiqarib, testda subclass bilan
override qilish. Production konstruktorlari va chaqiruvchilar tegilmaydi,
seam esa darhol paydo bo'ladi.

```java
// OLDIN: seam yo'q, chunki yaratish metod ichida qotib qolgan
public class PaymentService {
    public Receipt charge(Order order) {
        var gateway = new AcquirerGateway(AppConfig.acquirerUrl());
        return gateway.charge(order.total());
    }
}

// KEYIN: yaratish protected fabrika metodiga chiqdi, mantiq tegilmadi
public class PaymentService {
    public Receipt charge(Order order) {
        return createGateway().charge(order.total());
    }

    protected AcquirerGateway createGateway() { // enabling point: override
        return new AcquirerGateway(AppConfig.acquirerUrl());
    }
}

// Test manbasidagi subclass: production kodining imzolari o'zgarmadi
class TestablePaymentService extends PaymentService {
    private final AcquirerGateway fake = new FakeAcquirerGateway();

    @Override
    protected AcquirerGateway createGateway() {
        return fake;
    }
}
```

Feathers uchta variantni ajratadi va ularning qo'llanish sharti boshqa.

| Holat | Usul | Nimani override qilasiz |
|---|---|---|
| Bitta muammoli chaqiruv, ko'pincha statik metod yoki global | Extract and Override Call (348-bet) | chaqiruvni o'ragan yangi `protected` metod |
| Obyekt konstruktorda yaratiladi | Extract and Override Factory Method (350-bet) | yaratish ishini butunlay olgan `protected` fabrika metodi |
| Bitta obyektning ko'p metodi muammoli | Extract and Override Getter (352-bet) | maydonni qaytaradigan `protected` getter |

Uchala variantning mexanikasi, imzo ko'chirish sharti, Java va C++
farqi hamda lazy getter ning initsializatsiya xavfi pattern yozuvida
to'liq yozilgan: [chaqiruvni ajratib override
qilish](../patterns/23-testing-patternlari.md#2386-chaqiruvni-ajratib-override-qilish-extract-and-override-call--factory-method--getter).
Bu yerda faqat legacy ishidagi tartib muhim: oraliq qadam
chaqiruvchilarni tegmasdan seam beradi, maqsad esa baribir konstruktor
injection.

ESLATMA: Spring kontekstidagi uchta qo'shimcha shart shu korpusning
tavsiyasi. Fabrika metodi `private` yoki `final` bo'lmaydi, aks holda
override qilinmaydi. Override qiluvchi subclass faqat test manbasida
yashaydi va bean sifatida ro'yxatga olinmaydi. Va oraliq qadam maqsad emas:
test qoplamasi paydo bo'lgandan keyin fabrika metodi konstruktor
argumentiga ko'chiriladi, chunki shu paytda chaqiruvchilarni o'zgartirish
xavfi o'lchangan bo'ladi.

## 34.17 Statik chaqiruv va singleton: instance delegator va static setter

Statik metodni testda almashtirib bo'lmaydi: chaqiruv joyida obyekt yo'q,
demak object seam ham yo'q. Feathers bu holatni static cling deb ataydi va
oraliq yechimni beradi: statik metodni o'z joyida qoldirib, sinfga unga
delegat qiladigan instance metod qo'shish, keyin chaqiruvchilarni statik
chaqiruvdan obyekt chaqiruviga o'tkazish (Feathers, *Working Effectively
with Legacy Code*, 25-bob, 369-370-bet). Obyektni chaqiruvchiga yetkazish
uchun Parameterize Method (383-bet) yoki shunga o'xshash qadam ishlatiladi,
statik tipli tilda esa kompilyator qolgan joylarni o'zi ko'rsatadi
(371-bet).

```java
// 1-qadam: statik metod joyida qoladi, yoniga delegat instance metod qo'shiladi
public class BankingServices {
    public static void updateAccountBalance(long userId, Money amount) {
        /* mavjud mantiq */
    }

    public void updateBalance(long userId, Money amount) { // delegat
        updateAccountBalance(userId, amount);
    }
}

// 2-qadam: chaqiruvchi statik chaqiruv o'rniga obyektni oladi, seam paydo bo'ldi
public class SettlementJob {
    private final BankingServices services;

    public SettlementJob(BankingServices services) { this.services = services; }

    public void settle(Order order) {
        services.updateBalance(order.userId(), order.total());
    }
}
```

Feathers bu holatning noqulayligini yashirmaydi: o'nta statik va ikkita
instance metodi bor sinf g'alati ko'rinadi. Lekin yo'nalish aniq: vaqt
o'tib utility sinfga hamma chaqiruv delegat metodlar orqali o'tgach, statik
metodlarning tanasi instance metodlarga ko'chiriladi va statik metodlar
o'chiriladi (370-bet).

Global mutable holat singleton shaklida bo'lsa, qadam boshqacha. Feathers
singletonning uch xossasini sanaydi: konstruktor `private`, yagona nusxani
statik maydon ushlaydi, va nusxaga statik metod orqali yetiladi (372-bet).
Shu uchta xossa production'da bitta nusxani kafolatlaydi, lekin test
harness'da ham bitta nusxani majburlaydi. Yechim: singletonga nusxani
almashtiradigan statik setter qo'shish va konstruktorni `protected` qilish;
shundan keyin singletonni subclass qilib, yangi obyekt yasab, setter orqali
qo'yish mumkin (372-bet).

```java
public class PermitRepository {
    private static PermitRepository instance;

    protected PermitRepository() { } // private edi: subclass uchun ochildi

    public static PermitRepository instance() {
        if (instance == null) { instance = new PermitRepository(); }
        return instance;
    }

    // FAQAT test uchun qo'shilgan, production kodida chaqirilmaydi
    public static void setTestingInstance(PermitRepository replacement) {
        instance = replacement;
    }
}
```

Feathers ikki eslatmani birga beradi. Birinchisi: himoyani pasaytirgan joyga
izoh qoldiriladi, ya'ni bu test uchun ochilgani va production kodida
ishlatilmasligi yozib qo'yiladi (372-bet). Ikkinchisi qadamlar ichida:
setter yangi nusxani qo'yishdan oldin eskisini to'g'ri yo'q qilishi kerak,
va agar testda singletonni to'g'ri holatga keltirish uchun yopiq metodlar
kerak bo'lsa, singletondan interface ajratib, u o'z nusxasini shu interface
turida ushlashi mumkin (376-bet). Yengilroq alternativani ham beradi:
singletonga statik maydonni `null` ga qaytaradigan `resetForTesting` metodi
qo'shish, agar singletonning public metodlari kerakli holatni to'liq
tiklashga yetsa; yetmasa yoki tashqi resursga tegsa, static setter yaxshiroq
tanlov (9-bob, 122-bet). Chiqish yo'li esa parametr uzatish: globalga
muhtoj sinflarga umumiy superclass berib, obyektni ularga yaratilish
paytida uzatish mumkin, va shunda global asta-sekin yo'qoladi (376-bet).

Uch shaklning pattern yozuvi, Spring sharti va qaysi birini qachon
tanlash mezoni [statik metodni test uchun
ochish](../patterns/23-testing-patternlari.md#2385-statik-metodni-test-uchun-ochish-expose-static-method--introduce-instance-delegator--introduce-static-setter)
bo'limida.

Maqsad holati korpusda allaqachon bor: statik chaqiruv va
`getInstance()` o'rniga konstruktor injection, [singleton'dan
suiiste'mol](../patterns/25-anti-patternlar.md#2526-singletondan-suiistemol--statik-yopishqoqlik-singleton-abuse--static-cling)
yozuvida. Ikki pozitsiyani ajratadigan shart oddiy: sinfning testi bor va
chaqiruvchilarni o'zgartirish xavfi o'lchangan bo'lsa, to'g'ridan DI ga
o'tiladi; testi yo'q va chaqiruvchilar soni noma'lum bo'lsa, avval shu
bo'limdagi oraliq qadam, keyin DI.

## 34.18 Interface ajratish ishlamaganda: Adapt Parameter va Extract Implementer

Extract Interface eng arzon qadam, lekin u ikki holatda ishlamaydi.
Birinchisi: muammoli tur metod parametri bo'lib, u sizning emas, tashqi
standartning interface'i. Feathers misoli `HttpServletRequest`: undan
interface ajratib bo'lmaydi, chunki interface'dan interface ajratilmaydi va
standart interface'ni o'zgartirib bo'lmaydi, qo'lda fake yozish uchun esa
yigirmadan ortiq metodni implementatsiya qilishga to'g'ri keladi (Feathers,
*Working Effectively with Legacy Code*, 25-bob, 326-327-bet). Mock
kutubxonasi bu ishni qisqartiradi, lekin natijada production kod o'sha API
interface'iga bog'liq bo'lib qoladi (327-bet). Adapt Parameter boshqa yo'l
beradi: parametr uchun o'z tor interface'ingizni yozib, production
implementatsiyasi tashqi obyektni o'rab olsin, testda esa oddiy fake
ishlatilsin.

```java
// O'z interface'imiz: tashqi API emas, mas'uliyat tilida yozilgan
public interface ParameterSource {
    String value(String name);
}

// Production implementatsiyasi tashqi API ni o'rab oladi
public class ServletParameterSource implements ParameterSource {
    private final HttpServletRequest request;

    public ServletParameterSource(HttpServletRequest request) {
        this.request = request;
    }

    @Override
    public String value(String name) {
        String[] values = request.getParameterValues(name);
        return (values == null || values.length == 0) ? null : values[0];
    }
}

// Test uchun fake: bitta metod, bitta qator
public class MapParameterSource implements ParameterSource {
    private final Map<String, String> values = new HashMap<>();

    @Override
    public String value(String name) { return values.get(name); }
}
```

Feathers bu usulning narxini ham aytadi: Adapt Parameter Preserve Signatures
qoidasi buziladigan kam holatlardan biri, chunki metod imzosi o'zgaradi;
yangi tor interface parametrning hozirgi interface'idan juda farq qilsa,
jim xato kirib qolishi mumkin (328-bet). Shuning uchun uning qoidasi:
tanlov eng chiroyli tuzilish tomonga emas, o'zingiz ishonadigan qadam
tomonga egilsin, chiroyli tuzilish testdan keyin keladi (328-bet).

Ikkinchi holat: interface uchun eng to'g'ri nom sinfning o'z nomi bo'lib
chiqadi. Feathers bu muammoni nomlash muammosi deb qo'yadi: `I` prefiksini
yopishtirish yoki sun'iy nom o'ylab topish kod bazasini buzadi, shuning
uchun kod bazasida shunday konvensiya bo'lmasa, u bunday qilmaydi
(356-bet). Extract Implementer teskari yo'nalishda ishlaydi: sinf nomi
interface bo'lib qoladi, konkret metodlar esa pastdagi yangi sinfga
tushiriladi. Feathers yangi sinfga `Production` prefiksini qo'yishni odat
qilgan (357-bet), va qadamlar ichida eng muhimi oxirgisi: eski sinf
nusxasini yaratadigan hamma joy yangi production sinfiga o'tkaziladi va
kompilyator qolganini ko'rsatadi (359-bet).

```java
// OLDIN: sinf nomi chaqiruvchilarning hammasida ishlatilgan
public class ReportGenerator {
    public Report generate(ReportRequest request) { /* og'ir mantiq */ }
}

// KEYIN: nom interface'ga o'tdi, implementatsiya pastga tushdi.
// Chaqiruvchilarning bitta qatori ham o'zgarmaydi
public interface ReportGenerator {
    Report generate(ReportRequest request);
}

public class ProductionReportGenerator implements ReportGenerator {
    @Override
    public Report generate(ReportRequest request) { /* o'sha mantiq */ }
}
```

| Shart | Usul | Narxi |
|---|---|---|
| Sinf sizning kodingizda va interface uchun yangi nom topiladi | Extract Interface (362-bet) | eng arzon, xatoni kompilyator aytadi |
| Interface uchun eng to'g'ri nom sinfning o'z nomi | Extract Implementer (356-bet) | `new` chaqiruvlari yangi production sinfga ko'chadi |
| Muammoli tur metod parametri va u tashqi API interface'i | Adapt Parameter (326-bet) | imzo o'zgaradi, Preserve Signatures buziladi |

ESLATMA: Spring kontekstidagi ikki kuzatish shu korpusning qo'shimchasi.
Java'da IDE sinfni qayta nomlash va interface ajratishni birga bajaradi,
shuning uchun Extract Implementer kamdan kam kerak bo'ladi; u kerak
bo'ladigan joy - sinf nomi ko'p modulda yozilgan va o'sha nomni
chaqiruvchilarda o'zgartirmaslik talab qilinadigan holat. Natijada
`@Component` yangi production sinfiga ko'chadi, inyeksiya nuqtalari esa
eski nomni, ya'ni endi interface'ni, ko'rib turadi. Patternning umumiy
katalog yozuvi [Adapter](../patterns/02-strukturaviy-patternlar.md#21-adapter-adapter)
bo'limida, bu yerda esa uning bog'liqlik uzish uchun ishlatilishi.

## 34.19 Nimadan boshlash: qiymat va qiyinlik kvadranti

[Bazani ajratish](#348-malumotlar-bazasini-ajratish-eng-qiyin-qism-va-uning-tartibi)
tartibi "qanday" savoliga javob beradi, bu bo'lim esa undan oldin keladigan
"nimadan" savoliga. Newman javobni ikki qadamga bo'ladi: avval chegarani eng
arzon joyda sinash, keyin nomzodlarni ikki o'q bo'yicha tartiblash.

**Xatoni eng arzon joyda qilish.** Kod bazasi ichida kodni ko'chirish narxi
kichik: asboblar yordam beradi va muammo chiqsa tuzatish tez bo'ladi. Bazani
ajratish esa ancha ko'p ish, va baza o'zgarishini qaytarish ham xuddi shunday
murakkab; bir nechta iste'molchi ishlatadigan API ni butunlay qayta yozish yoki
ortiqcha bog'langan integratsiyani yechish ham katta ish bo'ladi. O'zgarish
narxi katta bo'lgani uchun bu amallar xavfli, va Newman ning yondashuvi oddiy:
xatoni ta'siri eng past bo'lgan joyda qilish (Sam Newman, *Monolith to
Microservices*, O'Reilly, 2020, 2-bob, 56-bet).

Eng past joy doska. Newman fikrlashning ko'p qismini aynan shu yerda bajaradi,
chunki o'zgarish va xato narxi shu yerda eng kichik: taklif qilinayotgan dizayn
chiziladi, keyin servis chegaralari deb o'ylanayotgan chiziqlar bo'ylab
use-case lar yurgiziladi (56-bet). Musiqa do'koni misolida bu shunday ko'rinadi:
mijoz plastinka qidirsa, saytda ro'yxatdan o'tsa, albom sotib olsa nima
bo'ladi? Qanday chaqiruvlar ketadi? G'alati aylanma havolalar ko'rinayaptimi?
Juda gaplashuvchi ikki servis chiqyaptimi, bu esa ular bitta narsa bo'lishi
kerakligini bildirmaydimi (56-bet). Uchta savolning har biri chegarani kod
yozilmasdan rad etishi mumkin.

**Nomzodlarni tartiblash.** Qiyinlik bahosi domen modelidan chiqadi: bounded
context lar orasidagi kiruvchi va chiquvchi bog'liqliklar soniga qarab qaysi
funksionallikni ajratish oson yoki qiyin bo'lishini taxmin qilish mumkin.
Newman ning misolida xabarnoma funksionalligiga ko'p joy murojaat qiladi,
shuning uchun uni ajratish mavjud kodda ko'p ish talab qiladi; hisob-faktura
esa kiruvchi bog'liqliksiz, shuning uchun uni ajratish osonroq va bu yerda
[bo'g'uvchi anjir](#347-boguvchi-anjir-strangler-usuli-bilan-bosqichma-bosqich-almashtirish)
yaxshi ishlaydi, chunki kiruvchi chaqiruvlarni monolitga yetib borishidan oldin
proxy qilish mumkin (58-59-betlar).

Bu baho taxmin ekanini Newman alohida eslatadi: domen modeli mavjud tizimning
mantiqiy ko'rinishi, monolitning kod tuzilmasi aynan shunday bo'lishiga hech
qanday kafolat yo'q, shuning uchun chalkashlik darajasini aniqlash uchun kodning
o'ziga ham qarash kerak bo'ladi; model yana bitta narsani ko'rsatmaydi, ya'ni
qaysi bounded context bazada ma'lumot saqlashini, shuning uchun oson ko'ringan
hisob-faktura ko'p ma'lumot boshqarayotgan bo'lsa, baza dekompozitsiyasi ishi
qo'shiladi va u birinchi ikki servis uchun tanlanmasligi mumkin (59-60-betlar).

Qiyinlikning o'zi yetarli emas. Newman ikkinchi o'qni qo'shadi va sababini
aytadi: tez g'alabalar harakat hissi va yondashuvning samarasi haqida erta
qayta aloqa beradi, shuning uchun ular oson narsalarni tanlashga undaydi, lekin
dekompozitsiyadan foyda ham olish kerak. Shuning uchun ikki o'qli sodda
tuzilma ishlatiladi: x o'qi dekompozitsiya keltiradigan qiymat, y o'qi
qiyinlik; har bir nomzod shu tekislikka qo'yiladi, va yuqori o'ng burchakdagi
funksionallik, ya'ni oson va foydali bo'lgani birinchi ajratiladi; shu
guruhdan bitta yoki ikkita servis birinchi nomzod bo'ladi (60-61-betlar).

```text
qiyin
  ^
  |  Xabarnoma            |  To'lov
  |  (ko'p kiruvchi       |  (foyda katta, lekin
  |   bog'liqlik)         |   baza ajratish kerak)
  |-----------------------+-----------------------
  |  Statik ma'lumotnoma  |  Hisob-faktura
  |  (oson, lekin foyda   |  (oson va foydali:
  |   kam)                |   birinchi nomzod)
oson
  +-------------------------------------------> qiymat
     kam                                   katta
```

Tartib bir marta tuzilib qotib qolmaydi. Newman ning so'zi bilan: o'zgarishlar
boshlangandan keyin ko'proq narsa bilinadi, oson deb o'ylangan narsaning bir
qismi qiyin bo'lib chiqadi, qiyin deb o'ylangan narsaning bir qismi oson bo'lib
chiqadi, va bu tabiiy; shuning uchun ustuvorlik mashqini qaytarib, rejani
yangilash muhim (61-bet).

Bitta tuzoq ro'yxatdan tashqarida va u maqsadga tegishli. Newman hisob-faktura
haqiqatan oson birinchi qadam bo'lishi mumkin, lekin maqsad bozorga chiqish
vaqtini yaxshilash bo'lsa va hisob-faktura funksionalligi deyarli o'zgarmasa,
bu vaqtni yaxshi sarflash bo'lmasligini aytadi (60-bet). Ya'ni x o'qidagi
"qiymat" mavhum foyda emas, aynan sizning yozilgan maqsadingiz bo'yicha
qiymat; uni biznes tilida ifodalash esa
[refaktoringni biznes bilan kelishish](#349-refaktoringni-biznes-bilan-kelishish-qiymat-tilida-tushuntirish)
bo'limida.

Kvadrant birinchi nomzodni tanlaydi, lekin uning ustiga yana bitta filtr
qo'yiladi: ko'rinadiganlik. Newman ning The Guardian misolida reja sahifa
bo'yicha ko'chirish edi va birinchi vertikal sifatida Travel tanlandi, qisman
kategoriyalash muammosi qiziq bo'lgani uchun, qisman esa u saytning eng ko'zga
ko'rinadigan qismi emasligi uchun (99-bet). Butun Travel bo'limini birdan
chiqarish o'rniga esa yanada kichik qadam qilingan: yangi tizimda
belgilangan, eng ko'p boriladigan 10 manzilni ko'rsatadigan bitta vidjet eski
sahifaga joylashtirildi. Maqsad ikki qatorda aytilgan: biror narsani tirik
qilib o'rganish, va xato chiqsa saytning asosiy qismlariga zarar
bermasligini ta'minlash. Ya'ni kvadrantdagi "oson va foydali" nomzodlar
ichidan eng kam ko'rinadigani birinchi boriladi; UI darajasida vidjet bo'yicha
kompozitsiyaning o'zi [patterns 27.2](../patterns/27-monolitdan-microservicega-migratsiya.md#272-ui-kompozitsiyasi-ui-composition)
da.

ESLATMA: yuqoridagi kvadrant chizmasidagi nomlar va joylashuv korpusning
namunasi: Newman o'qlarni va yuqori o'ng burchak qoidasini beradi, aniq
nomzodlarni esa o'z tizimingizdan qo'yasiz.

## 34.20 Bazani ajratishning besh qadami va ma'lumot suvereniteti narxi

[34.8](#348-malumotlar-bazasini-ajratish-eng-qiyin-qism-va-uning-tartibi)
Newman ning tanlovini va ko'chirish patternlarini beradi. *The Hard Parts*
xuddi shu ishni boshqa tomondan, baza jamoasining qadamlari sifatida yozadi va
besh qadamni raqamlab beradi (6-bob, 155-161-betlar). Ikki yozuv raqobatchi
emas: Newman qaysi tomondan boshlashni, bu ro'yxat esa bazaning o'zida nima
ketma-ketlikda bajarilishini aytadi.

| Qadam | Nima qilinadi | Oxirida nima bo'ladi |
|---|---|---|
| 1 | Bazani tahlil qilib data domain larni aniqlash: bog'liq jadvallar guruhlarga yig'iladi | domen nomzodlari ro'yxati, kod o'zgarmaydi |
| 2 | Jadvallar bounded context bo'yicha o'z sxemasiga biriktiriladi | har domen o'z sxemasida, servislar hali hamma narsaga tegadi |
| 3 | Servis ulanishlari faqat o'z sxemasiga qoldiriladi, boshqa domen ma'lumoti egasi orqali olinadi | servisga ma'lumot suvereniteti |
| 4 | Sxemalar alohida fizik baza serveriga ko'chiriladi | arxitektura kvanti bo'linadi |
| 5 | Eski serverga ulanish va undagi sxemalar olib tashlanadi | mustaqil deploy qilinadigan birliklar |

Ikkinchi qadamda ikki amaliy tafsilot bor. Birinchisi, jadvalni sxemaga
ko'chirish oddiy DDL: `ALTER SCHEMA payment TRANSFER sysops.billing` (kitob
misoli SQL Server sintaksisida, PostgreSQL da `ALTER TABLE ... SET SCHEMA`).
Ikkinchisi, o'z sxemasiga tegishli bo'lmagan jadval uchun vaqtincha synonym
yaratish mumkin, ya'ni symlink ga o'xshash, boshqa sxemadagi obyektga
alternativ nom beradigan konstruksiya; maqsadi sxemalararo so'rovni yo'qotish,
lekin unga kirish uchun ham o'qish yoki yozish huquqi kerak bo'ladi. Shu
sababli synonym o'tish vositasi, yechim emas. Domenlar bir-biriga qattiq
bog'langan bo'lsa, domenlarni birlashtirish kerak bo'ladi va natijada bir
nechta servis bitta data domain ga egalik qiladigan kengroq bounded context
hosil bo'ladi.

Uchinchi qadamda baza darajasidagi hamma kesib o'tuvchi narsa olib tashlanadi:
domenlar orasidagi tashqi kalit, view va trigger, hamda boshqa domen
jadvaliga tegadigan stored procedure va funksiyalar servis qatlamiga
ko'chiriladi. Natija kitobda "nirvana holati" deb atalgan, lekin narxi ochiq
yozilgan.

| Foydasi | Narxi |
|---|---|
| Jamoa sxemani boshqa domenga ta'sirini o'ylamasdan o'zgartiradi | Katta hajmli ma'lumotga kirish kerak bo'lganda ishlash muammosi chiqadi |
| Har servis o'z holatiga mos baza texnologiyasi va turini tanlaydi | Bazada referential integrity saqlanmaydi, demak yomon sifatli ma'lumot ehtimoli paydo bo'ladi |
| | Boshqa domen jadvallariga tegadigan baza kodi servis qatlamiga ko'chirilishi kerak |

Ikkinchi qator eng ko'p e'tibordan qoladigani: `FOREIGN KEY` yo'qolgani
tekshiruvni yo'q qilmaydi, uni ilovaga ko'chiradi. Spring loyihasida bu
amalda nimani bildiradi: `orders.customer_id` uchun baza endi kafolat
bermaydi, shuning uchun buyurtma yaratishda mijoz mavjudligini tekshirish
chaqiruvi, uning timeout i va mijoz o'chirilganda qoladigan yetim qatorlar
uchun muntazam tekshiruv (reconciliation) kerak bo'ladi. Buning shakli
[32-bob](32-tarmoq-timeout-va-integratsiya-haqiqati.md) dagi timeout va
integratsiya apparati bilan boradi.

To'rtinchi qadamda bitta tanlov qoladi va u to'xtash vaqti haqida. Kitob ikki
variantni beradi (160-bet). **Backup va restore**: har bir domen sxemasi
backup qilinadi, yangi serverlar ko'tariladi, sxemalar restore qilinadi,
servislar yangi serverdagi sxemalarga ulanadi va oxirida sxemalar eski
serverdan olib tashlanadi; bu yo'l odatda migratsiya uchun to'xtash talab
qiladi. **Replikatsiya**: avval yangi serverlar ko'tariladi, sxemalar
replikatsiya qilinadi, ulanishlar yangi serverlarga o'tkaziladi, keyin
sxemalar eski serverdan olib tashlanadi; to'xtash bo'lmaydi, lekin
replikatsiyani sozlash va muvofiqlashtirish uchun ancha ko'p ish talab
qiladi. Tanlov mezoni oddiy: ruxsat etilgan to'xtash oynasi bormi. Oyna
bo'lsa backup va restore arzonroq, bo'lmasa replikatsiya narxi ongli
qabul qilinadi.

Beshinchi qadamdan keyin ochiladigan imkoniyat ham yozilgan: domenlar
ajratilgandan keyin har bir baza serverini mavjudlik va masshtab uchun alohida
optimallashtirish, hamda ma'lumotni tahlil qilib eng mos baza turini tanlash
mumkin bo'ladi, ya'ni polyglot saqlash shu nuqtada mantiqiy bo'ladi, oldin
emas.

## 34.21 Deprecation ni jarayon sifatida yuritish: ega, almashtirish va orqaga qaytishni to'sish

Refaktoring va ajratishning oxirgi qadami eskisini o'chirish. Amalda aynan shu
qadam tugamay qoladi va tizimda ikki yo'l (eskisi va yangisi) yillab yonma-yon
yashaydi. *Software Engineering at Google* bu ishni alohida jarayon deb
qaraydi va boshlanish nuqtasi sifatida bitta tasdiqni oladi: kod aktiv emas,
majburiyat. Shundan bir nechta amaliy qoida chiqadi.

**Faqat yoshi uchun deprecate qilinmaydi.** Tizim yillar davomida sayqallanib,
shakl va funksiya namunasiga aylangan bo'lishi mumkin; LaTeX misolida
o'zgarishlar kam va kamdan kam bo'lsa ham tizim eskirgan emas. Kitobning
mezoni ikki shartli: deprecation isbotlanadigan darajada eskirgan tizimlar
uchun, va teng yoki yaxshi funksionallik beradigan almashtiruvchi mavjud
bo'lganda to'g'ri keladi.

**Deprecation qiyin, chunki almashtiruvchi boshqacha.** Hyrum qonuni shu
yerda ham ishlaydi: foydalanuvchi ko'p bo'lsa, kimdir tizimni kutilmagan
usulda ishlatayotgan bo'lish ehtimoli yuqori, va olib tashlash eng radikal
o'zgarish bo'lgani uchun eng ko'p yashirin bog'liqlikni ochib tashlaydi.
Yangi tizim yaxshiroq bo'lishi mumkin, lekin u boshqacha; agar aynan bir xil
bo'lsa, ko'chishning foydalanuvchi uchun foydasi bo'lmaydi. Natijada eski va
yangi tizim orasida birma-bir moslik kam uchraydi va eski tizimning har bir
ishlatilishi yangisi kontekstida alohida baholanishi kerak bo'ladi. Qarshilik
emotsional ham bo'ladi, "men bu kodni yaxshi ko'raman" degan javob tanish; bu
tushunarli, lekin tizim eskirgan bo'lsa u tashkilot uchun sof xarajat.

**Jarayonning aniq egasi bo'ladi.** Google ning xulosasi keskin: aniq ega
bo'lmasa, tizim qancha ogohlantirish va alert chiqarsa ham deprecation
sezilarli natijaga erishmaydi. Alternativalar yomonroq: hech narsani
deprecate qilmaslik, ya'ni har eski tizimni cheksiz ushlab turishga majburiyat
olish; yoki ishni tizim foydalanuvchilariga topshirish, ya'ni organik ravishda
hech qachon tugamaydigan advisory deprecation. Egasiz qolgan loyihalar ham
o'z-o'zidan yo'qolmaydi, va bunday ishni yon vazifa sifatida bergan jamoa uni
bajarmaydi: ustuvorlik raqobatida deprecation deyarli har doim pastga tushadi,
shuning uchun olib tashlash jamoaning asosiy maqsadi bo'lishi kerak.

**Ko'chish ishini eski tizimning egasi bajaradi.** Katta ko'lamli
o'zgarishlar (LSC) haqidagi bobdagi sabab uch qatorda: infratuzilma jamoasida
yuzlab ming havolani tuzatish uchun kerakli domen bilimi bor va har jamoani shu
bilimni qaytadan o'rganishga majburlash global jihatdan samarasiz; "moliyalash
berilmagan mandat" ni hech kim yoqtirmaydi, chunki yangi tizimning foydasi
tashkilot bo'ylab tarqaladi va bitta jamoa uchun o'z tashabbusi bilan
ko'chishga arzimaydi; va organik ko'chish deyarli tugamaydi, chunki dasturchi
yangi kod yozganda mavjud kodni namuna qilib oladi. Shuning uchun eskisini
olib tashlashdan manfaatdor jamoa ko'chishga mas'ul bo'lishi kerak.

**Orqaga qaytish (backsliding) to'siladi.** Eng ko'p e'tibordan qoladigan
qism: deprecate qilinayotgan narsaga yangi ishlatish qo'shilishini
to'xtatadigan asbob. Bo'lmasa, deprecation whack-a-mole ga aylanadi,
foydalanuvchi tanish tizimga yangi chaqiruv qo'shadi yoki kod bazasidan
namuna topadi, jamoa esa shu yangi chaqiruvlarni muntazam ko'chiradi; bu ham
samarasiz, ham ruhni tushiradi. Google da ikki daraja ishlatiladi: mikro
darajada statik tahlil review paytida muallifga yangi chaqiruv haqida xabar
beradi (eski simvollarga `@Deprecated` kabi annotatsiya qo'yiladi va xabar
matnini eski tizim egasi boshqaradi), makro darajada esa build dagi
ko'rinish ro'yxati (visibility whitelist) yangi bog'liqlik qo'shilishini
umuman to'sadi.

```java
// Mikro daraja: review da ko'rinadigan belgi.
@Deprecated(since = "4.2", forRemoval = true)
public interface LegacyPaymentClient {
    // Almashtiruvchi: com.shop.order.spi.PaymentAuthorizer
    AuthorizationResult authorize(String orderId, long amountMinor);
}
```

```java
// Makro daraja: build da to'siladigan qoida. Ro'yxat qisqarib boradi.
@ArchTest
static final ArchRule legacy_mijozga_yangi_bogliqlik_qoshilmaydi = noClasses()
        .that().resideOutsideOfPackages("com.shop.legacy..", "com.shop.migration..")
        .should().dependOnClassesThat()
        .haveFullyQualifiedName("com.shop.legacy.LegacyPaymentClient");
```

**Dizayn paytida deprecation o'ylanadi.** Kitob buni dasturiy injeneriyada
radikal, boshqa injeneriya sohalarida esa oddiy deb ataydi: atom
elektrostansiyasi loyihalanganda uning xizmat muddati tugagandan keyin
yopilishi hisobga olinadi va bunga mablag' ham ajratiladi. Dasturiy tizimlar
uchun Google jamoalariga beradigan savollar shu bobga to'g'ridan to'g'ri mos
tushadi: iste'molchi boshqa yechimga qanchalik oson o'ta oladi, tizim
qismlarini bosqichma-bosqich almashtirish mumkinmi. Shundan ham bitta
tashkiliy qoida chiqadi: tashkilot qo'llab-quvvatlashga tayyor bo'lmagan
loyiha boshlanmaydi, va bir vaqtda yuritiladigan deprecation ishlari soni
cheklanadi, chunki ikki tizimni ushlab turish va eski bilan moslikni saqlash
yangisining rivojini sekinlashtiradi.

## 34.22 Amalda qo'llash

Quyidagi ro'yxat shu korpusning o'z checklisti: boblardagi kitob qoidalarini
bitta ish tartibiga yig'adi.

- [ ] `git log --name-only` asosida oxirgi 2 yilda eng ko'p o'zgargan 30 faylni chiqarib, ularning hajmi bilan jadval tuzing va refaktoring nomzodlarini belgilang.
- [ ] `pg_stat_user_tables` va `pg_stat_statements` bo'yicha eng og'ir so'rovlarni va ishlatilmayotgan index'larni yozib oling, bu refaktoringdan oldingi asos bo'ladi.
- [ ] Tanlangan modulning 3 ta eng muhim ssenariysi uchun production ma'lumotidan characterization qayd fayli tayyorlang: har bir qayd yiqiladigan assert'dan boshlanadi.
- [ ] Modulda `new` operatori yoki `static` chaqiruv bilan qotib qolgan 5 ta bog'lanishni toping, Extract Interface bilan object seam qo'ying va har biri uchun enabling point qayerda ekanini yozib qo'ying.
- [ ] Yangi funksiyani eski metod ichiga yozish o'rniga Sprout Method yoki Wrap Method bilan qo'shib ko'ring va diffni taqqoslang.
- [ ] Konstruktorni o'zgartirishdan oldin oraliq qadamni sinab ko'ring: metod ichidagi bitta `new` ni `protected` fabrika metodiga chiqarib, testda subclass bilan override qiling; chaqiruvchilar tegilmaganini diffda ko'rsating.
- [ ] Modulda testda almashtirib bo'lmaydigan statik chaqiruv yoki `getInstance()` ni toping va biriga delegat instance metod yoki test uchun statik setter qo'yib, object seam hosil qiling.
- [ ] Tegilayotgan metod uchun ta'sirning uch yo'lini yozib chiqing (qaytish qiymati, uzatilgan obyekt, statik holat) va shu ro'yxatdan test nuqtalarini tanlang.
- [ ] Har bir pinch point (qoplama) testiga uni o'chirish sharti yozilsin: qaysi sinflar uchun tor test paydo bo'lgach u o'chiriladi.
- [ ] Bitta hisoblash mantiqi uchun parallel run yoqing: yangi kod natijasi log va metrikaga chiqsin, javob eski koddan qaytsin.
- [ ] Har bir feature flag uchun egasi va o'chirish muddatini yozib qo'ying, muddati o'tgan flag'lar ro'yxati sprint ko'rikida ko'rilsin.
- [ ] Bazani ajratishdan oldin Newman'ning ikki shartini yozib javob bering: monolitni o'zgartirish mumkinmi, ishlash va izchillikdan xavotir bormi. Javobga qarab avval sxemani yoki avval kodni ajratishni tanlang.
- [ ] `REVOKE` va `GRANT` orqali tanlangan jadvalga yozish huquqini faqat bitta modulga qoldiring, qoidani kodga emas bazaga tayantiring.
- [ ] Ikki tomonga yozish bor joyda reconciliation so'rovini yozib qo'ying va farq sonini metrikaga chiqaring.
- [ ] Checkpoint tartibini kelishib oling: maqsadni qayta aytish, kvantitativ o'lchov, jamoadan kvalitativ fikr, keyin qarorni o'zgartirish yoki saqlash.
- [ ] Tegmaslik qaroriga ham shakl bering: "muzlatilgan" modullar ro'yxati va to'rt mezon bo'yicha ularning holati yozilsin.

## Manbalar

- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), Preface (xvi-bet) - legacy kod ta'rifi: testlari yo'q kod, va kod qanchalik yaxshi yozilgani bu ta'rifni o'zgartirmaydi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 2-bob (18-19-bet) - legacy kodga o'zgarish kiritish algoritmining besh qadami va kod o'zgarishi oxirgi qadamda turishi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 4-bob (31-bet) - seam ta'rifi: xatti-harakatni o'sha joyni tahrirlamasdan o'zgartirish mumkin bo'lgan nuqta
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 4-bob (36-bet) - enabling point ta'rifi: har bir seam uchun bir xatti-harakatni tanlash qarori qabul qilinadigan joy
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 4-bob (33, 36 va 40-bet) - seam taksonomiyasi: preprocessing seam, link seam, object seam; preprocessing seam faqat C va C++ da
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 6-bob (59, 63, 67 va 71-bet) - Sprout Method, Sprout Class, Wrap Method va Wrap Class; Wrap Class Decorator patterniga bog'lanadi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 11-bob (155-bet) va 16-bob (210, 212 va 213-bet) - effect sketch, Notes/Sketching, Scratch Refactoring, Delete Unused Code
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 12-bob (174 va 182-bet) - interception point va pinch point: pinch point tabiiy inkapsulyatsiya chegarasi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 13-bob (186-bet) - characterization test ta'rifi va uni yozishning besh qadamli algoritmi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 17-bob (216-bet) - tizim haqida hikoya aytib berish usuli
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (362-bet) - Extract Interface eng xavfsiz bog'liqlik uzish usullaridan biri: xato bo'lsa kompilyator aytadi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 1-bob (3, 4, 5, 6 va 8-bet) - o'zgarishning to'rt sababi, tuzilish, funksionallik va resurs sarfi jadvali, metod chaqirilmaguncha xatti-harakat o'zgarmasligi, va Risky Change ning uch savoli
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 2-bob (9, 14, 17 va 18-bet) - Edit and Pray va Cover and Modify, yuqori darajali testning qoplama sifatidagi o'rni, Primitivize Parameter va Extract Interface ni test yo'q joyda bajarish, va kesish izi metaforasi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 4-bob (29-31-bet) - programmani matn varag'i deb ko'rish va shu qarashdan seam modeliga o'tish sababi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 9-bob (122-bet) - singleton uchun resetForTesting alternativasi va u yetmaydigan shart
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 11-bob (164, 165, 166-167 va 167-168-bet) - ta'sir tarqalishining uch yo'li, olti qadamli izlash evristikasi, private va package ko'rinish farqi, va ta'sir tahlilidan chiqadigan kod bazasi qoidalari
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 12-bob (184-bet) - pinch point testining ikki tuzog'i va testlarni sinf darajasiga tushirib pinch point testini o'chirish
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 15-bob (205, 206 va 207-bet) - Skin and Wrap the API va Responsibility-Based Extraction, ular orasidagi tanlov sharti va narxi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 16-bob (211-212-bet) - listing markup: mas'uliyatni guruhlash, blokni tutashtirish, ajratish nomzodini belgilash va ta'sirni belgilab borish
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 17-bob (220-223-bet) - Naked CRC va uning ikki qoidasi: kartochka nusxani bildiradi, ustma-ust kartochka to'plamni bildiradi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (326-329-bet) - Adapt Parameter: tashqi API interface'i o'rniga o'z tor interface'i, uning xavfi va Preserve Signatures buzilishi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (348-349, 350-351 va 352-355-bet) - Extract and Override Call, Extract and Override Factory Method va Extract and Override Getter, ularning qo'llanish shartlari va C++ chegarasi
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (356-359-bet) - Extract Implementer: sinf nomini interface sifatida qoldirib implementatsiyani pastga tushirish, Production prefiksi va qadamlar
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (369-371-bet) - Introduce Instance Delegator: static cling, delegat instance metod va statik metodlarni keyinroq o'chirish
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (372 va 376-bet) - Introduce Static Setter: singletonning uch xossasi, statik setter va protected konstruktor, eski nusxani yo'q qilish va globalni parametr uzatish bilan yo'qotish
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 2-bob - refaktoring kuzatiladigan xatti-harakatni o'zgartirmaydi, va Kent Beck ning ikki shlyapa metaforasi
- Martin Fowler, *Refactoring*, 2-nashr, Addison-Wesley, 2019, mundarija - "Defining Refactoring" 45-bet va "The Two Hats" 46-bet: ikki tushuncha 2-nashrda ham 2-bobda turadi
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 2-bob (33-bet) - microservice maqsad emas, o'tish ongli va asosli qaror bo'lishi kerak
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 2-bob (42-45-bet) - microservice yomon g'oya bo'lgan holatlar, shu qatorda noaniq domen va "yaxshi sabab yo'q"
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 2-bob (43-bet) - SnapCI misoli: chegara noto'g'ri chizilgach servislar qaytib bitta ilovaga qo'shilgani
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 2-bob (47-52-bet) - John Kotter ning sakkiz qadamli modeli, shoshilinchlik hissi (48-bet) va qisqa muddatli g'alabalar (51-bet)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 2-bob (53-bet) - Fowler ning big bang qayta yozish haqidagi gapi va bosqichma-bosqich ko'chish majburiyati
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 2-bob (56-61-bet) - xatoni ta'siri eng past joyda qilish va doskada use-case yurgizish (aylanma havola va juda gaplashuvchi servis savollari); domen modeli bo'yicha ustuvorlash, xabarnoma va hisob-faktura misoli; modelning mantiqiy ko'rinish ekani va kodga hamda ma'lumot saqlashga baribir qarash kerakligi; ikki o'qli kvadrant (x qiymat, y qiyinlik), yuqori o'ngdagi bir-ikki servisni birinchi tanlash va o'rganilgach ustuvorlikni qayta ko'rish; oson lekin o'zgarmaydigan funksionallik maqsadga xizmat qilmasligi
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 2-bob (71-73-bet) - o'lchov maqsaddan chiqadi, metrikani o'ynash mumkin, cycle time boshida yomonlashishi, kvalitativ fikr, checkpoint va sunk cost tuzog'i
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 3-bob (79-82-bet) - strangler fig: uch qadam, qayta yo'naltirishgacha tirik emasligi, to'xtatish imkoni va pattern ishlamaydigan holat
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 3-bob (104-105 va 112-bet) - branch by abstraction ning besh qadami va uning uzoq yashaydigan branch dan afzalligi
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 3-bob (113 va 117-bet) - parallel run: ikki implementatsiya ham chaqiriladi, bittasi haqiqat manbasi; narxi va GitHub Scientist
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 3-bob (118-bet) - canary release ning parallel run dan farqi va progressive delivery guruhi
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 4-bob (169-170-bet) - kod va bazani bitta qadamda birga ajratmaslik, va tartibning SHARTLI tanlovi: monolit o'zgartirilsa va ishlash yoki izchillik muhim bo'lsa avval sxema, aks holda avval kod
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 4-bob (128, 141, 145, 149 va 171-bet) - database view, change data ownership, synchronize data in application, tracer write, split table patternlari
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2020, 4-bob (153-bet) - nomuvofiqlik oynasi sinxronizatsiya mexanizmiga bog'liq va reconciliation jarayoni shart
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 2-bob - arxitektura muhim lekin shoshilinch emas, uni himoya qilish ishlab chiqish jamoasining javobgarligi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 2-bob, "Eisenhower's Matrix" - to'rt kvadrant, ularning tartibi va uchinchi toifani birinchi toifaga ko'tarish xatosi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 24-bob - qisman chegara: "Skip the Last Step", bir o'lchovli chegara va uning o'z-o'zidan buzilish xavfi
- ESLATMA: 34.1 va 34.2 dagi `actuator`, `git log` va `pg_stat_*` o'lchov buyruqlari shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 34.7 dagi canary bosqichlarining aniq ulushi, muddati va gateway konfiguratsiyasi shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 34.8 dagi `REVOKE`/`GRANT` ketma-ketligi va migratsiya tuzoqlari jadvalining PostgreSQL tafsilotlari shu korpusning amaliy tavsiyasi
- ESLATMA: 34.11 dagi "muzlatilgan modul" to'rt mezoni va 34.12 dagi bosqich ro'yxati shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 34.15 dagi qoplama testni kodda vaqtincha deb belgilash tavsiyasi shu korpusning qo'shimchasi
- ESLATMA: 34.16 dagi Spring shartlari (fabrika metodi private yoki final bo'lmasligi, override qiluvchi subclass faqat test manbasida turishi, keyin konstruktor injection ga o'tish) shu korpusning qo'shimchasi
- ESLATMA: 34.18 dagi Extract Implementer va `@Component` ning yangi production sinfiga ko'chishi haqidagi kuzatish shu korpusning qo'shimchasi
- ESLATMA: 34.2 dagi listingni fayl nusxasida belgilash moslashtirishi shu korpusning qo'shimchasi
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 3.7 - evolyutsion dizaynning refaktoring, test-driven dizayn va continuous integration bilan juftlashishi, refaktoringning arxitektura miqyosidagi o'zgarishga kam yo'l-yo'riq berishi (Amazon misoli) va legacy kodda test yetishmasligi
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 16.1.1 - mavjud kodning arxitektura abstraksiyalariga mos kelmasligi, uni modul va komponentlarga refaktoring qilish qimmatligi, tizimni yirik modul yoki komponentlar to'plami deb qarash va ichki quyi komponentlarini modellashtirmaslik
- Sam Newman, *Monolith to Microservices*, 1-nashr, O'Reilly, 2020, 2-bob (37-bet) - g'oyadan production gacha yo'lni modellash, bosqich davomiyligini o'lchash va investitsiya bankidagi olti hafta hamda 40 haftadan oshiq misoli; (42-bet) - qayta foydalanish maqsad emas vosita ekani va PDF generatsiyasi misolida muvofiqlashish narxi
- Sam Newman, *Monolith to Microservices*, 1-nashr, O'Reilly, 2020, 2-bob (53-bet) - servis ajratish production da ishlatilmaguncha tugallanmagan hisoblanishi va tracing, latency, referential integrity hamda cascading failure darslarining faqat production da ko'rinishi
- Sam Newman, *Monolith to Microservices*, 1-nashr, O'Reilly, 2020, 3-bob (99-bet) - The Guardian misolida birinchi ko'chiriladigan bo'lak saytning eng ko'zga ko'rinadigan qismi bo'lmasligi va Travel vertikalida bitta vidjetdan boshlash
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 6-bob (155-161-betlar) - monolit bazani ajratishning besh qadami (data domain larni aniqlash, jadvallarni sxemaga biriktirish va synonym, ulanishni o'z sxemasiga qoldirish, sxemalarni alohida serverga ko'chirish, o'tish), ma'lumot suvereniteti kelishuvi (mustaqil sxema o'zgarishi va mos baza turi tanlash foydasi; katta hajm, referential integrity yo'qolishi va baza kodini servis qatlamiga ko'chirish narxi) hamda sxemani ko'chirishda backup-restore va replikatsiya tanlovi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 15-bob ("Why Deprecate?", "Why Is Deprecation So Hard?", "Deprecation During Design", "Process Owners", "Preventing Backsliding" bo'limlari) - kod majburiyat ekani, faqat yoshi uchun deprecate qilinmasligi va teng funksiyali almashtiruvchi sharti, Hyrum qonuni va emotsional qarshilik, deprecation jarayonining aniq egasi bo'lishi (advisory deprecation tugamasligi), dizayn paytida deprecation savollari, hamda orqaga qaytishni statik tahlil annotatsiyasi va build dagi ko'rinish ro'yxati bilan to'sish
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 22-bob ("Who Deals with LSCs?" bo'limi) - ko'chish ishini eski tizim egasi bajarishi, moliyalashtirilmagan mandat muammosi va organik ko'chishning tugamasligi (yangi kod mavjud kodni namuna qilib yoziladi)
- ESLATMA: 34.1 dagi `legacy-core` ni qora quti deb belgilash misoli, 34.20 dagi PostgreSQL sintaksisi eslatmasi va `orders.customer_id` misoli, 34.21 dagi `@Deprecated` hamda ArchUnit kod misollari shu korpusning qo'shimchasi
- ESLATMA: 34.19 dagi nazorat ro'yxati shu korpusning o'z checklisti

---

[&larr; 33. Sxema migratsiyasi va to'xtashsiz reliz](33-sxema-migratsiyasi-va-toxtashsiz-reliz.md) · [Mundarija](README.md) · [35. Incident, on-call va post-mortem &rarr;](35-incident-on-call-va-post-mortem.md)
