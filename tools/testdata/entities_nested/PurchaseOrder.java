package shop.purchase;

import jakarta.persistence.*;
import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Set;

/**
 * Entity class for purchase orders. The class keeps "totals" in sync;
 * nothing in this comment may become a table or a column.
 */
@Entity
@Table(
    name = "purchase_order",
    uniqueConstraints = @UniqueConstraint(name = "uq_po_number", columnNames = {"number"}),
    indexes = {
        @Index(name = "idx_po_customer", columnList = "customer_id"),
        @Index(name = "idx_po_supplier", columnList = "created_by, supplier_id DESC")
    })
public class PurchaseOrder implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @SequenceGenerator(name = "po_seq", sequenceName = "po_seq", allocationSize = 50)
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "po_seq")
    private Long id;

    @Version
    private Long version;

    @Column(name = "number", length = 20, nullable = false)
    private String number;

    // This class maps the amount; "class amount" here must not leak.
    @Column(name = "amt", precision = 19, scale = 2, columnDefinition = "numeric(19,2)")
    private BigDecimal amount;

    @Column(length = 200)
    private String homepage = "https://example.com/orders;list{x}";

    @Column(length = 64)
    private String externalID;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(foreignKey = @ForeignKey(name = "fk_po_customer"), name = "customer_id")
    private Customer customer;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "supplier_id")
    private Supplier supplier;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "created_by")
    private Supplier createdBy;

    @ManyToMany
    @JoinTable(name = "purchase_order_supplier",
        joinColumns = @JoinColumn(name = "po_id"),
        inverseJoinColumns = @JoinColumn(name = "supplier_id"))
    private Set<Supplier> suppliers;

    @ElementCollection
    @CollectionTable(name = "po_tag", joinColumns = @JoinColumn(name = "po_id"))
    @Column(name = "tag", length = 30)
    private Set<String> tags;

    private transient String cache;

    public BigDecimal total() {
        if (amount == null) {
            return BigDecimal.ZERO;
        }
        String note = "private String ghost;";
        return amount;
    }
}
