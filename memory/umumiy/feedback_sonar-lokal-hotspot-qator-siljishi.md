---
type: feedback
---
# Lokal Sonar ko'zgusida hotspot qator siljishi gate ni yiqitadi

`sonar_local.py` serverdagi REVIEWED hotspot statusini qoida + fayl + qator bo'yicha ko'chiradi. O'sha faylga
yuqoridan qator qo'shilsa, eski hotspot boshqa qatorga suriladi, lokalda `TO_REVIEW` bo'ladi va gate
`new_security_hotspots_reviewed` / `security_hotspots_reviewed` shartlari bilan ERROR beradi. Serverning o'zi
hotspotni qator siljishida kuzatib, statusni saqlaydi.

- Tekshirish: serverda `api/hotspots/search?projectKey=<kalit>` dan shu qoida va fayldagi hotspot holati
  (`REVIEWED SAFE`, qaysi qator) va kodda o'sha ifoda faqat surilganmi (`git blame` sanasi o'zgarishdan oldin).
- Faqat surilgan bo'lsa: lokal ko'zguda `api/hotspots/change_status` (admin, `REVIEWED`/`SAFE`, izohda server
  qatori) bilan qo'llang, keyin `api/qualitygates/project_status` qayta tahlilsiz OK beradi.
- Ifoda o'zgargan bo'lsa bu yangi hotspot: kodni tuzating yoki foydalanuvchi server UI da ko'rib chiqadi.
