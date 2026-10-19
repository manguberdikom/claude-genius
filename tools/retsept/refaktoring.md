# refaktoring

Minimal shakl (patterns 23.24, architect 34.3, clean-code 38.1):

```java
// 1. Avval xarakterizatsiya testi: HOZIRGI xulq muzlatiladi (eski kodda yashil)
@Test void withdrawFeeAndLogAsToday() {
    var s = new BillingService(); var a = accountWith("500");
    s.withdraw(a, new BigDecimal("200"));
    assertThat(a.getBalance()).isEqualByComparingTo("296.00");
    assertThat(s.getLog()).containsExactly("withdraw 1 200.00 fee 4.00");
}
// 2. Keyin bitta harakat (Extract Method, Move to owner), test, keyingisi
```

Allaqachon bor, yozmang:
- Ish ro'yxati qo'lda emas: `python3 tools/metod_bormi.py <src> --audit` (ko'p yozuvchi maydon, takror blok, uzun metod); oldin va keyin sonlari hisobotda, kamayishi shart (architect 34.10)
- Har harakatdan keyin `run_tests.py <test> --yurgiz` (clean-code 38.2), qadam yiqilsa debug emas, oxirgi yashil holatga qaytish (clean-code 38.17)
- Takror mantiq uchun yangi metod emas: bor metodga chaqiruv yoki Extract Method (clean-code 32.2)

Tuzoqlar:
- Refaktoring va mantiq o'zgarishi bir qadamda: xatti-harakat jim o'zgaradi; ikki shlyapa alohida, refaktoringda xarakterizatsiya testi o'zgartirilmaydi (clean-code 38.4)
- Public imzo va xato matni (log, exception message) ham xulq: saqlanadi (clean-code 38.11)
- Servis boshqa obyekt getterlari bilan qoida hisoblab setter chaqiradi (feature envy): qoida va o'zgarish egasining bitta metodiga (`account.withdraw(total)`) (clean-code 33.18, 16.6)
- Public setter saqlanishi shart bo'lsa: ichki chaqiruv qolmaydi, setter `@Deprecated`, o'chirish Ochiq qaror (clean-code 36.12, 10.6)
- Ishlayotgan va o'zgarmaydigan kodga tegilmaydi; to'xtash nuqtasi audit nolga yaqinlashganda (architect 34.11, clean-code 38.6)
