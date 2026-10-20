# refaktoring

Minimal shakl (patterns 23.24, architect 34.3, clean-code 38.1):

```java
// 1. Xarakterizatsiya testi: kutilgan qiymat koddan, yiqilgan assert xabaridan (eski kodda yashil)
@Test void withdrawFeeAndLogAsToday() {
    var s = new BillingService(); var a = accountWith("500");
    s.withdraw(a, new BigDecimal("200"));
    assertThat(a.getBalance()).isEqualByComparingTo("296.00");
    assertThat(s.getLog()).containsExactly("withdraw 1 200.00 fee 4.00");
}
// 2. Keyin bitta harakat (Extract Method, Move), test, keyingisi
```

Allaqachon bor, yozmang:
- Ish ro'yxati qo'lda emas: `python3 tools/metod_bormi.py <src> --audit` (ko'p yozuvchi maydon, takror blok, uzun metod); oldin va keyin sonlari hisobotda (architect 34.10)
- Har harakatdan keyin `run_tests.py <test> --yurgiz` (clean-code 38.2), qadam yiqilsa debug emas, oxirgi yashil holatga qaytish (clean-code 38.17)

Tuzoqlar:
- Refaktoring va mantiq o'zgarishi bir qadamda: xatti-harakat jim o'zgaradi; ikki shlyapa alohida, refaktoringda xarakterizatsiya testi o'zgartirilmaydi (clean-code 38.4)
- Public imzo, qabul qilinadigan qiymat (`setStatus("X")` har satrni oladi), xato matni ham xulq: ichki tur o'zgarsa ham public kirish-chiqish saqlanadi (clean-code 38.11)
- Servis egasidan so'rab (getter, `canX()`, `covers()`) keyin uning mutatorini chaqiradi yoki umumiy `adjustBalance(delta)` ochadi (feature envy): tekshiruv va o'zgarish egasining bitta niyatli metodida, natija qaytadi (`account.withdraw(total)`) (patterns 26.16, clean-code 33.18, 16.6)
- Public setter saqlanishi shart bo'lsa: ichki chaqiruv qolmaydi, setter `@Deprecated`, o'chirish va `java:S1133` Ochiq qaror (clean-code 36.12, 10.6, sonarqube 28.7)
- Ishlayotgan, o'zgarmaydigan kodga tegilmaydi; qolgani hisobotda (architect 34.11, clean-code 38.6)
