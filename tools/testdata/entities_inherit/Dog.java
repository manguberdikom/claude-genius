package shop.zoo;

import jakarta.persistence.*;

@Entity
public class Dog extends Animal {

    @Column(length = 60)
    private String breed;
}
