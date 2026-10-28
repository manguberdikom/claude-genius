---
type: feedback
modified: 2026-10-28T00:00:00Z
---
# Reja kartasi o'z umumiy qoidasiga zid bo'lishi mumkin

- Katta rejada kartalar alohida yoziladi, umumiy qoidalar (masalan "mavjud jadvalga indeks faqat alohida kontekstda") boshqa bo'limda. Ijroda ikki karta shu qoidaga zid chiqdi (expand faylda oddiy `CREATE INDEX`), loyihaning lint testi ham buni rad etardi.
- Bundan tashqari foydalanuvchi boshqa sessiyada umumiy qaror bergan bo'lishi mumkin (memory da `feedback`): u reja qoidasidan ham ustun.
- Ijro boshida va har partiyadan oldin: kartadagi changeset/DDL ni reja qoidalari, loyiha lint qoidalari va `feedback` memory yozuvlari bilan solishtiring; zid bo'lsa qoida yutadi, kartaga qayd yoziladi, agentga aniq ko'rsatma beriladi.
