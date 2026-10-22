---
type: feedback
---
# Sonar ning "mexanik" tavsiyasi xulqni o'zgartirishi mumkin

Sonar issue ni tavsiyasi bo'yicha ko'r-ko'rona tuzatgandan keyin ta'sirlangan unit
testlar yurmaguncha commit qilinmaydi. Bitta partiyada ikki tavsiya 344 testni
yiqitdi:

- `java:S1612` (lambda o'rniga method reference): `() -> this.field.get()` maydonni
  chaqiruvda o'qiydi, `this.field::get` esa ifoda hisoblanganda darhol o'qiydi. Maydon
  initsializatori shu maydon e'lonidan oldin tursa, u hali null va NPE chiqadi. Tuzatish:
  maydonni ishlatuvchidan oldin e'lon qil.
- `java:S4276` (`Function<Long, T>` o'rniga `LongFunction<T>`): kalit null bo'lishi
  mumkin bo'lsa unboxing da NPE chiqadi. Null mumkin bo'lsa `Function` qoladi va
  `@SuppressWarnings("java:S4276")` ga sabab izohi yoziladi.
- Gate ni "yangi kod" bo'yicha baholashdan oldin har topilma qatorini asos commitga
  nisbatan diff bilan tasnifla (yangi fayl, tegilgan qator, eski qator). Qayta
  yaratilgan lokal loyihada yangi kod davri butun kodni qamrashi mumkin. Server dagi
  ko'rib chiqish statuslari ko'chmasa, hotspot va xavfsizlik reytingi shartlari
  eski koddan yiqiladi.
