package shop.shipping;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

@Embeddable
public class Address {

    @Column(length = 80)
    private String street;

    private String city;
}
