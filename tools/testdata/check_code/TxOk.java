package shop.service;

import java.io.IOException;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

interface OrderPort {
    @Transactional
    void place(Order order);
}

abstract class BaseService {
    @Transactional
    protected abstract void sync(Order order);
}

@Transactional
public class TxOk {

    private final RestTemplate restTemplate;

    TxOk(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public Item fetch(Long id) {
        return restTemplate.getForObject("/items/" + id, Item.class);
    }

    @Transactional(rollbackFor = {IOException.class})
    public void save(Order order) {
        repository.save(order);
    }

    public int parse(String raw) {
        try {
            return Integer.parseInt(raw);
        } catch (NumberFormatException ignored) { // kutilgan: raqam emas
        }
        try {
            return Integer.parseInt(raw.trim());
        } catch (NumberFormatException ignored) {
            // kutilgan: raqam emas
        }
        try {
            return Integer.parseInt(raw.strip());
        } catch (NumberFormatException ignored) { /* kutilgan */ }
        return 0;
    }
}
