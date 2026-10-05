package shop.service;

import org.springframework.transaction.annotation.Transactional;

/**
 * Izohdagi @KafkaListener va createNativeQuery belgi emas.
 */
public class Noise {

    private static final String BASE = "http://inventory/createQuery";

    // jdbcTemplate.update(...) eski usul edi
    @Transactional
    public void save(Order order) {
        repository.save(order);
    }
}
