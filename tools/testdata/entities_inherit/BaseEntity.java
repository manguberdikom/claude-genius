package shop.common;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

/**
 * Common base class for every entity: id, version and audit time.
 */
@MappedSuperclass
public abstract class BaseEntity {

    @Id
    @GeneratedValue
    private UUID id;

    @Version
    private Long version;

    @Column(nullable = false)
    private Instant createdAt;

    public UUID getId() {
        return id;
    }
}
