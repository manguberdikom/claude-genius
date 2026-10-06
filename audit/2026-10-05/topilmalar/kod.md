# Asbob kodi sifati va test tezligi

[Reja](../README.md) ilovasi. Prefiks: `KD`. Tasdiqlangan topilma: 21, rad etilgan: 0. Dalillar auditor va skeptik tekshiruvchi agentlar yozgan holicha, sana 2026-10-05.

## Kuchli tomonlar

- Faqat stdlib, tashqi bog'liqlik yo'q. Hook importi 17-29 ms (python3 -X importtime: guard 18.5 ms, suggest_sections 16.9 ms, check_code 29.3 ms), ya'ni hook latency asosan jarayon ishga tushishidan keladi, kod og'ir emas.
- Hook stdin o'qish bitta joyda: tools/hookio.py read_text/read_payload (utf-8-sig, BOM, isatty, buzuq JSON -&gt; None). 6 hook (budget, check_code, guard, handoff, suggest_sections, usage) shuni ishlatadi, takror yo'q.
- shell=True butun tools/ va install/ da 0 marta (grep -n 'shell=True' bo'sh). Test bo'lmagan koddagi 5 ta keng except hammasi izohlangan va asosli: hook fail-open (handoff.py:437, suggest_sections.py:131,473), run_tests.py:880 qo'shimcha tasnif, merge_settings.py:243 tmp ni o'chirib qayta raise qiladi.
- Encoding intizomi yaxshi: ruff --preview PLW1514 test bo'lmagan kodda faqat 2 ta (run_tests.py:757,785, qulf fayli, zararsiz). 7 CLI stdout ni reconfigure(encoding='utf-8') qiladi; PYTHONIOENCODING=cp1252 bilan rules_for, check_docs, eval_find, review_queue, cost_report, schema_from_entities hammasi rc=0.
- Statik sifat yuqori: ruff default qoidalar 752 KB kodda 41 topilma (30 tasi E741 'l' nomi); F,E9,B to'plami 20 ta; mypy default 8 xato (6 tasi reconfigure union-attr yolg'on ishga tushishi); vulture --min-confidence 60 faqat 1 (state.clear, testlarda ishlatiladi).
- Coverage o'lchandi va yuqori: guard.py 96%, rules_for.py 95%, run_tests.py 88% (870 dan 102 qamralmagan), suggest_sections.py 80% (main() nusxa klonda yuradi, shuning uchun hisobga tushmagan).
- Testlar o'zidan keyin tozalaydi: barcha yurishlardan keyin /tmp da run_tests_/test_doc_ qoldig'i 0, git status toza. CI matritsasi ubuntu + windows, Windows yo'llari (normcase/realpath, '\\'-&gt;'/', 8.3 qisqa nom) kodda o'ylangan.
- Atomik yozuv pid li tmp bilan budget.py:182, usage.py:333, state.py:75, build_index.py:416 da; budget.py:101 O_EXCL qulf Windows ni ham hisobga oladi, eskirgan qulfni 5 s da yechadi.

## O'lchovlar

