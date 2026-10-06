package shop.service;

import java.net.http.HttpClient;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.reactive.function.client.WebClient;

public class TxHttpVersion {

    private OrderRepository repository;

    @Transactional
    public HttpClient.Version version(Order order) {
        repository.save(order);
        HttpClient.Redirect redirect = HttpClient.Redirect.NORMAL;
        audit(redirect);
        return HttpClient.Version.HTTP_2;
    }

    @Transactional
    public void configure(WebClient.Builder builder) {
        repository.flush();
    }
}
