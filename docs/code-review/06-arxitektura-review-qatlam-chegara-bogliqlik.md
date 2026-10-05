<!-- doc: code-review | chapter: 6 | part: II. Arxitektura, dizayn va clean code review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 6. Arxitektura review: qatlam, chegara, bog'liqlik yo'nalishi (Architecture in a Diff)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [6.1 Importlar - arxitekturaning eng aniq ko'rsatkichi](#61-importlar---arxitekturaning-eng-aniq-korsatkichi)
- [6.2 Bog'liqlik yo'nalishi: ichki qatlam tashqarini bilmaydi](#62-bogliqlik-yonalishi-ichki-qatlam-tashqarini-bilmaydi)
- [6.3 Yangi paket va yangi modul - chegara haqida qaror](#63-yangi-paket-va-yangi-modul---chegara-haqida-qaror)
- [6.4 Yangi tashqi bog'liqlik - eng kam baholangan arxitektura qarori](#64-yangi-tashqi-bogliqlik---eng-kam-baholangan-arxitektura-qarori)
- [6.5 Arxitektura eroziyasini diffdan ko'rish](#65-arxitektura-eroziyasini-diffdan-korish)
- [6.6 Qatlam o'tkazib yuborilishi (layer skipping)](#66-qatlam-otkazib-yuborilishi-layer-skipping)
- [6.7 Chegaradan o'tadigan ma'lumot shakli](#67-chegaradan-otadigan-malumot-shakli)
- [6.8 Hisob mantiqi qayerda turadi](#68-hisob-mantiqi-qayerda-turadi)
- [6.9 Modullar orasidagi muloqot shakli](#69-modullar-orasidagi-muloqot-shakli)
- [6.10 Arxitektura izohini qanday yozish](#610-arxitektura-izohini-qanday-yozish)
- [6.11 Amalda qo'llash](#611-amalda-qollash)

</details>


Arxitektura PR da bitta diagramma sifatida ko'rinmaydi. U mayda belgilar orqali ko'rinadi: yangi import, yangi konstruktor parametri, yangi paket, bir qatlamdan boshqasiga o'tgan chaqiruv. Arxitektura buzilishi hech qachon bitta PR da sodir bo'lmaydi - u yuzta PR da bittadan satr bilan sodir bo'ladi. Shu sababli arxitektura review ning asosiy quroli - yo'nalishni kuzatish. Arxitektura qarorlarining o'zi (chegarani qayerdan o'tkazish, monolit yoki servis) [Arxitektor miyasi](../architect/README.md) da, bu yerda faqat diffdan o'qish.

## 6.1 Importlar - arxitekturaning eng aniq ko'rsatkichi

Fayl boshidagi importlar ro'yxati shu klassning tizimdagi o'rnini aytadi. Domen klassida `org.springframework.web` importi bo'lsa, qatlam buzilgan. Repository da `javax.servlet` bo'lsa, so'rov konteksti ma'lumot qatlamiga tushgan. Entity da `com.fasterxml.jackson` bo'lsa, tashqi shakl ma'lumot modeliga yopishgan.

```bash
# Diffda yangi qo'shilgan importlarni ko'rish: arxitektura review ning
# eng tez va eng foydali qadami.
git diff origin/main...HEAD -- '*.java' \
  | grep -E '^\+import' | sort | uniq -c | sort -rn

# Qatlam buzilishini qidirish.
git diff origin/main...HEAD -- 'src/main/java/**/domain/**' \
  | grep -E '^\+import (org\.springframework|jakarta\.persistence|com\.fasterxml)'

# Teskari yo'nalish: ichki qatlam tashqarini bilib qolgan.
grep -rn --include='*.java' 'import .*\.web\.' src/main/java/**/domain/ 2>/dev/null
```

| Diffda ko'rilgan import | Qayerda | Nimani bildiradi |
| --- | --- | --- |
| `org.springframework.web.*` | domain | Qatlam buzilgan, domen HTTP ni biladi |
| `jakarta.persistence.*` | domain | Domen ORM ga yopishgan (agar toza domen tanlangan bo'lsa) |
| `com.fasterxml.jackson.*` | entity | Tashqi JSON shakli jadval modeliga bog'langan |
| `...repository.*` | web/controller | Servis qatlami chetlab o'tilgan |
| Boshqa modulning `internal` paketi | har qanday joy | Modul chegarasi teshilgan |
| `java.sql.*` | service | Ma'lumot qatlami oqib chiqqan |
| `org.apache.http.*` | domain | Tashqi integratsiya domenga kirgan |

## 6.2 Bog'liqlik yo'nalishi: ichki qatlam tashqarini bilmaydi

Qatlamli arxitekturaning yagona qattiq qoidasi - bog'liqlik ichkariga qarab yo'naladi. Web application ni biladi, application domenni biladi, domen hech kimni bilmaydi. Infratuzilma domen e'lon qilgan interfeysni amalga oshiradi.

Review da bu qoida bitta savol bilan tekshiriladi: yangi `import` yoki konstruktor parametri bog'liqlikni ichkariga yoki tashqariga yo'naltirdimi.

```java
// Buzilish: domen servis infratuzilma klassiga bog'langan.
package com.acme.order.domain;

import com.acme.order.infra.sms.TwilioSmsClient;   // yo'nalish tashqariga

public class OrderNotifier {
    private final TwilioSmsClient sms;             // domen vendorni biladi
    public void notifyShipped(Order order) {
        sms.send(order.getPhone(), "Buyurtma jo'natildi");
    }
}

// To'g'ri: domen o'z ehtiyojini interfeys bilan e'lon qiladi (port),
// implementatsiya tashqarida turadi (adapter). Interfeys foydalanuvchi
// tomonda e'lon qilinadi - shuning uchun u domain paketida.
package com.acme.order.domain;

public interface CustomerNotifications {               // port, domen tilida
    void shipped(OrderId orderId, PhoneNumber to);
}

package com.acme.order.infra.sms;

@Component
class TwilioNotifications implements CustomerNotifications {   // adapter
    private final TwilioClient client;
    @Override public void shipped(OrderId orderId, PhoneNumber to) {
        client.send(to.value(), messages.shipped(orderId));
    }
}
// Review foydasi: domen testda soxta implementatsiya bilan ishlaydi,
// vendor almashtirilsa domen tegilmaydi, va interfeys nomi domen tilida.
```

Diqqat: bu yerda muhimi interfeys borligi emas, interfeys qayerda turgani. `infra` paketidagi interfeys va uning yonidagi yagona implementatsiyasi hech narsani yechmaydi - bu [7-bobdagi](07-bogliqlik-koheziya-va-abstraksiya-review.md) "soxta abstraksiya" holati.

## 6.3 Yangi paket va yangi modul - chegara haqida qaror

Diffda yangi paket paydo bo'lishi arxitektura qarori. Review savollari: bu paket nima bo'yicha ajratilgan (texnik qatlam yoki biznes xususiyati), uning tashqi yuzasi qanday, va kim unga kirish huquqiga ega.

Amaliy mezon - paket ichidagi klasslarning qanchasi `public`. Agar hammasi `public` bo'lsa, paket chegara emas, shunchaki papka. Haqiqiy chegara bir-ikki `public` tur va qolgan hammasi paket-private bo'lgan holatda paydo bo'ladi.

```java
// Modul chegarasini kod bilan majburlash: Spring Modulith yoki
// paket-private ko'rinish. Review da shu belgilar izlanadi.

// com/acme/billing/package-info.java
@ApplicationModule(
    allowedDependencies = { "shared::money", "customer::api" }   // aniq ro'yxat
)
package com.acme.billing;

// Modul ichidagi klasslar: faqat API public.
package com.acme.billing;
public interface BillingApi {                   // yagona kirish nuqtasi
    Invoice issue(IssueInvoiceCommand cmd);
}

package com.acme.billing.internal;
class InvoiceNumberGenerator { }                // paket-private: tashqaridan ko'rinmaydi
class VatCalculator { }                         // ichki detal

// Chegarani test bilan tekshirish (ArchUnit yoki Modulith).
@Test
void moduleBoundariesAreRespected() {
    ApplicationModules.of(Application.class).verify();   // Spring Modulith
}
```

## 6.4 Yangi tashqi bog'liqlik - eng kam baholangan arxitektura qarori

`pom.xml` ga bitta qator qo'shilishi diffda eng kichik o'zgarish, lekin oqibati eng uzoq muddatli: yangi kutubxona yangilanish majburiyati, CVE xavfi, transitive konflikt va litsenziya masalasi olib keladi.

| Review savoli | Nega muhim |
| --- | --- |
| Shu vazifa mavjud bog'liqlik bilan bajariladimi | Ko'pincha Spring yoki JDK da allaqachon bor |
| Kutubxona qancha faol: oxirgi reliz qachon | Tashlab ketilgan kutubxona kelajakdagi muammo |
| Transitive nimani olib keladi | Konflikt va kattalik |
| Litsenziya mos keladimi | GPL/AGPL yuridik masala |
| Necha satr kod uchun olinyapti | 20 satr uchun kutubxona - noto'g'ri savdo |
| Kim yangilaydi | Egasi yo'q bog'liqlik eskiradi |

```bash
# Yangi bog'liqlik haqiqatda nimani olib keldi.
./mvnw -q dependency:tree -Dincludes=':::' | grep -A20 'yangi-kutubxona'

# Konflikt bormi va qaysi versiya g'olib chiqqan.
./mvnw dependency:tree -Dverbose | grep -E 'omitted|conflict' | head -20

# Mavjud imkoniyatlar bilan bajariladimi: JDK va Spring da bormi.
# Masalan JSON uchun Jackson allaqachon bor, HTTP uchun RestClient bor,
# retry uchun Spring Retry yoki Resilience4j allaqachon loyihada bo'lishi mumkin.
grep -rn 'artifactId' pom.xml | sort | uniq | head -40
```

## 6.5 Arxitektura eroziyasini diffdan ko'rish

Eroziya bitta PR da ko'rinmaydi, lekin uning belgilari ko'rinadi. Quyidagi belgilar har biri alohida zararsiz, birgalikda esa tizim yo'nalishini o'zgartiradi.

| Belgi | Nimani bildiradi | Review javobi |
| --- | --- | --- |
| Konstruktor parametrlari soni 6 dan oshdi | Klass juda ko'p narsani biladi | Mas'uliyatni bo'lish yoki agregat kiritish |
| `@Autowired` maydon yoki `ApplicationContext` inyeksiyasi | Bog'liqlik yashiringan | Konstruktor inyeksiyasi |
| `static` yordamchi klassga yangi metod | Holatsiz "xudo klass" o'sib boryapti | Domen obyektiga ko'chirish |
| `util`, `common`, `helper`, `manager` paketi o'sdi | Egasi yo'q kod to'planyapti | Domen tilida nomlangan joyga ko'chirish |
| `shared` moduldagi klass biznes qoidasini bildi | Umumiy modul domenga aylanyapti | Qoidani egasiga qaytarish |
| Entity ga yangi `@Transient` hisob maydoni | Ma'lumot modeli hisob mantiqini yutyapti | Domen servisi yoki value object |
| DTO va entity bir xil klass | Tashqi shakl va saqlash bir-biriga qulflangan | Ajratish |
| Yangi `if (featureEnabled)` shoxlari | Vaqtinchalik flag doimiy bo'lib qolyapti | Flag ning o'chirilish sanasi |
| Boshqa modul jadvaliga `JOIN` | Sxema chegarasi teshilgan | API orqali o'qish yoki o'qish modeli |
| Sikl bog'liqlik (A -> B -> A) | Modullar aslida bitta | Birlashtirish yoki event bilan uzish |

```java
// Sikl bog'liqlikni ArchUnit bilan taqiqlash: eroziyaning eng aniq shakli.
@ArchTest
static final ArchRule no_cycles =
    slices().matching("com.acme.(*)..").should().beFreeOfCycles();

// "Util" to'planishini cheklash: yangi util klass qo'shilishini sekinlashtirish.
@ArchTest
static final ArchRule no_new_util_classes =
    noClasses().that().haveSimpleNameEndingWith("Util")
               .or().haveSimpleNameEndingWith("Helper")
               .or().haveSimpleNameEndingWith("Manager")
               .should().bePublic()
               .because("domen tilida nomlangan joyga tegishli bo'lsin");
```

## 6.6 Qatlam o'tkazib yuborilishi (layer skipping)

Controller to'g'ridan-to'g'ri repository ga murojaat qilsa, kod ishlaydi va test ham o'tadi. Muammo keyinroq chiqadi: tranzaksiya chegarasi yo'qoladi, avtorizatsiya tekshiruvi chetlab o'tiladi, va biznes qoidasi ikki joyda takrorlanadi.

```java
// Diffda uchraydigan shakl: tezkor yechim.
@RestController
class OrderController {
    private final OrderRepository orders;          // qatlam o'tkazib yuborilgan

    @GetMapping("/orders/{id}")
    OrderDto get(@PathVariable long id) {
        // Avtorizatsiya yo'q: har kim har qanday buyurtmani ko'radi.
        // Lazy maydon ochilsa - LazyInitializationException yoki N+1.
        return OrderDto.from(orders.findById(id).orElseThrow());
    }
}

// Review izohi: ikkita oqibat bor, ikkisi ham diffda ko'rinmaydi.
// 1) Avtorizatsiya: shu buyurtma so'rovchiga tegishlimi - tekshirilmagan.
// 2) Tranzaksiya: controller da tranzaksiya yo'q, OSIV yopilgan bo'lsa
//    lazy kolleksiya istisno tashlaydi, ochiq bo'lsa ulanish view gacha
//    egallanadi.

// To'g'ri: application servis chegarani egallaydi.
@Service
class OrderQueries {
    @Transactional(readOnly = true)
    @PreAuthorize("@orderAccess.canRead(#id, authentication)")
    public OrderDto byId(long id) {
        return orders.findProjectionById(id).orElseThrow(OrderNotFound::new);
    }
}
```

## 6.7 Chegaradan o'tadigan ma'lumot shakli

Arxitektura chegarasi ma'lumot shaklida ham ko'rinadi. Entity ni controller dan qaytarish - chegarani yo'q qilish: jadval ustuni nomi tashqi API shakliga aylanadi va keyin uni o'zgartirish breaking change bo'ladi.

| Chegaradan o'tayotgan narsa | Xavf | To'g'ri shakl |
| --- | --- | --- |
| JPA entity controller javobida | Jadval sxemasi API ga yopishadi, lazy proxy serializatsiyasi | Alohida DTO yoki record |
| Entity Kafka xabarida | Boshqa servis sxemangizga bog'lanadi | Aniq event sxemasi |
| `Map<String,Object>` servis chegarasida | Shartnoma yo'q, xato kompilyatsiyada tutilmaydi | Tipli record |
| Enum ordinal qiymati tashqariga | Tartib o'zgarsa ma'no o'zgaradi | Nom bo'yicha satr |
| Ichki istisno turlari tashqariga | Implementatsiya oqib chiqadi | Xato kodi va shakli |
| `LocalDateTime` API da (zonasiz) | Mijoz zonani bilmaydi | `Instant` yoki `OffsetDateTime` |

## 6.8 Hisob mantiqi qayerda turadi

Bitta hisob uch joyda bajarilishi mumkin: SQL da, Java da, yoki frontendda. Diffda yangi hisob paydo bo'lsa, review savoli - nega shu joyda.

| Joy | Qachon to'g'ri | Xavf |
| --- | --- | --- |
| SQL (aggregate, window) | Katta hajmni filtrlash va yig'ish | Mantiq yashiringan, test qiyin, portativ emas |
| Domen (Java) | Biznes qoidasi, invariant | Katta hajmni Java ga tortish |
| View/DTO mapping | Faqat formatlash | Biznes qoidasi taqdimotga tushib qolishi |
| Frontend | Faqat ko'rinish | Qoida ikki joyda, mos kelmaydi |

Qattiq qoida: pul, soliq, chegirma va huquq (kim nimani ko'rishi) hisobi hech qachon frontendda yoki faqat SQL da bo'lmaydi. Ular domen ichida, test bilan qoplangan joyda turishi kerak.

## 6.9 Modullar orasidagi muloqot shakli

Diffda yangi modullar aro chaqiruv paydo bo'lsa, uning shakli arxitektura qarori: sinxron chaqiruv, event, yoki umumiy ma'lumot.

```java
// Uch shakl va ularning review savollari.

// 1) Sinxron chaqiruv: eng oson, eng qattiq bog'liqlik.
//    Review savoli: chaqirilgan modul yiqilsa, bu operatsiya to'xtashi kerakmi?
Invoice invoice = billingApi.issue(cmd);     // billing yiqilsa - order ham yiqiladi

// 2) Domen eventi: bo'shashgan bog'liqlik, lekin yetkazish kafolati kerak.
//    Review savoli: event yo'qolsa nima bo'ladi? Tranzaksiya bilan atomikmi?
events.publish(new OrderPlaced(order.id(), order.total()));
// Agar bu @TransactionalEventListener(AFTER_COMMIT) bilan ishlanmasa va
// outbox bo'lmasa - commit o'tib, event yo'qolishi mumkin ([27-bob](27-izolyatsiya-poyga-holatlari-va-xabar.md)).

// 3) Umumiy jadval: eng yomon shakl, eng tez yechim.
//    Review javobi: boshqa modulning jadvaliga yozish - chegarani yo'q qilish.
jdbc.update("UPDATE billing_invoice SET status = ? WHERE id = ?", ...);  // blocker
```

## 6.10 Arxitektura izohini qanday yozish

Arxitektura izohi eng ko'p qarshilik keltiradigan izoh turi, chunki u ko'p ishni qayta qilishni talab qiladi. Shu sababli uning shakli muhim: oqibatni raqamda ko'rsatish, bitta alternativani taklif qilish va kelishuv nuqtasini aytish.

```text
# Yomon shakl: baholash, oqibat yo'q, alternativa yo'q.
"Bu dizayn noto'g'ri, clean architecture ga mos emas."

# Yaxshi shakl: belgi -> oqibat -> alternativa -> kelishuv.
suggest (arxitektura): OrderNotifier domen paketida TwilioSmsClient ga
bog'langan.

Oqibati: (1) domen testi uchun Twilio mock kerak bo'ladi, hozir 3 ta testda
shunday qilingan; (2) SMS provayderi almashtirilsa, domen kodi o'zgaradi;
(3) ArchUnit qoidamiz "domain framework-free" buni keyinroq bloklaydi.

Alternativa: domenda CustomerNotifications interfeysi, infra da Twilio
adapteri. O'zgarish hajmi: 1 interfeys + 1 klass ko'chirish, taxminan 30 satr.

Agar bu PR da qilish katta bo'lsa, tiket ochib shu sprintda yopsak bo'ladi -
lekin yangi kod shu yo'nalishda yozilmasa, keyingi oyda 10 joyda shunday
bo'ladi.
```

## 6.11 Amalda qo'llash

- [ ] Review ning birinchi qadamiga "diffdagi yangi importlar" tekshiruvini qo'shing va qatlam buzilishini grep bilan avtomatlashtiring.
- [ ] Qatlam qoidalarini ArchUnit testiga yozing: `domain` framework-free, `web` repository ga tegmaydi, `@Transactional` faqat application qatlamida.
- [ ] `slices().should().beFreeOfCycles()` qoidasini qo'shib, mavjud sikl bog'liqliklar ro'yxatini chiqaring.
- [ ] Loyihadagi paketlarni ko'rib, har birida nechta `public` klass borligini sanang: chegara bo'lishi kerak bo'lgan paketlarda ortiqcha `public` larni paket-private ga o'tkazing.
- [ ] Yangi bog'liqlik uchun PR shabloniga 6 savolli ro'yxat qo'shing (mavjud imkoniyat, faollik, transitive, litsenziya, hajm, egasi).
- [ ] Controller javoblarida JPA entity qaytarilgan joylarni toping va DTO ga o'tkazishni rejalashtiring.
- [ ] Eroziya belgilari jadvalidan uchtasini tanlab, repoda qanchaligini o'lchang: konstruktor parametrlari 6 dan ko'p klasslar, `Util`/`Helper` klasslar soni, `@Autowired` maydonlar.
- [ ] Modullar aro umumiy jadvalga yozadigan joylarni toping va ularni API yoki event ga o'tkazish tiketini ochingg.

---

[&larr; 5. Mashina va odam: SonarQube dan oldin topish](05-mashina-va-odam-sonarqube-dan-oldin-topish.md) · [Mundarija](README.md) · [7. Bog'liqlik, koheziya va abstraksiya review &rarr;](07-bogliqlik-koheziya-va-abstraksiya-review.md)
