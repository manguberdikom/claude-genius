---
type: feedback
---
# Spring IT: keshlangan context lar bir-biriga oqadi

To'liq IT yurishda (bir JVM, context keshi 32 ta) alohida o'tadigan sinflar
birga yiqiladi. Har sabab ko'p sinfni yiqitadi, shuning uchun avval yiqilishlarni
eng ichki `Caused by` bo'yicha guruhla, keyin tuzat.

- `TestTypeExcludeFilter` test sinfini faqat to'g'ridan-to'g'ri `@ExtendWith`,
  `@RunWith` yoki `@Test` metod bilan taniydi (`hasAnnotation`, meta emas). Abstract
  IT bazasida `@ExtendWith` faqat `@DataJpaTest` ichida bo'lsa, uning ichki
  `@Configuration` i ilova klassidan boshlangan context scan iga tushadi
  (`BeanDefinitionOverrideException`). Yechim: bazaga `@ExtendWith(SpringExtension.class)`.
- Ichki slice configni `@TestConfiguration` qilish yechim emas: context ning yagona
  sinfi test configuration bo'lsa, Boot qo'shimcha `@SpringBootConfiguration` ni
  qidiradi va repositorylar ikki marta ro'yxatga tushadi.
- spring-aspects classpath da bo'lsa, Spring Data `AuditingEntityListener` statik
  `AnnotationBeanConfigurerAspect` orqali sozlanadi. Auditingli context tirikligida
  qurilgan boshqa slice ning listeneri uning handleriga bog'lanadi. Kesh u context ni
  yopgach slice "context has been closed already" bilan yiqiladi, faqat sinflar
  tartibiga qarab. Yechim: auditing yoqiladigan IT larga `@DirtiesContext`, yopilishda
  aspekt bean factory ni bo'shatadi.
- O'z tranzaksiyasida commit qiladigan servisni (`NOT_SUPPORTED`, `REQUIRES_NEW`)
  sinovchi IT `@AfterEach` da yozganini tozalashi kerak. Aks holda rollback li
  slice lar umumiy bazada begona qator ko'radi. Test tranzaksiyasi qatorni qulflasa,
  `REQUIRES_NEW` tozalash qulfni kutib, socket timeout bilan uziladi: bunday test
  metodiga `@Transactional(propagation = NOT_SUPPORTED)`.
- `NOT_SUPPORTED` metod test tranzaksiyasidagi commit qilinmagan seedni ko'rmaydi.
  Test tranzaksiyasida o'qilgan entity esa keyingi o'qishda persistence context dan
  eski holida qaytadi.
- Gradle JUnit XML ni task oxirida yozadi: yurish o'rtasida papkada turgan XML
  oldingi yurishniki, unga tayanma.
