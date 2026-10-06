# A/B sinovi: manguberdi foyda beradimi

Bu papka sinovni tayyorlaydi, yurgizadi va baholaydi. Har yurish
alohida sessiya: bitta sessiya ikki holatni xolis solishtira olmaydi,
chunki u o'z ishini baholaydi.

Savol bitta: `/manguberdi` orkestratori, aktyorlar, budjet hisoblagichi
va majburiy `rules_for` natijani yaxshilaydimi, yoki faqat pul va vaqt
sarflaydimi.

| Fayl | Nima |
|---|---|
| `yurgiz.py` | runner: har (vazifa, holat, takror) uchun klon, config, `claude -p` |
| `baho.py` | mexanik baholovchi va ifloslanish filtri |
| `tahlil.py` | `natijalar.tsv` dan juft bootstrap va qaror |
| `umumiy.py` | uchalasining umumiy qismi |
| `vazifalar/` | 10 vazifa, prompt va qabul mezoni |
| `oltin/` | baholovchini kalibrlash uchun oltin yechimlar |
| `natijalar.tsv` | har yurishga bitta qator |

Asboblar `tools/` da emas: ular faqat shu sinovga tegishli va genius
asboblari qatoriga qo'shilmaydi. Har biri `--sinov` bilan o'zini
tarmoqsiz va pulsiz sinaydi.

## Sinov proyekti

| | |
|---|---|
| Repo | https://github.com/spring-projects/spring-petclinic |
| Commit | `500158f732419217507c7656904b8e6aa1bcc0d6` (`main`, 2026-10-05) |
| Spring Boot | 4.1.0 |
| Yig'uvchi | Maven (`./mvnw`), format darvozasi `spring-javaformat` bilan |
| B versiyasi | yurish paytidagi claude-genius commiti, `natijalar.tsv` ning `genius_commit` ustunida |

Boshlang'ich holat o'lchangan: konteyner talab qilmaydigan testlar
**76/76 yashil**, taxminan 20 sekundda (issiq Maven keshida):

```bash
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
```

Testcontainers talab qiladigan uchta sinov (`MySqlIntegrationTests`,
`PostgresIntegrationTests`, `PetClinicConcurrencyTests`) hamma joyda
chiqarib tashlanadi: ularning yiqilishi holatga emas, muhitga bog'liq.

**Seriya** bitta `genius_commit` va bitta `model` dan iborat. Orkestrator,
aktyorlar, `CLAUDE.md` yoki `rules_for` o'zgarsa, keyingi yurish yangi
seriya bo'ladi va eski seriya qatorlari bilan aralashtirilmaydi
(`tahlil.py` ikki seriyani birga hisoblamaydi).

## Ikki holat

| Holat | Qanday |
|---|---|
| **A** | Oddiy Claude Code. Alohida, bo'sh `CLAUDE_CONFIG_DIR`: skill, aktyor va hook yo'q, `GENIUS_HOOKS=off`. |
| **B** | Alohida `CLAUDE_CONFIG_DIR` ga genius o'rnatilgan: `manguberdi` skilli, olti aktyor, hooklar va ruxsatlar. Sessiya `/manguberdi` bilan boshlanadi, vazifa prompti shu sessiyaga `--resume` bilan beriladi. |

Nega A bo'sh config bilan: global o'rnatish `manguberdi` va olti
aktyorni `~/.claude` ga qo'yadi, `GENIUS_HOOKS=off` esa faqat hooklarni
o'chiradi. Ya'ni umumiy config da A ham orkestratorni yoki aktyorni
o'zi chaqira olardi va sinov orkestratorni orkestrator bilan
solishtirardi (OL-O8, KT-K3). Marshrut skilllari global o'rnatishga
kirmaydi, shuning uchun ular ikkala holatda ham yo'q. Demak sinov
o'lchayotgani aynan **o'rnatiladigan qatlam**: orkestrator, aktyorlarga
taqsimlash, budjet, hooklar va majburiy `rules_for`.

