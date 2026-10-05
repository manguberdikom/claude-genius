package shop.shipping;

import jakarta.persistence.*;
import java.util.UUID;

@Entity
public class Parcel {

    @Id
    private UUID id;

    @Version
    private Long version;
}
