package shop;

import java.math.BigDecimal;
import java.time.LocalDate;

public class Money {

    private BigDecimal amount;
    private LocalDate dueDate;

    public BigDecimal rate() {
        return new BigDecimal(0.07);
    }
}
