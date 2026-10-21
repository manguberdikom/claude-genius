---
type: feedback
---
# Maydon olib tashlangach ratchet allowlist eskiradi: javap bilan tekshir

- "Faqat kamayadi" allowlistlar (archunit `Class#field`, bean inventory) maydon yoki bean olib tashlanganda **eskirgan qator** testi bilan suite ni qizartiradi. Testlar yurmagan ijroda bu oxirigacha ko'rinmaydi.
- Bir nechta guruh entity maydonlarini olsa, hamma birlashgach allowlistni bir marta tekshiring. Manba regex i ishonchsiz: record komponenti, ichki sinf (`Outer#field` aslida `Outer$Inner` da) va umumiy nom (izohdagi `pinfl`) noto'g'ri natija beradi.
- Ishonchli yo'l: `compileJava` dan keyin `javap -p build/classes/.../Outer*.class` da `<field>;` bormi. Keyin faqat qoida testlarini yurgizing (architecture, bean inventory, changelog convention): to'liq suite siz ~20 s.
