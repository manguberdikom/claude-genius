# pul va son

Minimal shakl (clean-code 20.7, patterns 13.35):

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        Objects.requireNonNull(currency, "currency");
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.HALF_EVEN);
    }

    public Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("currency mismatch");
        }
        return new Money(amount.add(other.amount), currency);
    }
}
```

Allaqachon bor, yozmang:
- valyuta kodi va kasr soni jadvali o'rniga `java.util.Currency#getDefaultFractionDigits` (patterns 13.35)
- `new BigDecimal(double)` o'rniga `new BigDecimal("0.10")` yoki `BigDecimal.valueOf` (clean-code 20.1)
- qo'lda to'lib ketish tekshiruvi o'rniga `Math.addExact`, `Math.multiplyExact` (clean-code 20.3)
- format va kurs ko'p bo'lsa o'z Money kutubxonasi o'rniga JSR-354 Moneta yoki Joda-Money (patterns 13.35)

Tuzoqlar:
- pul, stavka uchun `double`/`float` ikkilik kasr xatosini yig'adi: `BigDecimal`, `long` tiyin yoki `Money`, bazada `numeric` (clean-code 20.1)
- `BigDecimal.equals` scale ni ham solishtiradi (`1.0` va `1.00` teng emas): qiymat uchun `compareTo` (clean-code 20.2)
- scale va `RoundingMode` siz `divide` aniq bo'linmasa `ArithmeticException` beradi: ikkalasini oshkor bering (clean-code 20.2)
- shartli chegirma: shart faqat stavka tanlaydi (chegirmasiz `ONE`), `multiply(rate).setScale(scale, mode)` keyin bir marta, scale yagona (code-review 14.3, clean-code 20.2, 37.17)
- DTO dagi `BigDecimal` pul `@Digits` bilan ustun `numeric(p,s)` ga moslab cheklanadi (`numeric(19,4)`: `@Digits(integer = 15, fraction = 4)`): aks holda ortiqcha kasr tekshirilmay o'tadi (patterns 13.35, code-review 26.2)
