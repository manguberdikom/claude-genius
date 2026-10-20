---
type: feedback
---
# Mavjud ma'lumotga unique index: HALT precondition tozalashsiz deployni to'xtatadi

- Poyga oynasini yopadigan unique (partial) index changesetiga "dublikat bor bo'lsa
  `onFail: HALT`" precondition qo'yilib, tozalash keyinga qoldirilsa, birinchi
  haqiqiy bazada deploy to'xtaydi: poyga indexdan oldin ishlagan, dublikat deyarli
  har doim bor.
- Indexning `changes` qismi tegilmaydi (checksum). Tozalash **alohida, oldin
  yuradigan** changesetda: `includeAll` da fayl nomi alfavit bo'yicha oldin
  (`_149_` < `_150_`). Index allaqachon o'tgan bazada u hech narsa o'zgartirmaydi.
- Qaysi qator qoladi: ilovaning o'zi "oxirgi" deb ko'rsatadigan tartib (uning
  `ORDER BY` i), aks holda foydalanuvchiga berilgan link o'chgan qatorga tushadi.
  O'chirish soft-delete, `last_modified_by` belgisi bilan: rollback va tekshiruv
  aynan shu qatorlarni topadi.
- Bir xil shablon boshqa indexlarda ham bo'lsa, ularning dublikat so'rovini
  deploydan oldin bazada tekshirishni hisobotda ayting.
