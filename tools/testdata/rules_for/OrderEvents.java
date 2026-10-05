package shop.service;

import org.springframework.retry.annotation.Retryable;
import org.springframework.transaction.event.TransactionalEventListener;

public class OrderEvents {

    @TransactionalEventListener
    @Retryable
    public void onPaid(OrderPaid event) {
        notifier.send(event);
    }
}
