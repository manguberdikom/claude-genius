# Qat'iy taqiqlar

Uchta amal taqiqlangan. Ular shunchaki tavsiya emas: `tools/guard.py`
ularni `PreToolUse` hook sifatida to'sadi, ya'ni unutib bo'lmaydi.

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

`psql -h`, `mysql -h`, `mongosh`, `redis-cli` va shunga o'xshash
ulanishlar.

Nega: sxemani bilish uchun ulanish shart emas. Entity sinflari jadval,
ustun, tur, tashqi kalit va indeksni to'liq tasvirlaydi. Ulanish esa
muhit, parol va ruxsat talab qiladi.

O'rniga: `python3 tools/schema_from_entities.py <src>`.

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
- `check_code.py` topilmasini e'tiborsiz qoldirish.
- Qoida raqamisiz o'zgarish kiritish.
- Ikki chaqiruvdan keyin uchinchi urinish.
- Foydalanuvchi so'ramagan faylni "yo'l-yo'lakay" tuzatish.
