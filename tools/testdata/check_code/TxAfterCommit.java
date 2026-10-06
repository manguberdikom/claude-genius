package shop.service;

import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

public class TxAfterCommit {

    private RestClient restClient;
    private OrderRepository repository;

    @Transactional
    public void place(Order order) {
        repository.save(order);
        TransactionSynchronizationManager.registerSynchronization(
                new TransactionSynchronization() {
                    @Override
                    public void afterCommit() {
                        restClient.post().uri("/notify/" + order.id()).retrieve();
                    }

                    @Override
                    public void afterCompletion(int status) {
                        restClient.post().uri("/audit/" + status).retrieve();
                    }
                });
    }
}

@Transactional
class OrderEvents {

    private RestTemplate restTemplate;
    private OrderRepository repository;

    public void place(Order order) {
        repository.save(order);
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onPlaced(OrderPlaced event) {
        restTemplate.postForObject("/notify", event, Void.class);
    }

    @TransactionalEventListener
    public void onPaid(OrderPaid event) {
        restTemplate.postForObject("/paid", event, Void.class);
    }
}
