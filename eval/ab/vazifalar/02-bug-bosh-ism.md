# 2-vazifa: bug, bo'sh ism tekshiruvi

**Tur:** bug tuzatish. **Tartib:** B birinchi, A ikkinchi.

## Tayyorlash (sessiya boshlanishidan OLDIN)

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
git apply <genius>/eval/ab/vazifalar/diff/bug-2.diff
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
`./mvnw test` ikki joyda yiqilyapti. Sababini top va tuzat.
```

## Qabul mezoni

1. `PetControllerTests.processCreationFormWithBlankName` va
   `processUpdateFormWithBlankName` yashil.
2. Butun to'plam yashil (76/76).
3. Tuzatish `PetValidator` da: bo'sh va faqat bo'sh joydan iborat ism
   yana rad etiladi. Test o'zgartirilmagan.

## Tekshiruv

```bash
./mvnw -B test -Dtest='PetControllerTests' -DfailIfNoSpecifiedTests=false
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
```

## Kiritilgan nuqson (baholovchi uchun)

`if (!StringUtils.hasText(name))` -> `if (name == null)`. Bo'sh satr va
faqat bo'sh joy endi o'tib ketadi. Ikki test yiqiladi (o'lchangan).
Diqqat: yiqilgan testlar `PetControllerTests` da, nuqson esa
`PetValidator` da, ya'ni xato joyi va simptom joyi boshqa fayl.
