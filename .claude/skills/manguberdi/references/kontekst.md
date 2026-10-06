# Kontekstni toza saqlash va ishni uzatish

Uzun ishda kontekst asta to'ladi va hech kim buni sezmaydi: javoblar
sekinlashadi, eski tafsilot yangisini siqib chiqaradi. Buning oldi
olinadi, tuzatilmaydi.

## Birinchi himoya: og'irlik asosiy sessiyaga tushmaydi

Ko'p o'qib oz qaytaradigan ish aktyorga uzatiladi, uzun chiqish
ularning kontekstida qoladi:

| Ish | Kim bajaradi |
|---|---|
| O'nlab bo'limni o'qib taqqoslash | `qidiruv` |
| 500 qatorlik log yoki test chiqishi | `tahlil` |
| Butun modul yoki proyektni o'qib review qilish (diffsiz tartib) | `review` |
| Entity va sxema tahlili | `tahlil` |

Asosiy sessiyada faqat qaror, yo'naltirish va yakuniy javob qoladi.

## Ikkinchi himoya: o'qish chegarasi

Bob fayli butunligicha o'qilmaydi, bo'lim o'qiladi (`tools/doc.sh show`).
16 KB dan katta bo'lakni o'qish `guard.py` tomonidan
to'siladi. Bu qoida emas, mexanizm: uni unutib bo'lmaydi.

## Ish tugaganda

Vazifa yakunlangach javobda **faqat natija** qoladi:

- nima qilindi, bir jumlada,
- o'zgargan fayllar va qoida raqamlari,
- tekshiruvlar holati,
- memory yozuvi.

Oraliq qidiruv natijalari, o'qilgan bo'limlar matni, urinib ko'rilgan
va tashlangan yo'llar takrorlanmaydi. Ular ishning bir qismi edi,
natijaning emas.

## Kontekst to'lsa

Belgini taxmin qilish shart emas, u o'lchanadi:

```bash
python3 tools/handoff.py            # kontekst hajmi va tavsiya
python3 tools/handoff.py --prompt   # yangi sessiya uchun tayyor matn
python3 tools/handoff.py --prompt --vazifa <nom>   # topshiriq faylga
```

`UserPromptSubmit` hooki (`handoff.py --hook`) har so'rovda shuni
o'lchaydi va chegaradan oshganda o'zi bir qator bilan aytadi, bir
sessiyada har pog'ona uchun bir marta. Shuning uchun to'lishni eslab
yurish shart emas.

O'lchov transkriptdagi haqiqiy raqamdan olinadi. Oyna hajmi
`CONTEXT_LIMIT`, `autoCompactWindow` sozlamasi yoki model jadvalidan
(haiku 200K, qolgani 1M), auto siqish bo'lgan bo'lsa o'sha nuqtadan
olinadi. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` berilgan bo'lsa oyna shu
foizga tushiriladi, chunki siqish o'sha yerda bo'ladi. Siqish bo'lgan,
kontekst chegaraning 75% idan yoki 400K tokendan (`CONTEXT_WARN`) oshgan
bo'lsa yangi sessiya tavsiya qilinadi.

Skill yangi sessiya ocha olmaydi, lekin `--prompt` tayyor topshiriq
beradi. Fakt qismini mashina to'ldiradi: branch, oxirgi commitlar,
`git diff --stat HEAD`, git da yo'q yangi fayllar, `REJA.md` dagi `[x]`
qadamlar (Bajarildi) va belgisizlari (Qolgan), memory indeksi. Siz faqat
`<...>` joylarini to'ldirasiz: Maqsad, Qarorlar, Keyingi qadam.

Topshiriqning siz to'ldiradigan qismi quyidagi beshta maydondan iborat
va **qisqa** bo'ladi. Uzun topshiriq yangi sessiyani ham to'ldiradi:

```
# Topshiriq: <vazifa nomi>

Maqsad: <bir jumla>
Bajarildi: <qadamlar, har biri bir qator>
Qolgan: <qadamlar, har biri bir qator>
Qarorlar: <qaror va qoida raqami, nega shunday tanlangan>
Keyingi qadam: <aniq birinchi harakat>
```

Qayerga yoziladi: `--prompt --vazifa <nom>` topshiriqni faylga o'zi
yozadi va yo'lini aytadi, keyin `<...>` joylari bitta Edit bilan
to'ldiriladi. Jami ikki navbat.

- Lokal sessiya: `.claude/.state/handoff/<nom>.md` (yoki
  `GENIUS_STATE_DIR` ostida). Git siz: na commit, na push, na memory
  indeksi qatori. Fayl shu mashinada qoladi.
- Bulut sessiyasi (`CLAUDE_CODE_REMOTE`): konteyner qaytarib olinadi,
  shuning uchun fayl proyekt memorysiga `project_<nom>.md` bo'lib
  yoziladi. Klonning o'zida bu klondagi memory papkasi, boshqa proyektda
  `GENIUS_MEMORY_DIR` (sukut `~/.claude/genius-memory`). Asbob kerakli
  `git -C <memory ildizi>` buyrug'ini beradi; ildiz git da bo'lmasa buni
  aytadi.

Boshqa proyektning vazifa matni ochiq klon reposiga yozilmaydi
(`memory/README.md`). Klondagi begona memory papkasini `git add` yoki
`git commit` qilishni `guard.py` foydalanuvchi qaroriga qo'yadi.

Keyin foydalanuvchiga asbob bergan qisqa prompt beriladi (u
`/manguberdi` bilan boshlanadi va topshiriq faylini ko'rsatadi), u
uni yangi sessiyaga yuboradi. Ish tugagach topshiriq fayli o'chiriladi.

## O'lchov

Kunlik token sarfi va uni qaysi aktyor sarflagani:
`python3 tools/usage.py` (dollarda, aktyor bo'yicha). `Stop` hook har
navbat oxirida uni o'zi yozib boradi, so'rash shart emas.

Har navbatdagi qat'iy kontekst `python3 tools/cost_report.py` bilan
o'lchanadi. Agar u byudjetdan oshsa, sabab odatda yangi qo'shilgan
doimiy matn bo'ladi, sessiya uzunligi emas.
