package shop;

import jakarta.persistence.*;

@Entity
public class Delivery {

    @Id
    private Long id;

    @Version
    private Long version;

    @ManyToOne(fetch = FetchType.LAZY)
    private Depot depot;

    @ManyToOne(fetch = FetchType.LAZY)
    private Depot courier;

    @ManyToOne(fetch = FetchType.LAZY)
    private Depot backup;
}
