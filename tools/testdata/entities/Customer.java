package shop.domain;

import jakarta.persistence.*;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "customers", indexes = {@Index(columnList = "email")})
public class Customer {

    @Id
    private Long id;

    @Version
    private Long version;

    @Column(name = "email", length = 190, nullable = false, unique = true)
    private String email;

    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    private Tier tier;

    @Column
    private Date registeredAt;

    @OneToMany(mappedBy = "customer", fetch = FetchType.LAZY)
    private List<Order> orders;
}
