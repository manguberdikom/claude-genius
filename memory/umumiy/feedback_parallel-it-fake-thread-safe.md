---
type: feedback
---
# Parallel IT dagi in-memory fake thread-safe bo'lishi kerak

Ikki thread bir vaqtda "tekshir, keyin yoz" qiladigan konkurentlik IT si (advisory lock, CyclicBarrier, N raund)
haqiqiy servis o'rniga in-memory fake (vault, blind index, kesh) ishlatsa, fake ning o'zi poyga manbai bo'ladi.

- Belgisi: ko'p raundli testda bitta raund "ikkalasi ham yutdi" (`[true, true]`), qolganlari yashil. Lock to'g'ri
  bo'lsa ham `HashMap`/`LinkedHashMap`/`ArrayList` ga parallel `put`/`add` yozuvni yo'qotadi, qulf ostidagi
  qidiruv birinchi yozuvchining tokenini ko'rmaydi.
- Nega oldin yashil edi: ko'pincha ikkinchi yo'l (masalan ochiq ustun bo'yicha qidiruv) poygani yashirgan.
  O'sha yo'l olib tashlanganda fake dagi nuqson birinchi marta chiqadi. Avval ishlab chiqarish poygasi deb
  qidirmang: qulf kaliti va qidiruv qulf ichidaligini tekshiring, keyin fake kolleksiyalariga qarang.
- Tuzatish: tartib kerak bo'lsa `ConcurrentSkipListMap` (o'suvchi kalit = qo'shilish tartibi), yozuvlar ro'yxati
  `CopyOnWriteArrayList`, bayroqlar `volatile`. Haqiqiy servis (server) baribir thread-safe, fake unga tenglashadi.
- Tasdiq: o'sha IT ni `integrationTest` vazifasida ketma-ket 3 marta yurgizing. `:test` vazifasi
  `@Tag("integration")` ni chiqarib tashlasa, IT u yerda yashil ko'rinadi, lekin aslida yurmaydi.
