package shop;

import org.springframework.kafka.annotation.KafkaListener;

public class Consumer {

    @KafkaListener(topics = "orders")
    public void onOrder(String payload) {
        handle(payload);
    }
}
