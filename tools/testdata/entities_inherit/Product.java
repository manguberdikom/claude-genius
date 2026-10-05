package shop.catalog;

import jakarta.persistence.*;
import shop.common.BaseEntity;

@Entity
@Table(name = "products")
public class Product extends BaseEntity {

    @Column(length = 120)
    private String title;
}
