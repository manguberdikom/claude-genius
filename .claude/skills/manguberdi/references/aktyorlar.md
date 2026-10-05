# Aktyorlar zanjiri

Zanjir bitta yo'nalishda ishlaydi, orqaga qaytish faqat kamchilik
topilganda bo'ladi va kamchilik **egasiga** qaytadi.

```
rejalashtiruvchi  (faqat zarur bo'lsa)
       |
       v
   dasturchi  <--- kod kamchiligi ----.
       |                                |
       v                                |
  test-muhandis  <--- test kamchiligi --+
       |                                |
       v                                |
     review  -------- kamchilik --------'
       |
       v (toza yoki to'xtadi)
    memory
```

## Chaqiruv budjeti

Har aktyor bitta vazifada **ko'pi bilan ikki marta** chaqiriladi.
Birinchi chaqiruv ishni bajaradi, ikkinchisi review topgan kamchilikni
tuzatadi. Uchinchisi yo'q. Ikkinchi chaqiruv promptida `2-chaqiruv` deb
yoziladi va kamchilikni qaytargan aktyorning (review yoki test-muhandis)
topilmalari fayl, qator va qoidasi bilan to'liq ko'chiriladi.

Budjet tugaganda va muammo qolganda zanjir to'xtaydi. Shunda yoziladi:
nima bajarildi, nima qolgan, nega ikki urinish yetmadi, nima
yetishmayapti. Uchinchi urinish o'rniga aniq savol beriladi. Undan
keyin memory bosqichi bajariladi: ikki urinishda ham qolgan kamchilik
`feedback` nomzodi, yarim qolgan reja `project` nomzodi (`memory.md`).

Budjet **sanaladi**, yodda saqlanmaydi: hook uni har yangi so'rovda
o'zi nolga tushiradi. Bitta so'rov ichida ikkinchi vazifa boshlansa:

```bash
python3 tools/budget.py --yangi-vazifa "<vazifa nomi>"
python3 tools/budget.py --holat          # jadval
```

`PreToolUse` hook har aktyor chaqiruvini hisoblaydi va uchinchisini
**to'sadi**. `qidiruv` va `tahlil` sanalmaydi: ular zanjir qadami emas,
o'qish asbobi, va ularni cheklash arzon yo'lni qimmat qiladi.

Chaqiruv behuda ketgan bo'lsa (aktyor boshqa sababdan yiqildi, xato
bilan tugadi yoki foydalanuvchi to'xtatdi):
`python3 tools/budget.py --tiklash <aktyor>`.

Bir necha modulli ish (to'liq review, keng tuzatish) normallashtirishda
modullarga bo'linadi va har qism
`python3 tools/budget.py --yangi-vazifa "<ish>: <modul>"` bilan
boshlanadi. Budjet aktyor bo'yicha alohida sanaladi, shuning uchun egasi
bo'yicha bo'lish shart emas. Bo'lish ish boshida qilinadi: to'siqdan
keyin yangi vazifa ochish uchinchi urinishni yashiradi.

## Ikkinchi chaqiruvning oldini olish

Budjet ikkita, lekin maqsad bittasida tugatish. Ikkinchi chaqiruv
deyarli har doim shu uch sababdan biri bilan keladi:

| Sabab | Oldini olish |
|---|---|
| Aktyor qoidani bilmagan | `rules_for.py` ni ishdan oldin chaqirish |
| Reviewer boshqa mezon bilan tekshirgan | ikkalasi bir xil ro'yxatni oladi |
| "Bajarildi" nimaligi aytilmagan | qabul mezoni normalizatsiyada belgilanadi |

Shuning uchun `rules_for.py` tavsiya emas, zanjirning birinchi qadami,
va u **majburlanadi**: `check_code.py` Java fayl yozilgandan keyin
(`PostToolUse`) shu fayl uchun chaqiruv bo'lganini tekshiradi. Bo'lmasa
modelga to'siq xabarini qaytaradi va shu fayl uchun `rules_for.py`
chaqirilmaguncha uning har yozuvida takrorlaydi. Yozuv bekor
qilinmaydi, fayl diskda qoladi, shuning uchun `rules_for.py` yozishdan
OLDIN chaqiriladi. Zanjir sifati odamning yodida qolishiga tayanmaydi.

## Kamchilik kimga qaytadi

`review` topilmasi turiga qarab yo'naltiriladi. Noto'g'ri aktyorga
qaytarilgan kamchilik ikki chaqiruvni behuda sarflaydi.

| Topilma turi | Egasi |
|---|---|
| Mantiq xatosi, pattern noto'g'ri qo'llangan, chegara buzilgan | `dasturchi` |
| Tranzaksiya, N+1, resurs yopilmagan, xato yutilgan | `dasturchi` |
| Test yo'q, assertion yo'q, test noto'g'ri turda, flaky | `test-muhandis` |
| Reja qadami bajarilmagan yoki reja noto'g'ri | `rejalashtiruvchi` |
| Hujjat yoki havola buzilgan | `dasturchi` |

## Har aktyor nimani qaytaradi

Qaytarilgan javob keyingi aktyor uchun **kirish** bo'ladi, shuning
uchun shakli qat'iy. Har javobda bo'lishi shart:

- bir jumlada natija,
- har qaror yoki topilma yonida `<hujjat> <raqam>`,
- nima **bajarilmagani** va nega,
- keyingi aktyor uchun kerakli aniq ma'lumot (fayl, qator, buyruq).

Javobda uzun log, to'liq fayl matni yoki stack trace bo'lmaydi: ular
aktyorning o'z kontekstida qoladi.

## Zanjir qachon qisqaradi

- Faqat savol berilgan bo'lsa (`doc.sh show`, `qidiruv`, `tahlil`),
  zanjir shu yerda tugaydi: kod o'zgarmaydi, review ishlamaydi. Memory
  bosqichi faqat foydalanuvchi javobni tuzatgan yoki yondashuvni rad
  etgan bo'lsa bajariladi.
- Faqat review so'ralgan bo'lsa, `dasturchi` va `test-muhandis`
  chaqirilmaydi: topilmalar hisobot sifatida beriladi va memory
  bosqichi bajariladi.
- Hujjat o'zgarishi kod emas: `check_docs.py` tekshiradi, test
  muhandisi chaqirilmaydi.
