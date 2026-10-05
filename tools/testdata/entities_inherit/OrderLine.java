package shop.order;

import jakarta.persistence.*;
import shop.catalog.Product;

@Entity
@Table(name = "order_lines", indexes = @Index(columnList = "product_id"))
public class OrderLine {

    @EmbeddedId
    private OrderLineId id;

    @MapsId("orderId")
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    private Purchase purchase;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id")
    private Product product;

    private int quantity;
}
