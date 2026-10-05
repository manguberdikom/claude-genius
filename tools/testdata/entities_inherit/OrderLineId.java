package shop.order;

import jakarta.persistence.Embeddable;
import java.io.Serializable;
import java.util.UUID;

@Embeddable
public class OrderLineId implements Serializable {

    private UUID orderId;

    private Integer lineNo;
}
