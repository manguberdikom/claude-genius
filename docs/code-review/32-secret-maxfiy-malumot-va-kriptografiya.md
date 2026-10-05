<!-- doc: code-review | chapter: 32 | part: VI. Xavfsizlik review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 32. Secret, maxfiy ma'lumot va kriptografiya review (Secrets, PII and Crypto)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [32.1 Logga maxfiy ma'lumot tushishi](#321-logga-maxfiy-malumot-tushishi)
- [32.2 PII va ma'lumot minimizatsiyasi](#322-pii-va-malumot-minimizatsiyasi)
- [32.3 Parol va token saqlash](#323-parol-va-token-saqlash)
- [32.4 Tasodifiylik](#324-tasodifiylik)
- [32.5 Shifrlash](#325-shifrlash)
- [32.6 Taqqoslash va vaqt hujumlari](#326-taqqoslash-va-vaqt-hujumlari)
- [32.7 TLS va sertifikatlar](#327-tls-va-sertifikatlar)
- [32.8 Review checklisti: secret va kriptografiya](#328-review-checklisti-secret-va-kriptografiya)
- [32.9 Amalda qo'llash](#329-amalda-qollash)

</details>


Bu bob ma'lumotning oshkor bo'lish yo'llarini va kriptografik xatolarni oladi. Ularning umumiy xususiyati: ular sodir bo'lganda hech narsa buzilmaydi, tizim normal ishlaydi, va muammo faqat keyinroq - ma'lumot tashqarida paydo bo'lganda - bilinadi.

## 32.1 Logga maxfiy ma'lumot tushishi

Bu eng ko'p uchraydigan ma'lumot oqishi yo'li, va review da eng oson topiladigan.

```java
// Naqsh 1: butun so'rovni logga yozish.
log.info("So'rov keldi: {}", request);           // parol, karta, token - hammasi
log.debug("Foydalanuvchi: {}", user);            // toString() da nima bor?

// Naqsh 2: istisno xabarida maxfiy ma'lumot.
throw new InvalidCardException("Karta raqami yaroqsiz: " + cardNumber);
// Bu istisno logga tushadi va karta raqami logda qoladi - PCI DSS buzilishi.

// Naqsh 3: HTTP mijoz loglari.
logging.level.org.springframework.web.client=DEBUG   // Authorization header logda

// Naqsh 4: SQL parametrlari logi.
logging.level.org.hibernate.orm.jdbc.bind=TRACE      // parol hash, PII
// Bu sozlama lokalda foydali, prodda - ma'lumot oqishi.

// Himoya 1: toString ni maskalash - eng ishonchli, chunki bir joyda.
public record PaymentRequest(String cardNumber, String cvv, Money amount) {
    @Override public String toString() {
        return "PaymentRequest[card=%s, cvv=***, amount=%s]"
               .formatted(mask(cardNumber), amount);
    }
    private static String mask(String card) {
        if (card == null || card.length() < 4) return "****";
        return "*".repeat(card.length() - 4) + card.substring(card.length() - 4);
    }
}

// Himoya 2: tipga maskalashni yashirish - unutish imkonsiz bo'ladi.
public final class Secret {
    private final String value;
    public Secret(String value) { this.value = value; }
    public String reveal() { return value; }         // aniq niyat bilan
    @Override public String toString() { return "***"; }   // log va xatolarda
}
// Ishlatilishi: Secret apiKey - uni tasodifan logga yozib bo'lmaydi.
```

```xml
<!-- Himoya 3: log darajasida maskalash (oxirgi himoya chizig'i). -->
<!-- logback-spring.xml -->
<configuration>
  <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
      <!-- Karta raqami naqshini maskalash -->
      <jsonGeneratorDecorator class="net.logstash.logback.decorate.MaskingJsonGeneratorDecorator">
        <defaultMask>****</defaultMask>
        <path>password</path>
        <path>cvv</path>
        <path>cardNumber</path>
        <path>authorization</path>
        <valueMask>
          <value>\b\d{13,19}\b</value>        <!-- karta raqamiga o'xshash -->
        </valueMask>
      </jsonGeneratorDecorator>
    </encoder>
  </appender>
</configuration>
```

## 32.2 PII va ma'lumot minimizatsiyasi

| Review savoli | Nega |
| --- | --- |
| Bu maydon haqiqatan kerakmi | Saqlanmagan ma'lumot oqib ketmaydi |
| Qancha vaqt saqlanadi | Saqlash muddati siyosati |
| Kim ko'ra oladi | Rol va audit |
| Eksport va hisobotlarda bormi | Oqish yo'li |
| Test ma'lumotida haqiqiy PII yo'qmi | Prod nusxasi test muhitida |
| Analitikaga yuboriladimi | Uchinchi tomon |
| Shifrlanganmi (saqlashda) | Baza nusxasi oqsa |
| O'chirish talabi bajariladimi | Huquqiy talab (26.7) |

```sql
-- PII ustunlarini belgilash: review va audit uchun.
COMMENT ON COLUMN customer.phone IS 'PII: telefon, saqlash muddati 3 yil';
COMMENT ON COLUMN customer.passport_number IS 'PII: sezgir, shifrlangan';

-- PII ustunlarini topish: audit so'rovi.
SELECT c.table_name, c.column_name, pd.description
  FROM information_schema.columns c
  LEFT JOIN pg_description pd
    ON pd.objoid = (quote_ident(c.table_schema)||'.'||quote_ident(c.table_name))::regclass
   AND pd.objsubid = c.ordinal_position
 WHERE pd.description LIKE 'PII%'
 ORDER BY 1, 2;
```

## 32.3 Parol va token saqlash

```java
// Parol: faqat moslashuvchan hash funksiyasi bilan.
@Bean
PasswordEncoder passwordEncoder() {
    // Argon2 yoki bcrypt. SHA-256 va MD5 - parol uchun TAQIQLANADI
    // (ular tez, ya'ni brute force ham tez).
    return new Argon2PasswordEncoder(16, 32, 1, 19 * 1024, 2);
    // Yoki: new BCryptPasswordEncoder(12);
}
// Review savollari: (1) parametrlar yetarlimi (bcrypt da cost >= 10);
// (2) migratsiya yo'li bormi (DelegatingPasswordEncoder eski hash larni
// qo'llab-quvvatlaydi va kirish paytida yangilaydi);
// (3) parol uzunligi chegarasi bormi (bcrypt 72 baytdan keyin kesadi).

// Token va API kalit: hash qilib saqlash (parol kabi).
// Bazada ochiq token saqlanmasligi kerak - baza nusxasi oqsa, hamma
// token ishlatilishi mumkin.
public record ApiKey(String id, String hashedSecret) {
    public static ApiKey generate(PasswordEncoder encoder) {
        byte[] raw = new byte[32];
        new SecureRandom().nextBytes(raw);                  // SecureRandom!
        String secret = Base64.getUrlEncoder().withoutPadding().encodeToString(raw);
        return new ApiKey(UUID.randomUUID().toString(), encoder.encode(secret));
        // `secret` faqat bir marta foydalanuvchiga ko'rsatiladi.
    }
}
```

## 32.4 Tasodifiylik

```java
// Zaif: taxmin qilinadigan.
new Random().nextInt();                          // seed vaqtdan, taxmin qilinadi
Math.random();                                   // xuddi shunday
UUID.randomUUID();                               // kriptografik (SecureRandom) - to'g'ri

// Kuchli: token, kalit, parol tiklash kodi uchun.
SecureRandom random = new SecureRandom();
byte[] token = new byte[32];
random.nextBytes(token);

// Review qoidasi: xavfsizlikka tegishli har qanday tasodifiy qiymat
// (token, parol tiklash kodi, sessiya ID, nonce, salt, OTP)
// SecureRandom bilan yaratiladi.

// Diqqat: OTP uchun 6 raqam - bu 10^6 variant. Brute force dan himoya
// urinishlar chegarasi bilan ta'minlanadi, tasodifiylik bilan emas.
int otp = random.nextInt(1_000_000);             // tasodifiy, lekin qisqa
// Review savoli: urinishlar soni cheklanganmi va kod qancha amal qiladi?
```

## 32.5 Shifrlash

```java
// Zaif: ECB rejimi (naqshlarni saqlaydi) va qattiq yozilgan IV.
Cipher c = Cipher.getInstance("AES/ECB/PKCS5Padding");          // taqiqlanadi
Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");          // IV kerak, autentifikatsiya yo'q

// To'g'ri: autentifikatsiyalangan shifrlash (AEAD), har marta yangi nonce.
public final class FieldEncryption {
    private static final int GCM_TAG_BITS = 128;
    private static final int NONCE_BYTES = 12;
    private final SecretKey key;
    private final SecureRandom random = new SecureRandom();

    public byte[] encrypt(byte[] plaintext, byte[] associatedData) throws Exception {
        byte[] nonce = new byte[NONCE_BYTES];
        random.nextBytes(nonce);                      // HAR SAFAR yangi
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(GCM_TAG_BITS, nonce));
        if (associatedData != null) cipher.updateAAD(associatedData);
        byte[] ct = cipher.doFinal(plaintext);
        return ByteBuffer.allocate(nonce.length + ct.length)
                         .put(nonce).put(ct).array();   // nonce ochiq saqlanadi
    }
}
// Review savollari: (1) nonce qayta ishlatilmaydimi (GCM da nonce
// takrorlanishi kalitni ochadi - eng xavfli xato); (2) kalit qayerdan
// keladi (KMS, Vault - koddan emas); (3) kalit rotatsiyasi qanday
// (shifrlangan ma'lumotga kalit versiyasi yozilganmi); (4) nima
// shifrlangan va nega aynan shu.
```

## 32.6 Taqqoslash va vaqt hujumlari

```java
// Zaif: token taqqoslash `equals` bilan - vaqt bo'yicha ma'lumot beradi.
if (providedToken.equals(storedToken)) { ... }
// `String.equals` birinchi farqda to'xtaydi, ya'ni bajarilish vaqti
// to'g'ri belgilar soniga bog'liq. Masofadan bu farqni o'lchash qiyin,
// lekin mumkin.

// To'g'ri: doimiy vaqtli taqqoslash.
if (MessageDigest.isEqual(provided.getBytes(UTF_8), stored.getBytes(UTF_8))) { ... }

// HMAC tekshirish (webhook imzosi) - eng ko'p uchraydigan joy.
public boolean verifyWebhook(byte[] body, String signatureHeader) throws Exception {
    Mac mac = Mac.getInstance("HmacSHA256");
    mac.init(new SecretKeySpec(webhookSecret, "HmacSHA256"));
    byte[] expected = mac.doFinal(body);
    byte[] provided = Hex.decode(signatureHeader);
    return MessageDigest.isEqual(expected, provided);      // doimiy vaqt
}
// Review savollari: (1) imzo tekshiriladimi umuman (ko'p loyihada webhook
// tekshirilmaydi - har kim xabar yuborishi mumkin); (2) xom tana bo'yicha
// tekshiriladimi (JSON qayta serializatsiya qilinsa imzo buziladi);
// (3) takrorlanishdan himoya bormi (timestamp va nonce).
```

## 32.7 TLS va sertifikatlar

```java
// Taqiqlanadi: sertifikat tekshiruvini o'chirish.
TrustManager[] trustAll = new TrustManager[]{ new X509TrustManager() {
    public void checkServerTrusted(X509Certificate[] c, String a) { }   // hech narsa
    ...
}};
// Review izohi: bu kod MITM hujumini to'liq ochib beradi. "Test uchun"
// yoki "staging da sertifikat yo'q" sababi qabul qilinmaydi - to'g'ri
// yechim: ichki CA ni truststore ga qo'shish.

// To'g'ri: ichki CA bilan.
// JVM ga: -Djavax.net.ssl.trustStore=/etc/ssl/internal-truststore.jks
// Yoki kodda aniq truststore:
SSLContext ctx = SSLContextBuilder.create()
    .loadTrustMaterial(new File("/etc/ssl/internal-ca.jks"), password)
    .build();
```

## 32.8 Review checklisti: secret va kriptografiya

| Savol | Nega |
| --- | --- |
| Logga maxfiy ma'lumot tushmaydimi | Eng ko'p uchraydigan oqish |
| `toString` maskalanganmi | Tasodifiy log |
| Istisno xabarida PII yo'qmi | Log va javob orqali oqish |
| Secret muhitdan yoki Vault danmi | Repoda kalit |
| Parol Argon2/bcrypt bilanmi | Tez hash brute force ga ochiq |
| Token hash qilib saqlanadimi | Baza nusxasi |
| `SecureRandom` ishlatilganmi | Taxmin qilinadigan token |
| Shifrlash AEAD (GCM) mi | Yaxlit emas shifrlash |
| Nonce har safar yangimi | GCM da halokatli xato |
| Kalit rotatsiyasi rejasi bormi | Kalit oqsa |
| Token taqqoslash doimiy vaqtlimi | Vaqt hujumi |
| Webhook imzosi tekshiriladimi | Yolg'on xabar |
| TLS tekshiruvi o'chirilmaganmi | MITM |
| PII saqlash muddati belgilanganmi | Huquqiy talab |

## 32.9 Amalda qo'llash

- [ ] Maxfiy ma'lumot tashuvchi barcha DTO va domen turlarida `toString` maskalanganini tekshiring.
- [ ] `Secret` yoki shunga o'xshash o'ram turini kiritib, API kalitlari va tokenlarni unga o'tkazing.
- [ ] Logback da maskalash dekoratorini sozlab, karta raqami va `authorization` naqshlarini maskalang.
- [ ] Prod log darajalarini tekshirib, `hibernate.orm.jdbc.bind` va web client DEBUG loglarini o'chiring.
- [ ] Parol enkoderini Argon2 yoki bcrypt (cost >= 12) ga o'tkazing va `DelegatingPasswordEncoder` bilan migratsiya yo'lini qo'ying.
- [ ] Bazada ochiq saqlanayotgan token va API kalitlarni hash ga o'tkazing.
- [ ] `new Random()` va `Math.random()` ishlatilgan xavfsizlikka tegishli joylarni `SecureRandom` ga o'tkazing.
- [ ] Shifrlash ishlatilgan joylarda rejim (GCM), nonke yangiligi va kalit manbasini tekshiring.
- [ ] Webhook qabul qiluvchilarda imzo tekshiruvi va doimiy vaqtli taqqoslash borligini tasdiqlang.
- [ ] PII ustunlarini `COMMENT ON COLUMN` bilan belgilab, saqlash muddati siyosatini yozing.

---

[&larr; 31. Kirish va chiqish xavfsizligi: SSRF, deserializatsiya, fayllar](31-kirish-va-chiqish-xavfsizligi-ssrf.md) · [Mundarija](README.md) · [33. Bog'liqlik va supply chain review &rarr;](33-bogliqlik-va-supply-chain-review.md)
