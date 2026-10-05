package shop.shipping;

import jakarta.persistence.*;

@Entity
@Table(name = "shipment", indexes = {
    @Index(columnList = "created_at"),
    @Index(columnList = "owner_id DESC")
})
public class Shipment {

    @Id
    private Long id;

    @Version
    private Long version;

    private OrderStatus status;

    @Convert(converter = StatusConverter.class)
    private OrderStatus legacyStatus;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parcel_id", unique = true)
    private Parcel parcel;

    @ManyToOne(fetch = FetchType.LAZY)
    private Parcel owner;

    @Embedded
    @AttributeOverride(name = "street", column = @Column(name = "wh_street", length = 120))
    @AttributeOverride(name = "city", column = @Column(name = "wh_city", length = 60))
    private Address warehouse;

    private Address origin;

    private java.time.LocalDateTime createdAt;

    private java.math.BigDecimal total;

    @OneToOne(mappedBy = "shipment")
    private Label label;

    @Column(columnDefinition = "jsonb")
    private String payload;
}
