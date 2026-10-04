package shop;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.atomic.AtomicInteger;

public class Concurrent {

    private final AtomicInteger counter = new AtomicInteger();
    private ExecutorService pool;

    public synchronized void bump() {
        counter.incrementAndGet();
    }
}
