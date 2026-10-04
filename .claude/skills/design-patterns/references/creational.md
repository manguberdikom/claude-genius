# Creational patterns

They control *how* objects come into existence, so call sites stop depending on
concrete types.

## Factory Method

**Problem:** call sites say `new StripeGateway()`, so adding a provider means
editing every one of them.

**Shape:** a single function/method decides the concrete type; callers receive
the interface.

```ts
interface PaymentGateway { charge(cents: number): Promise<Receipt> }

function createGateway(kind: GatewayKind): PaymentGateway {
  switch (kind) {
    case "stripe": return new StripeGateway(config.stripe)
    case "adyen":  return new AdyenGateway(config.adyen)
  }
}
```

**Trade-off:** the `switch` does not disappear — it moves to one place. That is
the whole win. Don't split it into a class hierarchy until construction logic
per type is genuinely non-trivial.

## Abstract Factory

**Problem:** you need *families* of objects that must be used together — a
Postgres connection with a Postgres migrator and a Postgres dialect.

**Shape:** one interface producing several related products.

```ts
interface DbFactory {
  connection(): Connection
  migrator(): Migrator
  dialect(): Dialect
}
```

**Trade-off:** only worth it with two or more real families. With one, it is
ceremony around a constructor.

## Builder

**Problem:** a constructor with many optional parameters, or an object that is
invalid until several steps complete.

**Shape:** step-by-step configuration, then one `build()` that validates.

```ts
const query = new QueryBuilder("orders")
  .where("status", "=", "paid")
  .orderBy("created_at", "desc")
  .limit(50)
  .build()
```

**Trade-off:** in languages with named/default arguments (Python, Kotlin, C#),
an options object or keyword arguments beats a Builder. Keep the Builder for
multi-step validation or immutable targets.

## Prototype

**Problem:** creating an object is expensive (parsing, I/O, heavy defaults) and
you need many near-identical copies.

**Shape:** clone an existing configured instance and adjust the differences.

**Trade-off:** shallow vs deep copy is the whole difficulty. Be explicit about
which one `clone()` performs, and document mutable shared fields.

## Singleton

**Problem:** exactly one instance must exist (a connection pool, a process-wide
cache) and code needs to reach it.

**Shape:** private constructor plus a single accessor.

**Trade-off — read before using:** a Singleton is global mutable state. It
hides dependencies from signatures, makes tests order-dependent, and forces
reset hooks between test cases. Prefer creating one instance at the
application's entry point and passing it in (dependency injection). Use the
pattern only where the runtime itself demands a single instance and injection is
genuinely unavailable.
