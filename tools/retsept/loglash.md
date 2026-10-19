# loglash

Minimal shakl (sonarqube 41.7, clean-code 29.1, clean-code 29.3):

```java
@Slf4j
@Component
@RequiredArgsConstructor
class SettlementJob {

    private final PaymentGateway gateway;

    void settleAll(List<String> paymentIds) {
        for (String paymentId : paymentIds) {
            try {
                gateway.capture(paymentId);
                log.info("to'lov yopildi: paymentId={}", paymentId);
            } catch (GatewayException e) {
                log.error("to'lov {} yopilmadi", paymentId, e);
            }
        }
    }
}
```

Allaqachon bor, yozmang:
- Qo'lda `LoggerFactory.getLogger(...)` maydoni o'rniga Lombok `@Slf4j` (sonarqube 41.7)
- `isDebugEnabled()` va `+` o'rniga `{}` yoki `log.atDebug().addArgument(() -> ...)` (clean-code 29.1)
- JSON encoder kutubxonasi o'rniga Boot 3.4+ da `logging.structured.format.console=ecs` (architect 30.2)
- traceId uchun o'z filtri o'rniga Micrometer Tracing, async uchun `ContextPropagatingTaskDecorator` (code-review 39.5)

Tuzoqlar:
- `e.getMessage()` stack trace ni yo'qotadi; istisno obyekti placeholder siz oxirgi argument (clean-code 29.3)
- Har qatlamda log va throw bitta xatoni bir necha marta yozadi; log faqat xatoni hal qilgan chegarada (clean-code 29.5)
- Parol, token, karta raqami `toString` orqali log ga oqadi; tur o'z `toString` ida maskalasin (clean-code 29.8)
