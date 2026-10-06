# 4-vazifa: refaktoring, OwnerController ning qidiruv yo'li

**Tur:** refaktoring. **Tartib:** B birinchi, A ikkinchi.

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
OwnerController dagi `processFindForm` bir vaqtda to'rt ish qilyapti:
formani tekshiradi, qidiradi, natija soniga qarab uch xil javob
qaytaradi va modelni to'ldiradi. Uni o'qishga oson qil. Xulq
o'zgarmasligi kerak.
```

## Qabul mezoni

1. Butun to'plam yashil (76/76), bitta test ham o'zgartirilmagan.
2. `processFindForm` ning tashqi xulqi aynan o'sha: bo'sh familiya hamma
   egani beradi, bitta topilma egaga yo'naltiradi, bir nechtasi
   ro'yxatni beradi, nol topilma formaga xato qo'yadi.
3. Format darvozasi o'tadi (`./mvnw spring-javaformat:validate`).
4. Diff faqat `owner` paketidagi ishlab chiqarish kodiga tegadi.

## Tekshiruv

```bash
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
./mvnw -B spring-javaformat:validate
git diff --stat src/test   # bo'sh bo'lishi kerak
```

## Baholovchi uchun

Bu vazifada "to'g'ri javob" bitta emas. Ko'r baholashda qaraladigan
narsa: yangi metodlar nomi niyatni aytadimi, shart takrorlanmaydimi,
javob qaytarish yo'li bitta joyda jamlanganmi. Xulq o'zgarsa yoki test
tahrirlansa `muvaffaqiyat` = 0.
