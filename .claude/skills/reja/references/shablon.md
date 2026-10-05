# 6-bosqich (b): REJA.md shabloni

Fayl joyi: loyiha ildizida `REJA.md`. Bir nechta reja bo'lsa -
`reja/<slug>-reja.md` (masalan `reja/outbox-reja.md`). Foydalanuvchi ochib
o'qiydigan joyda bo'lishi shart.

## Hajm matritsasi

| Hajm | Qachon | Majburiy bo'limlar |
|---|---|---|
| **S** | bitta modul, < 5 fayl, jadval tuzilishi o'zgarmaydi (indeks qo'shish mumkin), tashqi kontrakt buzilmaydi, yangi dependency yo'q | 1, 2, 3, 4, 7, 8, 9, 14, 16; 15 taxmin yoki ochiq savol bo'lsa |
| **M** | bir nechta modul yoki jadval tuzilishi o'zgaradi yoki yangi tashqi chaqiruv | 1-9, 11, 13, 14, 16; 15 taxmin yoki ochiq savol bo'lsa |
| **L** | chegara o'zgaradi, migratsiya, yangi infratuzilma, ko'p relizli ish | hammasi (1-16) |

Bo'limni bo'sh qoldirish o'rniga olib tashlash afzal. Olib tashlangan bo'lim
sababini kirishda bir qatorda aytish kerak ("sxema o'zgarmaydi - 12-bo'lim yo'q").

## Shablon

````markdown
# Reja: <qisqa nom>

| | |
|---|---|
| **Maqsad** | <bitta jumla, o'lchanadigan natija> |
| **Hajm** | S / M / L |
| **Vazifa turi** | yangi funksiya / refaktoring / bug / migratsiya / performance / integratsiya / xavfsizlik / test qarzi |
| **Sana** | YYYY-MM-DD |
| **Holat** | qoralama / kelishilgan / bajarilmoqda |
| **Taxminiy ish** | <qadamlar soni va qo'pol baho> |

## 1. Maqsad va kontekst

Nima uchun bu ish qilinadi, hozir nima og'riyapti (bir-ikki abzats, har da'vo
`fayl:qator` yoki metrika bilan).

## 2. Qamrov

**Kiradi:** <ro'yxat>

**Kirmaydi (non-goals):** <ro'yxat - bu bo'lim kelishuvni soddalashtiradi>

## 3. Aniqlangan haqiqatlar

| Haqiqat | Qiymat | Manba |
|---|---|---|
| Java / framework versiyasi | | `pom.xml:N` |
| Ma'lumotlar bazasi | | |
| New code coverage gate | | `sonar-project.properties:N` |
| Tegishli konfiguratsiya (timeout, pool, kesh) | | |
| Tegishli qoidalar (`CLAUDE.md`, ArchUnit) | | |

`TAXMIN:` bilan belgilangan qatorlar 15-bo'limga ham chiqadi.

## 4. Hozirgi holat

| Joy | Simptom | Nega muhim | Qo'llanmadagi mavzu |
|---|---|---|---|
| `X.java:120-180` | | | `patterns 25.1 (God Object)` |

Bog'liqlik eskizi (buzilgan yo'nalish `!` bilan):

```
web -> application -> domain <- infrastructure
!    domain -> infrastructure (`Order.java:14` JPA ga import)
```

## 5. Maqsadli dizayn

O'zgarishdan keyin tuzilish qanday bo'ladi: qatlamlar, yangi komponentlar,
ma'lumot oqimi. Matnli diagramma + 3-5 qator izoh. Yangi narsa nega shu joyda
turishi aytiladi.

## 6. Arxitektura qarorlari (ADR)

### ADR-1: <qaror sarlavhasi>

**Kontekst.** <o'lchov va `fayl:qator` bilan>

**Qaror.** <bitta tanlangan variant>

**Ko'rib chiqilgan variantlar.** <kamida ikkita, nega rad etilgani bilan>

**Oqibatlar.** <nima qurbon qilindi, nima qo'shildi>

**Taxminlar.** <nima to'g'ri bo'lsa qaror to'g'ri qoladi>

**Kuzatiladigan metrika.** <qaysi raqam qarorni tasdiqlaydi yoki rad etadi>

## 7. Pattern tayinlash

