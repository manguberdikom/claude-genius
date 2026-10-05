package shop.service;

import java.math.BigDecimal;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.transaction.annotation.Transactional;

public class Good {

    private static final Logger log = LoggerFactory.getLogger(Good.class);

    @Transactional
    public void save(Order order) {
        repository.save(order);
    }

    public BigDecimal fee() {
        return new BigDecimal("0.15");
    }

    public void load() {
        try {
            doWork();
        } catch (IllegalStateException e) {
            log.warn("ish bajarilmadi", e);
        }
    }
}
