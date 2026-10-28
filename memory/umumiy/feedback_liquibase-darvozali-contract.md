---
type: feedback
modified: 2026-10-28T00:00:00Z
---
# Liquibase contract (DROP) ni expand bilan bir relizda yuborish: belgi va ma'lumot darvozasi

- Ustun yoki jadval DROP i eski pod uni o'qiyotgan relizda yurmasligi kerak. Uni keyingi relizga qoldirish o'rniga shu relizda **darvoza** bilan yuborsa bo'ladi: har DROP changesetiga `preConditions` + `onFail: CONTINUE`.
  - Belgi sharti (afzal): expand relizining belgi changeseti BOSHQA deployda yozilgan: `SELECT count(*) FROM <sxema>.databasechangelog m WHERE m.id = '<belgi>' AND m.deployment_id <> (SELECT d.deployment_id FROM <sxema>.databasechangelog d ORDER BY d.orderexecuted DESC LIMIT 1)` (expectedResult 1). Vaqt kutilmaydi, DROP keyingi deployda yuradi. Chekka holat: shu deployda boshqa hech narsa yurmasa DROP yana bir deployga suriladi.
  - Vaqt sharti (eski): `dateexecuted <= now() - interval 'N days'`. `dateexecuted` JVM soati bilan zonasiz yoziladi, `now()` sessiya zonasida: farq soatlab siljiydi; belgi shartini afzal ko'ring.
  - Belgi deferred trekda bo'lsa (masalan jadval almashtirish), shart o'sha trekning changelog jadvalini o'qiydi.
  - Ma'lumot sharti: tashlanadigan ustun bo'sh yoki nusxasi boshqa joyda to'liq.
  - `CONTINUE` changesetni yozmaydi va keyingi deployda qayta tekshiradi. `MARK_RAN` uni abadiy o'tkazib yuboradi, `HALT` deployni to'xtatadi.
- Ikkinchi bosqich DROP ni birinchi contract markeriga bog'lang (zanjir: N, N+X, N+2X).
- Marker id ni changeset faylidan **aynan** oling. Parallel guruhda kartadagi nom bilan yozilgan id konvensiya talabi (id = fayl slugi bilan boshlanadi) tufayli boshqacha chiqdi; mos kelmasa darvoza jim va abadiy yopiq qoladi. Birlashtirishdan oldin `grep` bilan solishtiring.
- Xavf: ilova oldingi versiyaga rollback qilinsa va N kun o'tib yangi deploy bo'lsa, rolling oynada eski pod DROP qilingan ustunni o'qiydi. Reliz izohiga yozing.
- "Faqat dev da, rolling oyna yo'q" degan faraz noto'g'ri: dev da ham yangi pod Liquibase ni yurgizayotganda eski pod ishlaydi va uning scheduler i (`SELECT *` bilan entity o'qiydi) `Unable to find column position by name: <ustun>` beradi. Yangi pod Ready bo'lib eski pod to'xtagach xato o'zi to'xtaydi; kod tuzatilmaydi, qo'llangan changeset checksum sababli o'zgartirilmaydi. Xato to'xtamasa sabab yangi podning startup xatosi.
- PostgreSQL: `ADD CONSTRAINT c UNIQUE USING INDEX i` indeksni `c` nomiga qayta nomlaydi; test eski indeks nomini kutmasin.
