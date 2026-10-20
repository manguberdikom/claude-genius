# test: arxitektura

Minimal shakl (testing 14.3):

```java
@AnalyzeClasses(packages = "com.shop",
        importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {
    @ArchTest
    static final ArchRule layers = layeredArchitecture()
            .consideringOnlyDependenciesInLayers()
            .layer("Web").definedBy("..web..")
            .layer("Service").definedBy("..service..")
            .layer("Persistence").definedBy("..repository..")
            .whereLayer("Service").mayOnlyBeAccessedByLayers("Web")
            .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service");
    @ArchTest
    static final ArchRule noCycles = slices()
            .matching("com.shop.(*)..").should().beFreeOfCycles();
}
```

Allaqachon bor, yozmang:
- o'nlab qatlam `noClasses()` o'rniga `Architectures.layeredArchitecture()` (testing 14.3)
- modul paket qoidalari o'rniga `ApplicationModules.of(App.class).verify()` (testing 14.4)

Tuzoqlar:
- `@AnalyzeClasses` ostidagi oddiy `@Test` da `DoNotIncludeTests` ishlamaydi: qoida `@ArchTest` maydonida (sonarqube 40.5)
- eski loyihada yangi qoida yuzlab buzilish beradi: `FreezingArchRule.freeze(...)`, store git'da (testing 14.2)
- Sonar'dagi qoidani takrorlamang: ArchUnit'da faqat bog'liqlik, qatlam, nomlash, annotatsiya (sonarqube 40.5)
