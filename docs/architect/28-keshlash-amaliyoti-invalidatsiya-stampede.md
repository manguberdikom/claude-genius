<!-- doc: architect | chapter: 28 | part: V. Atrof ekotizim: operatsion haqiqat -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 28. Keshlash amaliyoti: invalidatsiya, stampede, Redis haqiqati (Caching in Practice)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [28.1 Kesh qo'yishdan oldin so'raladigan savollar](#281-kesh-qoyishdan-oldin-soraladigan-savollar)
- [28.2 Hit nisbati qanchadan boshlab foyda beradi](#282-hit-nisbati-qanchadan-boshlab-foyda-beradi)
- [28.3 Mahalliy kesh va taqsimlangan kesh tanlovi](#283-mahalliy-kesh-va-taqsimlangan-kesh-tanlovi)
- [28.4 Spring Cache abstraksiyasi mexanikasi va proxy chegarasi](#284-spring-cache-abstraksiyasi-mexanikasi-va-proxy-chegarasi)
- [28.5 Invalidatsiya: muddat, hodisa va versiya kaliti bo'yicha](#285-invalidatsiya-muddat-hodisa-va-versiya-kaliti-boyicha)
- [28.6 Kesh stampede va undan himoya usullari](#286-kesh-stampede-va-undan-himoya-usullari)
- [28.7 Eskirgan ma'lumotni ko'rsatish siyosati](#287-eskirgan-malumotni-korsatish-siyosati)
- [28.8 Kesh va tranzaksiya nomuvofiqligi](#288-kesh-va-tranzaksiya-nomuvofiqligi)
- [28.9 Redis operatsion haqiqati: xotira, eviction va bitta thread](#289-redis-operatsion-haqiqati-xotira-eviction-va-bitta-thread)
- [28.10 Katta kalit, uzun ro'yxat va KEYS buyrug'i xavfi](#2810-katta-kalit-uzun-royxat-va-keys-buyrugi-xavfi)
- [28.11 Serializatsiya tanlovi va kesh qiymati hajmi](#2811-serializatsiya-tanlovi-va-kesh-qiymati-hajmi)
- [28.12 Kesh ishlamay qolganda tizim yiqilmasligi](#2812-kesh-ishlamay-qolganda-tizim-yiqilmasligi)
- [28.13 Amalda qo'llash](#2813-amalda-qollash)

</details>



Kesh tizimga tezlik qo'shmaydi, u faqat sekinlikni yashiradi. Yashirilgan sekinlik kesh sovib qolgan paytda, odatda eng yuqori yuklamada, to'liq kuch bilan qaytib keladi. Shuning uchun kesh qarori "qancha tez bo'ladi" emas, "qanday nomuvofiqlikka va operatsion yukka rozi bo'lamiz" degan savol. Bu bobda raqamlar, sozlash parametrlari va kesh joriy qilgandan keyin chiqadigan tuzoqlar ko'rib chiqiladi.

## 28.1 Kesh qo'yishdan oldin so'raladigan savollar

Kesh ko'p holda profiling o'rniga qo'yiladi. Buyurtma ro'yxati 800 ms ishlayotgan bo'lsa, birinchi ish sababini topish: N+1 so'rovmi, index yo'qligimi, yoki og'ir agregatsiyami. N+1 bo'lsa kesh muammoni yashiradi, lekin ro'yxat eski qolaveradi va siz ikkita muammoga ega bo'lasiz.

Savollar ro'yxati qisqa. Bu ma'lumot qancha vaqt eskirishi mumkin. O'qish va yozish nisbati qanday. Qiymat hajmi kilobaytmi yoki megabaytmi. Eski qiymat ko'rsatilsa biznesda nima buziladi. Ombor qoldig'i uchun javob odatda "keshlamaymiz", chunki minusga sotib qo'yish narxi keshdan kelgan foydadan katta.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Nega sekin | Kesh qo'yadi | Avval `EXPLAIN ANALYZE` va profil oladi |
| Kesh nimaga qo'yiladi | "Tezlashtirish uchun" | DB yuklamasini N barobar kamaytirish uchun, raqam bilan |
| TTL qiymati | Hammaga 60 soat yoki 1 kun | Har kesh nomiga biznesdan so'ralgan eskirish chegarasi |
| Hit nisbati | O'lchanmaydi | Metrika bilan kuzatiladi, 0.9 dan past bo'lsa qayta ko'riladi |
| Invalidatsiya | `@CacheEvict` qo'yiladi va unutiladi | Commit dan keyin, kalit egasi servis ichida |
| Stampede | O'ylanmaydi | `sync`, jitter yoki taqsimlangan lock bilan yopiladi |
| Redis o'chsa | Tizim 500 qaytaradi | Zaxira yo'l DB ga tushadi, latency oshadi, xizmat tirik |
| Qiymat hajmi | Butun entity grafi | Faqat kerakli maydonlardan DTO |
| Xotira | Chegara yo'q | `maxmemory` va eviction siyosati aniq belgilangan |
| Kesh kaliti | `toString()` ga tayanadi | Aniq, versiyalangan, prefiksli kalit |

**Keshning oltin qoidasi.** Newman qoidani bir gapda beradi: siz va yangi ma'lumot manbai o'rtasida qancha kesh qatlami bo'lsa, ma'lumot shuncha eskiradi, mijoz ko'rgan qiymat qanchalik yangi ekanini aniqlash va invalidatsiya qaysi joyda kerakligi haqida fikrlash shuncha qiyinlashadi (*Building Microservices*, 2-nashr, 13-bob, "The Golden Rule of Caching"). Misoli tanish: `Inventory` server tomonda bir daqiqalik TTL bilan keshlaydi, `Recommendation` esa mijoz tomonda yana bir daqiqalik TTL bilan keshlaydi; mijoz keshi eskirganda yangi qiymat so'raydi, lekin so'rov server keshiga tushadi va u ham bir daqiqa eski bo'lishi mumkin, natijada qiymat ikki daqiqagacha eski bo'ladi, holbuki `Recommendation` o'zini bir daqiqa ichida deb hisoblaydi. Shundan ikki amaliy qoida chiqadi: keshni avvalo ishlash optimizatsiyasi deb qarash va iloji boricha kam joyda keshlash, Newmanning so'zi bilan ideal joy soni nol; kesh kesh ustiga qo'yilgan holatda esa TTL o'rniga timestamp asosidagi eskirish yaxshiroq, chunki u qatlamlar bo'ylab qo'shilib ketmaydi.
## 28.2 Hit nisbati qanchadan boshlab foyda beradi

Hisob oddiy formula bilan qilinadi. O'rtacha latency teng: `h * T_kesh + (1 - h) * (T_kesh + T_db)`. Bir ma'lumot markazi ichida Redis uchun `T_kesh` taxminan 1 ms, og'ir agregatsiya uchun `T_db` taxminan 40 ms deb olamiz.

| Hit nisbati | O'rtacha latency | DB ga tushadigan QPS (10 000 QPS dan) |
| --- | --- | --- |
| 0.50 | taxminan 21 ms | 5 000 |
| 0.80 | taxminan 9 ms | 2 000 |
| 0.90 | taxminan 5 ms | 1 000 |
| 0.95 | taxminan 3 ms | 500 |
| 0.99 | taxminan 1.4 ms | 100 |

Jadvaldan ikki xulosa chiqadi. Latency bo'yicha foyda 0.8 dan keyin to'yinadi, 0.9 dan 0.95 ga ko'tarilish foydalanuvchi uchun 2 ms beradi. DB yuklamasi bo'yicha foyda to'xtamaydi va buni arifmetika beradi, o'lchov emas: DB ga tushadigan so'rov ulushi miss rate ga teng, ya'ni hit rate 0.9 da 10 foiz, 0.99 da 1 foiz, demak DB so'rovi o'n barobar kamayadi. Maqsad latency bo'lsa 0.85 atrofi yetarli, maqsad DB ni saqlab qolish bo'lsa 0.97 dan past natija yetarli emas.

Teskari holat ham bor. `T_db` birlamchi kalit bo'yicha 2 ms bo'lsa, foyda bor yo'g'i 1 ms. Bunday joyga tarmoq orqali kesh qo'yish faqat nomuvofiqlik va yana bitta ishdan chiqish nuqtasini qo'shadi.

## 28.3 Mahalliy kesh va taqsimlangan kesh tanlovi

Caffeine JVM ichida ishlaydi, o'qish taxminan 100 nanosekund turadi, tarmoq ham serializatsiya ham yo'q. Narxi shu: 12 ta pod bo'lsa, 12 ta mustaqil kesh nusxasi bor va ularning invalidatsiyasi bir vaqtda bo'lmaydi. Shuning uchun mahalliy kesh faqat qisqa TTL bilan ishlatiladi.

Amalda bo'linish shunday. Valyuta kursi, soliq stavkasi, kategoriyalar va feature flag mahalliy keshga tushadi, TTL 30 soniyadan 5 minutgacha. Sessiya, idempotentlik kaliti va rate limit hisoblagichi Redis ga tushadi, chunki hamma pod ularni bir xil ko'rishi shart.

```java
@Configuration
@EnableCaching
class KeshSozlamasi {

  // Mahalliy kesh: qisqa TTL, qattiq hajm chegarasi, statistika yoqilgan
  @Bean
  CacheManager mahalliyKesh() {
    CaffeineCacheManager m = new CaffeineCacheManager("valyutaKursi", "soliqStavkasi");
    m.setCaffeine(Caffeine.newBuilder()
        .maximumSize(10_000)              // taxminan 10k * 500 bayt = 5 MB
        .expireAfterWrite(Duration.ofMinutes(2))
        .refreshAfterWrite(Duration.ofSeconds(90)) // fon rejimida yangilash
        .recordStats());                  // hit nisbatini o'lchash uchun shart
    return m;
  }
}
```

`recordStats()` chaqirilmasa hit nisbati ko'rinmaydi va siz kesh foydasini isbotlay olmaysiz. `refreshAfterWrite` muddati `expireAfterWrite` dan kichik bo'lishi shart, aks holda ishga tushmaydi. `refreshAfterWrite` ning xatti-harakatini aniq bilish kerak, chunki uni ko'pincha teskari tushunadilar: muddat o'tgandan keyin **birinchi** so'rov eski qiymatni oladi va yangilash fon rejimida boshlanadi. Ya'ni u chaqiruvchini bloklamaydi va yangi qiymatni darhol bermaydi; uning maqsadi aynan shu - eskirgan qiymatni berib turib, orqada yangilash. Shu sababli u stampede ni yumshatadi, lekin "har doim yangi ma'lumot" talabini bajarmaydi.

Mahalliy keshning o'qish tezligi haqidagi raqamlar bu bobda o'lchanmagan: ular tartibni ko'rsatish uchun keltirilgan va o'z muhitida o'lchanishi kerak.

Mahalliy va taqsimlangan kesh tanlovining ustiga uchinchi o'lcham qo'yiladi: kesh **kimning tomonida** turadi. Newman uch joyni ajratadi va har birining kelishuvini maqsad bilan bog'laydi.

| Joy | Nimaga eng mos | Narxi |
|---|---|---|
| Client-side (iste'molchi ichida) | latency va robustness: tarmoq chaqiruvi umuman yo'qoladi | invalidatsiya tanlovi cheklangan; iste'molchilar orasida nomuvofiq ko'rinish |
| Server-side (ma'lumot egasi ichida) | invalidatsiya nazorati va hamma iste'molchiga bir vaqtda foyda | round trip qoladi, demak latency va robustness uchun kuchsiz |
| Request cache (butun javob) | tezlik: Sales ham, Catalog ham chaqirilmaydi | juda tor, faqat o'sha so'rov shakliga xizmat qiladi |

Client-side keshning kuchi tarmoq chaqiruvidan qutulishida, shuning uchun u latency uchun ham, chidamlilik uchun ham eng samarali. Lekin iste'molchi ko'p bo'lsa muammo o'sadi: `Sales`, `Recommendation` va `Promotions` servislari `Catalog` ma'lumotini mahalliy keshlaganda, `Catalog` o'zgarsa hech qanday invalidatsiya mexanizmi uch iste'molchida ma'lumot aynan bir vaqtda yangilanishini kafolatlay olmaydi, ya'ni ular bir vaqtda turli ko'rinish ko'radi. Umumiy Redis ni iste'molchilar o'rtasida bo'lishish bu nomuvofiqlikni yo'qotadi va xotira sarfini ham kamaytiradi, lekin iste'molchi endi keshgacha round trip qilishi kerak bo'ladi, ya'ni client-side keshning asosiy afzalligi qisman yo'qoladi.

Server-side kesh iste'molchi uchun ko'rinmas, ya'ni ichki implementatsiya tafsiloti: shakli ilovadagi kesh ham, servis chegarasi ichidagi teskari proxy, yashirin Redis node i yoki o'qishni read replica ga yo'naltirish ham bo'lishi mumkin. Shundan ikki natija chiqadi: write-through kabi murakkabroq invalidatsiya mexanizmini shu yerda qurish osonroq, va hamma iste'molchi hech narsa qilmasdan foyda oladi. Narxi esa o'zgarmaydi, chaqiruv baribir qilinishi kerak, shuning uchun bu shakl latency ni qisqartirish va nosozlikka chidash uchun kuchsiz.

Qaror mezoni bitta savolga qisqaradi: nimadan qo'rqamiz. Agar tashvish uchidan uchiga latency bo'lsa client-side afzal; agar tashvish ma'lumot egasining yuki va invalidatsiya izchilligi bo'lsa server-side afzal. Korpusning [mahalliy va taqsimlangan kesh](#283-mahalliy-kesh-va-taqsimlangan-kesh-tanlovi) tanlovi shu uchlikning ustiga qo'yiladi, uning o'rnini bosmaydi.

## 28.4 Spring Cache abstraksiyasi mexanikasi va proxy chegarasi

`@Cacheable` hech qanday sehr qilmaydi. Spring bean atrofida proxy yaratadi, chaqiruv proxy ga kelganda kalit hisoblanadi, `Cache.get` chaqiriladi, qiymat bo'lsa metod ishga tushmaydi. `key` ifodasi berilmasa kalit barcha argumentlardan tuziladi va ularning `equals` bilan `hashCode` iga tayanadi. Entity ni argument qilib berish shuning uchun xavfli, uning `hashCode` i o'zgaruvchan.

Proxy chegarasi eng ko'p xato keltiradigan joy. Sinf o'z ichidagi `@Cacheable` metodni `this` orqali chaqirsa, chaqiruv proxy dan o'tmaydi va kesh chetlab o'tiladi. Xato jim kechadi, faqat hit nisbati nolga teng bo'lib turadi.

```java
@Service
public class HisobotServisi {

  // Kalit aniq yozilgan, argument primitiv turda
  @Cacheable(cacheNames = "kunlikSavdo", key = "#sanaIso + ':' + #filialId", sync = true)
  public SavdoHisoboti kunlikSavdo(String sanaIso, long filialId) {
    return agregatsiyaniHisobla(sanaIso, filialId); // taxminan 400 ms
  }

  public List<SavdoHisoboti> haftalik(long filialId, List<String> kunlar) {
    // this.kunlikSavdo(...) proxy dan o'tmaydi va kesh butunlay chetlab o'tiladi
    return kunlar.stream().map(k -> ozi.kunlikSavdo(k, filialId)).toList();
  }

  @Autowired @Lazy private HisobotServisi ozi; // oxirgi chora, afzali alohida bean
}
```

Yana bir tafsilot: metod `null` qaytarsa, Spring odatda `null` ni ham keshlaydi. Redis uchun `RedisCacheConfiguration` da `disableCachingNullValues()` chaqirilsa, mavjud bo'lmagan kalit har marta DB ga boradi. Mavjud bo'lmagan ID bilan hujum qilinsa bu DB ni urishga aylanadi, shuning uchun "yo'q" javobini qisqa TTL bilan keshlash to'g'ri qaror.

## 28.5 Invalidatsiya: muddat, hodisa va versiya kaliti bo'yicha

Uch usul bor va ular bir birini almashtirmaydi. Muddat bo'yicha invalidatsiya eng ishonchli, chunki u koddan bog'liq emas. Narxi aniq: TTL qancha bo'lsa, eskirish oynasi shuncha. Hisobot uchun 5 minut, narx uchun 30 soniya, kategoriya daraxti uchun 1 soat odatiy qiymatlar.

Hodisa bo'yicha invalidatsiya aniq, lekin mo'rt. Buyurtma o'zgarganda faqat buyurtma keshi emas, filial savdosi va mijoz statistikasi ham eskiradi. Bitta joy esdan chiqsa ma'lumot cheksiz eskirib qoladi, shuning uchun hodisa bo'yicha tozalash har doim TTL ustiga qo'yiladi, uning o'rniga emas.

Versiya kaliti eng mustahkam usul. Kesh kalitiga guruh versiyasi qo'shiladi, o'zgarish bo'lganda versiya oshiriladi va eski kalitlar o'z o'zidan ishlatilmay qoladi. Eski yozuvlar TTL yoki eviction bilan ketadi. Bu usul ommaviy o'chirishni keraksiz qiladi.

```java
@Service
@RequiredArgsConstructor
public class NarxKeshi {

  private final StringRedisTemplate redis;

  // Versiya kaliti kesh kaliti ichiga kiradi
  public String kalit(long filialId, long tovarId) {
    String v = redis.opsForValue().get("ver:narx:" + filialId);
    if (v == null) { v = "1"; redis.opsForValue().setIfAbsent("ver:narx:" + filialId, v); }
    return "narx:v" + v + ":" + filialId + ":" + tovarId;
  }

  // Bitta INCR: hamma eski kalit bir zumda ahamiyatsiz bo'ladi
  public void filialNarxlariOzgardi(long filialId) {
    redis.opsForValue().increment("ver:narx:" + filialId);
  }
}
```

## 28.6 Kesh stampede va undan himoya usullari

Stampede shunday sodir bo'ladi. Og'ir hisobot keshi TTL tugashi bilan bo'shaydi, shu millisekundda 300 ta parallel so'rov keladi va hammasi DB ga tushadi. DB connection pool 20 ta ulanishdan iborat bo'lsa, navbat o'sadi, timeout boshlanadi va kesh o'zi avariya sababiga aylanadi.

Birinchi himoya `@Cacheable(sync = true)`. U bir JVM ichida bir kalit uchun faqat bitta hisoblashga yo'l beradi, qolganlari natijani kutadi. Kafolat faqat pod ichida, 12 ta pod bo'lsa DB ga 12 ta so'rov boradi. Ko'p hollarda 300 dan 12 ga tushish yetarli.

Ikkinchi himoya TTL ga jitter qo'shish. Hamma kalitga aynan 300 soniya berilsa, ular birgalikda bo'shaydi va to'lqin paydo bo'ladi. TTL ni 300 va 360 soniya orasida tasodifiy tanlash to'lqinni yoyadi. Uchinchi himoya taqsimlangan lock, u faqat 1 soniyadan uzun hisoblash uchun ishlatiladi, chunki o'zi ham tarmoq chaqiruvi qo'shadi.

```java
// Faqat 1 soniyadan uzun hisoblash uchun: bitta egalik, qolganlar eski qiymat bilan
public SavdoHisoboti olish(String kalit) {
  SavdoHisoboti bor = keshdanOq(kalit);
  if (bor != null && !eskirishgaYaqin(bor)) return bor;

  // SET NX PX: atomar egallash, 10 soniyada o'z o'zidan bo'shaydi
  Boolean egallandi = redis.opsForValue()
      .setIfAbsent("lock:" + kalit, nodeId, Duration.ofSeconds(10));

  if (!Boolean.TRUE.equals(egallandi)) {
    return bor != null ? bor : kutibQaytaOq(kalit, Duration.ofMillis(300));
  }
  try {
    SavdoHisoboti yangi = agregatsiyaniHisobla(kalit);
    keshgaYoz(kalit, yangi, Duration.ofMinutes(5));
    return yangi;
  } finally {
    ozLockiniOchir("lock:" + kalit, nodeId); // faqat o'z lock ini o'chirish
  }
}
```

## 28.7 Eskirgan ma'lumotni ko'rsatish siyosati

Eng muhim qaror texnik emas, biznes qarori. Savol aniq qo'yilishi kerak: bu raqam 30 soniya eski bo'lsa kim zarar ko'radi. Boshqaruv panelidagi buyurtma soni uchun 60 soniya eskirish xalal bermaydi. To'lov balansi uchun esa eskirish mijoz da'vosiga aylanadi.

Shuning uchun har kesh nomi uchun ikki raqam yoziladi: odatdagi TTL va DB ishlamay qolganda eski qiymatni ishlatish chegarasi. Hisobotlar uchun bu 5 minut va 30 minut bo'lishi mumkin. Interfeysda "ma'lumot 14:05 holatiga" degan yozuv qo'shilsa, eskirish muammo bo'lishdan chiqib xususiyatga aylanadi.

## 28.8 Kesh va tranzaksiya nomuvofiqligi

Eng ko'p uchraydigan jim xato shu: kesh tranzaksiya ichida tozalanadi, keyin tranzaksiya rollback bo'ladi. Keyingi o'qish DB dan eski qiymatni olib keshga qaytaradi va nomuvofiqlik qotib qoladi. Rollback kam bo'lgani uchun bu testda ko'rinmaydi, produksiyada esa vaqti vaqti bilan tushunarsiz natija beradi.

To'g'ri yechim keshni commit dan keyin o'zgartirish. Spring da buning mexanizmi bor, `@TransactionalEventListener` ning `AFTER_COMMIT` fazasi. U tranzaksiya muvaffaqiyatli yakunlangandan keyin ishlaydi, rollback da umuman chaqirilmaydi.

```java
@Service
@RequiredArgsConstructor
public class BuyurtmaServisi {

  private final ApplicationEventPublisher nashriyot;

  @Transactional
  public void yetkazildiDebBelgila(long buyurtmaId) {
    buyurtmaRepo.statusniOzgartir(buyurtmaId, Status.YETKAZILDI);
    // Kesh hozir tozalanmaydi, faqat hodisa e'lon qilinadi
    nashriyot.publishEvent(new BuyurtmaOzgardi(buyurtmaId));
  }
}

@Component
@RequiredArgsConstructor
class KeshTozalovchi {
  private final CacheManager keshlar;

  // AFTER_COMMIT: rollback bo'lsa bu metod umuman chaqirilmaydi
  @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
  public void buyurtmaOzgardi(BuyurtmaOzgardi h) {
    keshlar.getCache("buyurtma").evict(h.buyurtmaId());
    keshlar.getCache("mijozStatistikasi").evict(h.mijozId());
  }
}
```

Yana bir tafsilot. Replikadan o'qiyotgan bo'lsangiz, commit dan keyin kesh darhol to'ldirilsa, replika lag i sababli eski qiymat keshga tushadi. Shuning uchun commit dan keyin faqat tozalash xavfsizroq, keyingi o'qish o'zi to'ldiradi.

## 28.9 Redis operatsion haqiqati: xotira, eviction va bitta thread

Redis buyruqlarni bitta thread da bajaradi. Atomarlik bepul keladi, lekin bitta sekin buyruq butun serverni to'xtatib turadi. 100 ming elementli ro'yxat ustida `LRANGE 0 -1` yoki katta kalitni `DEL` qilish o'n millisekundlar olishi mumkin, va shu vaqtda hamma mijoz kutadi.

`maxmemory` belgilanmagan Redis eng xavfli konfiguratsiya. U xotira tugaguncha o'sadi, keyin operatsion tizim uni o'ldiradi yoki swap ga tushib latency yuz barobar oshadi. Kesh uchun `maxmemory` fizik xotiraning taxminan 70 foizi qilib qo'yiladi, qolgani fragmentatsiya va buferlarga kerak.

Eviction siyosati kesh va navbat uchun boshqacha. Toza kesh uchun `allkeys-lru` yoki `allkeys-lfu` to'g'ri, joy tugaganda eski kalit chiqib ketadi. Idempotentlik kaliti yoki navbat saqlanadigan Redis da `allkeys-lru` ma'lumot yo'qotadi, u yerda `noeviction` va alohida instance kerak.

```bash
# Xotira va fragmentatsiya holati
redis-cli info memory | grep -E 'used_memory_human|maxmemory_human|mem_fragmentation_ratio'

# Kesh uchun: chegara, LRU, fon rejimida bo'shatish
redis-cli config set maxmemory 6gb
redis-cli config set maxmemory-policy allkeys-lru
redis-cli config set lazyfree-lazy-eviction yes

# Hit nisbati va chiqarib tashlangan kalitlar soni
redis-cli info stats | grep -E 'evicted_keys|keyspace_hits|keyspace_misses'

# 10 ms dan uzun buyruqlarni yozib borish
redis-cli config set slowlog-log-slower-than 10000
redis-cli slowlog get 10
```

`evicted_keys` o'sib borayotgan bo'lsa hit nisbati tushadi va DB yuklamasi jim oshadi. Bu metrika doimiy kuzatiladigan ro'yxatda bo'lsin.

## 28.10 Katta kalit, uzun ro'yxat va KEYS buyrug'i xavfi

`KEYS *` produksiyada ishga tushirilmaydi. U butun keyspace ni bitta thread da aylanib chiqadi, million kalitda bu bir necha soniya, va shu vaqtda Redis javob bermaydi. O'rniga kursor bilan yuradigan `SCAN` ishlatiladi. Spring tomonida ham shunga mos holat bor: Redis da butun kesh nomini tozalash prefiks bo'yicha skan va o'chirishga aylanadi, shuning uchun katta kesh ustida `@CacheEvict(allEntries = true)` arzon emas.

Katta kalit ikkinchi tuzoq. 10 MB lik JSON ni bitta kalitga yozish tarmoqni, serializatsiyani va bitta thread ni birdan uradi. Amaliy chegara: kesh qiymati taxminan 100 KB dan oshmasin, 1 MB esa kalitni bo'laklash signali.

| Tuzoq | Nimaga olib keladi | Yechim |
| --- | --- | --- |
| `KEYS` yoki keng `allEntries` tozalash | Redis bir necha soniya javob bermaydi | `SCAN`, yoki versiya kaliti bilan tozalashsiz invalidatsiya |
| 5 MB lik kesh qiymati | Tarmoq va bitta thread to'yinadi, latency sakraydi | Kerakli maydonlardan DTO, sahifalab bo'lish |
| `maxmemory` belgilanmagan | OOM yoki swap, latency yuz barobar | Chegara fizik xotiraning 70 foizi, LRU siyosati |
| Hamma kalitga bir xil TTL | TTL tugaganda to'lqin, DB ga stampede | TTL ga 10 dan 20 foiz jitter |
| Entity ni kesh kaliti qilish | Kutilmagan kalitlar, nol hit nisbati | Primitiv argumentlardan aniq `key` ifodasi |
| Tranzaksiya ichida `@CacheEvict` | Rollback dan keyin keshda eski qiymat | `AFTER_COMMIT` fazasida tozalash |
| `null` ni keshlamaslik | Mavjud bo'lmagan ID bilan DB ni urish | "Yo'q" javobini 30 soniyaga keshlash |
| Navbat va kesh bir Redis da | LRU idempotentlik kalitini o'chiradi | Alohida instance, `noeviction` siyosati |
| Timeout sozlanmagan | Redis sekinlashsa butun thread pool bloklanadi | Komanda timeout 100 dan 200 ms gacha |

## 28.11 Serializatsiya tanlovi va kesh qiymati hajmi

JDK serializatsiyasi eng yomon tanlov. Natija JSON dan katta, boshqa tildan o'qilmaydi, va sinf tuzilishi o'zgarganda deploy paytida eski yozuvlar xatolik beradi. Kesh uchun JSON ishlatiladi, u `redis-cli` dan ko'rinadi va debug qilinadi.

JSON ning narxi ham bor. Tur ma'lumoti saqlanadigan variantda har yozuvga sinf nomi qo'shiladi va kichik qiymatlarda ustama 30 foizga yetadi. Ikkinchi xavf shu: sinf nomi qiymat ichida saqlansa, paket nomini o'zgartirish barcha kesh yozuvini o'qilmas qiladi.

Amaliy qoida: keshga entity emas, barqaror DTO yoziladi. Buyurtma kartochkasi uchun bu taxminan 15 maydon, 600 bayt atrofida. Butun entity ni mijoz, manzil va qatorlar grafi bilan yozsangiz, o'sha narsa 20 KB ga chiqadi. 500 ming kalit uchun farq 300 MB va 10 GB orasida.

```yaml
spring:
  data:
    redis:
      timeout: 150ms          # Redis sekinlashsa tez taslim bo'lish
      connect-timeout: 200ms
      lettuce:
        pool:
          max-active: 16      # Lettuce multiplekslaydi, katta pool kerak emas
          max-idle: 8
          max-wait: 100ms     # cheksiz kutmaslik
  cache:
    type: redis
    redis:
      time-to-live: 300s      # standart TTL, kesh nomi bo'yicha alohida sozlanadi
      cache-null-values: true # mavjud emas javobini ham keshlash
      key-prefix: "sotuv:"
```

Timeout bu yerda eng muhim qator. Redis sekinlashsa chaqiruvchi thread uzoq kutadi, servlet thread pool to'ladi va butun servis javob bermay qoladi. 150 ms timeout bilan kesh chaqiruvi tez xato beradi va siz zaxira yo'lga o'tasiz.

## 28.12 Kesh ishlamay qolganda tizim yiqilmasligi

Kesh ixtiyoriy komponent bo'lishi kerak, majburiy emas. Redis o'chganda to'lov servisi to'xtasa, siz tezlik uchun ishonchlilikni sotib bo'lgansiz. Spring da bunga javob bor, `CacheErrorHandler` interfeysi. U kesh xatosini tutadi va tanlov beradi: xatoni yuqoriga chiqarish yoki log yozib metodni odatdagicha ishga tushirish.

```java
@Configuration
@EnableCaching
class KeshXatoSozlamasi implements CachingConfigurer {

  private static final Logger log = LoggerFactory.getLogger(KeshXatoSozlamasi.class);

  @Override
  public CacheErrorHandler errorHandler() {
    return new CacheErrorHandler() {
      // O'qishda xato: kesh yo'q deb hisoblanadi, metod DB ga boradi
      public void handleCacheGetError(RuntimeException e, Cache c, Object key) {
        log.warn("kesh o'qish xatosi, kesh={} kalit={}", c.getName(), key, e);
      }
      public void handleCachePutError(RuntimeException e, Cache c, Object key, Object v) {
        log.warn("kesh yozish xatosi, kesh={}", c.getName(), e);
      }
      // Tozalashda xato jiddiyroq: eski qiymat keshda qolib ketishi mumkin
      public void handleCacheEvictError(RuntimeException e, Cache c, Object key) {
        log.error("kesh tozalash xatosi, kalit={} eskirish xavfi bor", key, e);
      }
      public void handleCacheClearError(RuntimeException e, Cache c) {
        log.error("to'liq tozalash xatosi, kesh={}", c.getName(), e);
      }
    };
  }
}
```

Lekin xatoni yutish yetarli emas. Redis o'chganda hit nisbati nolga tushadi va 10 000 QPS ning hammasi DB ga boradi. DB bunga tayyor emas. Shuning uchun zaxira yo'lda ikki himoya kerak: og'ir so'rovlar uchun semafor bilan parallellik chegarasi, va eng qimmat hisobotlar uchun mahalliy Caffeine qatlami. Mexanizmlarning o'zi dizayn [patternlar hujjatida](../patterns/README.md), bu yerda muhimi shu: zaxira yo'l ham sig'im hisobiga ega bo'lsin.

Zaxira yo'l yozilgan bo'lsa yetarli emas, u sinovdan o'tishi kerak. Produksiyaga o'xshash muhitda Redis ni ataylab o'chirib, latency va DB connection pool holatini o'lchash kerak. Texnikani [testlash qo'llanmasidagi](../testing/README.md) resilience testlari bo'limi beradi, arxitektorning ishi bu sinovni rejaga kiritish.

Sig'im hisobining o'zi uchun esa Google ning qoidasi tayyor formula beradi: keshni latency maqsadiga yetish uchun, asosiy ilovani esa umumiy yukka qarab ta'minlang. Kitob bu qoidani production dan chiqqan dars deb ataydi va natijasini ham aytadi: kesh qatlami yo'qolganda nosozlik bo'lmagan, chunki keshsiz yo'l butun yukni ko'tarishga ta'minlangan edi, garchi yuqoriroq latency bilan. Kelishuv ham ochiq yozilgan: kesh sig'imi yo'qolishi riskini yumshatish uchun ortiqcha zaxiraga qancha sarflash kerakligi ongli qaror.

Amalda bu [8.2](08-ishlash-va-resurs-hissi-napkin-math.md#82-oddiy-hisob-kuniga-n-sorov-nechta-rps-boladi-choqqi-koeffitsienti) dagi hisobni ikki marta bajarishni bildiradi. Birinchi hisob kesh bor holat uchun: 10 000 QPS, hit nisbati 0.95, demak DB ga 500 QPS. Ikkinchi hisob kesh yo'q holat uchun: DB ga 10 000 QPS. Ikkinchi raqam uchun connection pool, `statement_timeout` va CPU sig'imi yetmasa, yechim uchtadan biri bo'ladi: DB sig'imini oshirish, zaxira yo'lda semafor bilan parallellikni cheklash, yoki quyidagi qoida bo'yicha funksiyani vaqtincha o'chirish.

Oxirgi variant alohida izoh talab qiladi, chunki u birinchi qarashda yechim emas, taslim bo'lish ko'rinadi. Newman esa uni ochiq tavsiya qiladi: ba'zan eng xavfsiz yo'l kesh ishlamay qolganda funksiyani o'chirish bo'ladi, aynan origin ortiqcha yuklanib jiddiyroq muammo keltirmasligi uchun. Shaklining tanlovi biznes savoliga qisqaradi: "eng ko'p sotilgan 10 mahsulot" bloki vaqtincha ko'rinmasligi butun katalogning sekinlashishidan arzonroqmi. Shu sababli har kesh uchun ADR da bitta qator bo'ladi: kesh o'lganda zaxira yo'l ishlaydimi, parallellik cheklanadimi, yoki funksiya o'chadimi.

## 28.13 Amalda qo'llash

- [ ] Har bir `@Cacheable` metod uchun jadval tuz: kesh nomi, TTL, kutilayotgan hit nisbati, toqat qilinadigan eskirish, qiymat hajmi. Bo'sh katak qolsa, o'sha kesh asossiz.
- [ ] Kesh qo'yishdan oldin so'rovni `EXPLAIN (ANALYZE, BUFFERS)` bilan o'lcha, N+1 yoki yo'q index emasligini isbotlab tiketga yoz.
- [ ] Caffeine da `recordStats()` yoq, Redis da `keyspace_hits`, `keyspace_misses`, `evicted_keys` ni metrikaga chiqar va hit nisbatiga ogohlantirish chegarasi qo'y.
- [ ] `@CacheEvict` chaqiruvlarini tranzaksiya ichidan `AFTER_COMMIT` fazasiga ko'chir, rollback holatini bitta test bilan yop.
- [ ] Eng qimmat uchta keshga `sync = true` va TTL ga 10 dan 20 foizgacha jitter qo'sh, bo'sh kesh ustiga yuklama berib DB so'rovini o'lch.
- [ ] `maxmemory` ni fizik xotiraning 70 foizida, siyosatni `allkeys-lru` da belgila, navbat va idempotentlik kalitlarini alohida instance ga ko'chir.
- [ ] Komanda timeout ini 100 dan 200 ms orasida sozla, `CacheErrorHandler` ni ula, Redis o'chirilgan holatda kritik yo'lni sinab ko'r.
- [ ] Kesh qiymatlarini entity dan barqaror DTO ga o'tkaz, eng katta kalitlarni `MEMORY USAGE` bilan o'lchab, 100 KB dan oshganini bo'lakla.

## Manbalar

- Sam Newman, *Building Microservices*, 2-nashr, O'Reilly, 2021, 13-bob ("The Golden Rule of Caching") - kesh qatlami ko'paygan sari ma'lumotning eskirishi va yangiligini aniqlash qiyinlashishi, ikki qatlamli bir daqiqalik TTL ning ikki daqiqaga aylanishi, keshni ishlash optimizatsiyasi deb qarash va ideal joy soni nol. Bu nashrning elektron nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- [Caffeine, README](https://raw.githubusercontent.com/ben-manes/caffeine/92cd6cca5fed23d8343ef7caf338631c977ae9ec/README.md) - `maximumSize`, `expireAfterWrite`, `refreshAfterWrite`; eskirgan yozuvga birinchi so'rov kelganda yangilash asinxron boshlanishi
- [Micrometer, Concepts](https://raw.githubusercontent.com/micrometer-metrics/micrometer-docs/06f377a95db21894939c6fff39441fe608e804a2/src/docs/concepts/index.adoc) - kesh metrikasi va teg kardinalligi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 13-bob ("Where to Cache", "Freshness Versus Optimization" bo'limlari) - client-side, server-side va request keshning kelishuvlari (tarmoq chaqiruvini yo'qotish va robustness; invalidatsiya tanlovining cheklanishi va iste'molchilar orasidagi nomuvofiqlik; umumiy Redis ning round trip qo'shishi; server-side keshning iste'molchiga ko'rinmasligi va write-through ni osonlashtirishi), hamda kesh ishlamay qolganda origin ni ortiqcha yuklamaslik uchun funksiyani o'chirish. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 25-bob ("Managing State" bo'limi) - keshni latency maqsadiga, asosiy ilovani esa umumiy yukka qarab ta'minlash, keshsiz yo'lning butun yukni (yuqoriroq latency bilan) ko'tarishi va ortiqcha zaxira narxining ongli kelishuv ekani
- ESLATMA: 28.12 dagi ikki marta sig'im hisobi (10 000 QPS va 0.95 hit nisbati misoli) hamda har kesh uchun ADR qatori tavsiyasi shu korpusning qo'shimchasi

---

[&larr; 27. Sozlash, connection pool va monitoring](27-sozlash-connection-pool-va-monitoring.md) · [Mundarija](README.md) · [29. Kafka operatsion haqiqati: partition, lag, rebalance, idempotentlik &rarr;](29-kafka-operatsion-haqiqati-partition-lag.md)
