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
| Butun modulni o'qib review qilish | `review` |
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

O'lchov transkriptdagi haqiqiy raqamdan olinadi, oynaning hajmi esa
siqish (compact) bo'lgan bo'lsa shu sessiyaning o'zidan. Siqish bo'lgan
yoki kontekst 75% dan oshgan bo'lsa yangi sessiya tavsiya qilinadi.

Skill yangi sessiya ocha olmaydi, lekin `--prompt` nusxalanadigan
topshiriq beradi: git holati, oxirgi commitlar va memory indeksi
mashina tomonidan to'ldiriladi, uch burchakli joylar sizdan.

Uzatish hujjati shu beshtadan iborat va **qisqa** bo'ladi. Uzun
topshiriq yangi sessiyani ham to'ldiradi:

```
# Topshiriq: <vazifa nomi>

Maqsad: <bir jumla>
Bajarildi: <qadamlar, har biri bir qator>
Qolgan: <qadamlar, har biri bir qator>
Qarorlar: <qaror va qoida raqami, nega shunday tanlangan>
Keyingi qadam: <aniq birinchi harakat>
```

Qayerga yoziladi: davom etayotgan ish holati `memory-protocol.md`
marshrutida `type: project`, ya'ni `memory/<proyekt-slug>/`. Shunda
yangi sessiya memory indeksini o'qib, ishni davom ettiradi.

Yozilgandan keyin foydalanuvchiga aytiladi: ish uzatildi, yangi
sessiyada `/manguberdi` chaqirilib, topshiriq fayli ko'rsatiladi.

## O'lchov

Har navbatdagi qat'iy kontekst `python3 tools/cost_report.py` bilan
o'lchanadi. Agar u byudjetdan oshsa, sabab odatda yangi qo'shilgan
doimiy matn bo'ladi, sessiya uzunligi emas.
