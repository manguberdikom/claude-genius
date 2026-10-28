---
type: feedback
modified: 2026-10-28T00:00:00Z
---
# Liquibase runAlways changeSet doim "yurmagan"

- `Liquibase.listUnrunChangeSets` `runAlways: true` changeSet ni har yurishda yurmagan ro'yxatiga qo'yadi, u muvaffaqiyatli yurgan bo'lsa ham.
- Ta'siri:
  - deferred trek "still pending" ogohlantirishi va xato hisoblagichi ish tugagandan keyin ham har tick da o'sadi;
  - "pending bo'sh" deb tekshiradigan IT yiqiladi.
- Yo'l: pending hisobida `changeSet.isAlwaysRun()` ni chiqarib tashlash; `runAlways` changeSet faqat shu yurishda yiqilgan bo'lsa pending hisoblanadi.
- Mock `ChangeSet` li unit test buni ushlamaydi: `isAlwaysRun()` u yerda `false`. Filtr haqiqiy changelog bilan IT da tekshiriladi.
