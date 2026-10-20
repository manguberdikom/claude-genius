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
- valyuta kasr soni jadvali o'rniga `Currency#getDefaultFractionDigits` (patterns 13.35)
- `new BigDecimal(double)`, hisoblangan `double` dan `valueOf` o'rniga satr yoki tiyin: `new BigDecimal("0.10")`, `BigDecimal.valueOf(tiyin, 2)` (code-review 14.3)
- qo'lda overflow tekshiruvi o'rniga `Math.addExact`, `multiplyExact` (clean-code 20.3)
- format, kurs ko'p bo'lsa o'z kutubxona o'rniga JSR-354 Moneta, Joda-Money (patterns 13.35)

Tuzoqlar:
- pul, stavka `double`/`float` da kasr xatosi yig'adi: `BigDecimal`, `long` tiyin, `Money`, bazada `numeric` (clean-code 20.1)
- `BigDecimal.equals` scale ni ham solishtiradi (`1.0` != `1.00`): `compareTo` (clean-code 20.2)
- scale va `RoundingMode` siz `divide` aniq bo'linmasa `ArithmeticException`: ikkalasi oshkor, yaxlitlash bitta metodda (clean-code 20.2, 37.8)
- shartli chegirma: shart faqat stavka tanlaydi (chegirmasiz `ONE`), `multiply(rate).setScale(scale, mode)` bir marta, scale yagona; chegirmasiz summa ham yaxlitlanadi: `Ochiq qaror` (code-review 14.3, clean-code 20.2, 37.17)
- DTO dagi pul `BigDecimal` `@Digits` bilan ustun `numeric(p,s)` ga mos (`numeric(19,4)`: `@Digits(integer = 15, fraction = 4)`), aks holda kasr o'tadi (patterns 13.35, code-review 26.2)
