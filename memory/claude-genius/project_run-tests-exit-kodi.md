---
type: project
---

# `run_tests.py` yiqilgan testda ham exit 0 qaytargan hol

2026-10-17 da aniqlandi. `run_tests.py --diff --yurgiz` chiqishida beshta
yiqilgan test ro'yxati va "Gradle qisqa formati xabarni bermaydi" eslatmasi
bor edi, lekin yakuniy satr `[exited with code 0]` bo'ldi. Agar faqat chiqish
kodiga ishonilsa, yiqilgan testlar commit qilinib ketar edi.

Kuzatilgan farq: o'sha chaqiruvda `HRM_SNAPSHOT_UPDATE=true` env o'rnatilgan
edi va Gradle snapshot yangilash rejimida ikkinchi marta yurgan. Ya'ni
shubha: ikki yurish bo'lganda oxirgisining kodi qaytariladi, birinchisining
yiqilishi esa faqat matnda qoladi.

Keyingi yurishda (env siz) asbob to'g'ri ishladi: "Natija: yashil, exit=0,
Yiqilgan test topilmadi" satri chiqdi.

## Qanday qo'llash

- `run_tests.py` natijasini **matndan** o'qi: "Natija: yashil" va "Yiqilgan
  test topilmadi" satrlari bo'lmasa, yashil deb hisoblama.
- Snapshot yangilash rejimini (`*_SNAPSHOT_UPDATE=true`) testni tasdiqlash
  bilan BIRGA chaqirma: avval snapshotni yangila, keyin env siz qayta yurgiz.
- Tuzatish kerak bo'lgan joy: ikki yurishda yakuniy exit kodini hisoblash
  mantiqi. Aniqlangan sabab hali tasdiqlanmagan, shuning uchun `tools/` ga
  o'zgarish kiritilmadi.