Ikkinchi himoya transkript filtri: A da `manguberdi` yoki aktyor
chaqiruvi topilsa yurish yaroqsiz (pastda, "Ifloslanish qoidasi").

Prompt matni ikkala holatda **aynan bir xil**: `yurgiz.py` uni
`vazifalar/` dagi faylning `## Prompt` blokidan oladi, bir harf ham
qo'shilmaydi. B dagi `/manguberdi` alohida birinchi navbat.

Holat tartibi almashinadi, chunki birinchi yurgizish muammoni o'rganib
qo'yishi mumkin. Har takrorda vazifalar ketma-ket, holatlar shu tartibda:

| Vazifa | Birinchi | Ikkinchi |
|---|---|---|
| 1, 3, 5, 7, 9 | A | B |
| 2, 4, 6, 8, 10 | B | A |

## Tayyorlov

Har yurish o'z papkasida, noldan:

1. **petclinic klon.** Vazifa faylidagi `## Tayyorlash` bajariladi,
   keyin `.git` qayta yaratiladi: bitta "boshlang'ich" commit (OL-O6).
   Bug vazifasida (1-3) diff shu commit ichida, ya'ni `git status` va
   `git diff` toza va javobni ko'rsatmaydi. Review vazifasida (8, 9)
   diff commitdan keyin qo'llanadi va ataylab ko'rinadi. Runner
   tayyorlovdan keyin commit soni 1 ekanini va `git status` ni
   tekshiradi.
2. **Asl holat.** Tayyor daraxt `asl/` ga nusxalanadi. Baholovchi diffni
   shu bilan solishtiradi, model git bilan nima qilgani (commit, stash,
   reset) natijaga ta'sir qilmaydi.
3. **Genius nusxasi (faqat B).** `git archive <commit>` dan, `eval/` va
   `audit/` papkasiz (OL-T-M2): javob kaliti va bug qatorlari yozilgan
   audit topilmalari sessiyaga ochilmaydi. Nusxa har yurish uchun
   yangidan olinadi, ya'ni `memory/` git dagi holatda va B oldingi
   yurishidan o'rganmaydi (OL-T-M1). Tozalik git blob xeshi bilan
   tekshiriladi (`memory_toza`), yurishdan keyin o'zgargan memory
   fayllari `memory-keyin.txt` ga yoziladi: B nimani o'rganganini shu
   ko'rsatadi.
4. **Config.** Har yurishning o'z `CLAUDE_CONFIG_DIR` i, shuning uchun
   Claude Code auto-memory, transkript va usage ham alohida. B config
   `install/manguberdi.ps1` qiladigan o'rnatishning Python dagi teng'i:
   skill va aktyorlar nusxadan, yo'llar `install/rewrite_paths.py` bilan
   mutlaq, hook jadvali repodagi `.claude/settings.json` dan, yo'li shu
   nusxaga bog'langan. Sinov proyekti izolyatsiyalangan va ishonchli,
   shuning uchun B ga `run_tests.py` opt-in ruxsati ham beriladi.

## Avtomatik yurish

```bash
python3 eval/ab/yurgiz.py --smoke              # quruq: reja va buyruqlar
python3 eval/ab/yurgiz.py --takror 3           # quruq: to'liq reja

# haqiqiy yurish: Claude Code sessiyasi ichidan EMAS, terminaldan
export ANTHROPIC_API_KEY=...                   # alohida config da login yo'q
env -u CLAUDE_CODE_SESSION_ID python3 eval/ab/yurgiz.py --smoke --yurgiz
env -u CLAUDE_CODE_SESSION_ID python3 eval/ab/yurgiz.py --takror 3 --chek 5 --yurgiz

python3 eval/ab/tahlil.py                      # natija va qaror
```

- **Sukut rejim quruq.** Hech narsa yaratilmaydi, `claude` chaqirilmaydi:
  reja, holat tartibi, har sessiya buyrug'i va jami chek chiqadi. Pul
  faqat `--yurgiz` bilan sarflanadi.
