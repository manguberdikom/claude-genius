---
type: feedback
---
# S5443: arxiv tekshiruvi uchun umumiy temp fayl o'rniga xotira

Yuklangan arxivni (xlsx, zip) central directory bo'yicha tekshirish uchun `Files.createTempFile` ishlatilsa,
Sonar `java:S5443` (umumiy yoziladigan papka) ni vulnerability deb belgilaydi va security rating 4 ga tushadi.

- POSIX ruxsatli `createTempFile(..., asFileAttribute(rw-------))` Windows da ishlamaydi, atributsiz shox
  baribir belgilanadi.
- Temp faylsiz yo'l: yuklama hajmi allaqachon cheklangan bo'lsa baytlarni o'qib, commons-compress
  `ZipFile.builder().setSeekableByteChannel(new SeekableInMemoryByteChannel(bytes))` bilan central directory ni
  o'qing. commons-compress Apache POI ning tranzitiv bog'liqligi, alohida qo'shish shart emas.
- Mavjud testlar `MultipartFile.getInputStream()` ni mock qilsa, `getBytes()` emas `getInputStream().readAllBytes()`.
