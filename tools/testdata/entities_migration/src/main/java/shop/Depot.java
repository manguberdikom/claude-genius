package shop;

import jakarta.persistence.*;

@Entity
public class Depot {

    @Id
    private Long id;

    @Version
    private Long version;
}
