# 3-vazifa: jim bug, sahifalash off-by-one

**Tur:** bug tuzatish (hech bir test yiqilmaydi). **Tartib:** A birinchi.

## Tayyorlash (sessiya boshlanishidan OLDIN)

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
git apply eval/ab/vazifalar/diff/bug-3.diff
```

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
   o'tadi**. Buni tekshirish uchun testni qo'shib, tuzatishni vaqtincha
   orqaga qaytarib ko'rish kerak.
3. Butun to'plam yashil.

## Tekshiruv

```bash
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
# Yangi test haqiqatan qo'riqlaydimi: tuzatishni orqaga qaytarib ko'rish
git stash && git apply eval/ab/vazifalar/diff/bug-3.diff   # bug qaytadi, test qoladi
```

## Kiritilgan nuqson (baholovchi uchun)

`PageRequest.of(validatedPage - 1, pageSize)` -> `PageRequest.of(validatedPage, pageSize)`.

**Bu bug hech bir mavjud testni yiqitmaydi: bug bilan ham 76/76 yashil
(o'lchangan).** Shuning uchun bu eng qiyin vazifa va eng muhim
o'lchov: `./mvnw test` ga qarab ishlash yetmaydi, kodni o'qish kerak.
Mavjud `OwnerControllerTests` repozitoriyni mock qiladi, shuning uchun
sahifa raqami unga ta'sir qilmaydi.
