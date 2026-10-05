# 7-vazifa: test yozish, Owner.addPet

**Tur:** test yozish. **Tartib:** A birinchi, B ikkinchi.

## Tayyorlash

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
```

## Prompt (ikkala holatda aynan bir xil)

```text
Owner.addPet da dublikat tekshiruvi bor, lekin u faqat qisman
qoplangan. addPet ning hamma shoxini test bilan yoping.
```

## Qabul mezoni

1. `OwnerTests` da kamida uch YANGI test, hammasi yashil.
2. Quyidagi shoxlar qoplangan: `null` berilgan holat, bir xil obyekt
   ikki marta, bir xil `id` li ikki boshqa obyekt, va yangi (id siz)
   hayvonning qo'shilishi.
3. Butun to'plam yashil, `git diff --stat src/main` bo'sh.

## Tekshiruv

```bash
./mvnw -B test -Dtest='OwnerTests' -DfailIfNoSpecifiedTests=false
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
git diff --stat src/main
```

## Baholovchi uchun

`addPet` da uch chiqish yo'li bor: `pet == null`, `contains(pet)` va
`id` bo'yicha takror. To'rtinchi holat qo'shilish. Ko'r baholashda
qaraladigan narsa: test nomlari nimani tekshirayotganini aytadimi va
assertion aniqmi (`assertEquals(1, size)` kabi), yoki faqat
`assertTrue` bilan cheklanganmi.
