package shop;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
class FlakyTest {

    @Test
    void waitsForJob() throws Exception {
        trigger();
        Thread.sleep(2000);
        assertEquals(1, count());
    }
}
