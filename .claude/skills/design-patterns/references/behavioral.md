# Behavioral patterns

They organize how objects communicate and how responsibility moves between them.

## Strategy

**Problem:** an `if`/`switch` picks between interchangeable algorithms, and new
cases keep arriving.

**Shape:** one interface, one implementation per algorithm, chosen by the caller.

```ts
type ShippingRate = (order: Order) => Cents

const flatRate: ShippingRate = () => 599
const byWeight: ShippingRate = (o) => Math.round(o.grams * 0.8)

function checkout(order: Order, rate: ShippingRate) {
  return order.subtotal + rate(order)
}
```

**Trade-off:** in a language with first-class functions, a function parameter
*is* the pattern. Reach for interfaces and classes only when a strategy needs
state or several related methods.

## Observer

**Problem:** several independent parts must react when something changes, and
the source shouldn't know who they are.

**Shape:** subject keeps a list of listeners and notifies them on change.

**Trade-off:** always return an unsubscribe handle and call it on teardown —
dangling listeners leak memory and fire after disposal. Notification order is
not a contract; if one listener depends on another having run, Observer is the
wrong tool (use an explicit pipeline).

## State

**Problem:** an object's behavior changes with its lifecycle stage, and the
checks (`if (status === "draft") ...`) are spread across many methods.

**Shape:** one class per state, each implementing the transitions it allows.

**Trade-off:** makes illegal transitions unrepresentable, at the price of more
types. With two states and one guard, a boolean is still better.

## Command

**Problem:** an action must be queued, retried, logged or undone — not just
executed.

**Shape:** reify the action as an object with `execute()` (and `undo()` when
needed), carrying its own parameters.

**Trade-off:** `undo()` is the hard part; it requires capturing enough prior
state to restore. Don't add it until undo is actually a requirement.

## Template Method

**Problem:** several flows share an identical skeleton but differ in a few
steps.

**Shape:** a base method defining the order, calling overridable hooks.

**Trade-off:** inheritance couples subclasses to the base's internals. Passing
the varying steps in as functions (Strategy) is usually more flexible and
easier to test.

## Iterator

**Problem:** callers need to traverse a collection without knowing its storage.

**Shape:** the language's own iteration protocol — `Symbol.iterator`,
`__iter__`, `IEnumerable`, generators.

**Trade-off:** almost never hand-written today; use the built-in protocol so
`for`-loops, spreads and comprehensions work. Note that mutating during
iteration is undefined behavior in most implementations.

## Mediator

**Problem:** a set of components all reference each other directly, so every
change ripples.

**Shape:** components talk to one mediator; it coordinates them.

**Trade-off:** the mediator accumulates logic and becomes a god object if it
coordinates too much. Keep one mediator per interaction, not per application.

## Chain of Responsibility

**Problem:** a request should pass through ordered handlers, any of which may
handle it or pass it on (middleware, validation layers, event filters).

**Shape:** each handler holds the next and decides whether to delegate.

**Trade-off:** failure to call the next handler silently drops the request —
the most common bug in middleware stacks. Make "pass through" the default.

## Visitor

**Problem:** you need new operations over a stable type hierarchy (AST nodes,
shapes) without touching each type for every operation.

**Shape:** each type accepts a visitor and dispatches to the matching method.

**Trade-off:** it trades easy *operations* for hard *types*: adding one node
type breaks every visitor. Use it only where the hierarchy is settled. In
languages with pattern matching or sum types, match exhaustively instead.
