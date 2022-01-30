Notes on [Applying UML and patterns book](https://www.amazon.com/Applying-UML-Patterns-Introduction-Object-Oriented/dp/0131489062/ref=sr_1_1?crid=RM5TPA4Z5G8G&dchild=1&keywords=applying+uml+and+patterns&qid=1631197141&s=books&sprefix=applying+u%2Cstripbooks%2C437&sr=1-1)

## UP - Iterative and evolutionary development

### Phases

### Inception
Feasibility phase, determine whether to continue with deeper exploration of the project.

1. Identify most requirements
2. Detailed analysis of 10% use cases (risk-driven and client-driven)
3. Analysis of critical non-functional requirements

### Elaboration
Most requirements are analysed in detail, using a risk-driven and client-driven
selection to implement the most significant ones (10%-20%) iteratively

### Construction
Iterative implementation of lower risk remaining elements. 

### Transition
Deployment



## Evolutionary Requirements

Find, communicate and document what is really needed, in a form that clearly communicates
both to the client development team.

**Caution**: Requirements are done iteratively, we don't have to define 100% of the requirements
before starting to program! Roughly 25%-50% of the requirements change on average, so we start
by fully analysing the most valuable ones, and start programming before all requirements are 
completed.

### Use Cases

Use Cases are **text** (not diagrams) stories widely used to discover and record requirements. 
They will be input to many subsequent activities in analysis/design.

The essence is **discovering** and **recording** functional requirements by writing **stories**
of using a system to fulfill **user goals**

Some guidelines:
* Use a black-box style: write responsibilities, not implementations
* Use and essential UI-free style
* Keep it terse
* Use an actor and actor-goal perspective


Further reading: 
* *Applying UML and patterns*
* *Writing Effective Use Cases*



## Analysis and Design
Do the right thing (analysis) and do the thing right (design)

Analysis refers to the problem-definition, understanding the problem while
design involves coming up with possible solutions.

**OOA/D**
Object-Oriented Analysis and Design refers to modeling domain concepts and then
mapping those concepts into software objects with responsibilities and collaborators.


### Domain Model
Illustrate noteworthy (real-situation, not software) concepts in a domain, acting as a source 
of inspiration for designing software objects (supporting LRG)

Further reading: 
* *Applying UML and patterns*


### System Sequence Diagrams
Use cases illustrate how an actor interacts with the SUD. During this interaction an actor
generates **system events**. SSDs show, for one particular *scenario* of a use case, the events
that external actors generate, their order and inter-system events.

> They illustrate the starting messages entering the domain-layer Controllers when 
> designing Use Case Realizations 

Use Case text and its implied system events are input to SSDs, which in turn serve as the starting
point to designing collaborating objects.

Why draw SSDs? It's useful to understand at a high-level what events the system must respond to,
and define the behavior of the system as a black-box to those events.


## Object design

> A critical design tool for software development is a mind well educated in design principles

We have two types of object models: 

* **dynamic models** help us design the logic and behavior. They include sequence,
communication, activity and state diagrams.
* **static models** help to define packages, classes, attributes and method signatures. 

> Dynamic diagrams are the **most useful**, interesting and difficult diagrams to create. 
> During dynamic modelling we apply all the famous GRASP, SOLID and the-like patters/guidelines.
> It's when we have to think through the concrete details of what messages to send, to whom,
> and in what order, that we get a deeper understanding.

Both models should be created in *parallel*: needed behavior and attributes discovered in 
dynamic models can be reflected in static ones.

Some decision-making and creative work will be done during design. However, in general, 
programming is not a trivial code-generation step. Done well, *ideas* and *understanding*
will be the main outcomes of design, not diagrams and documents. Expect lots of change and
deviation during programming.

### Responsibility driven design

A popular way of thinking about design is in terms of **responsibilities, roles and collaborations**.
We think of objects as having **responsibilities**: an abstraction of what they do, in terms of their 
**role**. Objects may **collaborate** with other objects.

The translation of responsibilities into classes and methods will depend on the size of the
responsibility: big ones may take hundreds of classes, while small ones make take a simple method.

### GRASP

GRASP is a set of principles to help with responsibility assignment. The name was chosen to
suggest the importance of *grasping* these principles to successfully design object-oriented
software.

> Start assigning responsibilities by clearly stating the responsibility

#### Protected Variations
*Problem:* How to design objects, systems and subsystems so that variations and/or instability
in those does not an undesirable impact on other elements?

*Solution:* Identify points of possible variations/instability and assign responsibilities to 
a stable interface around them. Therefore, internal objects collaborate with a stable interface
and changes are hidden behind the implementations.

> PV is a root principle motivating most of the mechanisms and patterns in programming and
> design to provide flexibility and protection from variation. 

#### Information Expert
*Problem:* What is a general principle of assigning responsibilities to objects? Well assigned
responsibilities lead to a system easier to understand, maintain, extend and reuse.

*Solution:* Assign the responsibility to the information expert, the class with all the info
to fulfill the responsibility.

**Where** do we look for classes that might have the information needed? 
1. If the Design Model has relevant info, look there
2. Else use (or expand) the Domain Model to inspire the creation of the corresponding design
classes

*Contraindications* When **high-cohesion** and/or **low-coupling** are affected, consider
other alternatives such us **pure fabrication**.

When information is distributed among multiple objects, consider the following guidelines:
* Prefer the object with the most information 
* If information is distributed evenly, consider high cohesion and low coupling among the
different alternatives
* Consider future possible evolution: knowledge of future requirements might favor one alternative

#### Low Coupling
*Coupling* is a measure of dependency. A highly coupled element (class | system | module) has many 
dependencies with other elements (class | system | module). 

It is a **general principle** to keep in mind in every design decision. 

Highly-coupled elements have more chance of suffering from these drawbacks:
* Harder to change: a change in element A may ripple across several other dependant elements
* Harder to understand: to understand element A one must also understand how it plays together with
its dependencies
* Harder to reuse: element A needs a bunch of other elements to operate, so it can't be re-used in
isolation.

*Problem:* How to support low change impact, easier understanding and increased re-use?

*Solution:* Assign responsibility so that coupling remains low. Between different design alternatives
favor the ones with lower coupling.

It is not high-coupling per-se that brings problems, but the coupling to unstable elements. Pick
your battles and aim for low coupling in those elements that are expected to be unstable in
some dimension (implementation, interface, etc.)


#### High Cohesion
*Cohesion* is a measure of how focused and related the responsibilities of a class are. A class
with low cohesion has too many (and/or to unrelated) responsibilities, suffering from the
following problems:
* Harder to understand and maintain
* Harder to reuse
* Susceptible to changes

*Problem:* How to keep objects focused and understandable? 

*Solution:* Assign responsibilities so that cohesion remains high: the responsibilities of an
object should be strongly related. 

Like *low coupling*, high cohesion is a general principle to keep in mind for every design
decision and to choose among design options.

#### Controller
*Problem:* Which objects should handle system operations? 

*Solution:* Assign the responsibility to a class using one of the following choices:
1. *Facade controller* (Facade onto the domain layer):
   1. Represents the overall system
   2. Represents the device the software is running within
2. Represents a *use case scenario* within which the system events occur. Often the same
<UseCaseName>Handler will be used for all scenarios within the same Use Case, so that information
about the state of the Use Case could be kept if needed.

Controllers are mostly coordinators, they delegate the work to the domain objects.

Facade controllers are more suitable when there aren't too many system operations. Otherwise,
the UseCaseHandlers might be more appropriate too support low coupling and high cohesion.  

#### Creator
*Problem:* Who should be responsible to create a new class instance?

*Solution:* Object C should create object O if:
* C contains or compositely aggregates O
* C closely uses O
* C has all (or most) needed data to create O
* C records O

If creation has complex logic, usually factories are used instead to support *low coupling* and
*high cohesion*

#### Pure Fabrication
*Problem:* How to assign responsibilities when following *Expert* leads to low-cohesion and/or
high-coupling? 

*Solution:* Assign the responsibilities to an artificial class (a class that does not represent
a concept from the domain) to support high-cohesion, low-coupling and reuse.

#### Indirection
*Problem:* How to assign responsibilities without a direct coupling between two (or more)
objects?

*Solution:* Assign the responsibility to an intermediate object that mediates between them. The
intermediary creates an indirection between the two of them, providing low-coupling.

#### Polymorphism
*Problem:* How to handle alternatives based on type? How to design pluggable components?

*Solution:* When related alternatives or behaviors vary by type, use polymorphic operations

## UML


## Glossary

UML
: Unified Modeling Language

LRG
: Low Representational Gap 

SUD
: System Under Discussion

GRASP
: General Responsibility Assignment Software Patterns