- **Sessiya ichidan yurgizilmaydi.** `CLAUDE_CODE_SESSION_ID` meros
  bo'lsa bola `claude -p` ota sessiya id sini oladi, budjet va usage
  aralashadi (PL-CC10). Runner bu o'zgaruvchi bo'lsa `--yurgiz` ni rad
  etadi va bola muhitidan uni har holda olib tashlaydi.
- **Buyruq.** `claude -p <prompt> --output-format json --max-budget-usd <chek>`.
  JSON dan `session_id`, `total_cost_usd`, `duration_ms` va
  `modelUsage` olinadi. B ning ikki navbati bitta chek ichida:
  ikkinchisiga birinchidan qolgani beriladi.
- **Ruxsat ikki holatda bir xil.** Sukut: bir xil `--allowedTools`
  ro'yxati (`Read`, `Edit`, `Write`, `./mvnw`, `git`, o'qish buyruqlari,
  `Skill`, `Task`). `--ruxsat bypass` faqat izolyatsiyalangan mashinada.
  `acceptEdits` ishlatilmaydi: print rejimida u ruxsat so'raydigan har
  narsani rad etadi va `./mvnw` yurmaydi. B ning genius asboblari uchun
  qo'shimcha ruxsati o'rnatishning o'zida, ya'ni sinalayotgan qatlam.
- **Chek.** `--chek` bitta sessiya uchun (sukut $5), `--jami-chek` butun
  yurish uchun (sukut chek x yurish soni). Keyingi sessiya jami chekdan
  oshadigan bo'lsa runner to'xtaydi.
- **Qayta boshlash.** Ifloslanmagan qatori bor katak qayta yurmaydi.
  Ifloslangan yurish qatori iz uchun qoladi, runner shu katakni bir
  marta qayta yurgizadi, keyingi chaqiruvda yana.
- **Ketma-ket.** Parallel yurgizilmaydi: Maven raqobati `daqiqa` ni
  buzadi.

Ketma-ketlik: avval smoke (1, 3, 8 vazifa x 2 holat x 1), uning narxi
va vaqti o'lchanadi, keyin 10 x 2 x 3 = 60 sessiya. Narx sessiyaga ~$1-4
deb olinsa to'liq yurish ~$60-240 (taxmin, smoke dan keyin aniqlanadi).

Har yurish papkasida (`~/genius-ab/yurish/<genius12>/<NN>-<H>-<k>-u<n>/`):
`pc/` (ish daraxti), `asl/`, `config/` (transkriptlar `config/projects/`
da), `genius/` (B), `claude-N.json` va `.err`, `javob.md` (yakuniy
javob), `memory-keyin.txt` (B), `qator.json`.

## Vazifalar

| # | Fayl | Tur | Tekshiruv |
|---|---|---|---|
| 1 | [01-bug-ism-uzunligi.md](vazifalar/01-bug-ism-uzunligi.md) | bug | `PetValidatorTests` |
| 2 | [02-bug-bosh-ism.md](vazifalar/02-bug-bosh-ism.md) | bug | `PetControllerTests` |
| 3 | [03-bug-sahifalash.md](vazifalar/03-bug-sahifalash.md) | bug (jim) | yangi regressiya testi bug qaytganda yiqiladi |
| 4 | [04-refaktoring-owner-controller.md](vazifalar/04-refaktoring-owner-controller.md) | refaktoring | butun to'plam |
| 5 | [05-refaktoring-getpet.md](vazifalar/05-refaktoring-getpet.md) | refaktoring | butun to'plam |
| 6 | [06-test-pettypeformatter.md](vazifalar/06-test-pettypeformatter.md) | test | yangi chegara holatlari, dublikat yo'q |
| 7 | [07-test-addpet.md](vazifalar/07-test-addpet.md) | test | yangi testlar va JaCoCo shoxlari |
| 8 | [08-review-kesh.md](vazifalar/08-review-kesh.md) | review | 4 kiritilgan nuqson |
| 9 | [09-review-pul-va-sana.md](vazifalar/09-review-pul-va-sana.md) | review | 4 kiritilgan nuqson |
| 10 | [10-reja-tashrif-narxi.md](vazifalar/10-reja-tashrif-narxi.md) | reja | reja mezoni |

