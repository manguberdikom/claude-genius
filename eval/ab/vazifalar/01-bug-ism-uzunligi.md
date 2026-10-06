# 1-vazifa: bug, uyquchi ism uzunligi

**Tur:** bug tuzatish. **Tartib:** A birinchi, B ikkinchi.

## Tayyorlash (sessiya boshlanishidan OLDIN)

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
git apply <genius>/eval/ab/vazifalar/diff/bug-1.diff
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
PetValidatorTests yiqilyapti. Sababini top va tuzat. Boshqa narsani
o'zgartirmang.
```

## Qabul mezoni

1. `PetValidatorTests` to'liq yashil.
2. Butun to'plam yashil (76/76).
3. `PetValidator.java` da chegara yana `MAX_NAME_LENGTH` ga teng, ya'ni
   30 belgidan uzun ism rad etiladi. `MAX_NAME_LENGTH` qiymati
   o'zgartirilmagan va test o'zgartirilmagan.

## Tekshiruv

```bash
./mvnw -B test -Dtest='PetValidatorTests' -DfailIfNoSpecifiedTests=false
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
git diff --stat   # faqat PetValidator.java bitta qatori (HEAD da bug bor)
```

## Kiritilgan nuqson (baholovchi uchun, modelga berilmaydi)

`name.length() > MAX_NAME_LENGTH` -> `> MAX_NAME_LENGTH + 1`. Bitta
test yiqiladi: `PetValidatorTests.validateWithLongPetName`
(o'lchangan). "Testni to'g'rilab qo'yish" yo'li ochiq, shuning uchun
3-mezon testga tegilmaganini talab qiladi.
