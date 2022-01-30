## Abstraction

An abstraction focuses on the outside view of an object and so serves to separate an 
object’s essential behavior from its implementation. 

Deciding on the right set of abstractions for a given domain is the central 
problem in object-oriented design.

## SRP - Single Responsibility Principle
Each class should only have a single responsibility, or, better put, a class should have
only one reason to change.

If we put SQL statements in a view that contains HTML markup, we’d all quickly agree that
changes to the markup will happen at different times, at different rates, and for different
reasons than changes to SQL statements. Our SQL statements change when we’re changing our
data model or need to do performance tuning. Our markup, on the other hand, changes when
we need to change the look and feel of the web application. These are different concerns
that change for different reasons. Putting SQL statements directly into a view is, therefore,
an SRP violation.

More often than not, however, it can be more challenging to see whether a class has multiple
reasons to change. What often helps is to look at the SRP from the perspective of code
cohesion: the lower the relatedness, the lower the cohesion, and the higher the risk a class
violates the SRP.

Being able to detect SRP violations is one thing, but determining whether a violation should
be fixed is yet another. It isn’t wise to apply the SRP if there are no symptoms. 
Needlessly splitting up classes that cause no maintainability problems can add extra complexity.
The trick in software design is to manage complexity.