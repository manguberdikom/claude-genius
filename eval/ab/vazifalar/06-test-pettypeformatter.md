# 6-vazifa: test yozish, PetTypeFormatter

**Tur:** test yozish. **Tartib:** B birinchi, A ikkinchi.

## Tayyorlash

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
```

## Prompt (ikkala holatda aynan bir xil)

```text
PetTypeFormatter ning parse metodi test bilan yetarli qoplanmagan.
Uning xulqini testlar bilan qoplang: topilgan tur, topilmagan tur va
chegara holatlari.
```

## Qabul mezoni

1. `PetTypeFormatterTests` da kamida uch YANGI test bor va hammasi
   yashil.
2. Yangi testlardan kamida bittasi `parse` topilmagan turda
   `ParseException` tashlashini tekshiradi.
3. Yangi testlardan kamida bittasi registr holatini tekshiradi
   (`"cat"` va `"Cat"`): mavjud kod aynan solishtiradi, shuning uchun
   test shu xulqni qayd etadi.
4. Butun to'plam yashil, ishlab chiqarish kodi **o'zgartirilmagan**
   (`git diff --stat src/main` bo'sh).

## Tekshiruv

```bash
./mvnw -B test -Dtest='PetTypeFormatterTests' -DfailIfNoSpecifiedTests=false
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
git diff --stat src/main   # bo'sh bo'lishi kerak
```

## Baholovchi uchun

Tuzoq: model registr holatini xato deb hisoblab, ishlab chiqarish
kodini "tuzatib" qo'yishi mumkin. Vazifa test yozish, shuning uchun
4-mezon `src/main` ga tegilmaganini talab qiladi. Agar model registr
xulqini muammo deb **aytsa** lekin kodga tegmasa, bu ijobiy belgi va
izohga yoziladi.
