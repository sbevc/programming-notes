# Dependency Injection

Notes taken
from [book](https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_stripbooks_sr_pg1_1?ie=UTF8&adId=A02738679T215RLHBK7D&url=%2FDependency-Injection-Principles-Practices-Patterns%2Fdp%2F161729473X%2Fref%3Dsr_1_1_sspa%3Fcrid%3DXHDMN7N6RQ24%26dchild%3D1%26keywords%3Ddependency%2Binjection%26qid%3D1631200257%26s%3Dbooks%26sprefix%3Ddependency.%2B%252Cstripbooks%252C130%26sr%3D1-1-spons%26psc%3D1&qualifier=1631200257&id=3977972627987957&widgetName=sp_atf)

# Intro


## What is DI?

DI is nothing more than a collection of design principles and patterns. It’s more about
a way of thinking and designing code than it is about tools and techniques. The purpose 
of DI is to make code maintainable. Small code bases, like a classic Hello World example,
are inherently maintainable because of their size. This is why DI tends to look like 
over-engineering in simple examples. The larger the code base becomes, the more visible the 
benefits.

> Dependency injection is a set of **software design principles and patterns** that
> help produce loosely-coupled systems.

> Loose coupling is a pervasive design principle, so DI (as an enabler) should be everywhere
> in your code base.

> DI must be pervasive. You can’t easily retrofit loose coupling onto an existing code base.

### Myths

1. DI is _only_ relevant for late binding

   Late binding means being able to replace parts of an application without recompiling the code. Its true that DI *
   enables* late binding, but there is much more to it.

2. DI is _only_ relevant for unit testing

   Analogous to late binding, although DI makes writing tests easier, there is much more to it

3. DI is an Abstract Factory on steroids

   Abstract Factory on steroids means a mechanism to get dependencies by name, which is considered and anti-pattern by
   DI. For example:

```python
def get_service(name):
    return all_services[name]
```

   **DI is the opposite** of this: dependencies have to be provided by a consumer.


## Purpose - Why DI?

DI helps us write **maintainable code** by empowering **loosely-coupled** code. Loosely-coupled code is easy-to-extend
code, which eases its maintenance.

> Program to an interface, not an implementation.

#### An analogy with electrical wiring

In many ways software design and patterns resembles electrical wiring.

We don't just attach one wire to the other in order to get electricity. Instead, we use plugs and sockets. As long as
the plug (the implementation) fits into the socket
(implements the interface), and it can handle the amount of volts and hertz (obeys the interface contract), we can
combine appliances in a variety of ways. What’s particularly interesting is that many of these common combinations can
be compared to well-known software design principles and patterns.

Highly-coupled systems resemble manually wiring: it makes it hard to replace components, and doing so may affect either
of the wires.

On the contrary, loosely-coupled systems resemble the socket-plug analogy: It's easy to insert new components (plugs) as
long as they fit the socket (interface)

Patterns analogies:

1. Decorator pattern: intercept one implementation with another resembles plugging a UPS in between the socket and plug
   to get extended functionality
2. Composite pattern: we can aggregate several implementations into one, resembling plugging diverse appliances into a
   power strip
3. Adapter pattern: we can adapt a 3rd-party api to a friendlier interface for our application, resembling plug
   adapters.

The advantage of loose coupling is the same in software design as it is in the physical socket and plug model: Once the
infrastructure is in place, it can be used by anyone and adapted to changing needs and unforeseen requirements without
requiring large changes to the application code base and infrastructure. This means that ideally, a new requirement
should only necessitate the addition of a new class, with no changes to other already-existing classes of the system.
This concept of being able to extend an application without modifying existing code is called the
**Open/Closed Principle**.

### Benefits

Let's consider a simple hello world example

```python
# Using DI
import typing

class Writer(typing.Protocol):
    def write(self, msg):
        raise NotImplementedError


class ConsoleWriter:
    def write(self, msg):
       print(msg)
        

def say_hello(writer: Writer):
   writer.write("Hello DI!")
   

writer = ConsoleWriter()
say_hello(writer)


# Not using DI
print("Hello DI!")
```

#### Extensibility
Successful software must be extended in possible unpredicted ways at the time of
its creation. Loosely-coupled code makes this task easier. 

