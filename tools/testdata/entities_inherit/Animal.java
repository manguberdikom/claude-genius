package shop.zoo;

import jakarta.persistence.*;

@Entity
@Table(name = "animals")
public class Animal {

    @Id
    private Long id;

    @Version
    private Long version;
}
