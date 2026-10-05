# 5-vazifa: refaktoring, Owner dagi takroriy getPet

**Tur:** refaktoring. **Tartib:** A birinchi, B ikkinchi.

## Tayyorlash

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
```

## Prompt (ikkala holatda aynan bir xil)

```text
Owner sinfida uch xil qidirish bor: getPet(String), getPet(String,
boolean) va getPet(Integer). Ichidagi sikl va null qaytarish har
birida takrorlanadi. Takrorni kamaytir va null qaytarishni ochiq qil.
Chaqiruvchilar buzilmasligi kerak.
```

## Qabul mezoni

1. Butun to'plam yashil (76/76), test o'zgartirilmagan.
2. `Owner` ning ommaviy API si saqlangan yoki chaqiruvchilar bilan
   birga moslangan: `PetController`, `VisitController` va
   `PetValidator` kompilyatsiyadan o'tadi.
3. Format darvozasi o'tadi.
4. Agar `Optional` kiritilgan bo'lsa, u maydon yoki parametr turi
   sifatida emas, qaytish turi sifatida ishlatilgan.

## Tekshiruv

```bash
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
./mvnw -B spring-javaformat:validate
git diff --stat src/test
```

## Baholovchi uchun

Diqqat: `getPet(String name, boolean ignoreNew)` ning `ignoreNew`
bayrog'i bool parametr hidining klassik misoli. Uni ikki nomli metodga
ajratish ham to'g'ri javob, saqlab qolish ham. Ko'r baholashda
qaraladigan narsa: takror kamayganmi va chaqiruv joylarida null
tekshiruvi tushunarli bo'lganmi.
