# Qat'iy taqiqlar

Uchta amal taqiqlangan. Ular shunchaki tavsiya emas: `tools/guard.py`
ularni `PreToolUse` hook sifatida to'sadi. Bu odatga qarshi to'siq,
xavfsizlik chegarasi emas: `bash -c` yoki skript ichidagi buyruqni
ko'rmaydi. Hook o'tkazib yuborgani ruxsat degani emas.

## 1. Konteyner

`docker run`, `docker compose up`, `docker build`, `docker pull`.

Nega: daqiqalar ketadi, katta chiqish beradi va javob odatda konteyner
ichida emas. Baza tuzilishi entity sinflarida, test xatosi chiqishda.

O'rniga:

```bash
python3 tools/schema_from_entities.py <src>
python3 tools/parse_test_output.py <chiqish-fayli>
```

`docker ps`, `docker logs`, `docker images` to'silmaydi: ular arzon
tashxis va ko'pincha aynan kerak.

## 2. Bazaga ulanish

`psql`, `mysql`, `mongosh`, `redis-cli` va shunga o'xshash har qanday
ulanish: host bilan ham, hostsiz (lokal) ham, `PGPASSWORD=...` yoki
`sudo -u` bilan ham, `docker exec` va `kubectl exec` ichida ham. Faqat
`--version` va `--help` ulanish emas.

Nega: jadval, ustun, tur va tashqi kalitni bilish uchun ulanish shart
emas, ularni entity sinflari va migratsiyalar beradi. Ulanish esa muhit,
parol va ruxsat talab qiladi.

Chegarasi: indeks, constraint, trigger va statistika faqat bazada
turadi, haqiqiy plan ham. Tuning uchun shular kerak bo'lsa ulanish
o'rinli: `EXPLAIN (ANALYZE, BUFFERS)` chiqishini kod bermaydi.

O'rniga (sxema uchun): `python3 tools/schema_from_entities.py <src>`.

## 3. PowerShell

`powershell`, `pwsh`, `.ps1` skriptlari.

Nega: bu muhitda ishlamaydi va yozilgan skript tekshirilmagan bo'lib
qoladi. Shu ishni `bash` yoki `python3` bilan bajaring: ikkalasi ham
shu yerda sinaladi.

## Chiqish yo'li

Uchala holat ham **yopiq emas**. Haqiqatan kerak bo'lsa buyruq oldiga
`COST_OK=1` qo'yiladi:

```bash
COST_OK=1 docker compose up -d
```

Lekin shart: nega arzon yo'l yetmagani **aytiladi**. "Shunchaki
ishonmadim" sabab emas. Sabab aytilmasa, bu taqiqni aylanib o'tish
bo'ladi, qaror emas.

## Yana nimalar qilinmaydi

Bular hook bilan to'silmaydi, lekin zanjir qoidasi:

- Testni o'tkazish uchun assertionni bo'shatish yoki testni o'chirish.
- `check_code.py` ning yangi yoki tegilgan qatordagi topilmasini
  e'tiborsiz qoldirish (ishdan oldin bor bo'lgani `Tegilmagan` da
  aytiladi).
- Qoida raqamisiz o'zgarish kiritish.
- Ikki chaqiruvdan keyin uchinchi urinishni boshqa yo'l bilan qilish:
  asosiy sessiyada o'zi tuzatish yoki behuda ketmagan chaqiruvni
  `budget.py --tiklash` yoki `--yangi-vazifa` bilan nolga tushirish.
  Aktyorning uchinchi chaqiruvini esa `budget.py` hook o'zi to'sadi.
- Foydalanuvchi so'ramagan faylni "yo'l-yo'lakay" tuzatish.
