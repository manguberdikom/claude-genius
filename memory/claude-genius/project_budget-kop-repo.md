---
type: project
---
# budget.py: repo bo'lmagan workspace dan ko'p repoga parallel aktyor

- Sessiya papkasi bir nechta repo ni o'z ichiga olgan workspace bo'lsa,
  `guruh:` qatorisiz kartadagi `papka:` budjetni repo bo'yicha ajratmaydi:
  har xil repoga yuborilgan uchinchi `dasturchi` umumiy hisobda to'siladi.
- Hozirgi aylanma yo'l: har repo alohida vazifa, har ishga tushirishdan oldin
  `budget.py --yangi-vazifa "<repo> ..."`. Ikkinchi chaqiruv ham shu tartibda.
- Tuzatish nomzodi: `guruh:` siz ham `papka:` dagi repo ildizi bo'yicha alohida
  hisob yuritish (har repo o'z `.git` i, kesishish yo'q).
