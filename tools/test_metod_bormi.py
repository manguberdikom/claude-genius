#!/usr/bin/env python3
"""metod_bormi.py: o'xshash metod topiladi, maydon yozuvchilari sanaladi.

    python3 tools/test_metod_bormi.py
"""

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import metod_bormi as M  # noqa: E402

ORDER = """package shop;
public class Order {
    private java.math.BigDecimal amount;
    private String status = "NEW";
    public Order(java.math.BigDecimal amount) { this.amount = amount; }
    public void markPaid() { this.status = "PAID"; }
    public void applyDiscount(java.math.BigDecimal rate) { amount = amount.multiply(rate); }
    public java.math.BigDecimal getAmount() { return amount; }
}
"""
SERVICE = """package shop;
public class OrderService {
    public Order findByStatus(String status) { return null; }
    void cancel(Order o) { o.setStatus("CANCELLED"); }
    public void refundPayment(Long id) { if (id == null) return; }
}
"""
TICKET = """package shop;
public class Ticket {
    private String state;
    public void setState(String state) { this.state = state; }
}
"""
LEGACY = """package shop;
public class Legacy {
    private String phase;
    @Deprecated(since = "1.1", forRemoval = false)
    public void setPhase(String phase) { this.phase = phase; }
}
"""
SERVICE_TEST = """package shop;
public class OrderServiceTest {
    void t(Order o, Ticket k) { o.setStatus("X"); k.setState("Y"); }
}
"""


def main():
    tmp = tempfile.mkdtemp(prefix="metod-")
    try:
        for name, text in (("Order.java", ORDER), ("OrderService.java", SERVICE),
                           ("Ticket.java", TICKET), ("Legacy.java", LEGACY),
                           ("OrderServiceTest.java", SERVICE_TEST)):
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as handle:
                handle.write(text)
        found = M.similar(tmp, ["refund", "status"])
        status_writers = {name for _, name, _ in M.writers(tmp, "status")}
        amount_writers = {name for _, name, _ in M.writers(tmp, "amount")}
        outside, open_setters, _, _ = M.audit(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    checks = [
        ("so'z bo'yicha metod topiladi (refundPayment, findByStatus)",
         any("refundPayment" in r for r in found) and any("findByStatus" in r for r in found)),
        ("if/return metod deb sanalmaydi", not any(" if(" in r or "return" in r.split()[1] for r in found)),
        ("status: domen metodi va tashqi setter ikki yozuvchi",
         status_writers == {"markPaid", "cancel"}),
        ("amount: konstruktor va domen metodi, getter emas",
         amount_writers == {"Order", "applyDiscount"}),
        ("audit: servis setteri tashqi yozuvchi, test fayli sanalmaydi",
         len(outside) == 1 and "OrderService.cancel" in outside[0] and "Test" not in outside[0]),
        ("audit: ochiq public setter alohida sanaladi, @Deprecated emas",
         len(open_setters) == 1 and "setState" in open_setters[0]),
    ]
    failures = 0
    for name, ok in checks:
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(checks) - failures, len(checks)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
