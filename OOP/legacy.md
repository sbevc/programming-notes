# Notes from  [Working effectively with legacy code](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052/ref=sr_1_1?crid=XIDFYHMIK28D&keywords=working+effectively+with+legacy+code&qid=1639056960&s=books&sprefix=working+effec%2Cstripbooks%2C499&sr=1-1)


## I don't have much time and I have to change it

Use with caution: we are adding tested code into the system, but unless we cover
the calling code, we aren't testing its use.

Example old code
```python
# Old code
class Employee:
    def __init__(self, pay_rate, time_cards):
        self.pay_rate = pay_rate
        self.time_cards = time_cards
        
    def pay(self, pay_dispatcher):
        amount = [tc.hours * self.pay_rate for tc in self.time_cards]
        pay_dispatcher.pay(amount)
    
```

In the following examples a new requirement comes in to log employee payments


#### Sprout Method
When adding new functionality, add the new code in a new method (instead of changing
old methods) and then call it where needed. We might not be able to test those calling
points, but at least we can test the new method.

If the class/function has many dependencies making it difficult to test, consider
adding the new code in a static method or plain function, and passing the instance
as an argument.

Example
```python
class Employee:
    ...
    def pay(self, pay_dispatcher):
        amount = [tc.hours * self.pay_rate for tc in self.time_cards]
        pay_dispatcher.pay(amount)
        self.log_payment(amount)
        
    def log_payment(self, amount):
        print(f"Payed {self}: ${amount}")
```

#### Sprout Class
Similar to Sprout Method, we create the new functionality in a new place (a class this time).

Essentially  two cases lead to Sprout Class:
1. We are adding an entirely new responsibility that doesn't belong to the previous class
2. The original class has to many dependencies to get it under test (making
it very difficult to instantiate and therefore test the new method). 

Example:
```python
class Employee:
    def __init__(self, dep1, dep2, dep3, ..., depn): ...
    
    def pay(self, pay_dispatcher):
        amount = [tc.hours * self.pay_rate for tc in self.time_cards]
        pay_dispatcher.pay(amount)
        EmployeePaymentLogger(self).log_payment(amount)

class EmployeePaymentLogger:
    def __init__(self, employee):
        self.employee = employee

    def log_payment(self, amount):
        print(f"Payed {self.employee}: ${amount}")
```


#### Wrap Method
Although adding behaviour to methods its easy, that's often not the best choice: the new code
might represent an entirely different responsibility. Chances are we are touching old methods
just because we need the new functionality to happen at the same time leading to *temporal coupling*.

Example
```python
class Employee:
    # Old pay method is moved to this one, which is wrapped by pay, keeping the same interface
    # to not disrupt callers.
    def _dispatch_payment(self, pay_dispatcher):
        amount = [tc.hours * self.pay_rate for tc in self.time_cards]
        pay_dispatcher.pay(amount)
        
    # Wrap old pay method, calling the old code plus our new log_payment
    def pay(self, pay_dispatcher):
        self._dispatch_payment(pay_dispatcher)
        self._log_payment()

    def _log_payment(self): ...
```


#### Wrap Class
Similar to wrap class and also known as the **Decorator Pattern**, we add the new behaviour into
a new class which wraps the old class.

Generally two situations lead  to Wrap Class:
1. The new functionality is totally unrelated: a new responsibility
2. The old class is already huge and in-cohesive, and we don't want to make it worse

Example
```python
class LoggedEmployee:
    def __init__(self, employee):
        self.employee = employee

    def pay(self, pay_dispatcher):
        amount = self.employee.pay(pay_dispatcher)
        # Log payment here ...
```

##### Summary:

| Name          | Advantages                                                                                           | Disadvantages                                                                                                       |
|---------------|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Sprout Method | 1. We are separating new code from old code 2. The new code can be tested                            | 1. The original class is not getting any better 2. We aren't adding tests to cover original functionality           |
| Sprout Class  | 1. Separate new code from old code 2. The new class should be easily tested                          | 1. Things that ideally should be in one class end up scattered into multiple ones just to make safe change possible |
| Wrap Method   | 1. We don't add any lines to the old method 2. The the functionality is independent from the old one | 1. We have to rename the wrapped method which can lead to poor names                                                |