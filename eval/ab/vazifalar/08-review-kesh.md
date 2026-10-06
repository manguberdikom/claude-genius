# 8-vazifa: review, qidiruv keshi

**Tur:** review (kod o'zgartirilmaydi). **Tartib:** B birinchi, A ikkinchi.

## Tayyorlash (sessiya boshlanishidan OLDIN)

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
rm -rf .git && git init -q && git add -A && git commit -qm "boshlang'ich"
git apply <genius>/eval/ab/vazifalar/diff/review-1.diff
rsync -a --exclude=.git ./ ../asl/   # baholovchi uchun asl holat
```

Diff `.git` qayta yaratilgandan KEYIN qo'llanadi: review qilinadigan
o'zgarish `git diff` da ataylab ko'rinadi.
Buni `eval/ab/yurgiz.py` o'zi qiladi, yuqoridagi buyruqlar qo'lda
takrorlash uchun.

## Prompt (ikkala holatda aynan bir xil)

```text
Bu diffni review qil. Nimani to'xtatasan va nega. Kodni o'zgartirmang,
faqat topilmalarni yoz.
```

Diff faqat `git diff` orqali ko'rinadi. Fayl yo'li berilmaydi: u
javob kaliti yonida turadi va sessiyaga ochilmaydi (OL-T-M2).

## Qabul mezoni

`muvaffaqiyat` = 1, agar **to'rtta kiritilgan nuqsondan kamida uchtasi**
topilgan bo'lsa. Nuqson topilgan deb hisoblanadi, agar topilma uning
sababini aytsa; faqat "keshni qayta ko'rib chiqing" degan gap
hisoblanmaydi.

## Kiritilgan nuqsonlar (baholovchi uchun, 4 ta)

| # | Nuqson | Nega muhim |
|---|---|---|
| R1-1 | `static` o'zgaruvchan `HashMap` so'rovlar orasida bo'lishiladi | `HashMap` thread-safe emas: parallel so'rovda buzilgan holat yoki cheksiz sikl |
| R1-2 | Kesh cheklanmagan: chiqarish siyosati ham, TTL ham yo'q | har yangi familiya va sahifa yozuv qo'shadi, xotira o'sadi |
| R1-3 | `catch (Exception e) { e.printStackTrace(); return Page.empty(); }` | xato yutiladi va foydalanuvchi "topilmadi" degan YOLG'ON javob oladi |
| R1-4 | Invalidatsiya yo'q | ega yangilangandan keyin ham eski sahifa qaytadi |

Yolg'on topilma deb sanaladi: diffda yo'q muammo (masalan "SQL
injection bor", "tranzaksiya yo'q") yoki mavjud kodga tegishli, diffga
tegishli bo'lmagan gap.

Qo'shimcha kuzatuv (sanalmaydi, lekin izohga yoziladi): topilma
qo'llanma bo'limi, Sonar kaliti yoki rasmiy hujjat bilan asoslanganmi.
