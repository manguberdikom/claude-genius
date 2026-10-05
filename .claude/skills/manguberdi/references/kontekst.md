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

Bob fayli butunligicha o'qilmaydi, bo'lim o'qiladi (`doc.sh show`).
1200 satrdan uzun faylni chegarasiz o'qish `guard.py` tomonidan
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
```

`UserPromptSubmit` hooki (`handoff.py --hook`) har so'rovda shuni
o'lchaydi va chegaradan oshganda o'zi bir qator bilan aytadi, bir
sessiyada har pog'ona uchun bir marta. Shuning uchun to'lishni eslab
yurish shart emas.

O'lchov transkriptdagi haqiqiy raqamdan olinadi. Oyna hajmi
`CONTEXT_LIMIT`, `autoCompactWindow` sozlamasi yoki model jadvalidan
(haiku 200K, qolgani 1M), auto siqish bo'lgan bo'lsa o'sha nuqtadan
olinadi. Siqish bo'lgan, kontekst oynaning 75% idan yoki 400K tokendan
(`CONTEXT_WARN`) oshgan bo'lsa yangi sessiya tavsiya qilinadi.

Skill yangi sessiya ocha olmaydi, lekin `--prompt` tayyor topshiriq
beradi: git holati, oxirgi commitlar va memory indeksini mashina
to'ldiradi, `<...>` ichidagi joylarni siz to'ldirasiz.

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

Qayerga yoziladi: to'ldirilgan beshta maydon (mashina bergan git
qismisiz, u git dan olinadi) `memory/<proyekt-slug>/project_<vazifa>.md`
ga yoziladi, `MEMORY.md` ga bir qator qo'shiladi, commit va push
qilinadi (`memory-protocol.md` marshruti, `type: project`).

Keyin foydalanuvchiga `--prompt` matni beriladi (u `/manguberdi` bilan
boshlanadi) va u matnni yangi sessiyaga yuboradi. Matn yo'qolsa ham
yangi sessiya memory indeksidan shu faylni topadi. Ish tugagach fayl va
indeks qatori o'chiriladi.

## O'lchov

Kunlik token sarfi va uni qaysi aktyor sarflagani:
`python3 tools/usage.py` (dollarda, aktyor bo'yicha). `Stop` hook har
navbat oxirida uni o'zi yozib boradi, so'rash shart emas.

Har navbatdagi qat'iy kontekst `python3 tools/cost_report.py` bilan
o'lchanadi. Agar u byudjetdan oshsa, sabab odatda yangi qo'shilgan
doimiy matn bo'ladi, sessiya uzunligi emas.
