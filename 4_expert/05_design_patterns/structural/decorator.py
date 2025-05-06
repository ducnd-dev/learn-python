"""
Decorator Design Pattern

The Decorator pattern allows behavior to be added to individual objects, 
either statically or dynamically, without affecting the behavior of other objects from the same class.
"""
from abc import ABC, abstractmethod


# Component Interface
class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass


# Concrete Component
class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponent"


# Base Decorator
class Decorator(Component):
    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self) -> str:
        return self._component.operation()


# Concrete Decorators
class ConcreteDecoratorA(Decorator):
    def operation(self) -> str:
        return f"ConcreteDecoratorA({self.component.operation()})"


class ConcreteDecoratorB(Decorator):
    def operation(self) -> str:
        return f"ConcreteDecoratorB({self.component.operation()})"


# Example usage
if __name__ == "__main__":
    # Create a simple component
    simple = ConcreteComponent()
    print(f"Client: I've got a simple component:")
    print(f"Result: {simple.operation()}", end="\n\n")

    # Decorate the component with Decorator A
    decorator1 = ConcreteDecoratorA(simple)
    # Decorate the component with Decorator B using Decorator A as base
    decorator2 = ConcreteDecoratorB(decorator1)
    print(f"Client: Now I've got a decorated component:")
    print(f"Result: {decorator2.operation()}")