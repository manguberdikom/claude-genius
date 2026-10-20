# Umumiy yozish qoidalari: test fayli

Test yozgan va ko'rgan har aktyor uchun bir xil (testing 5.13,
sonarqube 19.2, sonarqube 30.15).

- Daraja: domen qoidasi sof unit (Spring yo'q); SQL va JPA so'rovi real PostgreSQL Testcontainers, H2 emas; HTTP kontrakti `@WebMvcTest`; slice yetsa `@SpringBootTest` emas (testing 2.5, 7.12).
- Test implementatsiyani emas, xatti-harakatni tekshiradi: refaktoringda qizarmaydi (testing 5.1, 5.8).
- Mock faqat I/O chegarasida; value object, DTO, `record`, JDK sinfi real nusxa (testing 5.1, 5.7, 5.15).
- Assertionsiz test yo'q (`java:S2699`); getter va setter testi yo'q; bir test bitta xatti-harakat va bitta Act, nomi uni aytadi; bu assertion soni emas (testing 5.3, clean-code 30.5).
- Kutilgan qiymat qo'lda yozilgan literal, ishlab chiqarish formulasi yoki o'sha `RoundingMode` bilan hisoblanmaydi; happy path bilan birga chegara holat (bo'sh, nol, maksimum, xato yo'li) ham (code-review 35.7, 43.3).
- Test nomidagi xatti-harakatga tegishli bo'lmagan assertion, `verify`, `verifyNoMoreInteractions` yozilmaydi; `when(...)` bilan stub qilingan so'rov `verify` qilinmaydi (testing 5.16, 5.3).
- Testda bo'sh `catch` va `try/catch` + `fail()` yo'q: `assertThatThrownBy` (testing 5.9, sonarqube 27.6).
- Tashqi mijoz xatosi u haqiqatda otadigan tur bilan taqlid qilinadi: `thenThrow(new GatewayTimeoutException(..))`, HTTP da `withServerError()` (sonarqube 18.8, testing 9.4).
- `Thread.sleep` bilan kutish yo'q; flaky test `@Disabled` yoki qayta urinish bilan yopilmaydi, sababi (vaqt, tartib, umumiy holat) tuzatiladi.
- Oy int literal emas, `Month` enum: `LocalDate.of(2026, Month.OCTOBER, 7)`, `LocalDateTime.of(2026, Month.OCTOBER, 2, 8, 30)` ham (`java:S8694`).
- Tizim soati yo'q: `Clock.fixed(...)`; testda `Instant.now()`, `LocalDate.now(ZONE)`, `Clock.systemUTC()` yo'q (`java:S8692`).
- `assertThrows` va `assertThatThrownBy` lambdasida bitta chaqiruv, tayyorlash tashqarida; argumentdagi `x.getId()` va `rethrowing(f).run(() -> ..)` ham ikkinchi chaqiruv: oldindan `var id = x.getId();`, `var action = rethrowing(f);` (`java:S5778`).
- Faqat kirishi farq qiladigan uch test bitta `@ParameterizedTest(name = "{0}")` + `@MethodSource` (`java:S5976`).
- AssertJ maxsus assertion: `hasSize`, `isEmpty`, `hasToString`, `containsEntry` (`java:S5838`); actual avval, kutilgan keyin (`S3415`); bir subyektga ketma-ket `assertThat` bitta zanjirda (`S5853`); `allSatisfy`, `doesNotContain` dan oldin ro'yxat bo'sh emasligi (`S5841`).
- JVM system property ga yozilmaydi (`System.setProperty`, `getSystemProperties().put(..)`, `getSystemEnvironment().put(..)`): fork dagi keyingi testlarga sizadi, testlar tartibga bog'liq yiqiladi; `environment.getPropertySources().addFirst(new MapPropertySource(..))` (testing 15.14). <!-- agar: setProperty|getSystemProperties|getSystemEnvironment -->
- ArchUnit `ClassFileImporter` natijasi static maydonda saqlanmaydi (`static final JavaClasses`, `@BeforeAll`): yuzlab MB lik graf fork oxirigacha heap da qoladi, CI da bir forkdagi arxitektura testlari `OutOfMemoryError` bilan o'ladi; `SoftReference` keshli yordamchi yoki `@AnalyzeClasses` keshi (testing 15.14). <!-- agar: ArchUnit|ClassFileImporter -->
- Yetib bo'lmaydigan himoya sharti testlanmaydi: ishlab chiqarish kodi egasiga olib tashlash aytiladi (sonarqube 11.9).
- Testni o'tkazish uchun assertion bo'shatilmaydi.
