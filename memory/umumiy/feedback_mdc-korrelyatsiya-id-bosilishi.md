---
type: feedback
---
# Filtrda MDC ga qo'yilgan korrelyatsiya id ni kutubxonaning interceptor i bosib ketadi

- Javobga sarlavha yozadigan filtr (`OncePerRequestFilter`) va MDC ga yozadigan
  `HandlerInterceptor` ikki xil qatlamda ishlaydi: filtr birinchi, interceptor keyin.
  Shuning uchun kutubxonada `@Component` bo'lgan interceptor va uni ro'yxatga oladigan
  `WebMvcConfigurer` bo'lsa, u filtr qo'ygan MDC qiymatini **bosib ketadi**.
- **Nega muhim:** oqibati jim. Javob sarlavhasida bitta id, javob tanasidagi va log
  qatoridagi id boshqa bo'lib qoladi. Unit testlar MDC ni o'zi qo'ygani uchun yashil
  chiqadi, nomuvofiqlik faqat haqiqiy servlet kontekstida ko'rinadi.
- **Qanday tekshiriladi:** kutubxona jarida `grep` bilan `HandlerInterceptor` va
  `WebMvcConfigurer` ni izla, ilovaning `@ComponentScan` ro'yxatida o'sha paket
  borligini ko'r. Sarlavha orqali id uzatishga ishonma: kutubxonaning shartida xato
  bo'lishi mumkin.
- **Yechim:** o'z interceptorini `@Order(Ordered.LOWEST_PRECEDENCE)` va
  `InterceptorRegistration.order(LOWEST_PRECEDENCE)` bilan oxirgi qo'yib, MDC ga
  o'z qiymatini qayta yozish. Qiymatni so'rov atributida tashish kerak, MDC da emas.
  `afterCompletion` da faqat o'zi qo'ygan bo'lsa tozalash: id thread pool da qolmasin.
- Nazorat testi: autoconfig siz holatda id lar mos kelmasligini tekshiradigan test
  yozilsin, aks holda tuzatish ishlayotganini isbotlab bo'lmaydi.
- Fon oqimida (scheduler, executor) MDC bo'sh: `[ref=]` bo'sh chiqadi. Har run boshida
  o'z id sini qo'yib, oxirida olib tashlash kerak.
