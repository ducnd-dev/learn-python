"""
Bridge Design Pattern

The Bridge pattern decouples an abstraction from its implementation so that the two can vary independently.
It involves an interface acting as a bridge between the abstract class and implementing classes.

Key components:
1. Abstraction: Defines the abstraction's interface and maintains a reference to the implementor
2. RefinedAbstraction: Extends the abstraction interface
3. Implementor: Defines the interface for implementation classes
4. ConcreteImplementor: Implements the Implementor interface

This pattern is useful when you want to avoid a permanent binding between an abstraction and its implementation,
or when both the abstractions and their implementations should be extensible through subclasses.
"""

from abc import ABC, abstractmethod


# Implementor interface
class DrawingAPI(ABC):
    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        pass
    
    @abstractmethod
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        pass


# Concrete Implementors
class SVGDrawingAPI(DrawingAPI):
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"SVG: Drawing circle at ({x}, {y}) with radius {radius}")
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        print(f"SVG: Drawing rectangle at ({x}, {y}) with width {width} and height {height}")


class CanvasDrawingAPI(DrawingAPI):
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"Canvas: Drawing circle at ({x}, {y}) with radius {radius}")
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        print(f"Canvas: Drawing rectangle at ({x}, {y}) with width {width} and height {height}")


# Abstraction
class Shape(ABC):
    def __init__(self, drawing_api: DrawingAPI):
        self.drawing_api = drawing_api
    
    @abstractmethod
    def draw(self) -> None:
        pass
    
    @abstractmethod
    def resize(self, factor: float) -> None:
        pass


# Refined Abstractions
class Circle(Shape):
    def __init__(self, x: float, y: float, radius: float, drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self) -> None:
        self.drawing_api.draw_circle(self.x, self.y, self.radius)
    
    def resize(self, factor: float) -> None:
        self.radius *= factor
        print(f"Circle resized to radius {self.radius}")


class Rectangle(Shape):
    def __init__(self, x: float, y: float, width: float, height: float, drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self) -> None:
        self.drawing_api.draw_rectangle(self.x, self.y, self.width, self.height)
    
    def resize(self, factor: float) -> None:
        self.width *= factor
        self.height *= factor
        print(f"Rectangle resized to width {self.width} and height {self.height}")


# Extended Refined Abstraction
class ColoredShape(Shape):
    def __init__(self, shape: Shape, color: str):
        super().__init__(shape.drawing_api)
        self.shape = shape
        self.color = color
    
    def draw(self) -> None:
        print(f"Drawing with color {self.color}")
        self.shape.draw()
    
    def resize(self, factor: float) -> None:
        self.shape.resize(factor)


# Example usage
if __name__ == "__main__":
    # Create different implementations
    svg_api = SVGDrawingAPI()
    canvas_api = CanvasDrawingAPI()
    
    # Create shapes with different rendering APIs
    circle1 = Circle(1, 2, 3, svg_api)
    circle2 = Circle(5, 7, 11, canvas_api)
    
    rectangle1 = Rectangle(2, 2, 4, 3, svg_api)
    rectangle2 = Rectangle(1, 3, 5, 7, canvas_api)
    
    # Draw shapes
    print("=== Drawing Shapes ===")
    circle1.draw()
    circle2.draw()
    rectangle1.draw()
    rectangle2.draw()
    
    # Resize shapes
    print("\n=== Resizing Shapes ===")
    circle1.resize(2)
    circle1.draw()
    
    rectangle2.resize(0.5)
    rectangle2.draw()
    
    # Using the extended abstraction
    print("\n=== Using Extended Abstraction ===")
    red_circle = ColoredShape(circle1, "Red")
    red_circle.draw()
    
    blue_rectangle = ColoredShape(rectangle1, "Blue")
    blue_rectangle.draw()
    blue_rectangle.resize(1.5)
    blue_rectangle.draw()