Let's say a new requirement comes that only authenticated users should be able to write.
With the DI example it could be done without modifying the existing code

```python
class SecureWriter:
    def __init__(self, user, writer: Writer=None):
        self.user = user
        self.writer = writer or ConsoleWriter()
    
    def write(self, msg: str):
        if not self.user.is_authenticated:
            raise RuntimeError(f"User {self.user} can't write!")
        self.writer.write(msg)

user = input("Your username: ")
writer = AuthWriter(user)
say_hello(writer)
```

Note that the `say_hello` function remains unchanged because it depends on the Writer
abstraction. Loose coupling enables you to write code that’s 
**open for extensibility, but closed for modification**

#### Parallel development
Multiple teams working on interdependent features need just to agree on the interfaces.
They can program to an interface assuming the other teams' implementations are already there

#### Unit Testing
An application is considered **testable** if it can be unit tested. For code to be
unit-testable it must be possible to isolate it from its dependencies

> Almost by accident, loose coupling enables unit testing because consumers follow
> the Liskov Substitution Principle: they don’t care about the concrete types of 
> their Dependencies. This means that you can inject Test Doubles into the 
> System Under Test (SUT)

Test Doubles
It’s a common technique to create implementations of Dependencies that act as stand-ins
for real or intended implementations. Such implementations are called Test Doubles,
and they’ll never be used in the final application. Instead, they serve as placeholders
for real Dependencies when these are unavailable or undesirable to use.
A Test Double is useful when the real dependency is slow, expensive, destructive, or 
simply outside the scope of the current test. There’s a complete pattern language around
Test Doubles and many subtypes, such as Stubs, Mocks, and Fakes.

We could unit-test the `say_hello` function as the following
```python
class FakeWriter:   
   def write(self, msg):
      self.written_msg = msg
       
       
def test_say_hello():
    writer = FakeWriter()
    say_hello(writer)
    assert writer.written_msg == "Hello DI!"
```

#### Late Binding
Because the say_hello depends on an interface, *Writer*, late binding could be used to
determine the specific Writer implementation at runtime. As long as the plug conforms
to the socket, we can use any Writer

```python
import importlib
import conf

writer_cls = importlib.import_module(conf.WRITER)
say_hello(writer_cls())
```

**Conclusion**
Loose coupling provides many benefits: 
* code becomes easier to develop, maintain, and extend
* code becomes more Testable. 

It’s not even particularly difficult. We program against interfaces, not concrete
implementations. The only obstacle is to figure out how to get hold of instances 
of those interfaces. DI surmounts this obstacle by injecting the Dependencies from
the outside (the caller). 

## When? When to inject and not to

Categorizing dependencies into *stable* and *volatile* helps to decide when to apply
DI: **use it with the volatile dependencies**.

It is a matter of deciding where to put the **seams**. As in clothing, a seam in
code assembles together different components,  similar to the way a piece of clothing
is sewn together at its seams. **Everywhere you decide to program against an Abstraction
instead of a concrete type, you introduce a seam into the application.**

### Stable dependencies
In general stable dependencies are considered by exclusion: they are stable if they
aren't volatile. However, the following might be considered stable in most occasions:
* Standard library dependencies in general
* New versions are expected to be backward-compatible
* Deterministic algorithms
* You never expect to have to replace, wrap, decorate, or Intercept the class or
module with another.

### Volatile dependencies
These typically interfere with one or more benefices of loose coupling. A dependency can be
considered volatile if any of these criteria is true:
* **Needs a runtime environment** for it to work. The typical case are _databases_. If we
don't build a seam around them, later on is impossible to make changes and  drastically
affects testability. The filesystem and external API calls also fall into this category.
* **Is in development or doesn't yet exist**
* **Contains non-deterministic behavior** for example random numbers or the current
datetime

## DI in three dimensions

### Object Composition
Object Composition is moved away from the class to the caller; instead of a class
creating its dependencies, it moves this responsibility up to the caller adding flexibility
for future use-cases and testing.

### Object Lifetime
A class that has surrendered control of its dependencies gives up more than the power
to select particular implementations of an Abstraction. It also gives up the power to
control when instances are created and when they go out of scope.

TODO: Future ch-8 notes

### Interception
Related to composition, you can intercept dependencies to enhance them before
passing them into their consumers as with the `SecureWriter` example.


## DI Patterns

