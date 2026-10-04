<!-- doc: testing | chapter: 12 | part:  -->

[Java Spring loyihasida testlash](../../README.md) / [Testlash qo'llanmasi](README.md)

# 12. End-to-end va UI testlar (End-to-End & UI Testing)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [12.1 E2E testning o'rni va narxi](#121-e2e-testning-orni-va-narxi)
- [12.2 Qaysi senariylarni E2E qilish kerak](#122-qaysi-senariylarni-e2e-qilish-kerak)
- [12.3 API darajasidagi E2E](#123-api-darajasidagi-e2e)
- [12.4 UI avtomatlashtirish vositalari](#124-ui-avtomatlashtirish-vositalari)
- [12.5 Page Object va Screenplay patternlari](#125-page-object-va-screenplay-patternlari)
- [12.6 Barqaror UI test yozish qoidalari](#126-barqaror-ui-test-yozish-qoidalari)
- [12.7 Test muhiti va ma'lumot](#127-test-muhiti-va-malumot)
- [12.8 Parallel bajarish va vaqt byudjeti](#128-parallel-bajarish-va-vaqt-byudjeti)
- [12.9 Nosozlikni tahlil qilish](#129-nosozlikni-tahlil-qilish)
- [12.10 Vizual regressiya testlash](#1210-vizual-regressiya-testlash)
- [12.11 Mobil va cross-browser](#1211-mobil-va-cross-browser)
- [12.12 Smoke suite](#1212-smoke-suite)
- [12.13 Anti-patternlar](#1213-anti-patternlar)
- [12.14 Arxitektor nazorat ro'yxati](#1214-arxitektor-nazorat-royxati)

</details>



End-to-end (E2E) va UI testlar test piramidasining eng yuqori, eng sekin va saqlashi eng qimmat qatlami: ular tizimni foydalanuvchi ko'rgan holida - brauzer, HTTP, ma'lumotlar bazasi, navbat, reverse proxy va tashqi sandbox'lar bilan birgalikda - tekshiradi. Arxitektor bu qatlamdan qamrov emas, ishonch kutadi: deploy qilingan tizim pul keltiruvchi asosiy yo'llarni haqiqatan bajara oladimi. Shu sababli E2E to'plam kichik, ataylab tanlangan va texnik jihatdan juda barqaror bo'lishi shart. Bu bobda qancha E2E test kerakligi, vosita tanlash mezonlari, barqaror test yozish qoidalari, nosozlikni tahlil qilish artefaktlari va smoke to'plamning deploy quvuridagi o'rni ko'rib chiqiladi.

## 12.1 E2E testning o'rni va narxi

E2E test faqat bitta savolga yaxshi javob beradi: "alohida sinovdan o'tgan bo'laklar birgalikda ishlaydimi?". Bu savol arzimas emas - eng qimmat production incident'lari ko'pincha mantiq xatosi emas, balki wiring xatosi bo'ladi: noto'g'ri profil, ishga tushmagan Flyway migratsiya, yetishmayotgan environment variable, CORS va cookie `SameSite` sozlamasi, Spring Security filter zanjiridagi tartib, gateway'dagi timeout, JSON serializatsiyadagi sana formati. Bularning hech birini unit test ko'rmaydi, chunki ularning har biri aynan "hamma narsa birga ko'tarilganda" paydo bo'ladi.

Narx tomoni ham aniq. Bitta unit test millisekundlar, integration test (Testcontainers bilan) sekundlar, UI orqali o'tadigan E2E senariy esa odatda 20-120 sekund oladi. Bunga brauzer konteynerlari, test muhitini tiklash va nosozlikni qayta tekshirish vaqti qo'shiladi. Diagnostika qiymati past: qizil E2E test "biror joyda buzildi" deydi, qaysi komponent aybdorini aytmaydi. Saqlash narxi ham yuqori - frontend'dagi har bir refactoring locator'larni buzadi.

Shu sababli miqdor cheklanadi. Amaliy mo'ljal: o'rta kattalikdagi mahsulot uchun 15-40 ta E2E senariy, ulardan 5-10 tasi smoke to'plamda. Statistika buni majburlaydi: agar har bir test 1% ehtimol bilan "sababsiz" uzilsa, 20 testlik to'plam uchun muvaffaqiyat ehtimoli 0.99^20 ≈ 0.82 bo'ladi, ya'ni har beshinchi ishga tushirish asossiz qizil. 100 testda esa bu ko'rsatkich 0.37 ga tushadi va hech kim natijaga ishonmaydi. Demak E2E qatlamda flakiness byudjeti test soniga teng darajada muhim resurs.

Har bir E2E test uchun arxitektor bitta savolga javob talab qilishi kerak: "bu test uzilsa, qaysi daromad yoki majburiyat yo'li to'xtaydi?". Javob bo'lmasa, test pastroq qatlamga ko'chiriladi.

## 12.2 Qaysi senariylarni E2E qilish kerak

E2E qilinadigan senariylar ro'yxati qisqa va biznesga bog'langan bo'ladi:

- **Pul oqimi**: savatdan to'lovga, to'lovdan tasdiqlangan buyurtmaga qadar to'liq yo'l, shu qatorda to'lov provayderi webhook'i kelgandan keyingi holat o'zgarishi.
- **Ro'yxatdan o'tish va kirish**: signup, email tasdiqlash, login, parol tiklash, sessiya muddati tugashi. Bu yo'l uzilsa qolgan hamma narsa ahamiyatsiz.
- **Buyurtma yakunlash va bekor qilish**: inventar zaxirasi, yetkazib berish manzili, qaytarish (refund) yo'li.
- **Kritik hisobot va eksport**: oylik moliyaviy hisobot, PDF/Excel eksport - ko'pincha alohida servis, alohida template engine va alohida permission qatlamidan o'tadi.
- **Rollar bo'yicha bitta-bittadan asosiy yo'l**: admin va oddiy foydalanuvchi uchun bittadan "happy path".

E2E qilinmasligi kerak bo'lgan narsalar ro'yxati esa ancha uzun: forma validatsiyasi, chegara qiymatlari (minimal/maksimal summa, uzunlik), xato matnlari va tarjimalar, hisob-kitob formulalari (chegirma, soliq, valyuta konvertatsiyasi), rol va huquq kombinatsiyalarining to'liq matritsasi, sahifalash va saralash variantlari, retry va timeout mantig'i. Bularning barchasi unit yoki `@WebMvcTest` / slice qatlamida bir necha yuz marta tezroq va ishonchliroq tekshiriladi. Qoida sifatida: UI orqali bir xil sahifani har xil parametrlar bilan qayta-qayta o'tkazish - E2E'ni funksional test deb ishlatishning eng keng tarqalgan shakli va eng qimmat xatosi.

## 12.3 API darajasidagi E2E

E2E'ning eng foydali shakli ko'pincha brauzersiz bo'ladi: butun ilovani haqiqiy portda ko'tarib, haqiqiy ma'lumotlar bazasi va broker bilan, senariyni HTTP orqali o'tkazish. Bu brauzer qatlamidan tashqari deyarli hamma integratsiya xatosini topadi, lekin 10-20 marta tezroq va bir necha marta barqarorroq ishlaydi. Spring'da uchta variant mavjud: `TestRestTemplate` (eng oddiy, blocking), `WebTestClient` (reactive stack yoki fluent assertion kerak bo'lsa) va `RestAssured` (eng o'qiluvchan DSL, JSON path assertion'lari kuchli).

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@Testcontainers
class CheckoutApiE2ETest {

    @Container @ServiceConnection
    static PostgreSQLContainer<?> db = new PostgreSQLContainer<>("postgres:16-alpine");

    @LocalServerPort int port;

    @BeforeEach
    void setUp() { RestAssured.port = port; RestAssured.basePath = "/api"; }

    @Test
    void customerCanPayForOrder() {
        String token = TestUsers.signUpAndLogin("e2e-" + UUID.randomUUID() + "@shop.io");
        long orderId = given().contentType(JSON).auth().oauth2(token)
                .body(Map.of("sku", "SKU-1", "qty", 2))
                .post("/orders").then().statusCode(201)
                .extract().jsonPath().getLong("id");

        given().contentType(JSON).auth().oauth2(token)
                .body(Map.of("card", "4242424242424242"))
                .post("/orders/{id}/payment", orderId)
                .then().statusCode(200)
                .body("status", equalTo("PAID"))
                .body("paidAt", notNullValue());
    }
}
```

Bu yerda `@ServiceConnection` (Spring Boot 3.1+) konteyner URL'ini avtomatik `DataSource`ga bog'laydi, `@LocalServerPort` esa haqiqiy tasodifiy portni beradi - ya'ni so'rov to'liq Tomcat, filter zanjiri, controller va tranzaksiya qatlamidan o'tadi. Amaliy taqsimot: biznes senariylarining 70-80% ini API darajasida, faqat qolganini brauzerda tekshirish. UI qatlamiga esa faqat "foydalanuvchi haqiqatan bosib o'tadigan" yo'llar qoldiriladi.

## 12.4 UI avtomatlashtirish vositalari

| Vosita | Til / bog'lanish | Auto-wait | Tezlik | Barqarorlik | Debug artefaktlari | Parallel | Qachon tanlash |
|---|---|---|---|---|---|---|---|
| Selenium 4.x WebDriver | Java, Python, C#, JS | Yo'q (`WebDriverWait` qo'lda) | O'rta | O'rta (qo'lda kutishga bog'liq) | Screenshot, Grid video, BiDi/CDP log | Grid orqali yaxshi | Mavjud Grid, keng brauzer/legacy qamrov, real device cloud |
| Playwright for Java | Java (+ TS, Python, .NET) | Ha, web-first assertion | Yuqori | Yuqori | Trace viewer, video, HAR, console | JUnit 5 + context'lar bilan yaxshi | Yangi loyiha, tez va barqaror UI suite kerak |
| Selenide | Faqat Java (Selenium ustida) | Ha (`should*` kutadi) | O'rta-yuqori | Yuqori | Avto-screenshot, sodda hisobot | Grid orqali yaxshi | Java jamoasi Selenium ekosistemasida qolishni xohlasa |
| Cypress | Faqat JS/TS | Ha | Yuqori | Yuqori | Time-travel debug, video | Cloud/orkestratsiya bilan | Testlar frontend jamoasi qo'lida bo'lsa |

Tanlov mezonlari texnik emas, tashkiliy: **testlarni kim saqlaydi?** Agar E2E'ni backend/QA Java jamoasi yozsa, Playwright for Java yoki Selenide tanlanadi - bitta build, bitta CI, bitta dependency daraxti. Agar testlar frontend jamoasining mas'uliyatida bo'lsa, Cypress yoki Playwright'ning TypeScript runner'i mantiqiyroq, chunki u yerda snapshot assertion va fixture modeli kuchliroq. Yangi Java loyihasi uchun standart tavsiya: **Playwright for Java** - auto-wait va trace viewer flaky testlar bilan kurashda eng katta foyda beradi. Selenium esa zarur bo'lib qoladi, agar sizga Appium, real qurilma cloud'i yoki juda keng brauzer matritsasi kerak bo'lsa.

## 12.5 Page Object va Screenplay patternlari

Page Object - UI test kodining eng muhim abstraksiyasi: locator va o'zaro ta'sir detallari bitta klassda yashaydi, test esa faqat biznes tilida gapiradi. Qoida: Page Object assertion'lar bilan to'lib ketmasligi kerak, lekin "sahifa yuklandi" darajasidagi tekshiruvni o'zida ushlashi normal.

```java
public class LoginPage {
    private final Page page;

    public LoginPage(Page page) { this.page = page; }

    public LoginPage open() {
        page.navigate("/login");
        return this;
    }

    public CheckoutPage loginAs(String email, String password) {
        page.getByTestId("login-email").fill(email);
        page.getByTestId("login-password").fill(password);
        page.getByTestId("login-submit").click();
        assertThat(page.getByTestId("user-menu")).isVisible();
        return new CheckoutPage(page);
    }

    public String errorMessage() {
        return page.getByTestId("login-error").innerText();
    }
}
```

```java
public class CheckoutPage {
    private final Page page;
    private final Locator total;

    public CheckoutPage(Page page) {
        this.page = page;
        this.total = page.getByTestId("cart-total");
    }

    public CheckoutPage payWithTestCard() {
        page.getByTestId("card-number").fill("4242424242424242");
        page.getByTestId("pay-now").click();
        return this;
    }

    public void shouldBePaid(String expectedTotal) {
        assertThat(total).hasText(expectedTotal);
        assertThat(page.getByTestId("order-status")).hasText("PAID");
    }
}
```

Katta suite'larda Page Object klasslari 500 qatorga o'sib ketadi. Bunga yechim - **komponent darajasidagi abstraksiya**: `CartWidget`, `AddressForm`, `DataTable` kabi klasslar o'z ildiz `Locator`ini qabul qiladi (`page.getByTestId("cart")`) va ichida nisbiy qidiradi. Shunda bir xil komponent bir necha sahifada qayta ishlatiladi.

**Screenplay** pattern (Serenity BDD'da `Actor`, `Performable`, `Question`) bir qadam uzoqroq boradi: sahifa emas, foydalanuvchi vazifalari modellashtiriladi - `actor.attemptsTo(Login.withCredentials(user), Checkout.withTestCard())`. Bu ko'p rolli, ko'p foydalanuvchili senariylarda (masalan sotuvchi va xaridor bir senariyda) Page Object'dan toza chiqadi, lekin o'rganish narxi yuqori. Tavsiya: 30 testdan kichik suite uchun Page Object yetarli; ko'p aktyorli murakkab domenda Screenplay'ni ko'rib chiqing.

Locator strategiyasi barqarorlikning yarmi: birinchi tanlov - `data-testid` (dizayn o'zgarishidan himoyalangan, frontend bilan shartnoma sifatida kelishiladi), ikkinchi - `getByRole` va accessible name (bir vaqtda accessibility'ni ham tekshiradi), uchinchi - matn. XPath va uzun CSS zanjirlari (`div > div:nth-child(3) > span`) taqiqlanadi: ular DOM tuzilishiga bog'lanadi va har markup o'zgarishida buziladi. Playwright'da test atribut nomi `playwright.selectors().setTestIdAttribute("data-qa")` bilan moslashtiriladi.

## 12.6 Barqaror UI test yozish qoidalari

- **`Thread.sleep` qat'iy taqiqlanadi.** U yo testni sekinlashtiradi, yo sekin CI'da yetmaydi. Faqat auto-wait (`assertThat(locator).isVisible()`, Selenide'dagi `shouldBe`) yoki aniq shartga bog'langan kutish ishlatiladi: `page.waitForResponse("**/api/orders", () -> ...)`, `locator.waitFor()`.
- **Timeout bitta joyda sozlanadi**, test ichida emas: global `setDefaultTimeout` va faqat haqiqatan sekin operatsiya uchun lokal override.
- **Retry faqat infratuzilma uchun.** Konteyner ko'tarilmasligi, DNS, tarmoq uzilishi - qayta urinishga arziydi. Biznes senariyning o'zini retry qilish xatoni yashiradi (flaky testlar jarayoni [16-bobda](16-flaky-testlar-test-qarzi-va-test-kodini.md)).
- **Har test o'z ma'lumotini API orqali yaratadi** va unique identifikator ishlatadi (`"e2e-" + UUID.randomUUID() + "@shop.io"`). Shunda testlar bir-biriga ta'sir qilmaydi va parallel ishlaydi.
- **Testlar idempotent bo'ladi**: ikki marta ketma-ket ishga tushirilsa, bir xil natija berishi shart. Umumiy, oldindan tayyorlangan "demo" akkauntga bog'lanish parallel bajarishni darhol buzadi.
- **Kirish sessiyasi qayta ishlatiladi.** Har testda login UI orqali o'tish 5-15 sekundni behuda sarflaydi va eng mo'rt qadamni har testga ko'paytiradi. Playwright'da yechim - `storageState`.

```java
public final class AuthState {
    private static final Path STATE = Path.of("target/e2e/admin-state.json");

    public static synchronized Path adminState(Browser browser, String baseUrl) {
        if (Files.exists(STATE)) return STATE;
        try (BrowserContext ctx = browser.newContext(
                new Browser.NewContextOptions().setBaseURL(baseUrl))) {
            Page page = ctx.newPage();
            page.navigate("/login");
            page.getByTestId("login-email").fill(System.getenv("E2E_ADMIN_USER"));
            page.getByTestId("login-password").fill(System.getenv("E2E_ADMIN_PASS"));
            page.getByTestId("login-submit").click();
            assertThat(page.getByTestId("user-menu")).isVisible();
            ctx.storageState(new BrowserContext.StorageStateOptions().setPath(STATE));
        }
        return STATE;
    }
}
```

Keyin har test `browser.newContext(new Browser.NewContextOptions().setStorageStatePath(AuthState.adminState(...)))` bilan allaqachon kirgan holda boshlanadi. Login yo'lining o'zi esa alohida, bitta aniq test bilan tekshiriladi.

## 12.7 Test muhiti va ma'lumot

E2E uchun to'g'ri muhit - production bilan bir xil artefaktdan deploy qilingan, alohida ma'lumotlar bazasiga ega va faqat avtomatlashtirilgan testlar uchun ajratilgan `e2e` muhiti. Qo'l bilan sinovdan o'tkaziladigan staging bilan birga ishlatish flakiness'ning birinchi sababi: kimdir ma'lumotni o'zgartiradi va test tushadi.

Ma'lumot tayyorlashda tartib shunday: birinchi navbatda **ilovaning o'z API'si** orqali (haqiqiy validatsiya va domen qoidalaridan o'tadi, shartnoma o'zgarsa test ham o'zgaradi), API erisha olmaydigan holatlar uchun (muddati o'tgan obuna, arxivlangan buyurtma) esa faqat `e2e` profilida yoqiladigan **test-support endpoint**lari. To'g'ridan-to'g'ri SQL eng oxirgi chora: u sxemaga bog'lanadi, migratsiyadan keyin jimgina buziladi va domen invariantlarini chetlab o'tib, real bo'lmagan holat yaratadi.

```yaml
spring:
  config:
    activate:
      on-profile: e2e
  datasource:
    url: jdbc:postgresql://db:5432/shop_e2e
app:
  payments:
    provider: stripe
    mode: test                     # provayderning sandbox rejimi
    secret-key: ${STRIPE_TEST_SK}
    webhook-endpoint: /api/payments/webhook
  features:
    new-checkout: true             # feature flag bilan senariy holatini boshqarish
    email-sending: false           # SMTP o'rniga in-memory sink
  test-support:
    seed-endpoints-enabled: true   # faqat e2e profilida
```

Feature flag'lar E2E uchun ikki tomonlama foyda beradi: yangi yo'lni testda yoqib, production'da o'chirib turish mumkin; va flag holatini test boshida HTTP header yoki admin endpoint orqali o'rnatib, deterministik senariy olinadi. Tashqi to'lov tizimi esa albatta o'z sandbox'ida ishlatiladi (test kalitlari, provayderning e'lon qilgan test karta raqamlari), lekin webhook yetib kelishini kutish uchun testda aniq shart bo'yicha polling kerak - "sleep qilib umid qilish" emas. Barqarorligi past yoki pullik tashqi servislar E2E'da chegara adapteri darajasida stub bilan almashtiriladi.

## 12.8 Parallel bajarish va vaqt byudjeti

E2E suite uchun vaqt byudjeti oldindan e'lon qilinadi: smoke 2-5 daqiqa, to'liq suite 15-20 daqiqa. Byudjet buzilganda testlar qo'shilmaydi - ular qisqartiriladi yoki pastroq qatlamga ko'chiriladi.

Byudjetga erishishning uch vositasi bor. Birinchi - **suite ichidagi parallelizm**: JUnit 5'da `junit-platform.properties` orqali `junit.jupiter.execution.parallel.enabled=true`, `junit.jupiter.execution.parallel.mode.classes.default=concurrent` va `...config.fixed.parallelism=4`. Bu faqat testlar bir-biridan mustaqil ma'lumot ishlatganda ishlaydi. Ikkinchi - **sharding**: testlarni `@Tag` bo'yicha domenlarga bo'lib, CI matritsasida parallel joblar sifatida ishga tushirish. Uchinchi - **brauzer konteynerlari**: Selenium Grid 4 (hub + node-chrome), Testcontainers'ning `BrowserWebDriverContainer` (video yozish bilan) yoki Playwright'ning rasmiy `mcr.microsoft.com/playwright/java:v<versiya>-jammy` image'i - bu oxirgisi lokal va CI o'rtasida bir xil brauzer/font muhitini kafolatlaydi.

```yaml
e2e:
  runs-on: ubuntu-latest
  timeout-minutes: 20
  strategy:
    fail-fast: false
    matrix:
      shard: [auth, checkout, reporting]
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-java@v4
      with: { distribution: temurin, java-version: '21', cache: maven }
    - run: mvn -B verify -Pe2e -Dgroups=${{ matrix.shard }}
      env:
        E2E_BASE_URL: ${{ secrets.E2E_BASE_URL }}
    - if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: e2e-artifacts-${{ matrix.shard }}
        path: |
          target/e2e/**/*.zip
          target/e2e/**/*.png
```

Har test uchun qattiq timeout ham qo'yiladi (`junit.jupiter.execution.timeout.test.method.default=3m`), aks holda osilib qolgan bitta test butun job'ni CI limitiga qadar band qiladi.

## 12.9 Nosozlikni tahlil qilish

E2E testning qiymati uning nosozlik hisobotining sifati bilan belgilanadi. "Expected PAID but was NEW" degan xabar hech narsa bermaydi. Minimal artefakt to'plami: uzilish paytidagi to'liq sahifa screenshot'i, video yoki trace, brauzer console va network log'i, server tomonidagi ilova log'i va test identifikatorini so'rovlar bilan bog'lovchi korrelyatsiya header'i (`X-E2E-Test-Id`, yoki `traceparent`).

```java
public class PlaywrightArtifacts implements TestWatcher {

    @Override
    public void testFailed(ExtensionContext ctx, Throwable cause) {
        PwFixture pw = PwFixture.current(ctx);
        Path dir = Path.of("target/e2e", ctx.getRequiredTestClass().getSimpleName());
        String name = ctx.getDisplayName().replaceAll("\\W+", "_");

        pw.page().screenshot(new Page.ScreenshotOptions()
                .setPath(dir.resolve(name + ".png")).setFullPage(true));
        pw.context().tracing().stop(new Tracing.StopOptions()
                .setPath(dir.resolve(name + "-trace.zip")));
        pw.dumpConsoleAndNetwork(dir.resolve(name + "-browser.log"));
        pw.copyServerLogs(dir.resolve(name + "-app.log"));
    }

    @Override
    public void testSuccessful(ExtensionContext ctx) {
        PwFixture.current(ctx).context().tracing()
                .stop(new Tracing.StopOptions());   // artefakt saqlanmaydi
    }
}
```

Tracing test boshida `context.tracing().start(new Tracing.StartOptions().setScreenshots(true).setSnapshots(true).setSources(true))` bilan yoqiladi. Playwright trace viewer (`npx playwright show-trace trace.zip` yoki `trace.playwright.dev`) har qadamni DOM snapshot, network va console bilan ko'rsatadi - bu flaky testni tashxislashda eng kuchli vosita. Selenium tomonida ekvivalenti: `BrowserWebDriverContainer.withRecordingMode(VncRecordingMode.RECORD_FAILING, dir)` bilan video va BiDi/CDP orqali log yig'ish. Artefaktlar CI'da har shard uchun alohida yuklanadi va kamida bir necha hafta saqlanadi.

## 12.10 Vizual regressiya testlash

Vizual regressiya screenshot'ni ma'lum (baseline) rasm bilan piksel darajasida taqqoslaydi. U funksional test topa olmaydigan xatolarni ko'radi: buzilgan CSS, ustma-ust tushgan elementlar, yo'qolgan logotip, dark mode'da o'qilmaydigan matn.

Flakiness sabablari deyarli har doim bir xil: font yuklanishi va antialiasing (OS'ga bog'liq), animatsiya va `transition`, kursor miltillashi, scrollbar, dinamik ma'lumot (sana, ID, avatar), va viewport o'lchamining o'zgarishi. Shuning uchun qoidalar qat'iy: baseline faqat CI bilan **bir xil Docker image**da generatsiya qilinadi; animatsiya `page.addStyleTag` bilan o'chiriladi (`*, *::before { animation: none !important; transition: none !important; }`); vaqt va dinamik bloklar mask qilinadi yoki fixture bilan muzlatiladi; tolerance esa 0 emas, lekin juda kichik (0.1-0.5% piksel) bo'ladi - katta tolerance haqiqiy regressiyani yashiradi.

Java ekosistemasida tayyor snapshot assertion yo'q: Playwright'ning `toHaveScreenshot` imkoniyati faqat TypeScript runner'ida. Java uchun amaliy variantlar - `ashot` kutubxonasi (Selenium bilan), Applitools Eyes yoki Percy kabi cloud SDK'lar (AI/DOM asosida farqlarni filtrlaydi), yoki frontend tomonida Storybook + BackstopJS. Eng oqilona qarori: vizual testni E2E senariylaridan ajratish va komponent galereyasi darajasida ishlatish - u yerda sahifa holati deterministik, baseline'lar esa arzon.

## 12.11 Mobil va cross-browser

Brauzer matritsasi analitika bilan asoslanadi, "har ehtimolga qarshi" bilan emas. Amaliy model: har PR'da faqat Chromium; kechasi (nightly) Firefox va WebKit qo'shiladi; legacy brauzerlar faqat real foydalanuvchi ulushi bo'lsa. Playwright bitta API bilan uchta engine'ni beradi, bu matritsani kengaytirishni arzonlashtiradi.

Responsive tekshiruv alohida E2E senariy emas: bir necha asosiy sahifani belgilangan breakpoint viewport'larida (masalan 390x844, 768x1024, 1440x900) ochib, kritik elementlar ko'rinishini va bosilishini tasdiqlash yetarli. Playwright'da `new Browser.NewContextOptions().setViewportSize(390, 844).setHasTouch(true)` yoki `playwright.devices()` dan qurilma deskriptori ishlatiladi.

Native mobil ilova - bu butunlay boshqa suite. Appium 2.x (`java-client`, UiAutomator2 va XCUITest drayverlari) web E2E bilan bir xil Page Object yondashuvini qo'llaydi, lekin o'z infratuzilmasi (emulyator yoki real device cloud), o'z vaqt byudjeti va o'z mas'ul jamoasini talab qiladi. Uni web E2E quvuriga qo'shmaslik kerak: deploy'ni 40 daqiqalik emulyator jobiga bog'lab qo'yish mahsulot tezligini o'ldiradi.

## 12.12 Smoke suite

Smoke to'plam - deploy'dan keyin darhol ishga tushadigan, 2-5 daqiqada tugaydigan 5-10 senariy: tizim tirikmi, login ishlaydimi, asosiy sahifa ma'lumot bilan yuklanadimi, bitta buyurtma to'lanadimi, kritik hisobot generatsiya bo'ladimi. Bu to'plam `@Tag("smoke")` bilan belgilanadi va deploy quvurining gate'i bo'ladi: qizil bo'lsa, release avtomatik rollback qilinadi yoki trafik yangi versiyaga o'tkazilmaydi.

Smoke senariylari production'da ham xavfsiz bo'lishi uchun ular ko'proq o'qishga tayanadi, bitta yozuv operatsiyasi esa ajratilgan test akkaunt va test to'lov usuli bilan bajariladi hamda o'zidan keyin tozalanadi. Aynan shu senariylar keyinchalik production'da **synthetic monitoring** probe'lari sifatida qayta ishlatiladi - har 5 daqiqada ishlaydigan, alert'ga bog'langan tashqi tekshiruvlar (batafsil [15-bobda](15-ci-cd-da-test-pipeline.md)). Bitta senariy ta'rifini CI gate va synthetic monitoring o'rtasida bo'lishish - bu qatlamdan olinadigan eng yuqori qaytim.

## 12.13 Anti-patternlar

- **Biznes qoidalarini E2E bilan qoplash.** Chegirma formulasi yoki soliq hisobi UI orqali 40 senariyda tekshirilganda, suite sekin va mo'rt bo'ladi, xato joyi esa noaniq qoladi. Bu mantiq unit testga tegishli.
- **UI test ichida SQL bilan ma'lumotni "tuzatish".** Test o'rtasida `UPDATE orders SET status='PAID'` yozilsa, test real bo'lmagan holatni tekshiradi va sxema o'zgarishida jimgina buziladi. Ma'lumot API yoki ajratilgan test-support endpoint orqali tayyorlanadi.
- **Umumiy akkauntdan foydalanish.** Barcha testlar bitta `qa@company.com` bilan ishlasa, parallelizm imkonsiz, natijalar esa ishga tushirish tartibiga bog'lanib qoladi.
- **Barcha E2E testni har PR'da ishga tushirish.** Bu feedback'ni 30-40 daqiqaga cho'zadi va jamoani "qizilni e'tiborsiz qoldirish" madaniyatiga olib keladi. PR'da smoke + o'zgargan domen shard'i, to'liq suite esa merge'dan keyin yoki nightly.
- **Flaky testni retry bilan yashirish.** `rerunFailingTestsCount=3` statistikani yaxshilaydi, lekin haqiqiy race condition va noto'g'ri kutishni ko'rinmas qiladi - ya'ni production xatosini test bilan to'laydi.
- **Baseline'ni ko'r-ko'rona yangilash.** Vizual test qizil bo'lganda baseline'ni avtomatik qabul qilish vizual testni butunlay bekor qiladi.
- **Page Object'ni assertion ombori qilish.** Sahifa klassi ichida o'nlab biznes tekshiruvi bo'lsa, senariy niyati kodda ko'rinmaydi va qayta ishlatish yo'qoladi.

## 12.14 Arxitektor nazorat ro'yxati

- [ ] E2E senariylar soni cheklangan (15-40) va har biri aniq biznes/daromad yo'liga bog'langan; ro'yxat yozilib qo'yilgan.
- [ ] Biznes mantiqning asosiy qismi API va slice darajasida qoplangan; UI E2E faqat foydalanuvchi yo'lini tekshiradi.
- [ ] Barcha locator'lar `data-testid` yoki accessible role asosida; XPath va chuqur CSS zanjirlari CI'da taqiqlangan.
- [ ] Kodda `Thread.sleep` yo'q; kutish faqat auto-wait yoki aniq shart bilan amalga oshiriladi.
- [ ] Har test o'z ma'lumotini API orqali, unique identifikator bilan yaratadi; umumiy akkaunt va test tartibiga bog'liqlik yo'q.
- [ ] Nosozlikda screenshot, trace/video, brauzer va server log'lari avtomatik yig'iladi va CI artefakti sifatida saqlanadi.
- [ ] Smoke to'plam 5 daqiqadan oshmaydi, deploy gate'iga ulangan va synthetic monitoring bilan senariylarni bo'lishadi.
- [ ] To'liq suite uchun vaqt byudjeti e'lon qilingan, sharding va parallelizm sozlangan, retry faqat infratuzilma xatolari uchun ruxsat etilgan.

---

[&larr; 11. Xavfsizlik, tranzaksiya, asinxron va konkurentlik testlari](11-xavfsizlik-tranzaksiya-asinxron-va.md) · [Mundarija](README.md) · [13. Nofunksional testlar: performance, resilience, xavfsizlik &rarr;](13-nofunksional-testlar-performance-resilience.md)