Uchta bug va ikki review diffi `vazifalar/diff/` da. Har biri shu
commitga toza qo'llanadi (`git apply --check` bilan tekshirilgan) va
kompilyatsiyadan hamda format darvozasidan o'tadi, ya'ni vazifa
nuqsonlar haqida bo'ladi, formatlash haqida emas.

Bug diffi **vazifa boshlanishidan oldin** qo'llanadi va bu haqda
modelga aytilmaydi: u buzilgan kodni oldida ko'radi, xuddi haqiqiy
ishdagidek. Diff boshlang'ich commit ichida bo'lgani uchun uni
`git diff` bilan "topib bo'lmaydi".

## Nima o'lchanadi

Har yurish uchun `natijalar.tsv` ga bitta qator. Runner hammasini o'zi
to'ldiradi, `yolgon_topilma` va `kor_baho` dan tashqari: ularni ko'r
hakam beradi.

| Ustun | Qanday olinadi |
|---|---|
| `vazifa` | 1-10 |
| `holat` | A yoki B |
| `takror` | 1-3 (2-bosqichda ham 1-3) |
| `sessiya_id` | `claude -p` JSON dagi `session_id`, transkript shu nom bilan |
| `genius_commit` | yurishdagi claude-genius commiti (12 belgi), seriya kaliti |
| `model` | `--model` yoki JSON dagi `modelUsage` kalitlari |
| `muvaffaqiyat` | `baho.py` mexanik bahosi: qabul mezoni to'liq bajarildimi, 1 yoki 0 |
| `xato_topildi` | faqat review: 4 nuqsondan nechtasi (kalit so'z bo'yicha, hakam tasdiqlaydi) |
| `yolgon_topilma` | faqat review: mavjud bo'lmagan muammo soni, hakam beradi |
| `usd` | JSON dagi `total_cost_usd`, B da ikki navbat yig'indisi |
| `token` | `modelUsage` yig'indisi, faqat ma'lumot uchun, qarorga kirmaydi |
| `daqiqa` | JSON dagi `duration_ms` |
| `aralashuv` | avtomatik yurishda 0 |
| `kor_baho` | ko'r baholash, 1-5 |
| `ifloslangan` | 1 bo'lsa yurish yaroqsiz, tahlilga kirmaydi |
| `memory_toza` | B nusxasidagi `memory/` yurish boshida git dagi holatda edimi |
| `izoh` | yiqilgan mezonlar, xato navbatlar, ifloslanish sababi |

Muvaffaqiyat **ikkilik**: qabul mezoni to'liq bajarilsa 1, aks holda 0.
"Deyarli" degan baho yo'q, aks holda natijani keyin talqin qilib
bo'ladi.

## Ifloslanish qoidasi

Yurish yaroqsiz (`ifloslangan=1`), agar uning transkriptida (subagent
transkriptlari ham):

1. A holatida `Skill` tool_use `manguberdi` ni chaqirgan, `/manguberdi`
   slash buyrug'i bor, yoki `Task`/`Agent` tool_use ning
   `subagent_type` i olti aktyordan biri (`rejalashtiruvchi`,
   `dasturchi`, `test-muhandis`, `review`, `qidiruv`, `tahlil`);
2. har holatda biror tool_use kirishida `eval/ab` yo'li bor (javob
   kaliti);
3. B holatida `manguberdi` yuklangani izi yo'q;
4. transkript umuman yo'q.

Yaroqsiz qator o'chirilmaydi, katak qayta yurgiziladi. Ifloslanish soni
holat bo'yicha `tahlil.py` chiqishida turadi.