### Composition Root
*Problem:* Where should we create the objects?

*Solution:* As close as possible to the application entry point. 

DI pushes instance creation as close as possible to the entry point, where they are created
by a *COMPOSITION ROOT*. 

> If using a *DI CONTAINER* the composition root should be the only
> place where the container is used! If not we are leaning towards the *SERVICE LOCATOR* 
> anti-pattern. Also, moving the composition of classes out of the Composition Root leads
> to either the Control Freak or Service Locator anti-patterns

### Constructor Injection
One way to supply dependencies is when constructing the instances.

A possible disadvantage is that some frameworks don't provide hooks to customize instance
creation, they create your classes assuming they'll have no construction dependencies.

### Method Injection
Supply dependencies in method calls.

Useful for:
1. Methods of domain entities that require some out-of-domain infrastructure. Instead of coupling
to the outside world, we program against an interface. Supplying it in a method call is better than
at construction time because that dependency most probably will be needed only in that method.
2. When the dependency varies with each call

## DI Anti-patterns
Anti-patterns are, more or less, a formalized way of describing common mistakes that
people make again and again.

### Control Freak
The Control Freak anti-pattern is the antithesis of DI. It occurs every time you 
**create a Volatile Dependency outside the Composition Root**. It’s a violation of the
Dependency Inversion Principle and looses all the benefits from loosely-coupled code.

It's difficult to get outside the control freak mindset because is the *normal*
way to instantiate classes: a class just instantiates its dependencies.

Gross example:
```python
# Control Freak
class Product:
    def __init__(self):
        self.memstore = Redis()  # Product couples itself with Redis volatile dependency

# Using DI
class Product:
    def __init__(self, memstore: MemoryStore):  # Depend on an abstraction
        self.memstore = memstore
```

More subtle variations:
```python
# Hardcode the volatile dependency in a method outside the init
class Product:
    def __init__(self, memstore: MemoryStore):
        self.memstore = memstore

    def initialize(self):
        # Same as before, directly initialize volatile dependency but outside the init.
        # you don’t gain much by defining a variable as an Abstraction if you hard-code
        # it to always have a specific concrete type. Directly newing up Dependencies 
        # is one example of the Control Freak anti-pattern. 
        self.memstore = Redis()

# Initialize the dependency through factories. The tight-coupling to a volatile dependency
# is still there, moved up on level of indirection.
def memstore_factory():
   return Redis()


class Product:
    def __init__(self):
        self.memstore = memstore_factory()


# Provide a local default. Although the dependency is still configurable, we loose the
# ability to intercept it
class Product:
    def __init__(self, memstore: MemoryStore = None):
        self.memstore = memstore or Redis()
```

### Service Locator
The service locator anti-pattern provides a way to globally request dependencies

```python
def service_locator(name):
    return all_services[name]

class Product:
    def __init__(self):
        self.memstore = service_locator("memstore")
```

The downsides to this anti-pattern are:
1. Classes loose re-usability as we have to drag along the service locator with them
2. Classes have hidden dependencies. The whole dependency graph is available through the
service locator, being temping to just couple the class to whatever service is available

> Querying for DePenDencies, even if through a Di contAiner, becomes a service LocAtor 
> if used incorrectly. When application code (as opposed to infrastructure code) actively 
> queries a service in order to be provided with required DePenDencies, then it has become 
> a service Locator.


### Ambient context
Similar to service locator anti-pattern, but jus expose a single global dependency. For example:


```python
# logging example
import logging

logger = logging.getLogger(__name__)

def my_func():
    logger.info("I'm doing something useful")

# datetime example
import datetime as dt

def my_func():
    print(f"Now is: {dt.datetime.now()}")
```

The ambient context disadvantages include:
1. The dependency is hidden
2. Testing becomes more difficult
3. It's hard to change the dependency based on context

## Code Smells
In this chapter, we’ll look at the most common code smells that appear when you apply 
DI to a code base and how you can resolve them. 

