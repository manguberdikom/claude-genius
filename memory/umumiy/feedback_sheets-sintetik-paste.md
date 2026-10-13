---
type: feedback
---
# Google Sheets ga brauzer orqali ko'p qator yozish

- `navigator.clipboard.writeText` Chrome oynasi orqada bo'lganda
  `NotAllowedError: Document is not focused` beradi. `document.hasFocus()`
  `true` bo'lsa ham, `document.visibilityState` `hidden` bo'lsa ishlamaydi.
- Ishlaydigan yo'l: `DataTransfer` ga `text/plain` (TSV) va `text/html`
  (`<table>`) qo'yib, `new ClipboardEvent('paste', {clipboardData, bubbles:
  true, cancelable: true})` ni `document.activeElement` ga dispatch qilish.
  Sheets sintetik hodisani qabul qiladi, `isTrusted` ni tekshirmaydi.
  Buferga umuman tegilmaydi.
- Katalakni tanlash: Name Box ni bosib `A171` deb yozib Enter. Ishonchli,
  sichqoncha bilan qidirishdan tez.
- Skrinshot koordinata ramkasi viewport CSS piksellaridan kichik bo'lishi
  mumkin. `getBoundingClientRect()` dan olingan koordinatani
  `ramka_eni / window.innerWidth` ga ko'paytirib bosish kerak.
- Natijani skrinshotdan emas, tabni CSV qilib qayta o'qib tekshir.