## Baholash

**Mexanik qism** (`baho.py`) vazifa faylidagi qabul mezonini kod bilan
tekshiradi: surefire XML dagi test natijasi, `asl/` bilan fayl
darajasidagi diff (test o'zgarmagan, faqat maqsadli fayl o'zgargan),
maqsadli qator, 3-vazifada yangi test bugli `src/main` da yiqiladimi,
7-vazifada JaCoCo shoxlari. Arzon mezon avval yuradi, biri yiqilsa Maven
yurmaydi va `izoh` da birinchi yiqilgan mezon turadi.

Review (8, 9) va reja (10) vazifalarida mexanik qism kalit so'z
bo'yicha sanaydi va kod o'zgarmaganini tekshiradi. Bu taxminiy: kalit
so'z nuqsonning sababini aytganini kafolatlamaydi, shuning uchun hakam
`xato_topildi` ni tasdiqlaydi va zarur bo'lsa `muvaffaqiyat` ni
tuzatadi, tuzatish `izoh` ga yoziladi.

Kalibrlash (R1.1 qabul sharti): oltin yechim `oltin/` dan qo'llanganda
har vazifa 1, bo'sh yechimda 0 olishi shart.

```bash
python3 eval/ab/baho.py --sinov              # Maven siz, soxta daraxt va soxta transkript
python3 eval/ab/baho.py --kalibr --pc <petclinic klon yoki mirror>   # haqiqiy Maven
```

2026-10-06 dagi `--kalibr` natijasi: oltin 10/10, bo'sh yechim 0 olgani
10/10.

**Ko'r hakam.** Diff sifatini va review topilmalarini **uchinchi**
sessiya baholaydi, u A va B ni bilmaydi.

1. Har vazifa uchun ikki diff `A.diff` va `B.diff` nomi bilan emas,
   tanga tashlab `1.diff` va `2.diff` nomi bilan saqlanadi. Moslik
   alohida faylda, hakamga berilmaydi.
2. Hakam sessiyaga faqat vazifa matni (prompt va qabul mezoni) va ikki
   diff yoki ikki javob beriladi. Qo'llanma, hooklar va bu papka
   berilmaydi.
3. Baho 1-5: 1 = noto'g'ri yoki xavfli, 3 = ishlaydi lekin tozalash
   kerak, 5 = shunday qoldirib ketiladi. Review da hakam
   `yolgon_topilma` ni ham sanaydi.
4. Hakam qaysi diff qaysi holatdan ekanini **bilmasligi** kerak,
   shuning uchun unga `natijalar.tsv` ko'rsatilmaydi.

## Qaror qoidasi

Bu qoida 2026-10-06 da, `natijalar.tsv` da birorta natija qatori yo'q
paytda yozilgan va natijaga qarab o'zgartirilmaydi. Shu band commit
tarixida birinchi natija qatoridan oldin turadi. Hisob `tahlil.py` da,
o'zgarsa ikkalasi bitta commitda o'zgaradi va yangi seriya boshlanadi.

Avvalgi qoida (B >= A + 2 vazifa va token_B <= 1.5 token_A, bitta
yurish) hech qachon qo'llanmagan. U ikki sababga ko'ra almashtirildi:
effekt yo'q bo'lsa ham B 23% ehtimol bilan qolardi, haqiqiy +20 foiz
punktda esa faqat 60% (OL-O9). Narx xom token bilan o'lchanardi, aralash
model va keshda u haqiqiy narxni aks ettirmaydi (OL-T-M3).

