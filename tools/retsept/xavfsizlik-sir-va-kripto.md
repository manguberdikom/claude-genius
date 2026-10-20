# xavfsizlik: sir va kripto

Minimal shakl (code-review 32.3, 32.4):

```java
@Bean
PasswordEncoder passwordEncoder() {
    return new Argon2PasswordEncoder(16, 32, 1, 19 * 1024, 2);
}
private static final SecureRandom RANDOM = new SecureRandom();
static String newToken() {
    byte[] raw = new byte[32];
    RANDOM.nextBytes(raw);
    return Base64.getUrlEncoder().withoutPadding().encodeToString(raw);
}
```

Allaqachon bor, yozmang:
- SHA-256/MD5 bilan parol hash o'rniga `Argon2PasswordEncoder` yoki `BCryptPasswordEncoder(12)` (code-review 32.3)
- hash migratsiyasi o'rniga `DelegatingPasswordEncoder` (code-review 32.3)
- `String.equals` bilan token tekshirish o'rniga `MessageDigest.isEqual` (code-review 32.6)
- o'z shifri o'rniga `Cipher.getInstance("AES/GCM/NoPadding")` va `GCMParameterSpec` (code-review 32.5)

Tuzoqlar:
- GCM da nonce takrorlansa kalit ochiladi, ECB esa taqiq: har shifrlashda `SecureRandom` dan yangi 12 bayt nonce oling (code-review 32.5)
- token, OTP yoki salt `Random`/`Math.random` bilan taxmin qilinadi: faqat `SecureRandom` (code-review 32.4)
- token va API kalit bazada ochiq saqlanmaydi, `toString` da sir logga tushmaydi: hash qilib saqlang, maskalang (code-review 32.3, 32.1)
- `Argon2PasswordEncoder(saltLen, hashLen, parallelism, memoryKiB, iterations)`: parallelism va memory almashsa jim kuchsiz; `defaultsForSpringSecurity_v5_8()` 16 MiB, OWASP 19 MiB dan past (code-review 32.3)
- kalit, parol, API kalit Java literal yoki repodagi faylda emas: muhit yoki Vault/KMS, topilgani rotatsiya (code-review 32.5, 32.8)
