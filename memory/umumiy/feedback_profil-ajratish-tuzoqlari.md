---
type: feedback
---
# application.yml ni profil fayllariga ajratish: uch tuzoq

- **Base nomini o'zgartirmang.** Kutubxona jarlari ham `classpath:application.yml`
  olib kelsa, servisning o'z `application.yml` i ularni yopib turadi. Base
  `application.yaml` deb nomlansa jar dagi `application.yml` yuklanadi va undan
  ustun keladi. Avval `unzip -l` bilan qaramlik jarlarida `application*.yml` borligini
  tekshiring; bo'lsa base `.yml` qoladi, profil fayllari ham `.yml`.
- **Placeholder guard da origin ni `OriginLookup.getOrigin(source, name)` bilan
  oling.** `OriginTrackedMapPropertySource.getProperty()` qiymatni o'zi ochib
  beradi, `instanceof OriginTrackedValue` real muhitda hech qachon true bo'lmaydi.
  Boot 3.x fat jar URL i `jar:nested:<jar>/!BOOT-INF/classes/!/application.yml`
  (`/BOOT-INF/...` emas). Qo'lda `MapPropertySource` ga o'ram solgan test yashil
  bo'lib qoladi: guardni haqiqiy `bootJar` ni `env -i ... SPRING_PROFILES_ACTIVE=prod
  java -jar` bilan yurgizib tekshiring (baza kerak emas, guard ulanishdan oldin).
- **Nashr qilinadigan oddiy jar.** Servis kutubxona sifatida ham nashr qilinsa,
  oddiy `jar` taskidan `application*.yml` va guard ro'yxatlangan
  `META-INF/spring.factories` ni `exclude` qiling, aks holda guard va profil
  fayllari host ilovaga o'tadi. `bootJar` ga tegilmaydi.
- Bugun bo'sh sukut bilan ixtiyoriy kalitni (`${X:}`, masalan alohida migratsiya
  useri yoki URL i) "muhitga xos" deb sukutsiz qilish prod ni keraksiz to'xtatadi:
  bo'sh qiymatning ma'nosi bor-yo'qligini kodda tekshiring.
- **Profilni o'z env nomi bilan tanlash.** `spring.profiles.active: ${MY_PROFILE:}` deployda ishlamay qolishi mumkin:
  konteyner entrypoint i ko'pincha boshqa env ni `-Dspring.profiles.active` qilib beradi, system property esa
  config faylidan ustun. Yechim: `EnvironmentPostProcessor` (`Ordered.HIGHEST_PRECEDENCE`, ConfigData dan oldin)
  OS env ni o'qib `addFirst(MapPropertySource(spring.profiles.active=...))` qiladi va bosilgan qiymatni DeferredLog
  ga yozadi. Tekshiruv: fat jarni `MY_PROFILE=a -Dspring.profiles.active=b SPRING_PROFILES_ACTIVE=c` bilan yurgizib,
  `profile is active: "a"` ni ko'rish. EPP ichida start to'xtasa DeferredLog chiqmaydi, xato xabarining o'zi
  profilni aytsin.
