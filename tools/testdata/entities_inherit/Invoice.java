package shop.billing;

import jakarta.persistence.*;
import java.math.BigDecimal;
import lombok.AccessLevel;
import lombok.experimental.FieldDefaults;

@Entity
@FieldDefaults(level = AccessLevel.PRIVATE)
public class Invoice {

    @Id
    Long id;

    @Version
    Long version;

    String title;

    BigDecimal amount;
}
