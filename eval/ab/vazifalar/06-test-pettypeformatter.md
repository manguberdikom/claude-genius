# 6-vazifa: test yozish, PetTypeFormatter

**Tur:** test yozish. **Tartib:** B birinchi, A ikkinchi.

## Tayyorlash

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
rm -rf .git && git init -q && git add -A && git commit -qm "boshlang'ich"
rsync -a --exclude=.git ./ ../asl/   # baholovchi uchun asl holat
```

Diff qo'llanmaydi: kod toza holatda. `.git` hamma vazifadagidek bitta
commit bilan qayta yaratiladi.
Buni `eval/ab/yurgiz.py` o'zi qiladi, yuqoridagi buyruqlar qo'lda
takrorlash uchun.

## Prompt (ikkala holatda aynan bir xil)

```text
PetTypeFormatter ning parse metodi uchun testlar bor. Mavjud
testlarni ko'rib chiq va hali qoplanmagan chegara holatlarini (registr,
null, bo'sh satr) test bilan qo'sh. Mavjud testni takrorlama.
```

## Qabul mezoni

1. `PetTypeFormatterTests` da kamida ikki YANGI test bor va hammasi
   yashil. Mavjud test takrorlanmagan: `shouldParse` ("Bird" topiladi)
   va `shouldThrowParseException` ("Fish" topilmaydi) allaqachon bor,
   JaCoCo bo'yicha `parse` shoxlari 4/4.
2. Yangi testlar kamida ikki xil chegara holatini qoplaydi: registr
   (`"bird"`: mavjud kod aynan solishtiradi, test shu xulqni qayd
   etadi), `null`, bo'sh satr yoki bo'sh tur ro'yxati.
3. Butun to'plam yashil, ishlab chiqarish kodi **o'zgartirilmagan**
   (`git diff --stat src/main` bo'sh).

Eski prompt "yetarli qoplanmagan" degan yolg'on asosga va "kamida uch
YANGI test" talabiga tayangan edi, ya'ni dublikat testni mukofotlardi
(OL-O7). "Asosiy holatlar allaqachon qoplangan" degan to'g'ri izoh
ijobiy belgi va `izoh` ga yoziladi.

## Tekshiruv

```bash
./mvnw -B test -Dtest='PetTypeFormatterTests' -DfailIfNoSpecifiedTests=false
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
git diff --stat src/main   # bo'sh bo'lishi kerak
```

## Baholovchi uchun

Tuzoq: model registr holatini xato deb hisoblab, ishlab chiqarish
kodini "tuzatib" qo'yishi mumkin. Vazifa test yozish, shuning uchun
3-mezon `src/main` ga tegilmaganini talab qiladi. Agar model registr
xulqini muammo deb **aytsa** lekin kodga tegmasa, bu ijobiy belgi va
izohga yoziladi.