| Joy | Hozir | Pattern | Nega | Narxi | Qo'llanmada qidirish |
|---|---|---|---|---|---|
| `OrderService.java:142-198` | uch joyda bir xil `switch` | Strategy + registry | yangi tur mavjud kodga tegmaydi | +1 interfeys, +3 sinf | `patterns 8.21 (Strategy Registry via Map<String, Bean>)` |

Tekshirilgan anti-patternlar: <nomlari va nega tushmaydi>.

## 8. Qadamlar

Har qadam mustaqil tekshiriladi va loyihani yashil qoldiradi.

### 1-qadam. <imperativ sarlavha>

**Nega.** <bir-ikki jumla>

**Nima qilinadi.**
- `fayl` (yangi/o'zgaradi): <aniq o'zgarish>

**Qilinmaydi.** <chegara: nima bu qadamda tegilmaydi>

**Test.** <daraja, fayl, oracle>

**Qabul mezoni.** `<buyruq>` -> `<kutilgan natija>`

### 2-qadam. ...

## 9. Test matritsasi

| O'zgarish | Daraja | Joy | Ma'lumot | Oracle |
|---|---|---|---|---|

Test qiyin joylar va ularning yechimi:

| To'siq | Yechim | Qadam |
|---|---|---|

## 10. Sifat darvozasi

| Shart | Talab | Reja uchun ma'nosi |
|---|---|---|

Xavfdagi Sonar qoidalari: <o'zgarish turiga qarab, `sonarqube <raqam> (<mavzu>)` shaklida>.

Exclusion qo'shilsa: qaysi fayl, nega halol.

## 11. Risklar

| Risk | Ehtimol / ta'sir | Yumshatish va qanday bilib olamiz |
|---|---|---|

## 12. Ma'lumot va migratsiya

- Sxema o'zgarishi: expand/contract bosqichlari va qaysi reliz bilan ketishi
- Migratsiya fayli nomi va orqaga qaytarish yo'li
- Katta jadvalga indeks: `CONCURRENTLY`, kutilgan davomiylik
- Ma'lumot to'ldirish (backfill): hajm, partiya, davomiylik, qayta ishga tushirish

## 13. Reliz va qaytarish

- Tartib: migratsiya -> kod -> flag yoqish -> kuzatuv -> tozalash
- Feature flag nomi va default qiymati
- Rollback: nima qaytariladi, nima qaytmaydi (ma'lumot), qaror nuqtasi
- Kuzatiladigan signallar va alertlar

## 14. Definition of Done

- [ ] <buyruq bilan tekshiriladigan band>
- [ ] <...>

## 15. Ochiq savollar va taxminlar

| # | Savol / taxmin | Kim javob beradi | Javobsiz ta'siri |
|---|---|---|---|

## 16. Manbalar

- Kod: `fayl:qator` ro'yxati
- Config: `pom.xml`, `application.yml:22`, `sonar-project.properties:12`
- Qo'llanmalar (`<hujjat> <raqam> (<mavzu>)` shaklida):
  - `patterns 8.21 (Strategy Registry via Map<String, Bean>)`, `patterns 10.14 (Transactional Outbox)`
  - `architect 19 (Spring tranzaksiyalari va ularning chegaralari)`
  - `testing 8 (Testcontainers bilan real infratuzilmada test)`
  - `sonarqube 9 (Coverage qanday o'lchanadi)`
  - `code-review 11 (Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern)`
- Hujjatlar: `spec.pdf` s.14, 22; `prompt-design.pdf` s.3-7
- Memory: `CLAUDE.md` (Lombok taqiqi), `memory/<proyekt-slug>/MEMORY.md`, `docs/adr/0004-*.md`
````

## To'ldirilgan mikro-namuna (S hajm)

````markdown
# Reja: buyruq ro'yxatiga keyset pagination qo'shish

| | |
|---|---|
| **Maqsad** | `/api/orders` chuqur sahifa (10k+ qator) p99 1.8 s -> 300 ms, `cursor` bilan |
| **Hajm** | S |
| **Vazifa turi** | performance |

S hajm: 5, 6, 10-13 bo'limlar yo'q - jadval tuzilishi va kontrakt o'zgarmaydi,
indeks 1-qadamda. 15-bo'lim yo'q: taxmin va ochiq savol qolmadi.

## 1. Maqsad va kontekst
`OrderController.java:38` `PageRequest.of(page, size)` bilan ishlaydi; 50k
offsetda PostgreSQL 50k qatorni tashlab o'tadi (`EXPLAIN` da
`Rows Removed by Offset`). Kunlik 4k so'rovning ~12% i 10k dan katta offset.

## 2. Qamrov
Kiradi: `GET /api/orders` ro'yxati. Kirmaydi: boshqa endpointlar, UI ni
`cursor` ga o'tkazish (alohida ish).

## 3. Aniqlangan haqiqatlar
| Haqiqat | Qiymat | Manba |
|---|---|---|
| Spring Boot | 3.3.4 | `pom.xml:9` |
| Migratsiya | Flyway, oxirgisi `V11` | `db/migration/` |

## 4. Hozirgi holat
| Joy | Simptom | Nega muhim | Qo'llanmadagi mavzu |
|---|---|---|---|
| `OrderRepository.java:21` | `findAll(Pageable)` offset asosida | offset o'sgani sari so'rov sekinlashadi | `patterns 7.7 (Keyset / Cursor Pagination)` |
| `orders` jadvali | `(created_at, id)` indeksi yo'q | keyset so'rovi indekssiz butun jadvalni saralaydi | `architect 23 (Indekslar)` |

## 7. Pattern tayinlash
| Joy | Hozir | Pattern | Nega | Narxi | Qo'llanmada qidirish |
|---|---|---|---|---|---|
| `OrderRepository.java:21` | offset pagination | Keyset / cursor pagination | offset o'smaydi, indeks bo'yicha o'qish | API ga ixtiyoriy `cursor` parametri qo'shiladi, `page` eski klientlar uchun qoladi | `patterns 7.7 (Keyset / Cursor Pagination)` |

## 8. Qadamlar
### 1-qadam. Indeks qo'shish
**Nega.** Keyset so'rovi `(created_at, id)` bo'yicha tartib talab qiladi.
**Nima qilinadi.** `db/migration/V12__orders_created_at_id_idx.sql`:
`CREATE INDEX CONCURRENTLY idx_orders_created_at_id ON orders (created_at DESC, id DESC);`
**Qilinmaydi.** Kod o'zgarmaydi.
**Test.** `MigrationIT` - migratsiya bo'sh va to'liq bazada o'tadi, indeks `indisvalid = true`.
**Qabul mezoni.** `mvn -q verify` -> yashil; `MigrationIT` `pg_indexes` da
`idx_orders_created_at_id` ni topadi. Sessiyadan tashqari, staging da:
`EXPLAIN (ANALYZE, BUFFERS) SELECT ... ORDER BY created_at DESC, id DESC LIMIT 20`
-> `Index Scan`, `Seq Scan` emas.

### 2-qadam. Repository metodi
...

## 9. Test matritsasi
| O'zgarish | Daraja | Joy | Ma'lumot | Oracle |
|---|---|---|---|---|
| keyset so'rovi | slice (`@DataJpaTest` + Testcontainers) | `OrderRepositoryIT` | 50 buyruq, bir xil `created_at` li 3 ta | cursor bilan sahifalar kesishmaydi va qator tushib qolmaydi |

## 14. Definition of Done
- [ ] `mvn -q verify` yashil (`MigrationIT`, `OrderRepositoryIT`)

Relizdan keyin kuzatiladi, DoD ga kirmaydi (sessiyada tekshirilmaydi): staging
`EXPLAIN` da `Index Scan`, p99 `http.server.requests` < 300 ms.

## 16. Manbalar
- Kod: `OrderController.java:38`, `OrderRepository.java:21`
- Config: `pom.xml:9`, `db/migration/`
- Qo'llanmalar: `patterns 7.7 (Keyset / Cursor Pagination)`, `architect 23 (Indekslar)`
````

## Yakuniy shakl talablari

- Jadval ustunlari shablondagidek, qo'shimcha ustun kiritilmaydi
- Har qadamda beshlik to'liq (`references/prompt-dizayn.md` 6.3)
- Fayl 10 daqiqada o'qiladi: S ~1 varaq, M ~3, L ~6
- Chatga reja ko'chirilmaydi - xulosa + fayl yo'li + eng muhim qaror + eng katta risk
