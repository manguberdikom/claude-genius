package shop.service;

import java.math.BigDecimal;
import org.springframework.transaction.annotation.Transactional;

public class Bad {

    private RestTemplate restTemplate;

    @Transactional
    public void placeOrder(Long id) {
        var res = restTemplate.getForObject("/pay/" + id, String.class);
        save(res);
    }

    public BigDecimal fee() {
        return new BigDecimal(0.15);
    }

    public void load() {
        try {
            doWork();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void quiet() {
        try {
            doWork();
        } catch (IllegalStateException e) {
        }
    }

    public void debug() {
        System.out.println("here");
    }

    // Izohdagi System.out.println va "catch (Exception e) {}" sanalmasligi kerak.
    private String note = "printStackTrace() satr ichida";
}
