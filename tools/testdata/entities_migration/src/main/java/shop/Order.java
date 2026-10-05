package shop;

import jakarta.persistence.*;

// "order" band so'z, shuning uchun jadval nomi qo'shtirnoqda.
@Entity
@Table(name = "\"order\"")
public class Order {

    @Id
    private Long id;

    @Version
    private Long version;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "depot_id")
    private Depot depot;
}
