package shop.service;

import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestClient;

public class TxStaticFactory {

    private OrderRepository repository;

    @Transactional
    public String place(Order order) {
        repository.save(order);
        return RestClient.create().get().uri("/stock/" + order.id())
                .retrieve().body(String.class);
    }
}
