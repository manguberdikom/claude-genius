# Aktyorlar zanjiri

Zanjir bitta yo'nalishda ishlaydi, orqaga qaytish faqat kamchilik
topilganda bo'ladi va kamchilik **egasiga** qaytadi.

```
rejalashtiruvchi  (faqat zarur bo'lsa)
       |
       v
   arxitektor  <--- kod kamchiligi ----.
       |                                |
       v                                |
  test-muhandis  <--- test kamchiligi --+
       |                                |
       v                                |
     review  -------- kamchilik --------'
       |
       v (toza)
    memory
```

## Chaqiruv budjeti

Har aktyor bitta vazifada **ko'pi bilan ikki marta** chaqiriladi.
Birinchi chaqiruv ishni bajaradi, ikkinchisi review topgan kamchilikni
tuzatadi. Uchinchisi yo'q.

Budjet tugaganda va muammo qolganda zanjir to'xtaydi. Shunda yoziladi:
nima bajarildi, nima qolgan, nega ikki urinish yetmadi, nima
yetishmayapti. Uchinchi urinish o'rniga aniq savol beriladi.

Budjetni kuzatish uchun har vazifada shu jadval yuritiladi:

```
aktyor            1-chaqiruv   2-chaqiruv   holat
rejalashtiruvchi  bajarildi    -            tugadi
arxitektor        bajarildi    bajarildi    tugadi
test-muhandis     bajarildi    -            tugadi
review            bajarildi    bajarildi    toza
```

## Ikkinchi chaqiruvning oldini olish

Budjet ikkita, lekin maqsad bittasida tugatish. Ikkinchi chaqiruv
deyarli har doim shu uch sababdan biri bilan keladi:

| Sabab | Oldini olish |
|---|---|
| Aktyor qoidani bilmagan | `rules_for.py` ni ishdan oldin chaqirish |
| Reviewer boshqa mezon bilan tekshirgan | ikkalasi bir xil ro'yxatni oladi |
| "Bajarildi" nimaligi aytilmagan | qabul mezoni normalizatsiyada belgilanadi |

Shuning uchun `rules_for.py` tavsiya emas, zanjirning birinchi qadami.
U chaqirilmagan bo'lsa, review topilmasi aktyorning xatosi emas,
jarayonning xatosi.

## Kamchilik kimga qaytadi

`review` topilmasi turiga qarab yo'naltiriladi. Noto'g'ri aktyorga
qaytarilgan kamchilik ikki chaqiruvni behuda sarflaydi.

| Topilma turi | Egasi |
|---|---|
| Mantiq xatosi, pattern noto'g'ri qo'llangan, chegara buzilgan | `arxitektor` |
| Tranzaksiya, N+1, resurs yopilmagan, xato yutilgan | `arxitektor` |
| Test yo'q, assertion yo'q, test noto'g'ri turda, flaky | `test-muhandis` |
| Reja qadami bajarilmagan yoki reja noto'g'ri | `rejalashtiruvchi` |
| Hujjat yoki havola buzilgan | `arxitektor` |

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

- Faqat savol berilgan bo'lsa (`qidiruv`, `tahlil`), zanjir shu yerda
  tugaydi: kod o'zgarmaydi, review va memory ishlamaydi.
- Faqat review so'ralgan bo'lsa, `arxitektor` va `test-muhandis`
  chaqirilmaydi: topilmalar hisobot sifatida beriladi va memory
  bosqichi bajariladi.
- Hujjat o'zgarishi kod emas: `check_docs.py` tekshiradi, test
  muhandisi chaqirilmaydi.
