# tenglik shartnomasi

Minimal shakl, proxy maydoni bo'sh, shuning uchun `other.getId()` (clean-code 28.1, sonarqube 41.5):

```java
@Override
public boolean equals(Object o) {
    return this == o || o instanceof Payment other && id != null && id.equals(other.getId());
}

@Override
public int hashCode() {
    return Payment.class.hashCode();
}
```

Allaqachon bor, yozmang:
- Value object uchun qo'lda equals/hashCode o'rniga `record` (clean-code 15.3)
- Qo'lda compareTo hisobi o'rniga `static final` maydondagi `Comparator.comparing(..).thenComparing(..)` (clean-code 15.6)
- float/double `==` o'rniga `Double.compare`, null bo'lishi mumkin maydonda `Objects.equals`, massivda `Arrays.equals` (clean-code 15.3)
- Ko'p maydonli hash uchun `Objects.hash(a, b, c)`; issiq yo'lda boxing sabab qo'lda `31 * result + ...` (clean-code 15.2)

Tuzoqlar:
- equals yozilib hashCode qolib ketsa HashMap obyektni topmaydi: ikkalasi bir xil maydonlardan birga yoziladi (clean-code 15.2)
- Entity da `@Data` yoki hamma maydon bo'yicha tenglik proxy va o'zgaruvchan maydonda buziladi: tenglik id yoki o'zgarmas biznes kalit ustida, hash barqaror (sonarqube 41.5)
- compareTo da `a - b` to'lib ketib tartibni teskari qiladi: Comparator zanjiri ishlatiladi (clean-code 15.6)
