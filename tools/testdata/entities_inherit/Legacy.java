package shop.legacy;

import jakarta.persistence.*;
import org.springframework.data.jpa.domain.AbstractPersistable;

@Entity
public class Legacy extends AbstractPersistable<Long> {

    @Column(length = 50)
    private String code;
}
