package shop.fleet;

import jakarta.persistence.*;

@Entity
@Inheritance(strategy = InheritanceType.JOINED)
public class Vehicle {

    @Id
    private Long id;

    @Version
    private Long version;

    @Column(length = 16)
    private String plate;

    @Enumerated(EnumType.STRING)
    @Column(length = 10)
    private Fuel fuel;

    public enum Fuel {
        PETROL("p"), DIESEL("d");

        private final String code;

        Fuel(String code) {
            this.code = code;
        }
    }
}
