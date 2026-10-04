<!-- doc: code-review | chapter: 3 | part: I. Review ning mohiyati va iqtisodi -->

[Kod review](../../README.md) / [Kod review](README.md)

# 3. Reviewer ning tahlil apparati: niyat, invariant, xavf yuzasi (The Reviewer's Analytical Apparatus)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [3.1 Review ning uch o'qishi](#31-review-ning-uch-oqishi)
- [3.2 Niyatni koddan tiklash, tavsifdan emas](#32-niyatni-koddan-tiklash-tavsifdan-emas)
- [3.3 Invariantni topish: nima har doim rost bo'lishi kerak](#33-invariantni-topish-nima-har-doim-rost-bolishi-kerak)
- [3.4 Xavf yuzasi: o'zgarish nimaga tegadi](#34-xavf-yuzasi-ozgarish-nimaga-tegadi)
- [3.5 Ko'rinmayotgan kodni ko'rish](#35-korinmayotgan-kodni-korish)
- [3.6 Miyada ishga tushirish: beshta ssenariy](#36-miyada-ishga-tushirish-beshta-ssenariy)
- [3.7 Chuqurlik darajasi: xavf bo'yicha triage](#37-chuqurlik-darajasi-xavf-boyicha-triage)
- [3.8 Kognitiv tuzoqlar](#38-kognitiv-tuzoqlar)
- [3.9 Review ni qachon to'xtatish](#39-review-ni-qachon-toxtatish)
- [3.10 Review natijasini yozib qoldirish](#310-review-natijasini-yozib-qoldirish)
- [3.11 Amalda qo'llash](#311-amalda-qollash)

</details>


Yaxshi reviewer diffni o'qimaydi, u diffni tahlil qiladi. Farq shunda: o'qish satrlarni ko'radi, tahlil esa kodning ortidagi uchta narsani tiklaydi - muallif nimani nazarda tutgan, kod qanday qoidani buzmasligi kerak va bu o'zgarish nimaga tegib ketadi. Shu uchlik topilmasa, qolgan hamma izoh didga aylanadi. Bu bob shu apparatni beradi, keyingi boblar esa uni Java, Spring va PostgreSQL ga qo'llaydi.

## 3.1 Review ning uch o'qishi

Bitta diffni uch marta o'qish kerak, har safar boshqa savol bilan. Uchini birlashtirgan reviewer ikkinchi faylda chalg'iydi va uchinchi faylda faqat nomlash haqida yozadi.

Birinchi o'qish - niyat. Bu o'zgarish qanday muammoni yechadi, va shu muammo shu joyda yechilishi kerakmi. Satrlarga qaramaydi, fayllar ro'yxati va umumiy shaklga qaraydi. Odatda 5 daqiqa.

Ikkinchi o'qish - mexanika. Kod aytganini qiladimi: null yo'llari, chegaraviy qiymatlar, tur konversiyasi, tranzaksiya chegarasi, poyga holati, resurs yopilishi. Bu eng uzun qism.

Uchinchi o'qish - xavf. Bu kod prodda birinchi marta ishga tushganda nima bo'ladi: eski ma'lumot bilan, ikki instansda, yuk ostida, tashqi servis javob bermaganda, migratsiya yarim qolganda.

| O'qish | Savol | Nimaga qaraydi | Vaqt ulushi |
| --- | --- | --- | --- |
| 1. Niyat | Nima uchun va nega shu yerda | PR tavsifi, fayllar ro'yxati, public API | 15% |
| 2. Mexanika | Kod aytganini qiladimi | Satrlar, shartlar, turlar, chegaralar | 55% |
| 3. Xavf | Prodda nima bo'ladi | Migratsiya, konfiguratsiya, yuk, nosozlik | 30% |

## 3.2 Niyatni koddan tiklash, tavsifdan emas

PR tavsifi muallifning o'zi haqida aytgan gapi. Kod esa haqiqat. Tajribali reviewer avval tavsifni o'qiydi, keyin uni unutib, koddan niyatni mustaqil tiklaydi va ikkisini taqqoslaydi. Farq chiqsa - bu eng qimmatli topilma.

Uch xil farq uchraydi. Birinchi: tavsifda aytilgan, kodda yo'q (masalan "idempotentlik qo'shildi" deyilgan, lekin kalit bo'yicha unique constraint yo'q). Ikkinchi: kodda bor, tavsifda yo'q (yo'l-yo'lakay o'zgartirilgan timeout, olib tashlangan tekshiruv). Ikkinchisi xavfliroq, chunki uni hech kim kutmagan. Uchinchi: ikkisi ham bor, lekin kod boshqa narsani qiladi.

```java
// PR tavsifi: "Buyurtma bekor qilishni qo'shdim".
// Koddan tiklangan niyat: buyurtma statusini CANCELLED ga o'tkazish.
// Farq: tavsifda pul qaytarish haqida bir og'iz gap yo'q, kodda esa bor.
@Transactional
public void cancel(long orderId, String reason) {
    Order order = orders.findById(orderId).orElseThrow();
    order.setStatus(CANCELLED);
    order.setCancelReason(reason);
    // Bu satr tavsifda yo'q edi. Reviewer uchun bu asosiy savol:
    // to'lov qaytarish shu tranzaksiya ichida sinxron chaqirilyaptimi?
    paymentClient.refund(order.getPaymentId(), order.getTotal());
    orders.save(order);
}
// Review izohi (blocker): tashqi to'lov chaqiruvi DB tranzaksiyasi ichida.
// refund 30 sekund javob bermasa, DB ulanishi va qulf shu vaqt egallanadi.
// Bundan tashqari refund o'tib, keyin commit yiqilsa, pul qaytgan, status
// hali ACTIVE bo'lib qoladi. Outbox yoki ikki qadamli holat kerak.
```

## 3.3 Invariantni topish: nima har doim rost bo'lishi kerak

Invariant - tizim holati haqida har doim rost bo'lishi kerak bo'lgan gap. "Buyurtma summasi qatorlar summasiga teng", "hisobdagi qoldiq manfiy bo'lmaydi", "bitta idempotentlik kaliti bitta to'lovga tegishli", "yetkazilgan buyurtma bekor qilinmaydi". Xatolarning katta qismi - buzilgan invariant.

Reviewer ning ishi: diffdan ta'sirlangan invariantlar ro'yxatini tuzish va har biri uchun himoya qayerda ekanini topish. Himoya uch joyda bo'lishi mumkin - domen obyekti ichida, ma'lumotlar bazasi constraint ida, yoki hech qayerda. Uchinchi javob eng ko'p uchraydi.

| Invariant | Eng ishonchli himoya | Yetarsiz himoya |
| --- | --- | --- |
| Qoldiq manfiy emas | DB `CHECK (balance >= 0)` + domen tekshiruvi | Faqat servisdagi `if` |
| Kalit yagona | DB `UNIQUE` indeks | `findBy` keyin `save` (poyga) |
| Status o'tishi qoidali | Domen ichida state machine | Controller dagi `switch` |
| Summalar mosligi | Agregat ichida hisoblash | Alohida `update` so'rovlari |
| Sana oralig'i to'g'ri | DB `CHECK (ends_at > starts_at)` | Faqat frontend validation |

Shu jadvalning asosiy xabari: ikki instansda ishlaydigan ilovada faqat Java kodidagi `if` invariantni himoya qilmaydi. Tekshiruv va yozuv orasida boshqa instans o'zgartirishi mumkin. Shu sababli har bir invariant uchun review savoli bitta: "ikki parallel so'rov bu tekshiruvni chetlab o'ta oladimi".

## 3.4 Xavf yuzasi: o'zgarish nimaga tegadi

Diff o'zgargan satrlarni ko'rsatadi, lekin xavf o'zgarmagan kodda yashaydi. Xavf yuzasi - shu o'zgarish ta'sir qiladigan hamma narsa: chaqiruvchilar, bir xil jadvalga yozadigan boshqa kod, kesh, tashqi mijozlar, batch ishlar, hisobotlar.

```bash
# Xavf yuzasini git bilan o'lchash. Diffda yo'q, lekin ta'sirlangan joylar.
BASE=origin/main

# 1) O'zgargan public metodlarning chaqiruvchilarini topish.
git diff -U0 $BASE...HEAD -- '*.java' \
  | grep -oE '^\+.*(public|protected) [A-Za-z<>,\[\] ]+ ([a-z][A-Za-z0-9]*)\(' \
  | grep -oE '[a-z][A-Za-z0-9]*\($' | tr -d '(' | sort -u \
  | while read -r m; do
      n=$(grep -rln --include='*.java' "\.$m(" src/main/java | wc -l)
      printf '%-35s %s ta faylda chaqiriladi\n' "$m" "$n"
    done

# 2) O'zgargan jadvalga yozadigan boshqa joylarni topish.
git diff $BASE...HEAD -- 'src/main/resources/db/**' \
  | grep -ioE '(alter|create) table ([a-z_]+)' | awk '{print $3}' | sort -u \
  | while read -r t; do
      echo "--- $t jadvaliga tegadigan kod:"
      grep -rln --include='*.java' --include='*.sql' -i "$t" src/main | head
    done

# 3) Shu fayllar bilan tarixda birga o'zgargan fayllar (yashirin bog'liqlik).
for f in $(git diff --name-only $BASE...HEAD -- '*.java'); do
  git log --format='%H' -20 -- "$f" \
    | xargs -I{} git show --name-only --format= {} 2>/dev/null
done | sort | uniq -c | sort -rn | head -15
```

Uchinchi buyruq eng foydali: tarixda shu fayl bilan birga o'zgargan fayllar - yashirin bog'liqlik xaritasi. Agar `OrderService.java` tarixda 20 marta `InvoiceMapper.java` bilan birga o'zgargan bo'lsa, lekin bu PR da `InvoiceMapper` tegilmagan bo'lsa, bu savol: nega bu safar kerak bo'lmadi.

## 3.5 Ko'rinmayotgan kodni ko'rish

Eng qimmat xatolar diffda bor narsada emas, yo'q narsada yashaydi. Diff yo'q narsani ko'rsatmaydi, shu sababli reviewer uni ro'yxat bo'yicha so'raydi.

| Yo'q bo'lishi mumkin bo'lgan narsa | Savol | Oqibati |
| --- | --- | --- |
| Validation | Tashqi kirish qayerda tekshirilgan | Buzilgan ma'lumot bazaga tushadi |
| Avtorizatsiya | Bu endpointni kim chaqira oladi | Boshqa foydalanuvchi ma'lumotiga kirish |
| Timeout | Tashqi chaqiruvda chegara bormi | Thread va pool to'lib qoladi |
| Index | Yangi `WHERE` ustuni indekslanganmi | Seq scan, sekin so'rov |
| Test | Chegaraviy holat qamralganmi | Regressiya keyingi PR da chiqadi |
| Log va metrika | Xato bo'lsa, qanday bilamiz | Ko'r incident |
| Migratsiyaning orqaga yo'li | Qaytarish rejasi bormi | Reliz qaytarilmaydi |
| Idempotentlik | Ikki marta kelsa nima bo'ladi | Ikki marta to'lov, dublikat qator |
| Null holati | Bu maydon bo'sh kelsa | NPE yoki jim noto'g'ri hisob |
| Bo'sh to'plam holati | Ro'yxat bo'sh bo'lsa | `get(0)`, noto'g'ri o'rtacha, 0 ga bo'lish |

Bu jadval review ning asosiy quroli. Har bir PR uchun o'ninchi qatorga tushmasdan kamida birinchi oltitasini o'tish kerak.

## 3.6 Miyada ishga tushirish: beshta ssenariy

Tajribali reviewer kodni o'qiyotganida uni ishga tushiradi. Beshta ssenariy har doim qo'llaniladi va ularning har biri boshqa sinf xatoni ochadi.

Birinchi: happy path. Hamma narsa yaxshi ishlagan holat. Muallif odatda shuni test qilgan.

Ikkinchi: bo'sh va chegaraviy kirish. Null, bo'sh satr, bo'sh ro'yxat, nol, manfiy son, juda uzun satr, `Integer.MAX_VALUE`, kelasi sanadagi vaqt.

Uchinchi: ikki marta. Bir xil so'rov ikki marta keldi (foydalanuvchi ikki marta bosdi, retry ishladi, Kafka xabarni qayta yetkazdi).

To'rtinchi: ikki parallel. Ikki so'rov bir vaqtda, ikki instansda. Tekshiruv va yozuv orasida nima o'zgarishi mumkin.

Beshinchi: o'rtada yiqilish. Kod yarmida protsess o'ldi, yoki tashqi chaqiruv timeout bo'ldi, yoki commit yiqildi. Qaysi holat qoladi.

```java
// Shu beshta ssenariyni qo'llash uchun misol. Kod bir qarashda to'g'ri.
@Transactional
public Reservation reserve(long eventId, int seats, String idemKey) {
    Event event = events.findById(eventId).orElseThrow();
    if (event.getAvailable() < seats) {                 // (1)
        throw new NotEnoughSeatsException();
    }
    event.setAvailable(event.getAvailable() - seats);   // (2)
    return reservations.save(new Reservation(eventId, seats, idemKey));
}
// 1-ssenariy: ishlaydi.
// 2-ssenariy: seats = 0 yoki manfiy bo'lsa? Tekshiruv yo'q. Manfiy seats
//             bilan available oshib ketadi - joy "yaratiladi".
// 3-ssenariy: idemKey bo'yicha UNIQUE yo'q. Ikki marta kelsa - ikki bron.
// 4-ssenariy: (1) va (2) orasida boshqa instans ham o'qidi. Ikkisi ham
//             o'tadi, available manfiyga tushadi. Optimistik versiya yoki
//             atomik UPDATE kerak.
// 5-ssenariy: save o'tib, commit yiqilsa - butun tranzaksiya qaytadi, bu
//             to'g'ri. Lekin bu yerda tashqi chaqiruv bo'lsa, bo'lmaydi.
```

Shu beshlikdan ikkinchi, uchinchi va to'rtinchisi - review ning eng ko'p qaytim beradigan qismi, chunki ularni testlar odatda qamramaydi va statik tahlil ko'rmaydi.

## 3.7 Chuqurlik darajasi: xavf bo'yicha triage

Hamma PR ni bir xil chuqurlikda o'qish - resursni noto'g'ri sarflash. Reviewer birinchi 2 daqiqada chuqurlik darajasini tanlashi kerak va buni ongli qilishi lozim.

| Daraja | Qachon | Nima qilinadi | Vaqt |
| --- | --- | --- | --- |
| Skim | Docs, log matni, test qo'shish, lokalizatsiya | Niyat va shakl | 5 daqiqa |
| Normal | Ichki mantiq, yangi endpoint, refactoring | Uch o'qish, chegaraviy holatlar | 20-40 daqiqa |
| Deep | Migratsiya, pul, auth, concurrency, tashqi API | Uch o'qish + 5 ssenariy + checklist | 1-2 soat |
| Audit | Ma'lumot ko'chirish, kriptografiya, ko'p modulga tegadigan refactoring | Deep + lokal ishga tushirish + qaytish rejasi | Yarim kun |

Chuqurlikni tanlash mezoni - "xato bo'lsa, qaytarish qancha turadi" degan savol. Qaytarish arzon bo'lsa (kod o'zgarishi, qayta deploy), Normal yetadi. Qaytarish qimmat bo'lsa (ma'lumot o'zgargan, tashqi mijoz moslashgan, pul ko'chgan), Deep yoki Audit.

## 3.8 Kognitiv tuzoqlar

Reviewer ham odam, va uning diqqati bir necha tanish tarzda aldanadi.

Birinchi tuzoq - birinchi taassurot (anchoring). Diffning boshida ko'rilgan uslub xatosi diqqatni uslubga qulflaydi va keyingi fayldagi tranzaksiya xatosi ko'rinmaydi. Qarshi chora: birinchi o'qishda hech qanday izoh yozmaslik.

Ikkinchi tuzoq - muallif obro'si (authority bias). Senior yozgan kodni yuzaki o'qish va junior kodini satr-satr tekshirish. Amalda senior ham xuddi shunday xato qiladi, lekin uning xatosi ko'proq joyga tarqaydi. Qarshi chora: muallif ismini ko'rmasdan o'qishga urinish, yoki checklistni har ikki holatda bir xil qo'llash.

Uchinchi tuzoq - charchoq. Birinchi fayl batafsil, oltinchi fayl "LGTM". Qarshi chora: katta PR ni ikki o'tirishga bo'lish, yoki eng xavfli fayldan boshlash.

To'rtinchi tuzoq - tanishlik (mere exposure). Kod uslubi o'ziga tanish bo'lsa, u to'g'ri ko'rinadi. Shu sababli "men shunday yozmagan bo'lardim" degan hissiyot izohga aylanmasligi kerak, agar ortida aniq sabab bo'lmasa.

Beshinchi tuzoq - tugatish istagi (sunk cost). Muallif ikki hafta ishlagan PR ni rad qilish qiyin. Lekin yondashuv noto'g'ri bo'lsa, ikki hafta allaqachon ketgan va uni "saqlash" uchun yana ikki oy to'lash mantiqsiz.

## 3.9 Review ni qachon to'xtatish

Review tugadi deb hisoblash uchun uchta shart bor: uch o'qish bajarildi, ko'rinmayotgan kod ro'yxati o'tildi, va qolgan savollar yozib qoldirildi. To'rtinchi shart yo'q - mukammallik shart emas.

Review ni to'xtatish kerak bo'lgan ikki holat alohida. Birinchi: diff juda katta yoki tuzilmagan - bu holda satrlarni o'qishni boshlamasdan, "bo'lib yuborish" deb javob berish to'g'ri va halol. Ikkinchi: PR da asosiy dizayn savoli ochiq - detallarga izoh yozish ma'nosiz, chunki yondashuv o'zgarsa, kod ham o'zgaradi. Bu holda bitta savol yozib, javobni kutish kerak.

```text
# Dizayn savoli ochiq bo'lganda review javobi: detallarga tushmaslik.

Hozircha satrlarga izoh yozmadim, chunki bitta asosiy savol bor.

Bu yerda refund DB tranzaksiyasi ichida sinxron chaqirilgan. Shu qaror
o'zgarsa (outbox yoki ikki qadamli holat), quyidagi 4 fayl ham o'zgaradi,
shuning uchun avval shuni kelishib olsak foydali.

Variantlar:
1) Outbox: status o'zgaradi + outbox qatori, worker refund chaqiradi.
   Narxi: bir jadval va worker. Foyda: tranzaksiya qisqa, retry bepul.
2) Sinxron qoldirish + qisqa timeout + idempotentlik kaliti.
   Narxi: tranzaksiya tashqi servisga bog'liq qoladi.

Men 1-variantni taklif qilaman. Qaysi birini tanlasak, keyin satr-satr
o'qib chiqaman.
```

## 3.10 Review natijasini yozib qoldirish

Review ning chiqishi - izohlar emas, xulosa. Xulosa to'rt qismdan iborat: nimani tekshirdim, nimani tekshirmadim, bloklaydigan narsalar, va qolgan xavf. Bu to'rtlik keyingi incidentda juda qimmat bo'ladi, chunki u o'sha paytda nima bilinganini ko'rsatadi.

Xulosa yozishning yon foydasi ham bor: u reviewer ni o'z ishini baholashga majbur qiladi. "Tekshirmadim" ro'yxati bo'sh bo'lsa, demak reviewer o'ziga haddan ortiq ishongan.

## 3.11 Amalda qo'llash

- [ ] Keyingi review da uch o'qishni ongli ajratib bajaring va birinchi o'qishda hech qanday izoh yozmang.
- [ ] Har bir PR uchun ta'sirlangan invariantlar ro'yxatini yozing va har biri uchun himoya qayerda ekanini (domen, DB constraint, hech qayerda) belgilang.
- [ ] Faqat Java kodidagi `if` bilan himoyalangan invariantlarni toping va ularga DB darajasidagi `UNIQUE` yoki `CHECK` qo'shishni talab qiling.
- [ ] Xavf yuzasini o'lchaydigan git skriptini repoga `scripts/review-impact.sh` sifatida qo'shing.
- [ ] Ko'rinmayotgan kod jadvalini (10 band) PR shabloniga reviewer uchun ro'yxat sifatida qo'shing.
- [ ] Beshta ssenariyni (happy, chegara, ikki marta, ikki parallel, o'rtada yiqilish) oxirgi uchta PR ga qo'llab, nechta yangi savol chiqqanini sanang.
- [ ] Chuqurlik darajalari jadvalini `REVIEW.md` ga kiritib, har PR da darajani izohda ko'rsatishni odat qiling.
- [ ] Review xulosasi shablonini (tekshirdim / tekshirmadim / blocker / qolgan xavf) joriy qiling.

---

[&larr; 2. Review iqtisodi: xato narxi, navbat va PR hajmi](02-review-iqtisodi-xato-narxi-navbat-va-pr.md) · [Mundarija](README.md) · [4. Diffni o'qish mexanikasi &rarr;](04-diffni-oqish-mexanikasi.md)