- Eng sekin 5 suite, bittalab, Popen sitecustomize bilan sanaldi (POPEN_LOG=... PYTHONPATH=scratch/hookpp python3 tools/test_X.py): test_doc 11.97 s / 343 subprocess (hammasi doc.sh), test_run_tests 6.05 s / 118, test_suggest 6.33 s / 11, test_budget 7.77 s / 145 (81 ta budget.py), test_guard 6.78 s / 144 (hammasi guard.py).
- test_doc ichki taqsimot (scratch/time_doc.py): 48 CASES 1.16 s (24 ms/ta); check_exact_refs 4.41 s (~295 doc.sh path/checklist); check_index_freshness 3.69 s (5 marta build_index); check_python_stub 1.48 s. doc.sh path 12 ms/ta, checklist 15 ms/ta, build_index.py butun korpusda 704-716 ms.
- test_run_tests holatlar bo'yicha (scratch/time_cases.py): 'vaqt tugasa 3' 2248 ms (--vaqt 2 va FAKE sleep(30)), qolgan 41 holat 150-340 ms. tree+git init/add/commit 142 ms, tayyor repo copytree 20 ms, bitta run_cli --yurgiz 149 ms.
- test_budget: 'parallel chaqiruvda hisob yo'qolmaydi' 2094 ms (5 tur x time.sleep(0.3) + 6 jarayon), qolganlari 190-400 ms.
- Guard jarayon ichida prototip (stdin/stdout almashtirish + SystemExit ushlash, repo o'zgarmadi): 144 chaqiruv 0.02 s (0.12 ms/ta) vs subprocess 5.54 s (38 ms/ta), natija bir xil: True.
- suggest_sections.suggest(): 47-50 ms/chaqiruv, tokens() har chaqiruvda 7192 marta, read_tsv 4 fayl. lru_cache bilan read_tsv+tokens+term_vocabulary+title_terms keshlansa 9.9 ms/chaqiruv, natija bir xil: True. Hook to'liq (stdin JSON bilan) 98-109 ms, ensure_fresh 10 ms.
- check_docs.py 3.07 s. cProfile: kirill tekshiruvi check_docs.py:400 unicodedata.name 6.67 mln marta; set(text) bilan 0.78 s -&gt; 0.047 s, natija bir xil. check_regression 22 ta re.I naqsh x 258 fayl = 1.37 s, eng sekini 'sighup...work_mem' 0.25 s.
- ruff 0.15.20 (tizimda): default 41 topilma; --select F,E9,B: 20 (B905 9, B007 5, F401 3, B904 2, F811 1); keng to'plam 2489 (581 PTH118, 576 UP031 uslubiy). ruff butun tools+install ni 38 ms da tekshiradi.
- mypy 1.20.2: default 8 xato; --check-untyped-defs 88 xato 23 faylda (50 var-annotated, 13 union-attr, 12 attr-defined, 7 assignment). Haqiqiy xato topgani: budget.py:178 'float - None'.
- coverage 7.16.2 venv da (scratch/kodaudit/venv, .pth orqali subprocess ham): guard 96% (qamralmagan 167-168, 285, 290-291, 310-311), rules_for 95% (233, 252-253, 301-302, ...), run_tests 88% (409, 524-534, 299-311, 834-836, 1088-1099, ...), suggest_sections 80%.
- CI (gh run view): 'Asbob sinovlari' ubuntu 38-40 s, windows 78-109 s; 'Qidiruv o'rni' (eval_find) ubuntu 9-12 s, windows 61-81 s. Oxirgi 30 run dan 15 tasi failure; tools job 7 runda yiqilgan, 2 tasida faqat windows (masalan 37360089029). Log yuklab bo'lmadi (403 Forbidden).
- Takror hisobi (grep va ast): git wrapper 5 ta (docref.py:165, rules_for.py:248, handoff.py:268, run_tests.py:170, guruh.py:39); os.replace bilan atomik yozuv 7 faylda; STATE_DIR ta'rifi 4 joyda; tanasi aynan bir xil funksiya gh_slug (build_single.py, check_docs.py); 25 test faylida o'z runner tsikli.

## Topilmalar

### KD-K1. run_tests --diff non-ASCII nomli faylni ko'rmaydi va 'o'zgarish yo'q' deydi

- Og'irlik: yuqori; tur: sifat; mehnat: S; holat: tuzatish bilan tasdiqlandi.
- Dalil: tools/run_tests.py:409-411: run_git(root, 'diff', '--name-status', 'HEAD') va 'ls-files --others' -z siz va core.quotepath=off siz. Git non-ASCII yo'lni qo'shtirnoq va oktal bilan beradi: M "src/main/java/uz/xizmat/Qo\312\273l.java". Keyin run_tests.py:415 os.path.exists filtri uni jim tashlaydi. Sinov (scratch/nonascii.py, test_run_tests.gradle_shop asosida): 'V2__add_col.sql' -&gt; 'Reja: 2 test sinfi ... OrderRepositoryIT'; 'V2__qoʻshimcha_ustun.sql' -&gt; "Ta'sirlangan test yo'q: o'zgarish yo'q"; 'V3__add col.sql' (bo'sh joy) -&gt; to'g'ri. Untracked 'YangiʻTest.java' ham -&gt; "o'zgarish yo'q". guruh.py:108,152,177,190 ham -z siz.
- Ta'sir: O'zbekcha nomli Flyway migratsiya yoki resurs o'zgarganda test-muhandis va dasturchi 'ta'sirlangan test yo'q' deb yashil xulosa oladi, baza testlari yurmaydi. Bu jim noto'g'ri javob.
- Tavsiya: run_tests.py changed_files(): 'diff --name-status -z' va 'ls-files -z --others --exclude-standard'; NUL bo'yicha parse: status tokeni, keyin R/C uchun 2 yo'l, qolganlariga 1 yo'l. run_git (run_tests.py:170) ga encoding='utf-8', errors='surrogateescape' MAJBURIY: aks holda Windows cp1252 da Q3 dagi mojibake yoki UnicodeDecodeError. test_run_tests.py ga 2 holat: tracked 'orders/src/main/resources/db/migration/V2__qoʻshimcha_ustun.sql' -&gt; OrderRepositoryIT tanlanadi; untracked non-ASCII test fayli -&gt; 'o'zgargan test'. guruh.py ga tegish shart emas (ixtiyoriy, kosmetik).
- O'lchov: Yangi 2 holat test_run_tests da yashil; scratch/nonascii.py ikkinchi qatori 'Reja: 2 test sinfi' beradi.
- Tekshiruvchi izohi: Mustaqil takrorladim (scratchpad/skeptik/k1.py, test_run_tests.gradle_shop asosida, 6 holat): 'V2__add_col.sql' -&gt; 'Reja: 2 test sinfi (migratsiya 2)'; 'V2__qoʻshimcha_ustun.sql' va 'V2__über.sql' -&gt; "Ta'sirlangan test yo'q: o'zgarish yo'q"; 'V3__add col.sql' to'g'ri; untracked 'YangiʻTest.java' -&gt; "o'zgarish yo'q", ASCII 'YangiTest.java' -&gt; 'Reja: 1 test sinfi'. git yo'lni "...\312\273..." qilib qo'shtirnoqlaydi, run_tests.py:415 dagi os.path.exists uni jim tashlaydi, --yurgiz bilan exit 0 (case_tasir_yoq shuni kutadi). Mexanizm to'g'ri. Lekin 'kritik' mubolag'a: faqat non-ASCII nomli fayllarga tegadi, Java sinf nomlari amalda ASCII, aralash diffda faqat o'sha fayl tushadi. guruh.py qismi noto'g'ri: 106 (dirty, faqat bo'shlik), 152 (son va ekranga chiqarish), 176-177 va 190 (overlap ikkala tomonda bir xil qo'shtirnoqlangan nomlar bilan kesishadi) - u yerda faqat kosmetik, natija buzilmaydi.

### KD-T-M1. main hozir Windows da qizil: test_run_tests 'tashxis: kontekst ishga tushishi logdan', log_path realpath siz

- Og'irlik: yuqori; tur: sifat; mehnat: S; holat: skeptik tekshiruvchi qo'shgan (alohida qayta tekshirilmagan).
- Dalil: GitHub MCP get_job_logs, run 37360089029 (HEAD 8f47f42), job 111932227900 'tools (windows-latest)': 'XATO tashxis: kontekst ishga tushishi logdan', '41/42 o'tdi', 'yiqilgan: tools/test_run_tests.py'. 682ca87 yashil, holat qo'shilgan 4f08025 bilan qizil. Taxminiy sabab: test log yo'lini log_path(os.path.realpath(root)) bilan yozadi (test_run_tests.py:588), CLI esa git bo'lmagan papkada project_root() fallback (run_tests.py:179-193) os.path.abspath qaytaradi, realpath siz; log_path (807-810) root ni normallashtirmaydi, root_lock (784) esa realpath ishlatadi. Windows da TEMP qisqa nom bilan (logda 'C:/Users/RUNNER~1/...'), subprocess cwd shu nomni saqlaydi -&gt; sha1 farq -&gt; log topilmaydi. Linux da symlink bilan tasdiqladim: project_root('m1/link/kontekst') link yo'lini qaytaradi, log_path(root) == log_path(realpath) -&gt; False. Windows da sinalmadi.
- Ta'sir: main Windows CI qizil, ya'ni har push 'failure' va keyingi haqiqiy regressiya ko'rinmay qoladi (Q1). Foydalanuvchida: git siz loyihada symlink yoki qisqa nom orqali kirilsa --tashxis --yurgiz yozgan logni topmaydi.
- Tavsiya: run_tests.py: log_path() ichida root_lock kabi hashlib.sha1(os.path.realpath(root).encode('utf-8')) va project_root() fallbackida os.path.realpath(path) qaytarish. test_run_tests ga Linux holat: kontekst logini symlink orqali ochilgan root bilan yozib, CLI ni boshqa yozilishdagi cwd dan --tashxis bilan chaqirish.
- O'lchov: Keyingi push da 'tools (windows-latest)' yashil, test_run_tests 42/42 (yangi symlink holati bilan 43/43) Linux va Windows da.

### KD-T1. test_guard 144 marta python ishga tushiradi, 5.5 s ning deyarli hammasi jarayon narxi

- Og'irlik: o'rta; tur: tezlik; mehnat: S; holat: tuzatish bilan tasdiqlandi.
- Dalil: tools/test_guard.py:389-398 run_guard() har payload uchun subprocess.run([sys.executable, GUARD]). Popen sanog'i: 144. Prototip (guard.main() jarayon ichida, sys.stdin=StringIO, redirect_stdout, SystemExit ushlanadi): 144 chaqiruv 0.02 s vs 5.54 s, natija bir xil. guard.decide() (guard.py:258-269) sys.exit(0) qiladi, shuning uchun refaktoringsiz ham ishlaydi.
- Ta'sir: Lokal 5.8-6.8 s, Windows CI da python ishga tushishi 2-3 barobar qimmat, shuning uchun windows 'Asbob sinovlari' 78-109 s ning katta qismi.
- Tavsiya: Auditor tavsiyasi: run_guard_inproc + subprocess faqat 6-8 E2E holatda (not json, BOM baytlari, GENIUS_HOOKS=off, CLAUDE_PROJECT_DIR yo'q, cp1252 prompt, bitta HINT). stdin uchun io.TextIOWrapper(io.BytesIO(raw), encoding='utf-8') ishlatilsin, chunki hookio.read_text avval .buffer ni o'qiydi; finally da cwd va CLAUDE_PROJECT_DIR tiklansin. Metrika: test_guard &lt; 1 s Linux da, 138/138.
- O'lchov: python3 tools/test_guard.py Linux da &lt; 1.5 s (hozir 5.8-6.8 s), 138/138 o'tdi; windows CI 'Asbob sinovlari' qadami kamida 10 s qisqaradi.
- Tekshiruvchi izohi: Takrorlandi: test_guard 5.77-6.00 s, 138/138. Prototip (scratchpad/skeptik/t1.py: run_guard jarayon ichida, os.chdir, stdin = TextIOWrapper(BytesIO), redirect_stdout, SystemExit ushlanadi) 143 chaqiruv bilan 0.06 s, butun chiqish subprocess varianti bilan bir xil (diff bo'sh). guard.py ishga tushishi 42 ms, bo'sh python 15 ms; 143 + 1 (GENIUS_HOOKS=off) = 144 Popen. Faktlar to'g'ri, lekin 'yuqori' ortiqcha: faqat test vaqti (lokal butun suite 48.4 s ning 12%), mahsulot xulqiga ta'sir yo'q.

### KD-T2. test_doc 12 s: 295 ta doc.sh chaqiruv va 5 marta butun korpusni indekslash

- Og'irlik: o'rta; tur: tezlik; mehnat: M; holat: tuzatish bilan tasdiqlandi.
- Dalil: test_doc.py:135-157 check_exact_refs: X.10 bo'limlarning har biri uchun alohida doc.sh path va checklist = 4.41 s (12-15 ms/ta). test_doc.py:196-202 sandbox() butun docs/ ni (6.4 MB) nusxalaydi, check_index_freshness (205-255) 5 marta rebuild = 3.69 s (build_index 704-716 ms). check_python_stub 1.48 s. test_suggest.py:245-262 hook_cases ham butun docs/ ni nusxalab 2 marta rebuild qiladi.
- Ta'sir: Eng sekin suite (umumiy 49 s ning 25%). Parallel yurishda ham makespan shu suite bilan chegaralanadi. Windows Git Bash da har bash fork yana qimmatroq.
- Tavsiya: (a) check_exact_refs: ThreadPoolExecutor(max_workers=min(8, os.cpu_count())), natija tartibi saqlanadi. (b) tools/testdata/mini_docs (manifest + 1 hujjat, 2 bob, 3-4 bo'lim); sandbox() testdata ni ignore qiladi, shuning uchun nusxa alohida ko'chiriladi. Fixture test_suggest hook_cases dagi EXPECTED[1][0] ('circuit breaker ...') uchun taklif beradigan 1-2 bo'limni o'z ichiga olsin, aks holda output_shape_ok yiqiladi. (c) check_python_stub ham mini korpusda. Butun sinf tekshiruvi asl indeksda qoladi.
- O'lchov: python3 tools/test_doc.py &lt; 4 s (hozir 12 s), 54/54; check_index_freshness &lt; 0.5 s (mini korpusda build_index ~0.1 s, taxmin).
- Tekshiruvchi izohi: Takrorlandi: test_doc 10.9-11.2 s, 54/54. Bo'linishi (scratchpad/skeptik/t2.py): CASES 48 ta 1.12 s; check_exact_refs 4.31 s va 283 doc.sh chaqiruv (295 emas; suite jami 340); check_index_freshness 3.94 s, 5 rebuild; check_python_stub 1.72 s; doc.sh path 17 ms/ta, build_index 1.05 s. build_index faqat manifest.json ga tayanadi (build_index.py:276), mini korpus ishlaydi; test_suggest.py:251 ham butun docs/ ni nusxalaydi. Faqat test vaqti, shuning uchun orta.

### KD-T4. test_run_tests: bitta holat 2.25 s uxlaydi, 17 holat git repo ni noldan yasaydi

- Og'irlik: o'rta; tur: tezlik; mehnat: S; holat: tasdiqlandi.
- Dalil: test_run_tests.py:382-386 case_vaqt_tugadi '--vaqt 2' + FAKE da time.sleep(30) (test_run_tests.py:285); run_tests.py:1233 '--vaqt' type=int, 1 s dan kam berib bo'lmaydi. O'lchov: 2248 ms. git_shop/commit 17 marta, har biri 142 ms (init+add+commit), tayyor repo copytree 20 ms.
- Ta'sir: Suite 6 s dan ~4 s i shu ikkisi. Har yangi CLI holati yana 150 ms qo'shadi.
- Tavsiya: run_tests.py:1233 type=float; test '--vaqt', '0.3' (sekin runnerda vaqt birinchi buyruqdan oldin tugasa ham 124 qaytadi, barqaror). _GIT_TEMPLATE faqat gradle_shop() + commit qiladigan holatlarga, copytree(symlinks=True). Metrika: test_run_tests &lt; 2.5 s, 42/42.
- O'lchov: python3 tools/test_run_tests.py &lt; 2.5 s (hozir 6.05 s), 42/42.
- Tekshiruvchi izohi: Takrorlandi (scratchpad/skeptik/t4.py): case_vaqt_tugadi 2257 ms, --vaqt type=int (run_tests.py:1233); tree+commit 125 ms, copytree 15 ms; suite 6.11-6.13 s, 42/42. Kichik tuzatish: git repo 15 holatda noldan yasaladi (17 sonida def qatorlari ham sanalgan). '%d' % float Python da yiqilmaydi (run_tests.py:832, 1335), float ga o'tish xavfsiz.

### KD-T5. test_budget: 145 subprocess va qat'iy sleep(0.3) bilan sinxronlash

- Og'irlik: o'rta; tur: ikkalasi; mehnat: M; holat: tuzatish bilan tasdiqlandi.
- Dalil: test_budget.py:84-89 parallel(): jarayonlar ochiladi, keyin time.sleep(0.3), 5 tur (test_budget.py:302) = 1.5 s faqat kutish; holat 2094 ms. 81+27+18+... = 145 marta budget.py ishga tushadi (31 ms/ta).
- Ta'sir: 7.8 s; sleep bilan sinxronlash sekin Windows runnerda yetmasa poyga sinalmay qoladi (test baribir o'tadi, ya'ni zaif sinov).
- Tavsiya: Fayl o'rniga stdout handshake: har jarayon [sys.executable, '-c', "import sys; sys.path.insert(0, TOOLS); import budget; print('R', flush=True); sys.exit(budget.main())"] bilan ochiladi; ota jarayon har birining stdout dan 'R' qatorini o'qiydi (hammasi tayyor), keyin payloadlarni yozadi. sleep yo'qoladi va sinxronlash runner tezligiga bog'liq emas. Parallel bo'lmagan holatlar budget.main() ni jarayon ichida (budget.STATE_DIR va budget.LOG tmp ga, stdin/stdout almashtirib). Metrika: test_budget &lt; 2 s, 26/26.
- O'lchov: test_budget &lt; 2 s, 26/26; parallel holat kutish vaqti sleep emas, ready fayllar soni bilan aniqlanadi.
- Tekshiruvchi izohi: Takrorlandi (scratchpad/skeptik/t5.py): 145 subprocess, time.sleep jami 1.80 s, suite 5.87-6.19 s (7.8 s emas). parallel() (test_budget.py:79-97) jarayonlarni ochib qat'iy 0.3 s kutadi; sekin runnerda jarayonlar import tugatib stdin kutish nuqtasiga yetmasa poyga zaif sinaladi - mantiqan to'g'ri (Windows da sinalmadi). Taklif qilingan GO-fayl va 5 ms polling keraksiz murakkab.

### KD-T6. CI suitelarni ketma-ket yurgizadi; Windows da 2-3 barobar sekin

- Og'irlik: o'rta; tur: tezlik; mehnat: M; holat: tuzatish bilan tasdiqlandi.
- Dalil: .github/workflows/docs.yml 'Asbob sinovlari': for f in tools/test_*.py; do python "$f"; done. CI: ubuntu 38-40 s, windows 78-109 s; 'Qidiruv o'rni' (eval_find.py:209, 120 marta bash doc.sh find) ubuntu 9-12 s, windows 61-81 s. Lokal ketma-ket 49 s, eng uzuni 12.2 s; 4 yadroda LPT jadval bo'yicha nazariy makespan ~12.5 s (taxmin, butun suiteni parallel yurgizmadim). Umumiy holat: test_check_code.py:448 jonli .claude/.state/rules_for ni solishtiradi; qolgan suitelar temp papka va GENIUS_STATE_DIR ishlatadi.
- Ta'sir: Har push da Windows tools job ~2.5 daqiqa; T1-T5 dan keyin ham ketma-ket yurish yig'indiga teng qoladi.
- Tavsiya: Avval T1-T5 (parallelsiz ham ~48 s -&gt; ~26 s). Keyin tools/run_all_tests.py: oldin indeksni bir marta yasash (CI da index/ yo'q, aks holda bir nechta suite bir vaqtda yasaydi), so'ng ThreadPoolExecutor (-j os.cpu_count()), chiqish buferda va tartib bilan, 'yiqilgan:' qatori va eng sekin 5 suite. docs.yml tsikli shu buyruqqa. eval_find: rank o'lchovi parallel, vaqt o'lchovi alohida ketma-ket 20 so'rovlik namunada.
- O'lchov: Linux 'Asbob sinovlari' &lt;= 15 s (hozir 38-40), windows &lt;= 40 s (hozir 78-109); T1-T5 bilan birga Linux &lt;= 8 s (taxmin).
- Tekshiruvchi izohi: CI raqamlari tasdiqlandi (gh run view --json jobs): windows 'Asbob sinovlari' 78/82/86/109 s, 'Qidiruv o'rni' 61-81 s; ubuntu 28-40 va 8-12 s. 26 suiteni bittalab o'lchadim: jami 48.4 s, eng uzuni test_doc 11.2 s; 4 yadroli LPT ~12.5 s hisobi to'g'ri (taxmin, parallel yurgizilmadi). Xatolar: (1) eval_find.py:209 test_ranking (3 so'rov), 240 ta doc.sh find esa run_find() da (eval_find.py:79-82); (2) eval_find har so'rov vaqtini o'lchab median/p95 chiqaradi (120-124), ThreadPool bu o'lchovni ifloslaydi; (3) test_check_code allaqachon GENIUS_STATE_DIR bilan izolyatsiya qilingan (38-39), 448 dagi jonli snapshot ataylab qo'riqchi; boshqa suitelar jonli .claude/.state ga yozmaydi, parallel yurish uni buzmaydi. 'Yuqori' ortiqcha: faqat CI vaqti.

### KD-Q1. CI main tez-tez qizil, Windows tools job sababini ko'rish qiyin

- Og'irlik: o'rta; tur: sifat; mehnat: S; holat: tuzatish bilan tasdiqlandi.
- Dalil: gh run list --limit 30: 14 success, 15 failure. Yiqilgan joblar: 'installer (powershell)' ko'p, tools job 7 runda, faqat 'tools (windows-latest)' 2 runda (37360089029: 'Asbob sinovlari' failure, 109 s). gh run view --log-failed: 403 Forbidden, sababni bu yerdan aniqlab bo'lmadi.
- Ta'sir: Qizil main odatiy holga aylansa, haqiqiy regressiya (masalan K1 turidagi) ko'rinmay qoladi.
- Tavsiya: Karantin ro'yxati qilinmasin. M1 ni darhol tuzatib main ni yashilga qaytarish. run_all_tests (T6) har yiqilgan suite uchun birinchi XATO qatorini GITHUB_STEP_SUMMARY ga yozsin (qator logda bor, faqat ko'rinmaydi). Yiqilgan suite chiqishi upload-artifact bilan. installer joblaridagi yiqilish alohida ko'rilsin.
- O'lchov: Keyingi 20 runda tools job success ulushi; yiqilganda sabab job Summary da 1 qatorda ko'rinadi.
- Tekshiruvchi izohi: Sabab aniqlanadi: GitHub MCP get_job_logs bilan Windows logi o'qildi. Run 37360089029 (HEAD 8f47f42), job 111932227900: 'XATO tashxis: kontekst ishga tushishi logdan', '41/42 o'tdi', 'yiqilgan: tools/test_run_tests.py'. Run 37356743989 (4ca313b): 'XATO --modul: butun modul, boshqasi yo'q'. 682ca87 yashil, 4f08025 (holat qo'shilgan commit) bilan yana qizil. Ya'ni main hozir Windows da haqiqiy regressiya bilan qizil (missed M1). gh run list 30: 16 failure / 14 success. Karantin tavsiyasi zararli: aynan shu haqiqiy regressiyani 'beqaror' deb yashirgan bo'lardi.

### KD-Q3. Git chaqiruvi 5 xil, encoding va timeout har xil; rules_for non-UTF8 lokalda yiqiladi

- Og'irlik: o'rta; tur: sifat; mehnat: M; holat: tuzatish bilan tasdiqlandi.
- Dalil: docref.py:165 (_git, timeout 20, encoding yo'q), rules_for.py:248-254 (_git, timeout YO'Q, faqat OSError ushlanadi, encoding yo'q), handoff.py:268 (timeout 20, encoding yo'q), run_tests.py:170 (timeout 60, encoding yo'q), guruh.py:39 (bayt, timeout 120). eval_skill.py:143 ham text=True encoding siz. Sinov: LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 python3 tools/rules_for.py --diff (non-ASCII o'zgargan fayl bilan) -&gt; 'UnicodeDecodeError: ascii codec can't decode byte 0xca', rc=1. Windows da default cp1252: crash emas, lekin mojibake yo'l (taxmin, Windows da sinalmadi).
- Ta'sir: rules_for Java yozishdan oldin majburiy; u yiqilsa yoki noto'g'ri yo'l bersa check_code hook belgini topmaydi va zanjir buziladi.
- Tavsiya: Umumiy run_git: capture_output, encoding='utf-8', errors='surrogateescape', timeout=20, (OSError, SubprocessError) ushlanadi; yo'l ro'yxati olinadigan joyda -z (u bilan quotepath ahamiyatsiz). rules_for._git ga timeout. Sinov: test_rules_for da nomi 'U+0441' escape bilan yasalgan fayl (manbada kirill harf bo'lmasin) - windows-latest CI uni tabiiy sinaydi.
- O'lchov: grep -c 'subprocess.run(\["git"' tools/*.py (testsiz) 5 -&gt; 1; yuqoridagi LC_ALL=C sinovi rc=0 va fayl ro'yxatida to'g'ri nom.
- Tekshiruvchi izohi: Linux dalili sun'iy: 'LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0' bilan haqiqatan UnicodeDecodeError (0xca), lekin oddiy LC_ALL=C da PEP 538/540 tufayli Python UTF-8 rejimiga o'tadi (utf8_mode=1): rules_for --diff rc=0, chiqish UTF-8 lokal bilan bir xil. Haqiqiy xavf Windows: text=True encoding siz cp1252 bilan dekodlaydi; 'Qoʻl' -&gt; 'QoÊ»l' (yo'l yo'q, fayl jim tushadi), kirillcha 's' harfi (U+0441, baytlari D1 81) yoki 'Á' (C3 81) -&gt; 0x81 cp1252 da yo'q, UnicodeDecodeError, rules_for._git faqat OSError ushlaydi -&gt; crash (Windows da sinalmadi). 5 wrapper tasdiqlandi (docref:165, rules_for:248 timeout siz, handoff:268, run_tests:170, guruh:39). rules_for allaqachon -z ishlatadi.

### KD-Q4. Umumiy yordamchilar 4-7 faylda qayta yozilgan

- Og'irlik: o'rta; tur: sifat; mehnat: L; holat: tuzatish bilan tasdiqlandi.
- Dalil: Atomik yozish: budget.py:182, usage.py:333, state.py:75, build_index.py:416, handoff.py:420-425 (pid siz qat'iy STATE+'.tmp', qulfsiz), merge_settings.py:234 (mkstemp), guruh.py. Holat papkasi: state.py:26, budget.py:49, run_tests.py:135, handoff.py:36 (GENIUS_STATE_DIR ni e'tiborsiz qoldiradi). Indeks yangiligi va qayta yasash: docref.py:29-61 va suggest_sections.py:120-138 deyarli bir xil tana, doc.sh:56-68 bash nusxasi. TSV o'qish: docref._rows, suggest_sections.read_tsv, eval_find.rows (70), rules_for.py:231,343, review_queue.py:73. Transkript papkasini topish: usage.py:93-130 va handoff.py:68-133 (config_dir, slug regex, 200 belgi kesish ikkalasida). Qulf: run_tests.py:752-778 queue_lock va 781-805 root_lock deyarli bir xil 25 satr. gh_slug build_single.py va check_docs.py da aynan bir xil (ast dump). Yo'lni POSIX ga: check_code.py:102, rules_for.py:294,521, handoff.py (2), run_tests.rel.
- Ta'sir: Bir joydagi tuzatish (masalan K1 dagi quotepath yoki handoff dagi tmp poygasi) boshqalarga yetmaydi; handoff ikki sessiya bir proyektda bo'lsa os.replace FileNotFoundError ni keng except yutadi va ogohlantirish takrorlanadi (taxmin).
- Tavsiya: geniuslib.py rejasi to'g'ri, lekin: ensure_index(timeout) parametrli, hook 8 s beradi. 1-qadam (run_git + atomic_write_text) K1/Q3 bilan bir PR; state_dir (handoff GENIUS_STATE_DIR ga) 2-qadam; qolganlari faqat o'sha fayl tegilganda, alohida katta refaktoring PR siz. Har qadamdan keyin barcha suite bittalab.
- O'lchov: os.replace 7 -&gt; 1 fayl, STATE_DIR ta'rifi 4 -&gt; 1, git wrapper 5 -&gt; 1, transkript topish 2 -&gt; 1; barcha 26 suite yashil.
- Tekshiruvchi izohi: Takrorlar tasdiqlandi: os.replace 7 faylda (budget, build_index, guruh, handoff, state, usage, install/merge_settings); STATE_DIR budget:49, run_tests:135, state:26, handoff:36 esa GENIUS_STATE_DIR ni e'tiborsiz qoldiradi; gh_slug build_single va check_docs da AST bo'yicha aynan bir xil; queue_lock va root_lock (run_tests 750-805) bir xil tana; handoff.save_state pid siz STATE+'.tmp'. Lekin 4-qadam zararli: docref.ensure_index timeout=120 s, suggest_sections.ensure_fresh esa ataylab REBUILD_TIMEOUT=8 s (hook promptni bloklamasin); suggest_sections docref ni chaqirsa hook 120 s gacha osilishi mumkin.

### KD-Q5. Hook xatolari ko'rinmaydi: fail-open to'g'ri, lekin iz qolmaydi

- Og'irlik: o'rta; tur: sifat; mehnat: S; holat: tasdiqlandi.
- Dalil: Faqat suggest_sections.py:451-454 da GENIUS_HOOK_DEBUG bor. handoff.py:437 'except Exception: return 0' izsiz. settings.json barcha hooklarda '|| exit 0'. K2 da budget hook har chaqiruvda traceback bilan yiqildi, foydalanuvchi buni ko'rmaydi.
- Ta'sir: Refaktoringdan keyin hook butunlay ishlamay qolsa (K2 kabi) budjet, guard yoki taklif jim o'chadi va sifat sezilmasdan pasayadi.
- Tavsiya: hookio.fail_open(name, exc): holat papkasidagi hook_errors.log ga bitta qator, 200 qatordan kesish. Log yo'li GENIUS_STATE_DIR ni hurmat qilsin (testlar jonli .claude/.state ga yozmasin, test_check_code jonli snapshotni tekshiradi). guard.main atrofida 'except Exception' (SystemExit ushlanmasin, decide() sys.exit(0) qiladi). handoff --hook hisobotida 24 soatlik xato soni.
- O'lchov: K2 ssenariysi hook_errors.log da 'budget TypeError' qatorini qoldiradi; test_hookio da fail_open holati.
- Tekshiruvchi izohi: suggest_sections.quiet (451-454) dagina GENIUS_HOOK_DEBUG; handoff.hook (437) 'except Exception: return 0'; .claude/settings.json dagi 7 hook buyrug'ining hammasi '|| exit 0'. K2 ssenariysida traceback stderr ga chiqadi va rc=1 '|| exit 0' bilan yutiladi.

### KD-Q8. Muhim yo'llar coverage dan tashqarida

- Og'irlik: o'rta; tur: sifat; mehnat: M; holat: tuzatish bilan tasdiqlandi.
- Dalil: coverage report (scratch/kodaudit/covrc, subprocess .pth bilan): run_tests.py 88%, qamralmagan: 409 (base...HEAD diff, PR tarmog'i), 524-534 (src/test/resources o'zgarishi), 299-311 (Windows 'cmd /c gradlew.bat' va bajarilmaydigan gradlew uchun 'sh gradlew'), 834-836 (OSError -&gt; 127), 1088-1099 (Maven tashxisi). guard.py 167-168 (shlex ValueError fallback), 285, 290-291 (boshqa diskdagi relpath ValueError). rules_for.py 252-253.
- Ta'sir: K1 ham aynan shu 'diff' yo'lining sinalmagan chekkasida edi; Windows runner tanlash faqat CI windows da bilvosita sinaladi.
- Tavsiya: Auditorning 5 holati + K1 dagi non-ASCII holat. os.name monkeypatch faqat Project._runner() chaqiruvi atrofida va darhol tiklansin (queue_lock/root_lock os.name='nt' da msvcrt import qiladi). Qamrov foizi maqsad emas, hisobot qadami sifatida.
- O'lchov: run_tests.py coverage &gt;= 93%, guard.py &gt;= 98%.
- Tekshiruvchi izohi: Coverage ni mustaqil qayta yurgizdim (coverage 7.16.2, subprocess .pth): run_tests.py 870 stmt, 102 missing, 88%, missing ro'yxati auditor bilan aynan bir xil. Lekin 'K1 aynan shu sinalmagan chekkada' noto'g'ri: K1 qatorlari 410-411 qamralgan (faqat 409 base...HEAD qamralmagan); K1 ni satr qamrovi emas, kirish sinfi (non-ASCII nom) topadi. Muhim qo'shimcha: Windows runner tarmog'i (303-306) Windows CI da ham yurmaydi, chunki run_cli doim GENIUS_TEST_RUNNER beradi (test_run_tests.py:345) va plan_for runner=['./gradlew'] (95).

### KD-K2. budget.json dagi bitta buzuq slot budjet hookini butunlay o'chiradi

- Og'irlik: past; tur: sifat; mehnat: S; holat: tuzatish bilan tasdiqlandi.
- Dalil: tools/budget.py:178: 'now - slot.get("seen", slot.get("started", 0)) &lt;= KEEP' save() da, try dan tashqarida. Sinov: GENIUS_STATE_DIR ga {"sessions":{"boshqa":{"seen":null,"calls":{}}}} yozib 3 marta Agent dasturchi payload: har biri 'TypeError: unsupported operand type(s) for -: float and NoneType', rc=1, deny chiqmadi. Toza holatda 3-chaqiruv permissionDecision=deny. settings.json dagi '|| exit 0' xatoni yutadi. mypy --check-untyped-defs ham shuni topdi. fresh() (budget.py:153) da ham xuddi shunday 'now - slot.get("started", 0)'.
- Ta'sir: Boshqa sessiya yoki eski versiya yozgan bitta noto'g'ri qiymat aktyor budjeti (2 chaqiruv chegarasi) ni HAMMA sessiyada fayl qo'lda o'chirilguncha jim o'chiradi. Xarajat nazorati yo'qoladi, hech kim bilmaydi.
- Tavsiya: Bitta joyda tozalash: load() da slotni faqat isinstance(slot, dict) bo'lsa va started/seen (bor bo'lsa) int yoki float bo'lsa qoldirish, calls dict bo'lmasa {}. Shunda save, fresh, cli_key, slot_of hammasi himoyalanadi. test_budget.py ga holat: qo'shni slot seen=null, started="x", slot=[] bo'lsa ham 3-chaqiruv deny, traceback yo'q. Q5 bilan bir PR da.
- O'lchov: Yuqoridagi qayta ishlab chiqarish ssenariysida 3-chaqiruv deny, traceback yo'q; yangi test holati yashil.
- Tekshiruvchi izohi: Mexanizm takrorlandi (scratchpad/skeptik/k2.sh, cwd = klon): {"seen":null} qo'shni slot bilan 3 chaqiruvning hammasi 'TypeError: unsupported operand type(s) for -: float and NoneType', rc=1, deny yo'q; started="x" bilan ham shunday; toza holatda 3-chaqiruv deny. Lekin 'boshqa sessiya yoki eski versiya yozadi' asossiz: budget.json ni faqat budget.py yozadi, git tarixidagi 7 versiyaning hammasi seen/started ga time.time() float yozadi, yozuv atomik (pid tmp + os.replace). Trigger faqat qo'lda tahrir. Tavsiya ham to'liq emas: cli_key() (budget.py:209) dagi max(pool, key=lambda k: pool[k].get('seen', 0)) ham None va float ni solishtirib yiqiladi, _num faqat save() va fresh() da yetmaydi.

### KD-T3. suggest_sections har chaqiruvda butun indeksni o'qib qayta tokenlaydi

- Og'irlik: past; tur: ikkalasi; mehnat: M; holat: tuzatish bilan tasdiqlandi.
- Dalil: suggest_sections.py:403-425 suggest(): read_tsv('sections.tsv'), load_idf (df.tsv), read_tsv('aliases.tsv'), term_vocabulary(aliases) | title_terms(sections) har safar. cProfile: bitta suggest 7192 marta tokens() (suggest_sections.py:100), test_suggest da jami 532219. O'lchov: 47-50 ms/chaqiruv, keshlangan prototip 9.9 ms, natija bir xil. Hook to'liq 98-109 ms.
- Ta'sir: test_suggest 6.1 s dan ~3.5 s shu takrordan. Hookda har prompt ~35-40 ms ortiqcha (UserPromptSubmit hooklari parallel yursa ham bu hook eng sekini, 147 ms).
- Tavsiya: 1) Test uchun: _corpus() kesh, kalit index/.stamp mtime. 2) Hook uchun ixtiyoriy: build_index alohida index/vocab.tsv va title_tokens.tsv yozadi; sections.tsv ustunlari o'zgartirilmasin (doc.sh, docref, test_doc.read_index row[4]/row[7] pozitsiya bo'yicha o'qiydi). 2-qadam faqat 20 yurishli hook median o'lchovi &gt;= 30 ms yutuq ko'rsatsa; o'zgarishdan keyin test_doc va eval_find qayta.
- O'lchov: test_suggest &lt; 3 s, 73/73; hook median 20 yurishda &lt;= 65 ms (hozir ~100 ms); eval_find 1-o'rin 61/120 o'zgarmaydi.
- Tekshiruvchi izohi: Raqamlar takrorlandi: suggest() 42-60 ms (median ~46), shundan yuklash ~22 ms (sections 3.9, df 6.3, aliases 1.0, vocab 11.3 ms); cProfile 10 chaqiruvda 71920 tokens() = 7192/chaqiruv; hook to'liq 90-125 ms. Lekin: (1) modul darajasidagi _corpus() keshi faqat testga yordam beradi, hook har prompt uchun yangi jarayon va suggest() bir marta chaqiriladi; (2) prompt boshiga 35-40 ms model javobi (soniyalar) oldida sezilmaydi. Haqiqiy yutuq test_suggest dagi ~2.5 s.

### KD-Q2. CI da ruff, mypy, coverage yo'q, real unused import va loop o'zgaruvchilari qolgan

- Og'irlik: past; tur: sifat; mehnat: S; holat: tuzatish bilan tasdiqlandi.
- Dalil: pyproject.toml/ruff.toml/mypy.ini yo'q. ruff --select F,E9,B: install/uninstall_settings.py:42 F401 'merge_settings.norm', run_tests.py:47 F401 'io', test_rewrite_paths.py:102 F811 contextlib, test_uninstall_settings.py:25 F401, B007 run_tests.py:658,699 va code_gap.py:88, B904 merge_settings.py:88,90. mypy default: 8 (6 tasi reconfigure yolg'on), --check-untyped-defs: 88, ulardan budget.py:178 haqiqiy (K2).
- Ta'sir: K2 turidagi xatoni mexanik vosita topadi, lekin hech kim yurgizmaydi. Ruff 38 ms, ya'ni narxi deyarli nol.
- Tavsiya: ruff.toml: target-version='py38', select=['F','E9','B'], ignore=['B905','E741'] (zip strict 3.10+); BLE001 va PLW1514 qo'shilmasin. CI tools job (faqat ubuntu) ga versiyasi qadalgan 'pipx run ruff==0.15.20 check tools install'. 4 ta F401/F811 ni 'ruff check --fix --select F401,F811'. mypy gating emas.
- O'lchov: ruff check tools install 0 topilma bilan CI da yashil; yangi F401/B007 PR da qizil.
- Tekshiruvchi izohi: ruff 0.15.20 --select F,E9,B: 20 topilma, ro'yxat auditor bilan mos (F401 x3, F811, B007, B904 x2, B905 x10); C901 raqamlari ham mos. Lekin real nuqson yo'q: ishlatilmagan import va o'zgaruvchilar; yagona real topilma (budget.py:178, mypy) K2 va u faqat qo'lda tahrirda chiqadi. Konfiguratsiya xatolari: PLW1514 ruff 0.15.20 da preview qoidasi ('Selection PLW1514 has no effect because preview is not enabled'); target-version py39 noto'g'ri, o'rnatuvchi 'Python 3.8+' deydi (install/manguberdi.ps1:320); BLE001 hooklardagi ataylab fail-open except larni belgilaydi (3 ta). S602/S604 0 topilma. mypy --check-untyped-defs men 102 oldim (88 flaglarga bog'liq).

### KD-Q6. check_docs ning uchdan biri bitta qatorda: har belgi uchun unicodedata.name

- Og'irlik: past; tur: tezlik; mehnat: S; holat: tasdiqlandi.
- Dalil: check_docs.py:400: sorted({c for c in text if 'CYRILLIC' in unicodedata.name(c, '')}), 6.67 mln chaqiruv. O'lchov: 0.78 s; {c for c in set(text) ...} bilan 0.047 s, 230 faylda natija bir xil. check_regression (check_docs.py:162-180) 22 re.I naqsh = 1.37 s.
- Ta'sir: check_docs 3.07 s, har docs tahriridan keyin va CI da yuradi; tejash ~0.7 s (25%).
- Tavsiya: check_docs.py:400 da 'for c in text' -&gt; 'for c in set(text)'. check_regression oldindan filtri ixtiyoriy. Metrika: check_docs &lt;= 2.2 s, 'Hammasi joyida' o'zgarmaydi.
- O'lchov: python3 tools/check_docs.py &lt;= 2.3 s, 'Hammasi joyida' o'zgarmaydi.
- Tekshiruvchi izohi: check_docs 2.75-2.84 s; cProfile: check_docs.py:400 setcomp 2.02 s cum, unicodedata.name 6.67 mln chaqiruv. 235 faylda asl usul 0.777 s, set(text) bilan 0.054 s, natija bir xil.

### KD-Q7. Bir nechta funksiya juda murakkab; fayllarni o'lcham bo'yicha bo'lish shart emas

- Og'irlik: past; tur: sifat; mehnat: M; holat: tuzatish bilan tasdiqlandi.
- Dalil: ruff C901: check_docs.py:383 main 63 (270 satr), run_tests.py:481 select 53 (143 satr), rules_for.py:486 main 39 (147 satr), run_tests.py:1212 main 25, run_tests.py:1056 diagnose 25. run_tests.py 1349 satr, 7 ta '# --' bo'lim; schema_from_entities.py 1052 satr, 5 bo'lim, eng murakkab funksiya 16.
- Ta'sir: check_docs.main ichidagi 10 ta qoida alohida sinalmaydi (test_check_docs butun skriptni yurgizadi); select() ga yangi fayl turi qo'shish regressiya xavfi yuqori (K1 shu atrofda).
- Tavsiya: check_docs.main ni qoida funksiyalariga bo'lish va har biriga test_check_docs da alohida holat (eng foydali qism). select() jadvalga faqat yangi fayl turi qo'shilganda. C901 max-complexity=25 bilan Q2 dagi ruff ga, qolgan 3 ta uchun vaqtinchalik noqa.
- O'lchov: ruff --select C901 max-complexity 25 da 0 topilma; test_check_docs da har qoida uchun alohida holat.
- Tekshiruvchi izohi: ruff C901 raqamlari mos (check_docs.main 63, run_tests.select 53, rules_for.main 39, run_tests.main 25, diagnose 25). Lekin 'K1 shu atrofda' noto'g'ri: K1 changed_files() da (run_tests.py:395-418), select() (481) da emas. Murakkablik o'zi nuqson emas, run_tests 88% qamralgan. max-complexity=25 da 25 lik ikkitasi o'tadi, 3 ta qoladi.

### KD-Q9. Hujjat va holat fayllariga atomik bo'lmagan yozuv

- Og'irlik: past; tur: sifat; mehnat: S; holat: tasdiqlandi.
- Dalil: review_status.py:127 io.open(path,'w').write(new) (bob fayli), add_code.py:92 (bob fayli), review_queue.py:159, sonar_snapshot.py:122, build_single.py:147. ruff SIM115 test bo'lmagan kodda 35 ta context manager siz open. Bular newline='\n' siz, Windows da CRLF yozadi (.gitattributes eol=lf normallashtiradi).
- Ta'sir: Yozish o'rtasida uzilish bobni kesib qoldiradi; docs git da, shuning uchun commit qilinmagan tahrir yo'qolishi mumkin, xolos.
- Tavsiya: Q4 dagi atomic_write_text(path, text) (pid tmp, newline='\n') ga o'tkazish, Q4 1-qadami ichida.
- O'lchov: ruff --select SIM115 test bo'lmagan kodda 0.
- Tekshiruvchi izohi: 5 joy tasdiqlandi: review_status.py:127, add_code.py:92, review_queue.py:159, sonar_snapshot.py:122, build_single.py:147 (open(...).write, newline siz). SIM115 test bo'lmagan kodda 35. .gitattributes '* text=auto eol=lf'.

### KD-Q10. Vaqt tugaganda faqat bevosita bola jarayon o'ldiriladi

- Og'irlik: past; tur: sifat; mehnat: S; holat: tuzatish bilan tasdiqlandi.
- Dalil: run_tests.py:829-833 subprocess.run(argv, timeout=left); TimeoutExpired da Python faqat bevosita jarayonni kill qiladi. Windows da argv = ['cmd','/c','gradlew.bat'] (run_tests.py:303-306), ya'ni java nevara jarayon. Linux da gradlew/mvnw oxirida exec java qiladi, shuning uchun muammo asosan Windows da (taxmin, Windows da sinalmadi).
- Ta'sir: Windows da vaqt tugagach Gradle/Maven JVM ishlashda davom etib build/ papkani va log faylni band qilishi mumkin; keyingi --yurgiz root_lock bilan emas, fayl qulfi bilan yiqiladi (taxmin).
- Tavsiya: Popen(start_new_session=True) + try/finally: istalgan chiqishda (TimeoutExpired, KeyboardInterrupt, SIGTERM handler) proc tirik bo'lsa os.killpg(SIGTERM), 5 s, keyin SIGKILL; Windows da 'taskkill /T /F /PID'. Test: FAKE 'nevara' rejimi ham timeout, ham SIGINT holati uchun, nevara pid 1 s ichida yo'q.
- O'lchov: Yangi holat Linux va Windows CI da yashil: nevara pid timeoutdan keyin 1 s ichida yo'q.
- Tekshiruvchi izohi: run_tests.py:829-836 subprocess.run(timeout) faqat bevosita bolani o'ldiradi, Windows da argv 'cmd /c gradlew.bat' (303-306) - mantiqan to'g'ri (Windows da sinalmadi). Lekin tavsiyadagi start_new_session=True yon ta'sirli: build yangi sessiyaga chiqadi, terminaldagi Ctrl+C va Claude Code Bash vositasi o'z jarayon guruhini to'xtatganda build unga kirmaydi va yetim qoladi. Faqat timeout yo'lini tuzatish yangi yetim build manbaini ochadi.

### KD-Q11. 25 test faylida o'z runneri: bitta holatni yurgizib bo'lmaydi, vaqt chiqmaydi

- Og'irlik: past; tur: tezlik; mehnat: M; holat: tasdiqlandi.
- Dalil: 25 faylda 'OK if ok else XATO' tsikli, 15 tasida 'for name, fn in CASES'. sys.argv ni faqat 2 test fayli o'qiydi: -k filtr yo'q. Har holat vaqtini o'lchash uchun scratch/time_cases.py yozishga to'g'ri keldi.
- Ta'sir: Bitta holatni tuzatishda butun suite (6-12 s) qayta yuradi; sekin holat qaysi biri ekanini runner aytmaydi, T1-T5 dagi sabablar shu tufayli ko'rinmay qolgan.
- Tavsiya: tools/testkit.py (stdlib): run_cases(CASES, argv) -&gt; exit kodi, '-k' filtr, '--vaqt' bilan 200 ms dan uzun holatlar. Avval T1-T5 tegadigan 5 sekin suite, qolganlari tegilganda.
- O'lchov: python3 tools/test_guard.py -k docker faqat mos holatlarni yurgizadi; --vaqt chiqishida eng sekin holatlar.
- Tekshiruvchi izohi: 25 faylda 'OK if ok else XATO', 16 tasida 'for name, fn/check in' tsikli, sys.argv faqat test_rules_for va test_run_tests da. -k filtr va holat vaqti yo'q; men ham har holat vaqti uchun alohida skript yozishga majbur bo'ldim (t2.py, t4.py).

### KD-T-M2. CI faqat Python 3.12 da, o'rnatuvchi esa 3.8+ ni va'da qiladi

- Og'irlik: past; tur: sifat; mehnat: S; holat: skeptik tekshiruvchi qo'shgan (alohida qayta tekshirilmagan).
- Dalil: .github/workflows/docs.yml da barcha joblar python-version '3.12'; install/manguberdi.ps1:320 'ishlaydigan Python 3.8+ topilmadi'. ast.parse(feature_version=(3,8)) barcha tools/*.py va install/*.py da xatosiz, ya'ni hozir buzilmagan, lekin runtime 3.9+ API (dict | dict, str.removeprefix, zip(strict=)) kirib qolsa hech narsa ushlamaydi. Q2 dagi target-version='py39' tavsiyasi ham shu nomuvofiqlikdan.
- Ta'sir: Eski Pythonli foydalanuvchida hooklar SyntaxError yoki AttributeError bilan yiqiladi va '|| exit 0' tufayli guard, budjet va taklif jim o'chadi.
- Tavsiya: docs.yml tools job matritsasiga ubuntu da eng past qo'llab-quvvatlanadigan versiyani qo'shish (setup-python runner da beradigan eng pasti); agar 3.8 berilmasa o'rnatuvchidagi minimal talabni sinaladigan versiyaga ko'tarish. ruff target-version shu versiyaga teng.
- O'lchov: CI da minimal Python versiyasida 'Asbob sinovlari' yashil; o'rnatuvchi xabari va CI matritsasi bir xil versiyani aytadi.