**Hisob.** Birlik vazifa. Har vazifada holat bo'yicha o'rtacha
muvaffaqiyat va o'rtacha USD olinadi. Farq d = vazifalar bo'yicha
o'rtacha (pB - pA), juft. Narx nisbati r = jami USD_B / jami USD_A.
Ishonch chegarasi juft bootstrap bilan: vazifalar va har vazifa ichida
takrorlar qaytarib olinadi, 10000 marta, urug' 20261005. Chegaralar bir
tomonli 90%: quyi = 10-persentil, yuqori = 90-persentil. Ifloslangan
qator kirmaydi. Qaror faqat kamida 10 vazifa x 3 takror bo'lganda
chiqadi, smoke qaror bermaydi.

**B qoladi**, agar quyidagilardan biri bajarilsa:

1. *Ustunlik:* d ning quyi chegarasi > 0 **va** r ning yuqori chegarasi
   <= 1.5;
2. *Non-inferiority:* d ning quyi chegarasi >= -0.05 **va** r ning
   yuqori chegarasi <= 1.0.

Narx sharti ikkala yo'lda ham bor: B qanchalik yaxshi bo'lsa ham, 1.5
barobardan qimmat bo'lsa qolmaydi.

**B olib tashlanadi**, agar d ning yuqori chegarasi < 0 (B aniq
yomonroq) yoki r ning quyi chegarasi > 1.5 (B aniq qimmat).

**Bosqichli to'ldirish.** 1-bosqich: 10 vazifa x 2 x 3. Natija yuqoridagi
ikki holatning birortasiga tushmasa (NOANIQ), 10 ta yangi vazifa
qo'shiladi va 20 x 2 x 3 gacha to'ldiriladi. Yangi vazifalar natijani
ko'rmagan holda, shu papkadagi shakl va kalibrlash talabi bilan
yoziladi. 2-bosqichda ham "B qoladi" sharti bajarilmasa, B olib
tashlanadi: isbot yuki orkestratorda.

Quvvat (`tahlil.py --quvvat`, simulyatsiya, vazifa qiyinligi Beta(1.5, 1),
USD lognormal; taxmin):

| Holat | 10 x 3 | 20 x 3 |
|---|---|---|
| +20 foiz punkt, narx x1.2 | 51% qoladi, 49% noaniq | 80% qoladi |
| effekt yo'q, narx x1.2 | 6% qoladi (yolg'on ijobiy) | 5% qoladi |
| effekt yo'q, narx x2.0 | 100% olib tashlanadi | 100% olib tashlanadi |

**Olib tashlansa** quyidagilar ketadi: orkestrator (`/manguberdi` skilli
va `references/`), budjet hisoblagichi (`tools/budget.py` va uning
hooklari) va majburiy `rules_for` darvozasi (`check_code.py` dagi
zanjir sharti).

Qoladi: marshrut skilllari, `docs/` qo'llanmalari, `review` aktyori,
`tools/doc.sh` va qidiruv qatlami, `guard.py` ning katta bob to'sig'i.
Ular bu sinovda o'lchanmaydi, shuning uchun qaror ularga tegmaydi.

Review vazifalarida (8, 9) `xato_topildi` va `yolgon_topilma` qo'shimcha
dalil: `yolgon_topilma` B da A dan ko'p bo'lsa, bu qarorga qarshi dalil
bo'lib hisobotda aytiladi, lekin yuqoridagi shartlarni almashtirmaydi.

Natija qanday chiqsa ham shu README ga yoziladi: "B qoldi, chunki ..."
yoki "B olib tashlandi, chunki ...", `tahlil.py` raqamlari va seriya
(`genius_commit`, `model`) bilan.

## Nima o'lchanmaydi, ochiq aytilsin

- Uzoq muddatli foyda: memory va qoidalarning bir necha haftadagi
  ta'siri. Har yurish toza memory bilan boshlanadi.
- Katta legacy loyihadagi xulq: petclinic kichik va toza.
- Odamning qulayligi: avtomatik yurishda aralashuv yo'q, qanoat
  o'lchanmaydi.
- Marshrut skilllari: ular ikkala holatda ham yo'q.
- Review va reja vazifalarining mexanik bahosi kalit so'zga tayanadi va
  hakam tasdig'isiz yakuniy emas.
