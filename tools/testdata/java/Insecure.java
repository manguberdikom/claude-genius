package shop.web;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.web.multipart.MultipartFile;

public class Insecure {

    @PersistenceContext
    private EntityManager em;

    private String apiKey = System.getenv("API_KEY");

    public Object findByName(String name) {
        return em.createNativeQuery(
                "select * from users where name = '" + name + "'").getResultList();
    }

    public void upload(MultipartFile file) {
        store(file);
    }
}
