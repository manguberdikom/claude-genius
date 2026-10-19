# mapper

Minimal shakl (patterns 8.14):

```java
@Mapper(componentModel = "spring",
        unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface OrderMapper {

    OrderResponse toResponse(Order order);

    List<OrderResponse> toResponses(List<Order> orders);
}
```

Allaqachon bor, yozmang:
- Qo'lda setter zanjiri o'rniga MapStruct `@Mapper(componentModel = "spring")` generatsiya qilgan bean (sonarqube 11.7)
- Ro'yxat uchun stream/loop o'rniga `List<B> toXs(List<A>)` metod imzosi (patterns 8.14)
- PATCH dagi `if (x != null)` zanjiri o'rniga `@MappingTarget` va `NullValuePropertyMappingStrategy.IGNORE` (patterns 8.14)
- Bitta oddiy DTO uchun mapper sinfi o'rniga record ichida `static from(entity)` (clean-code 26.6)

Tuzoqlar:
- `unmappedTargetPolicy` qo'yilmasa yangi maydon jimgina `null` qoladi; `ReportingPolicy.ERROR` bilan build da ushlang (sonarqube 11.7)
- Tranzaksiya yopilgach controller da map qilish lazy maydonda `LazyInitializationException` yoki N+1 beradi; service chegarasida, oldindan fetch qilingan ma'lumotni map qiling (architect 17.7)
- ModelMapper kabi reflection mapper nom o'zgarishini faqat production da ochadi, mapper ichidagi biznes qoidasi esa yashirinadi; MapStruct oling va mapper faqat ko'chirsin (patterns 8.14)
