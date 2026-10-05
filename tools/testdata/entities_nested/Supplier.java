package shop.purchase;

import jakarta.persistence.*;
import java.util.UUID;

/** Supplier entity class without @Table: the table name comes from the class. */
@Entity public class Supplier {

    @Id
    private UUID id;

    @Version
    private Long version;

    @Column(length = 80)
    private String name;
}
