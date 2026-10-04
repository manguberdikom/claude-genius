# Bu repoda ishlash qoidasi

Repo to'rtta monolit qo'llanmadan iborat: **4.6 MB, ~1.67M token, 135 bob,
2285 bo'lim**. Eng kattasi (`java-spring-design-patterns.md`) yolg'iz o'zi
~837k token — 200k kontekst oynasidan to'rt barobar katta.

**Shuning uchun bu fayllar hech qachon to'liq o'qilmaydi.** Bitta `###` bo'lim
medianasi atigi ~700 token, ya'ni javob deyarli har doim kichik bo'lakda turadi.
Vazifa — o'sha bo'lakni bir urinishda topish.

## Kirish protokoli

Hamma narsa bitta skript orqali: `tools/doc.sh`.

```sh
tools/doc.sh find "circuit breaker"       # sarlavha va inglizcha taxalluslar bo'yicha
tools/doc.sh find -f "pg_stat_statements" # matn ichidan ham (sekinroq, ~80 ms)
tools/doc.sh show patterns 17.2           # faqat o'sha bo'limni chiqaradi
tools/doc.sh toc                          # hujjatlar ro'yxati
tools/doc.sh toc sonar                    # boblar ro'yxati
tools/doc.sh outline patterns 17          # bobdagi bo'limlar
```

Odatiy yo'l ikki qadam: `find` bo'lim raqamini beradi, `show` matnni beradi.
`find` ko'pi bilan 20 ta natija chiqaradi (`-n N` bilan o'zgaradi).

Hujjat kalitlari: `patterns`, `mindset`, `sonar`, `testing`.

## Nima qilmaslik kerak

- `cat`, `less` yoki chegarasiz `Read` — `java-spring-*.md` fayllarida.
  Buni `tools/guard_bigdocs.py` (PreToolUse hook) to'sadi; u
  `.claude/settings.json` da ulangan, sinovlari `tools/test_guard.py` da.
- Bobni butunligicha o'qish. `show` 1200 satrdan uzun blokni chiqarmaydi;
  o'rniga ichidagi bo'limlar ro'yxatini beradi. Haqiqatan kerak bo'lsa `--force`.
- Monolitni qo'lda `grep` qilib satr raqamini izlash. `find -f` shuni qiladi
  va natijani bo'lim raqamiga bog'laydi.

Chegaralangan o'qish ruxsat etilgan: `sed -n '8499,8543p'`, `grep`, `head`,
`limit` berilgan `Read`.

## Indeks

`index/` dagi to'rtta TSV — `docs`, `chapters`, `sections`, `aliases`.
Ularni `tools/build_index.py` monolitlardan yasaydi; hujjatlarga tegmaydi.

Indeks o'z-o'zini tiklaydi: `doc.sh` har chaqiruvda manba faylning o'zgarish
vaqtini tekshiradi va indeks eskirgan bo'lsa qayta yasaydi. Hujjat
tahrirlangandan keyin qo'lda hech narsa qilish shart emas. Majburiy qayta
yasash: `tools/doc.sh rebuild`.

Indeks grep qilinadi, o'qilmaydi — uni ham to'liq kontekstga olmang.

## Til

Hujjatlar o'zbek lotin yozuvida, texnik atamalar inglizcha (bean, proxy,
cache, quality gate, coverage). Inglizcha pattern nomlari `aliases.tsv` da
bo'lim raqamiga bog'langan, shuning uchun `find "Circuit Breaker"` ishlaydi.
Apostrof hamma joyda ASCII `'` — qidiruvda normalizatsiya kerak emas.
