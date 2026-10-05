package shop.order;

import jakarta.persistence.*;
import shop.common.BaseEntity;

@Entity
@Table(name = "purchases")
public class Purchase extends BaseEntity {

    @Column(length = 20)
    private String number;
}
