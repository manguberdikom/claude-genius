# Structural patterns

They compose objects so that the resulting structure is easier to change than
the sum of its parts.

## Adapter

**Problem:** an external library's interface doesn't match the one your code
already depends on.

**Shape:** a thin class implementing *your* interface, delegating to theirs.

```ts
class S3Storage implements FileStore {          // your interface
  constructor(private s3: S3Client) {}
  async read(path: string): Promise<Buffer> {
    const res = await this.s3.send(new GetObjectCommand({ Key: path, Bucket: BUCKET }))
    return Buffer.from(await res.Body!.transformToByteArray())
  }
}
```

**Trade-off:** keep adapters free of business logic. The moment one starts
making decisions, it has become a service with a misleading name.

## Decorator

**Problem:** behavior (retry, caching, metrics, logging) must be added to some
instances, chosen at runtime, without a subclass per combination.

**Shape:** a wrapper implementing the same interface as the thing it wraps.

```ts
class RetryingGateway implements PaymentGateway {
  constructor(private inner: PaymentGateway, private attempts = 3) {}
  async charge(cents: number) {
    let lastError: unknown
    for (let i = 0; i < this.attempts; i++) {
      try { return await this.inner.charge(cents) } catch (e) { lastError = e }
    }
    throw lastError
  }
}
```

**Trade-off:** chains get opaque fast. Three wrappers is usually the limit
before stack traces and debugging suffer. In Python or JS, a higher-order
function is often the lighter form of the same idea.

## Facade

**Problem:** callers must orchestrate five subsystems in the right order to do
one meaningful thing.

**Shape:** one class exposing a small task-oriented API over the subsystems.

**Trade-off:** a Facade must not become the place where everything lands. If it
grows past a handful of cohesive operations, split it by use case.

## Proxy

**Problem:** you need caching, lazy initialization, access control or
instrumentation around an object without changing its callers.

**Shape:** same interface as the target, with the extra concern around the
delegation.

**Trade-off:** indistinguishable from Decorator in structure; the difference is
intent — Proxy controls *access*, Decorator adds *behavior*. Pick the name that
describes why it exists.

## Composite

**Problem:** clients must treat a single item and a group of items the same way
(files and folders, a layout node and its children).

**Shape:** leaf and container implement one interface; the container forwards to
its children.

**Trade-off:** operations that make sense only for leaves (or only for
containers) end up on the shared interface. Accept a few `UnsupportedOperation`
cases, or don't use Composite.

## Flyweight

**Problem:** very many objects duplicate identical immutable state (glyphs,
tile types, interned tokens).

**Shape:** share one instance of the intrinsic state; pass the varying extrinsic
state as arguments.

**Trade-off:** a memory optimization, so only apply it with measurements in
hand. It adds a cache and makes identity comparisons subtle.
