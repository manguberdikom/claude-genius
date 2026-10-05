package shop.service;

import java.io.IOException;
import org.springframework.transaction.annotation.Transactional;

public class Tx {

    private RestTemplate restTemplate;
    private WebClient webClient;

    @Transactional
    public void archive(AuditRecord record) {
        restTemplate.postForObject("/audit", record, Void.class);
    }

    @Transactional(rollbackFor = {IOException.class})
    public void refund(Long id) throws IOException {
        webClient.post().uri("/refund/" + id).retrieve();
    }
}

@Transactional
class TxWide {

    private final RestClient restClient = RestClient.create();

    public void notify(Long id) {
        restClient.post().uri("/notify/" + id).retrieve();
    }
}
