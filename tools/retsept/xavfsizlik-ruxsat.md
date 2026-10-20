# xavfsizlik: ruxsat

Minimal shakl (code-review 30.3, 30.1; architect 20.8):

```java
@Configuration
@EnableMethodSecurity
class SecurityConfig {
    @Bean
    SecurityFilterChain api(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(a -> a
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(o -> o.jwt(withDefaults()))
            .build();
    }
}

@PreAuthorize("@orderAccess.canRead(#id, authentication)")
public OrderResponse get(UUID id) { ... }
```

Allaqachon bor, yozmang:
- `WebSecurityConfigurerAdapter` merosi o'rniga `SecurityFilterChain` bean va lambda uslubi (architect 20.3)
- qo'lda JWT parse qiluvchi filtr o'rniga `oauth2ResourceServer(o -> o.jwt(...))` (patterns 25.23)
- so'rovdagi `userId` o'rniga `@AuthenticationPrincipal` (code-review 30.2)

Tuzoqlar:
- `isAuthenticated()` egalikni tekshirmaydi (IDOR): `findByIdAndCustomerId` yoki policy bean, begona resursga 404 (code-review 30.1)
- self-invocation, `private`/`final` metod proxy dan o'tmaydi, `@PreAuthorize` jim o'chadi: tekshiruvni public bean metodiga qo'ying (architect 20.8)
- birinchi mos qoida ishlaydi: aniqdan umumiyga yozing, oxirida `anyRequest().authenticated()` (architect 20.13)
- `@PostAuthorize` yozish metodida: yon ta'sir allaqachon bo'lgan, faqat o'qishda (architect 20.8)
