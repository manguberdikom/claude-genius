# O'zgarishlar

Har versiya `VERSION` faylida, o'rnatilgani `python3 tools/versiya.py`
da ko'rinadi. Yangi versiya chiqqanda shu ro'yxatning boshiga yoziladi.

## 0.3.0 (2026-10-19)

- Qaror opus da, ijro sonnet da: `rejalashtiruvchi` opus, har kod
  vazifasiga (Tez yo'ldan tashqari) 25 qatorgacha ijro rejasi beradi;
  `dasturchi`, `test-muhandis`, `review` sonnet da reja bilan ishlaydi.
  O'lchov: opus reja + sonnet kod minimal 9.2, takror 0 (opus yolg'iz
  8.5, sonnet yolg'iz 7.5).
- Review rejaning "yozilmaydi" ro'yxatini ham tekshiradi.
- Tez yo'l `rules_for --belgilar` dagi `tez_yol:` qarori bilan.
- DRY: "bir ish bitta metod" umumiy qoidada va kartalarda.
- Global o'rnatishda agentlardagi skill reference yo'li mutlaq.
- `usage.py`: katta sessiya fonda saqlanadi.

## 0.2.0 (2026-10-19)

- `dasturchi` opus da (0.3.0 da o'zgardi).
- Retsept kartalari (`tools/retsept/`): har belgiga eng kichik to'g'ri
  shakl, "allaqachon bor, yozmang" ro'yxati va tuzoqlar, bo'lim raqami bilan.
- Umumiy yozish qoidalari (`umumiy-kod.md`, `umumiy-test.md`): to'rt
  aktyor bir xil bilimni `rules_for` dan oladi; shartli bandlar faqat mos
  kodda chiqadi.
- `rules_for --vazifa`: fayl hali o'z ichiga olmagan mavzuning kartasi;
  vazifa kartasi birinchi. `--belgilar`: Tez yo'l qarori uchun qisqa chiqish.
- `qidiruv` va `tahlil` aktyorlari olib tashlandi.
- SKILL.md qisqardi (16 KB dan 12 KB); partiya ta'rifi; Tez yo'l vazifa
  belgilari bo'yicha; kod vazifasida nomzod bo'lim o'qilmaydi.
- Memory va hujjatlar `<workspace>/docs-local/` da, `.git/info/exclude`
  orqali git dan tashqarida; zaxira nusxa (`.bak`) yaratilmaydi.
- O'rnatuvchi: o'z skill va aktyor fayllarini zaxiralamaydi, eski
  zaxiralarni o'chiradi; `versiya.py` o'rnatilgan versiyani aytadi.
- `check_code`: takroriy import (`java:S1128`); yangi belgi xabari bir marta.
- Korpus: 222 bob odam tasdiqlagan (226 dan); kitob iqtiboslari betiga solishtirilgan.

## 0.1.0

- Birinchi versiya: olti hujjat, `manguberdi` orkestratori, hooklar.
