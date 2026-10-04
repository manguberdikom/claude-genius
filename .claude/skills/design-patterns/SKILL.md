---
name: design-patterns
description: Pick and apply classic software design patterns (creational, structural, behavioral) when refactoring or designing new code. Use when a task involves object creation strategies, decoupling modules, swapping algorithms at runtime, adding behavior without subclassing, or when the user names a pattern (factory, strategy, observer, adapter, decorator, singleton, repository, etc.) or asks "what pattern fits here?".
---

# Design Patterns

A pattern is a named solution to a recurring design problem. Patterns are
vocabulary, not goals: reach for one when the *problem* it solves is already
present in the code, never to make a design look sophisticated.

## How to use this skill

1. Name the actual problem in one sentence ("every new payment provider forces
   an edit to three `switch` statements").
2. Match it against the table below.
3. Read the matching reference file for the full shape, trade-offs and example.
4. Apply the smallest version of the pattern that solves the problem.

## Selection guide

| Problem you see in the code | Pattern | Reference |
| --- | --- | --- |
| `new ConcreteThing()` scattered across call sites | Factory Method / Abstract Factory | `references/creational.md` |
| Constructor with 6+ optional parameters | Builder | `references/creational.md` |
| Expensive object copied with slight variations | Prototype | `references/creational.md` |
| Genuinely one instance, global access needed | Singleton (last resort — prefer DI) | `references/creational.md` |
| Third-party API's shape doesn't match your interface | Adapter | `references/structural.md` |
| Behavior must be added per-instance, at runtime | Decorator | `references/structural.md` |
| Caller needs a simple door into a complex subsystem | Facade | `references/structural.md` |
| Need caching, lazy loading, access control around an object | Proxy | `references/structural.md` |
| Tree of items where leaves and groups are used alike | Composite | `references/structural.md` |
| Thousands of objects sharing identical immutable state | Flyweight | `references/structural.md` |
| `if/switch` choosing between interchangeable algorithms | Strategy | `references/behavioral.md` |
| Many parts must react to one thing changing | Observer | `references/behavioral.md` |
| Object behaves differently per lifecycle stage | State | `references/behavioral.md` |
| Actions need queueing, logging, undo | Command | `references/behavioral.md` |
| Fixed algorithm, varying steps | Template Method | `references/behavioral.md` |
| Walking a collection without exposing its internals | Iterator | `references/behavioral.md` |
| Objects know too much about each other | Mediator | `references/behavioral.md` |
| Request should pass through ordered handlers | Chain of Responsibility | `references/behavioral.md` |
| New operation needed over a stable type hierarchy | Visitor | `references/behavioral.md` |

## Rules of application

- **Duplication first, pattern second.** Wait for the third occurrence of the
  problem. Two is a coincidence; three is a shape.
- **Match the codebase's idiom.** In a language with first-class functions, a
  Strategy is often a function parameter, not an interface with three classes.
  In Python, a Decorator is often `functools.wraps`, not a wrapper class.
- **One pattern, one problem.** A class implementing three patterns at once is
  a smell, not a showcase.
- **Patterns have costs.** Each one adds indirection: more files, a longer
  stack trace, more to read before the logic appears. If the `switch` has two
  branches that never grow, leave the `switch`.
- **Don't rename for the sake of it.** Adding `Factory`/`Manager`/`Impl`
  suffixes to existing classes is not refactoring.

## Anti-patterns to watch for

- **Singleton as global state** — makes tests order-dependent and hides
  dependencies. Inject the instance instead.
- **Abstract Factory with one implementation** — speculative generality; the
  second implementation may never arrive.
- **Observer without teardown** — unsubscribed listeners are a memory leak and
  a source of events firing after disposal.
- **Deep decorator chains** — four wrappers around one object makes behavior
  impossible to reason about; collapse them.
- **Visitor over a hierarchy that keeps growing** — every new type breaks every
  visitor. Visitor fits stable hierarchies with changing operations, not the
  reverse.