### Constructor over-injection
This happens when a class takes too many dependencies, for example:
```python
class OrderService:
    def __init__(
        self,
        order_repository: IOrderRepository,
        message_service: IMessageService,
        billing_system: IBillingSystem,
        location_service: IlocationService,
        inventory_manager: IInventoryManagement
    ):
        self.order_repository = order_repository
        self.message_service = message_service
        self.billing_system = billing_system
        self.location_service = location_service
        self.inventory_manager = inventory_manager

    def approve_order(self, order):
        self.update_order(order)
        self.notify(order)

    def update_order(self, order):
       order.approve()
       self.order_repository.save(order)

    def notify(self, order):
        self.message_service.send_receipt(order)
        self.billing_system.notify_accounting(order)
        self.fulfill(order)

    def fulfill(self, order):
        wh = self.location_service.find_wharehouse(order)
        self.inventory_manager.notify_wharehouse(wh)
```

Having many dependencies probably means that we are violating the SRP, which leads to code
that is harder to maintain.

Although constructor over-injection seems to be caused by DI, that is not the case. DI magnifies
this issue, it makes it visible for us (if not using DI, we would still have all those dependencies
in an indirect fashion.) It is a good thing that DI makes this problem stand out: we can recognize it
and search for solutions.

> Constructor Injection makes it easy to spot SRP violations. Instead of feeling uneasy about
> Constructor Over-injection, you should embrace it as a fortunate side effect of 
> Constructor Injection. It’s a signal that alerts you when a class takes on too much
> responsibility.

How to refactor a class/function with too many responsibilities depends on the specific
application

We have 2 common approaches to solve this problem: 
1. Facade services
2. Domain Events

#### Facade Services
A Facade Service hides a natural cluster of interacting Dependencies, 
along with their behavior, behind a single Abstraction.

When a class is taking too many dependencies we can search for clusters of interactions
within the dependencies. There may be a subset of dependencies that only interact with
each other and can be refactored into a facade service. 

Following on the example we see that `location_service` and `inventory_manager` only
interact with each other. An abstraction might be missing here, in fact, we could introduce
an IOrderFulfillment abstraction to take this responsibility, reducing the depencies from 
5 to 4:
```python
class OrderService:
    def __init__(
        self,
        order_repository: IOrderRepository,
        message_service: IMessageService,
        billing_system: IBillingSystem,
        order_fulfillment: IOrderFulfillment,
        # location_service: IlocationService,
        # inventory_manager: IInventoryManagement
    ):
        ...
    def fulfill(self, order):
        self.order_fulfillment.fulfill(order)
```

Another abstraction that we are missing is the notification. We can decouple the OrderService
class from the notifications by creating an abstraction IOrderNotification:

```python
import typing


class INotificationService(typing.Protocol):
    def order_approved(self, order) -> None: ...


class OrderService:
    def __init__(self, order_repository: IOrderRepository, notification_service: INotificationService):
        self.order_repository = order_repository
        self.notification_service = notification_service

    def approve_order(self, order):
        self.update_order(order)
        self.notification_service.order_approved(order)

    def update_order(self, order):
        order.approve()
        self.order_repository.save(order)
```

Combining this change with the *Composite pattern* for multiple notifications:
```python
# define composite notifications
class CompositeNotificationService:
    def __init__(self, services: list[INotificationService]):
        self.services = services

    def order_approved(self, order):
        for service in self.services:
            service.order_appoved(order)


# Composite root
order_service = OrderService(
   order_repository=DjangoOrderRepository(),
   notification_service=CompositeNotificationService([
      OrderApprovedReceiptSender(MessageService()),
      AccountingNotifier(BillingSystem()),
      OrderFullfilment(LocationService(), InventoryManagement()),  
   ])
)
```

Now the OrderService was greatly simplified by finding missing abstractions. DI just made
this evident with construction over-injection.




## Glossary

#### Service

In DI terminology, we often talk about services and components. A service is typically an Abstraction, a definition for
something that provides a service. An implementation of an Abstraction is often called a component, a class that
contains behavior. Because both service and component are such overloaded terms, throughout this book, you’ll typically
see us use the terms “Abstraction” and “class” instead.

#### Seam
A seam is a place where an application is assembled from its constituent parts,
similar to the way a piece of clothing is sewn together at its seams


#### Object Composition
The task of creating concrete instances of dependencies


#### Cross cutting concerns
Aspects that aren't directly related to a feature but rather relate to many areas. For
example logging, performance, security, etc. When you draw diagrams of layered 
application architecture, Cross-Cutting Concerns are often represented as vertical 
blocks placed beside the layers. 