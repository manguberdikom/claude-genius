package shop.shipping;

import jakarta.persistence.*;

@Entity
public class Label {

    @Id
    private Long id;

    @Version
    private Long version;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "shipment_id", unique = true)
    private Shipment shipment;
}
