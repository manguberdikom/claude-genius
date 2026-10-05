package shop.domain;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "order_no", length = 32, nullable = false)
    private String orderNo;

    @Column(nullable = false)
    private BigDecimal totalAmount;

    @Enumerated
    private OrderStatus status;

    @ManyToOne
    @JoinColumn(name = "customer_id")
    private Customer customer;

    @OneToMany(fetch = FetchType.EAGER)
    private List<OrderLine> lines;

    @Column
    private Instant createdAt;

    private String note;
}
