---
type: feedback
modified: 2026-10-28T00:00:00Z
---
# Servisda `EntityManager.flush()` istisnosi tarjima qilinmaydi

- Spring istisno tarjimasi (`DataIntegrityViolationException`) faqat `@Repository` proksi orqali ishlaydi. Servis yoki helper ichida to'g'ridan-to'g'ri `entityManager.flush()` unique/FK buzilishini Hibernate istisnosi bo'lib tashlaydi. `@ControllerAdvice` dagi `DataIntegrityViolationException` handleri uni ushlamaydi va javob 409 o'rniga 500 bo'ladi.
- Avval buzilish commit paytida chiqardi va tranzaksiya menejeri uni tarjima qilardi. `flush()` qo'shilishi bilan xulq jim o'zgaradi, unit test buni ko'rmaydi.
- Yo'l: `repository.saveAndFlush(x)` yoki `repository.flush()` (shu EntityManager ni flush qiladi, lekin tarjima bilan). `refresh()` uchun EntityManager qolishi mumkin.
- Review da: diffda yangi `entityManager.flush()` ko'rinsa, advice qaysi istisnolarni ushlashini tekshiring.
