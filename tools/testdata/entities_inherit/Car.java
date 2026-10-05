package shop.fleet;

import jakarta.persistence.Entity;

@Entity
public class Car extends Vehicle {

    private int seats;
}
