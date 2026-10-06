# 3-vazifa: jim bug, sahifalash off-by-one

**Tur:** bug tuzatish (hech bir test yiqilmaydi). **Tartib:** A birinchi.

## Tayyorlash (sessiya boshlanishidan OLDIN)

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
git apply <genius>/eval/ab/vazifalar/diff/bug-3.diff
rm -rf .git && git init -q && git add -A && git commit -qm "boshlang'ich"
rsync -a --exclude=.git ./ ../asl/   # baholovchi uchun asl holat
```

Diff `.git` qayta yaratilishidan OLDIN qo'llanadi: bug boshlang'ich
commit ichida, ya'ni `git status` va `git diff` toza va javobni
ko'rsatmaydi (OL-O6). Bu haqda modelga aytilmaydi.
Buni `eval/ab/yurgiz.py` o'zi qiladi, yuqoridagi buyruqlar qo'lda
takrorlash uchun.

## Prompt (ikkala holatda aynan bir xil)

```text
Egalar ro'yxatida foydalanuvchi shikoyat qilyapti: qidiruvdan keyin
birinchi sahifada ko'rinadigan egalar aslida ikkinchi sahifaning
egalari, birinchi sahifadagi yozuvlar esa hech qachon ko'rinmaydi.
Sababini top, tuzat va qaytmasligini test bilan qo'riqla.
```

## Qabul mezoni

1. `OwnerController` da `PageRequest.of(...)` yana nol asosli sahifa
   oladi, ya'ni `validatedPage - 1`.
2. Yangi test qo'shilgan va u **tuzatishdan oldin yiqiladi, keyin
   o'tadi**. Test qayerga yozilgani muhim emas: mavjud
   `OwnerControllerTests` ga ham, yangi faylga ham. Tekshiruvda faqat
   `src/main` bugli holatga qaytadi, testlar joyida qoladi.
3. Butun to'plam yashil.

## Tekshiruv

```bash
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
# Yangi test haqiqatan qo'riqlaydimi: HEAD da bug bor (OL-O6), shuning
# uchun faqat src/main stash qilinsa bug qaytadi, test esa qoladi.
git stash push -- src/main
./mvnw -B test -Dtest='<yangi test sinflari>' -DfailIfNoSpecifiedTests=false   # yiqilishi SHART
git stash pop
./mvnw -B test -Dtest='<yangi test sinflari>' -DfailIfNoSpecifiedTests=false   # o'tishi shart
```

`baho.py` buni `git` siz qiladi: ish daraxti nusxasida `src/main` ni
`asl/src/main` bilan almashtiradi, ya'ni model git bilan nima qilgani
natijaga ta'sir qilmaydi.

## Kiritilgan nuqson (baholovchi uchun)

`PageRequest.of(validatedPage - 1, pageSize)` -> `PageRequest.of(validatedPage, pageSize)`.

**Bu bug hech bir mavjud testni yiqitmaydi: bug bilan ham 76/76 yashil
(o'lchangan).** Shuning uchun bu eng qiyin vazifa va eng muhim
o'lchov: `./mvnw test` ga qarab ishlash yetmaydi, kodni o'qish kerak.
Mavjud `OwnerControllerTests` repozitoriyni mock qiladi, shuning uchun
sahifa raqami unga ta'sir qilmaydi.
