---
type: feedback
---
# Liquibase contract (DROP) ni expand bilan bir relizda yuborish: vaqt darvozasi

- Ustun yoki jadval DROP i eski pod uni o'qiyotgan relizda yurmasligi kerak. Uni keyingi relizga qoldirish o'rniga shu relizda **darvoza** bilan yuborsa bo'ladi: har DROP changesetiga `preConditions` + `onFail: CONTINUE`.
  - Vaqt sharti: expand relizining shartsiz yuradigan birinchi changeseti `databasechangelog` da `dateexecuted <= now() - interval 'N days'` (expectedResult 1).
  - Ma'lumot sharti: tashlanadigan ustun bo'sh yoki nusxasi boshqa joyda to'liq.
  - `CONTINUE` changesetni yozmaydi va keyingi deployda qayta tekshiradi. `MARK_RAN` uni abadiy o'tkazib yuboradi, `HALT` deployni to'xtatadi.
- Ikkinchi bosqich DROP ni birinchi contract markeriga bog'lang (zanjir: N, N+X, N+2X).
- Marker id ni changeset faylidan **aynan** oling. Parallel guruhda kartadagi nom bilan yozilgan id konvensiya talabi (id = fayl slugi bilan boshlanadi) tufayli boshqacha chiqdi; mos kelmasa darvoza jim va abadiy yopiq qoladi. Birlashtirishdan oldin `grep` bilan solishtiring.
- Xavf: ilova oldingi versiyaga rollback qilinsa va N kun o'tib yangi deploy bo'lsa, rolling oynada eski pod DROP qilingan ustunni o'qiydi. Reliz izohiga yozing.
- PostgreSQL: `ADD CONSTRAINT c UNIQUE USING INDEX i` indeksni `c` nomiga qayta nomlaydi; test eski indeks nomini kutmasin.
