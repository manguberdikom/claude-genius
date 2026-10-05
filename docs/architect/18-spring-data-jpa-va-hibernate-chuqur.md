<!-- doc: architect | chapter: 18 | part: III. Spring chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 18. Spring Data JPA va Hibernate chuqur (Spring Data JPA and Hibernate)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [18.1 Persistence context: birinchi daraja kesh, dirty checking, flush tartibi](#181-persistence-context-birinchi-daraja-kesh-dirty-checking-flush-tartibi)
- [18.2 Entity holatlari: transient, managed, detached, removed va ular orasidagi o'tish](#182-entity-holatlari-transient-managed-detached-removed-va-ular-orasidagi-otish)
- [18.3 Lazy loading mexanikasi, proxy va `LazyInitializationException` sababi](#183-lazy-loading-mexanikasi-proxy-va-lazyinitializationexception-sababi)
- [18.4 N+1 so'rov muammosi: topish usuli va to'rt xil yechim](#184-n1-sorov-muammosi-topish-usuli-va-tort-xil-yechim)
- [18.5 Faqat kerakli ustunni olish: interfeys va record proyeksiyasi](#185-faqat-kerakli-ustunni-olish-interfeys-va-record-proyeksiyasi)
- [18.6 `@OneToMany` to'plamlar: `List` va `Set` farqi, yangilashdagi tuzoqlar](#186-onetomany-toplamlar-list-va-set-farqi-yangilashdagi-tuzoqlar)
- [18.7 Identifikator strategiyalari: `IDENTITY`, `SEQUENCE` va batch insert ga ta'siri](#187-identifikator-strategiyalari-identity-sequence-va-batch-insert-ga-tasiri)
- [18.8 Optimistik va pessimistik lock: `@Version`, `PESSIMISTIC_WRITE` qachon](#188-optimistik-va-pessimistik-lock-version-pessimistic_write-qachon)
- [18.9 Hibernate statistikasi va yozilgan SQL ni ko'rish sozlamalari](#189-hibernate-statistikasi-va-yozilgan-sql-ni-korish-sozlamalari)
- [18.10 Spring Data metod nomlari, `@Query`, `Specification` va ularning chegarasi](#1810-spring-data-metod-nomlari-query-specification-va-ularning-chegarasi)
- [18.11 Qachon JPA dan voz kechib `JdbcClient` yoki to'g'ridan-to'g'ri SQL yozish kerak](#1811-qachon-jpa-dan-voz-kechib-jdbcclient-yoki-togridan-togri-sql-yozish-kerak)
- [18.12 Ikkinchi daraja kesh: foydasi va xavfi](#1812-ikkinchi-daraja-kesh-foydasi-va-xavfi)
- [18.13 Amalda qo'llash](#1813-amalda-qollash)

</details>



Hibernate bilan ishlashdagi eng keng tarqalgan xato uni "ob'ektni jadvalga saqlaydigan kutubxona" deb tushunishdir. Aslida u tranzaksiya davomida yashaydigan holat mashinasi: o'zi ushlab turgan ob'ektlarni kuzatadi, o'zgarishlarni to'playdi va qat'iy belgilangan paytda SQL ga aylantiradi. Arxitektor uchun asosiy savol "qanday annotatsiya qo'yaman" emas, "bu kod oxirida PostgreSQL ga nechta va qanday so'rov ketadi" degan savol. Bob shu savol atrofida quriladi.

## 18.1 Persistence context: birinchi daraja kesh, dirty checking, flush tartibi

Persistence context bu `EntityManager` ichidagi identity map: kalit birlamchi kalit, qiymat managed entity. Bir tranzaksiyada bitta `id` bo'yicha ikki marta `findById` chaqirsangiz, ikkinchisi SQL yubormaydi. Bu keshni o'chirib ham, sozlab ham bo'lmaydi, u faqat session hayotiga bog'liq.

Dirty checking shu identity map ustida ishlaydi. Entity yuklanganda Hibernate uning maydonlarini alohida massivga nusxalab oladi. Flush da har bir managed entity ning joriy qiymatlari shu nusxaga maydon-maydon solishtiriladi. Demak dirty checking narxi persistence context dagi entity soniga proportsional va har flush da qaytariladi. 50 ming entity ni bitta tranzaksiyaga yuklab, ichida 1000 so'rov bajarsangiz, 50 million maydon taqqoslash olasiz.

Flush uch holatda bo'ladi: commit dan oldin, `flush()` ni qo'lda chaqirganda, va so'rovdan oldin, agar so'rov tegadigan jadvalga navbatda o'zgarish bor bo'lsa. Flush dagi SQL tartibi sizning kod tartibingizga emas, Hibernate ning action queue siga bog'liq: avval orphan removal, keyin insert, keyin update, keyin to'plam o'chirish va yangilash, eng oxirida entity delete.

```java
@Transactional
public void hisobniYopish(Long buyurtmaId) {
    Buyurtma b = buyurtmaRepo.findById(buyurtmaId).orElseThrow();
    b.setHolat(Holat.YOPILGAN);   // hali hech qanday UPDATE yo'q
    // save() shart emas: b managed, dirty checking o'zi topadi.
    // bu so'rov buyurtma jadvaliga tegadi, shuning uchun UPDATE
    // ANA SHU YERDA yuboriladi, commit da emas
    long ochiq = buyurtmaRepo.countByHolat(Holat.OCHIQ);
    log.info("qolgan ochiq buyurtma: {}", ochiq);
}
```

Shu tartib bitta klassik xatoni tug'diradi: unique constraint ostidagi qatorni o'chirib, o'rniga yangisini qo'shsangiz, avval INSERT ketadi va constraint buziladi. Yechim ikkisi orasida aniq `flush()` chaqirish yoki amalni bitta UPDATE ga aylantirish.

## 18.2 Entity holatlari: transient, managed, detached, removed va ular orasidagi o'tish

Transient: `new` qilingan, identifikatori yo'q. Managed: persistence context ichida, dirty checking ostida. Detached: ilgari managed bo'lgan, identifikatori bor, lekin o'zgarishlari kuzatilmaydi. Removed: `remove` chaqirilgan, flush da DELETE ketadi.

Eng ko'p xato detached bilan bo'ladi. Controller ga kelgan JSON dan `Tolov` yasalib `save()` chaqirilsa, Spring Data `isNew()` ni tekshiradi: identifikator bo'sh bo'lsa `persist`, aks holda `merge`. `merge` esa avval bazadan shu id ni SELECT qiladi, qiymatlarni managed nusxaga ko'chiradi va MANAGED NUSXANI qaytaradi. Siz uzatgan ob'ekt detached bo'lib qoladi.

```java
// XATO: natija tashlab yuborilgan, tolov hali ham detached
tolovRepo.save(detachedTolov);
detachedTolov.setHolat(Holat.TASDIQLANGAN); // hech qayerga yozilmaydi

// TO'G'RI: merge dan butunlay qochish, bitta SELECT va bitta UPDATE
Tolov managed = tolovRepo.findById(dto.id()).orElseThrow();
managed.applyFrom(dto);
```

`merge` ning yashirin narxi ham shu: har bir `save` uchun qo'shimcha SELECT. Mingta qatorni yangilovchi importda bu mingta keraksiz so'rov.

## 18.3 Lazy loading mexanikasi, proxy va `LazyInitializationException` sababi

Lazy bog'lanish proxy orqali ishlaydi. Hibernate bayt-kod darajasida entity sinfidan voris yasaydi, uning ichida faqat identifikator to'ldirilgan bo'ladi. Birinchi metod chaqirilganda proxy o'z session iga murojaat qilib SELECT yuboradi va o'zini to'ldiradi. To'plamlar uchun `PersistentBag` yoki `PersistentSet` xuddi shunday kechiktirilgan.

`LazyInitializationException` proxy o'z session ini topolmaganda tashlanadi: tranzaksiya yopilgan, lekin ob'ekt hali hayot va kimdir uning to'ldirilmagan qismini so'rayapti. Bu entity ni DTO ga aylantirmasdan controller ga qaytarganda yuz beradi.

Bu yerda `spring.jpa.open-in-view` haqida aniq pozitsiya kerak. Spring Boot da u sukut bo'yicha yoqilgan va session ni HTTP javob yozilib bo'lguncha ochiq ushlaydi. Xato "yo'qoladi", o'rniga ikki yomonroq narsa keladi: serializatsiya paytidagi kutilmagan SELECT lar va connection ning javob tugaguncha pool da band turishi. 10 connection li pool da bu throughput ni sezilarli pasaytiradi.

```yaml
spring:
  jpa:
    open-in-view: false   # session ni HTTP qatlamiga chiqarmaymiz
    properties:
      hibernate:
        # pagination ustida collection fetch ni jim kechirmaslik
        query.fail_on_pagination_over_collection_fetch: true
        default_batch_fetch_size: 50
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
```

## 18.4 N+1 so'rov muammosi: topish usuli va to'rt xil yechim

N+1 ni ko'z bilan topish qiyin, kod toza ko'rinadi. Uni raqam bilan topish kerak: statistikani yoqib, bitta use case dagi so'rov sonini o'lchash. 20 buyurtmani mijozi bilan ko'rsatadigan endpoint 21 so'rov yuborsa, bu N+1.

```sql
-- bitta ro'yxat so'rovi
select b.id, b.mijoz_id, b.summa from buyurtma b where b.holat = 'OCHIQ';
-- keyin har qator uchun alohida so'rov, 20 marta
select m.id, m.nomi from mijoz m where m.id = 101;
select m.id, m.nomi from mijoz m where m.id = 102;
```

Birinchi yechim `join fetch`: bitta so'rovda hammasi. To'plam bilan ishlatganda dekart ko'paytmasi paydo bo'ladi, shuning uchun `Set` yoki `distinct` kerak. Muhimi: to'plam fetch bilan `Pageable` ni birga ishlatib bo'lmaydi, Hibernate hamma qatorni xotiraga olib, kesishni Java da bajaradi. Yuqoridagi `fail_on_pagination_over_collection_fetch` aynan shuni xatoga aylantiradi.

Ikkinchi yechim `@EntityGraph`: bir metod uchun deklarativ fetch rejasi. Uchinchi yechim `@BatchSize` yoki global `default_batch_fetch_size`: Hibernate N alohida so'rov o'rniga `where id in (?, ?, ...)` bilan guruhlaydi va 21 so'rov 2 ga tushadi. To'rtinchi va ko'pincha eng to'g'ri yechim: entity ni umuman yuklamaslik, faqat kerakli ustunlarni proyeksiya qilish.

```java
// 1) join fetch: to'plamsiz bog'lanish uchun eng sodda
@Query("select b from Buyurtma b join fetch b.mijoz where b.holat = :h")
List<Buyurtma> ochiqBuyurtmalar(@Param("h") Holat h);

// 2) entity graph: to'plam bo'lmasa pagination bilan ham xavfsiz
@EntityGraph(attributePaths = {"mijoz", "valyuta"})
Page<Buyurtma> findByHolat(Holat holat, Pageable pageable);

// 3) batch fetch: to'plamni guruhlab olish
@OneToMany(mappedBy = "buyurtma", fetch = FetchType.LAZY)
@BatchSize(size = 50)
private Set<BuyurtmaQatori> qatorlar;
```

Tanlash qoidasi: ro'yxat ekrani uchun proyeksiya, bitta ob'ektni tahrirlash uchun entity graph, oldindan bilinmaydigan navigatsiya uchun global batch fetch size.

| Tuzoq | Nega yuz beradi | Yechim |
| --- | --- | --- |
| `MultipleBagFetchException` | ikki `List` to'plam bir so'rovda fetch qilingan | to'plamlarni `Set` ga o'tkazish yoki birini batch fetch ga qoldirish |
| Noto'g'ri sahifa | collection fetch da limit xotirada qo'llanadi | sahifada faqat id larni olib, ikkinchi so'rovda fetch qilish |
| Takroriy qatorlar | `join fetch` dekart ko'paytmasi | `Set` ishlatish yoki `distinct` |
| `List` dan bitta element o'chirishda hamma qator qayta yozilishi | bag semantikasi | `Set` yoki `@OrderColumn` |
| `IDENTITY` da batch insert ishlamasligi | har insert dan keyin id o'qilishi shart | `SEQUENCE` ga o'tish |
| Importda har `save` da SELECT | detached ob'ekt uchun `merge` | yangi ob'ektlarda id ni bo'sh qoldirish |

## 18.5 Faqat kerakli ustunni olish: interfeys va record proyeksiyasi

Hisobot ekranida entity yuklash sof yo'qotish: 30 ustun, nusxa massiv va identity map yozuvini to'laysiz, ekranga 4 ustun chiqadi. Interfeys proyeksiyasi faqat getter lardan tashkil topadi va Hibernate kerakli ustunlarni tanlab oladi. Record proyeksiyasi esa DTO ni bevosita so'rov natijasi qiladi.

```java
public record BuyurtmaSatri(Long id, BigDecimal summa, String mijozNomi) {}

public interface BuyurtmaRepo extends JpaRepository<Buyurtma, Long> {

    @Query("""
           select new com.ombor.dto.BuyurtmaSatri(b.id, b.summa, b.mijoz.nomi)
           from Buyurtma b where b.holat = :h
           """)
    List<BuyurtmaSatri> satrlar(@Param("h") Holat h);

    // dinamik proyeksiya: bitta so'rov, turli shakldagi natija
    <T> List<T> findBySanaAfter(LocalDate sana, Class<T> turi);
}
```

```sql
-- natijadagi SQL aynan shunday, qo'shimcha so'rov qolmaydi
select b.id, b.summa, m.nomi
from buyurtma b join mijoz m on m.id = b.mijoz_id
where b.holat = 'OCHIQ';
```

Muhim chegara: proyeksiya faqat o'qish uchun. Natijani o'zgartirib saqlash kerak bo'lsa, entity kerak. Shuning uchun repository da ikki xil metod bo'ladi: ekran uchun proyeksiya, buyruq uchun entity.

## 18.6 `@OneToMany` to'plamlar: `List` va `Set` farqi, yangilashdagi tuzoqlar

`@OrderColumn` siz `List` bu bag: tartibsiz va takrorlanishga ruxsat beradigan to'plam. Hibernate bag dan bitta elementni o'chirishni ifodalay olmaydi, chunki qatorni aniqlovchi pozitsiya yo'q. Shu sababli butun bog'lanishni o'chirib, qolganini qayta kiritadi. 200 qatorli buyurtmadan bitta qatorni olsangiz, bazaga 1 DELETE va 199 INSERT ketadi.

```sql
-- List (bag) dan bitta qator o'chirilganda
delete from buyurtma_qatori where buyurtma_id = 42;
insert into buyurtma_qatori (buyurtma_id, mahsulot_kodi, soni) values (42, 'A-1', 3);
-- ... qolgan 198 qator qayta kiritiladi

-- Set da xuddi shu amal
delete from buyurtma_qatori where id = 7781;
```

`Set` da bu muammo yo'q, sharti `equals` va `hashCode` ni to'g'ri yozish. Ularni `id` ustiga qurish xato: yangi element hali id siz bo'lganda hashCode o'zgarib ketadi va `Set` buziladi. To'g'ri yo'l biznes kaliti yoki ilova tomonida yasalgan UUID.

Ikkinchi tuzoq: to'plamni to'liq almashtirish. `setQatorlar(yangiRoyxat)` Hibernate kuzatayotgan to'plam ob'ektini tashlab yuboradi va butun to'plam qayta yoziladi. To'g'ri usul ichini o'zgartirish, yaxshisi `addQator` va `removeQator` metodlari orqali ikki tomonni sinxron ushlash. `orphanRemoval = true` bo'lsa, to'plamdan chiqarilgan element bazadan ham o'chadi va buyurtma qatorlari uchun bu aynan kerakli xatti-harakat.

## 18.7 Identifikator strategiyalari: `IDENTITY`, `SEQUENCE` va batch insert ga ta'siri

`IDENTITY` PostgreSQL da identity ustunga tayanadi va qiymat faqat INSERT dan keyin ma'lum bo'ladi. Hibernate esa identity map ga qo'shish uchun identifikatorni darhol talab qiladi. Natijada `persist` chaqirilgan zahoti INSERT ketadi va batch yig'ish imkoniyati butunlay yo'qoladi. 10 ming qatorli import 10 ming round trip ga aylanadi, har biri taxminan 0.3 dan 1 ms bo'lsa, faqat tarmoqqa 3 dan 10 sekund ketadi.

`SEQUENCE` da Hibernate `nextval` ni oldindan so'rab, id ni INSERT dan oldin biladi. `allocationSize` bilan pooled optimizer ishlaydi: bitta `nextval` dan keyin 50 id ilova xotirasida tarqatiladi. Shart: baza sequence idagi `increment by` qiymati `allocationSize` ga teng bo'lishi kerak.

```java
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "harakat_seq_gen")
@SequenceGenerator(name = "harakat_seq_gen",
                   sequenceName = "harakat_seq",
                   allocationSize = 50)   // sequence increment by 50 bo'lishi shart
private Long id;
```

Batch ishlashi uchun `jdbc.batch_size` dan tashqari `order_inserts` va `order_updates` ham kerak, aks holda turli entity turlari aralashganda batch uzilib ketadi. `@Version` ishlatilsa, versiyali qatorlarni batch qilish sozlamasi `hibernate.jdbc.batch_versioned_data` deb nomlanadi va uni yoqish ko'pincha shart emas: Hibernate hujjatida uning standart qiymati "generally `true`, though can vary based on Dialect" deb yozilgan, ya'ni tekshirish kerak, qo'shish emas. Batch size uchun boshlang'ich nuqta 50 dan 100 gacha olinadi, lekin bu o'lchanmagan taxmin: chegarani o'z yuklamangizda o'lchab tanlang, chunki foydali qiymat qator kengligi va tarmoq kechikishiga bog'liq.

## 18.8 Optimistik va pessimistik lock: `@Version`, `PESSIMISTIC_WRITE` qachon

`@Version` qo'shilganda Hibernate har UPDATE ga versiya shartini qo'shadi. UPDATE 0 qator o'zgartirsa, kimdir oldin ulgurgan va Hibernate `OptimisticLockException` tashlaydi, Spring uni `ObjectOptimisticLockingFailureException` ga o'raydi. Hech qanday lock olinmaydi, shuning uchun bu usul arzon va nizo kam bo'lgan joyda to'g'ri tanlov: foydalanuvchi tahrirlaydigan kartochka, profil, buyurtma sarlavhasi.

```sql
-- optimistik: versiya shart ichida, 0 qator qaytsa ilova xato tashlaydi
update buyurtma set holat = 'YOPILGAN', version = 8 where id = 42 and version = 7;

-- pessimistik: qator commit gacha band qilinadi
select qoldiq from ombor_qoldiq where mahsulot_kodi = 'A-1' for update;
```

Pessimistik lock boshqa hol uchun: qiymat o'qilgandan keyin darhol unga tayanib yoziladigan va retry qimmat joylar, ya'ni ombor qoldig'i va hisobdan pul yechish. `PESSIMISTIC_WRITE` PostgreSQL da `FOR UPDATE` ga aylanadi.

```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
Optional<OmborQoldiq> findByMahsulotKodi(String kod);

// navbat shaklidagi ish: band qatorlarni butunlay chetlab o'tish
@Query(value = """
       select * from tolov_vazifa where holat = 'YANGI'
       order by id limit :n for update skip locked
       """, nativeQuery = true)
List<TolovVazifa> navbatdanOl(@Param("n") int n);
```

Pessimistik lock da ikki raqamni oldindan belgilash kerak: lock kutish vaqti va tranzaksiya uzunligi. PostgreSQL da `lock_timeout` ni tranzaksiya boshida taxminan 3 sekundga qo'yish xavfsiz amaliyot. Lock ushlab turgan tranzaksiya ichida tashqi HTTP chaqiruv qilish esa jiddiy xato: tashqi servis sekinlashsa, hamma qoldiq yangilash navbatga tizilib qoladi.

## 18.9 Hibernate statistikasi va yozilgan SQL ni ko'rish sozlamalari

`spring.jpa.show-sql=true` ni lokalda ham ishlatmaslik kerak: u System.out ga yozadi, parametrlarni ko'rsatmaydi va log tizimidan tashqarida qoladi. To'g'ri sozlama logger lar orqali.

```properties
logging.level.org.hibernate.SQL=DEBUG
# bog'langan parametrlar, Hibernate 6 da aynan shu logger
logging.level.org.hibernate.orm.jdbc.bind=TRACE
spring.jpa.properties.hibernate.generate_statistics=true
logging.level.org.hibernate.stat=DEBUG
# chegaradan sekin so'rovlarni alohida belgilash, ms
spring.jpa.properties.hibernate.session.events.log.LOG_QUERIES_SLOWER_THAN_MS=100
```

`generate_statistics` yoqilganda har session tugaganda qisqa hisobot chiqadi: nechta JDBC statement, nechta so'rov, nechta collection fetch, qancha vaqt. Shu raqam N+1 ni ob'ektiv aniqlaydi. Uni production da doimiy yoqmaslik kerak, lekin yuklama va integratsiya testlarida yoqish kerak. Eng foydali qoida: muhim use case uchun so'rov sonini test bilan qotirib qo'yish, ya'ni "buyurtma ro'yxati 3 so'rovdan oshmaydi". Buni qanday yozish [testlash qo'llanmasidagi](../testing/README.md) Spring slice testlari bo'limiga tegishli.

## 18.10 Spring Data metod nomlari, `@Query`, `Specification` va ularning chegarasi

Metod nomi bo'yicha so'rov sodda holat uchun ideal, lekin tez buziladi. `findByHolatAndSanaBetweenAndMijozShahriOrderBySummaDesc` kabi nom o'qilmaydi. Amaliy chegara ikki, ko'pi bilan uch shart. Undan keyin `@Query` ga o'tish kerak, chunki JPQL matni review qilinadi.

`Specification` dinamik filtr uchun: foydalanuvchi 8 filtrdan ixtiyoriy kombinatsiyani tanlasa, har biri uchun metod yozib bo'lmaydi. Narxi bor: Criteria kodi SQL dan uch barobar uzun va nima generatsiya bo'lishini ko'rish qiyin. Yana bir chegara: `Specification` va `Pageable` birga kelganda count so'rovi ham shu specification bilan quriladi, va unda fetch join xatoga olib keladi. Shuning uchun specification ichida natija turini tekshirib, count paytida fetch qo'shmaslik kerak.

Eng muhim chegara shu: JPQL ham, Criteria ham PostgreSQL ning kuchli qismini ifodalay olmaydi. Window funksiya, CTE, `distinct on`, `lateral`, `jsonb` operatorlari, to'liq matn qidirish va `insert ... on conflict` JPA modeliga sig'maydi. Bu yerda kurashish kerak emas.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Ro'yxat ekrani | entity yuklash, keyin DTO ga mapping | so'rovda record proyeksiyasi, entity yuklanmaydi |
| Lazy xato | `open-in-view` ni yoqib qo'yish | `open-in-view: false`, tranzaksiya ichida DTO yasash |
| N+1 | hamma bog'lanishni EAGER qilish | use case bo'yicha entity graph yoki batch fetch size |
| Ommaviy import | har qator uchun `save` | `SEQUENCE`, batch size 50, davriy `flush` va `clear` |
| Qoldiqni yechish | o'qib, hisoblab, keyin yozish | `for update` yoki bitta atomar UPDATE |
| Nizo boshqaruvi | lock umuman ishlatilmaydi | `@Version` sukut bo'yicha, `PESSIMISTIC_WRITE` faqat pul va qoldiqda |
| Hisobot | JPQL ni murakkablashtirish | `JdbcClient` va read-only tranzaksiya |
| Kesh | `@Cacheable` ni hamma joyga qo'yish | o'zgarmas ma'lumot uchun aniq region, TTL va invalidatsiya rejasi |
| Performans tekshiruvi | "sekin" degan hisga tayanish | statistikadan so'rov soni, `explain analyze` dan plan |
| Sahifalash | `offset` ni cheksiz o'stirish | katta offset da kalit bo'yicha keyset sahifalash |

## 18.11 Qachon JPA dan voz kechib `JdbcClient` yoki to'g'ridan-to'g'ri SQL yozish kerak

JPA ning kuchi domen ob'ektining hayot aylanishini boshqarishda: bitta buyurtmani yuklash, tahrirlash, saqlash. Kuchsiz joyi ommaviy o'qish va ommaviy yozish. Spring Framework 6.1 dan beri `JdbcClient` mavjud va shu bo'shliqni toza to'ldiradi: nomli parametrlar, record ga mapping.

```java
public List<KunlikTushum> kunlikTushum(LocalDate dan, LocalDate gacha) {
    // window funksiya JPQL da ifodalanmaydi, demak SQL bu yerda o'rinli
    return jdbc.sql("""
            select kun, summa, sum(summa) over (order by kun) as jamlanma
            from (select date(yaratilgan_at) kun, sum(summa) summa from tolov
                  where yaratilgan_at >= :dan and yaratilgan_at < :gacha
                  group by 1) t
            order by kun
            """)
        .param("dan", dan).param("gacha", gacha)
        .query(KunlikTushum.class).list();
}
```

Qaror mezoni sodda. Natija domen ob'ekti bo'lmasa va o'zgartirilmasa, JPA shart emas. So'rov aniq SQL konstruksiyasiga tayansa, JPA shart emas. Bir operatsiya 10 mingdan ortiq qatorga tegsa, `update ... from` yoki `insert ... on conflict` shaklidagi bitta SQL deyarli har doim entity sikldan tez. Shu paytda ikki narsa esda bo'lsin: bunday SQL persistence context ni bilmaydi, shuning uchun bir tranzaksiyada entity bilan aralashtirmaslik yaxshi, va u keshni ham chetlab o'tadi.

## 18.12 Ikkinchi daraja kesh: foydasi va xavfi

Ikkinchi daraja kesh session lar orasida yashaydi va `SessionFactory` ga tegishli. U birlamchi kalit bo'yicha entity yuklashni tezlashtiradi, yoqish uchun provider va entity da concurrency strategiyasi talab qiladi. Foydali joyi aniq: kam o'zgaradigan ma'lumot. Valyuta ro'yxati, soliq stavkasi, mahsulot kategoriyasi, mamlakat kodi. Bunday jadvallar yiliga bir necha marta o'zgaradi, ularni har so'rovda bazadan olish bekor.

Xavfi aniq. Query cache alohida mexanizm va jadvalning oxirgi o'zgarish vaqtiga tayanib bekor qilinadi, shu sababli tez o'zgaradigan jadvalda faqat xotira yeydi. Native SQL yoki JPQL `update` orqali qilingan ommaviy o'zgarish keshni bekor qilmaydi, natijada eskirgan ma'lumot qoladi. Ilova bir nechta nusxada ishlaganda mahalliy kesh nusxalari farq qiladi va foydalanuvchi so'rov qaysi nusxaga tushganiga qarab turli javob oladi.

Shuning uchun qoida: ikkinchi daraja keshni butun ilovaga yoqmaslik. Faqat sanab o'tilgan o'zgarmas entity larga, aniq TTL bilan, va o'zgarish faqat administrativ yo'l bilan bo'ladigan joyda. Qolgan holatda application darajasidagi kesh ko'proq nazorat beradi, chunki unda nima keshlangani va qachon tozalangani kodda ko'rinib turadi.

## 18.13 Amalda qo'llash

- [ ] `spring.jpa.open-in-view=false` qilib, chiqqan har bir `LazyInitializationException` ni service qatlamida proyeksiya yoki DTO bilan tuzatish.
- [ ] Eng band uchta endpoint uchun `generate_statistics` yoqib so'rov sonini o'lchash va har biriga yuqori chegarani test bilan qotirish.
- [ ] Ro'yxat va hisobot so'rovlarini record proyeksiyasiga o'tkazish, entity ni faqat yozish yo'lida qoldirish.
- [ ] `IDENTITY` ishlatayotgan entity larni topib, ommaviy yozuv bo'ladiganlarini `SEQUENCE` va `allocationSize = 50` ga ko'chirish, sequence `increment by` ni moslash.
- [ ] `jdbc.batch_size`, `order_inserts`, `order_updates` ni yoqib, import oqimida batch ishlayotganini PostgreSQL log i bo'yicha tasdiqlash.
- [ ] Pul va ombor qoldig'iga tegadigan metodlarda `@Version` yoki `PESSIMISTIC_WRITE` dan birini ongli tanlash va qarorni izoh bilan qoldirish.
- [ ] Lock ushlaydigan tranzaksiyalarda tashqi HTTP chaqiruvi yo'qligini tekshirish va `lock_timeout` ni taxminan 3 sekundga belgilash.
- [ ] Window funksiya yoki CTE talab qiladigan hisobotlarni `JdbcClient` ga chiqarib, read-only tranzaksiyada bajarish.

## Manbalar

- [hibernate-orm, `BatchSettings.java` (6.6)](https://raw.githubusercontent.com/hibernate/hibernate-orm/6.6/hibernate-core/src/main/java/org/hibernate/cfg/BatchSettings.java) - `hibernate.jdbc.batch_size` standarti 0, `hibernate.order_inserts` va `hibernate.order_updates` standarti `false`, `hibernate.jdbc.batch_versioned_data` standarti "generally `true`"
- [Hibernate User Guide, Batching](https://raw.githubusercontent.com/hibernate/hibernate-orm/6.6/documentation/src/main/asciidoc/userguide/chapters/batch/Batching.adoc) - "Hibernate disables insert batching at the JDBC level transparently if you use an identity identifier generator"
- [Hibernate User Guide, Identifiers](https://raw.githubusercontent.com/hibernate/hibernate-orm/6.6/documentation/src/main/asciidoc/userguide/chapters/domain/identifiers.adoc) - `allocation-size` aynan sequence ning "increment by" si; pooled va pooled-lo optimizerlari shu qiymatga tayanadi
- [jakartaee/persistence, `SequenceGenerator.java`](https://raw.githubusercontent.com/jakartaee/persistence/master/api/src/main/java/jakarta/persistence/SequenceGenerator.java) - `allocationSize() default 50`

---

[&larr; 17. Spring MVC va WebFlux: so'rov yo'li, thread modeli, REST dizayni](17-spring-mvc-va-webflux-sorov-yoli-thread.md) · [Mundarija](README.md) · [19. Spring tranzaksiyalari va ularning chegaralari &rarr;](19-spring-tranzaksiyalari-va-ularning.md)
