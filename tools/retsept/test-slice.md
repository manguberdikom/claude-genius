# test: slice

Minimal shakl (testing 7.2):

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @Autowired MockMvcTester mvc;
    @MockitoBean OrderService orderService;

    @Test
    void returnsOrder() {
        given(orderService.findById(42L)).willReturn(new OrderView(42L, "NEW"));
        assertThat(mvc.get().uri("/api/orders/42"))
                .hasStatusOk().bodyJson().extractingPath("$.status").isEqualTo("NEW");
    }
}
```

Allaqachon bor, yozmang:
- Eskirgan `@MockBean`/`@SpyBean` o'rniga `@MockitoBean`/`@MockitoSpyBean` (testing 7.2)
- JSONni qo'lda `ObjectMapper` bilan solishtirish o'rniga `JacksonTester` va `isEqualToJson` (testing 7.6)
- `@DataJpaTest` da ma'lumot sinalayotgan repository bilan emas, `TestEntityManager.persistFlushFind` bilan (testing 7.4)

Tuzoqlar:
- `@DataJpaTest` test bo'lmagan DataSource ni jimgina H2 ga almashtiradi (Boot < 3.4 da har qandayini); Boot 3.4+ standarti `Replace.NON_TEST` `@ServiceConnection` yoki `@DynamicPropertySource` bergan DB ni saqlaydi, boshqa holatda `replace = Replace.NONE` (patterns 25.45, testing 7.4)
- `em.flush()` va `em.clear()` siz query SQL ni emas, first-level cache ni tekshiradi (testing 7.4)
- `@DataJpaTest` har testni rollback qiladi: poyga va qulf testlarini u bilan yozmang (code-review 36.3)
