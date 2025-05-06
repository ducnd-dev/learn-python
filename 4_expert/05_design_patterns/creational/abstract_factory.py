"""
Abstract Factory Design Pattern

The Abstract Factory pattern provides an interface for creating families of related
or dependent objects without specifying their concrete classes.

Key components:
1. AbstractFactory: Declares an interface for operations that create abstract products
2. ConcreteFactory: Implements operations to create concrete products
3. AbstractProduct: Declares an interface for a type of product object
4. ConcreteProduct: Defines a product to be created by the corresponding factory
5. Client: Uses only the interfaces declared by AbstractFactory and AbstractProduct

This pattern is useful when a system should be independent of how its products are created,
composed, and represented, and when families of related product objects are designed to be
used together.
"""

from abc import ABC, abstractmethod


# Abstract Products
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def click(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def toggle(self) -> str:
        pass


class TextInput(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def get_value(self) -> str:
        pass
    
    @abstractmethod
    def set_value(self, value: str) -> None:
        pass


# Concrete Products for Light Theme
class LightButton(Button):
    def render(self) -> str:
        return "Rendering a light-themed button"
    
    def click(self) -> str:
        return "Light-themed button clicked"


class LightCheckbox(Checkbox):
    def __init__(self):
        self.checked = False
    
    def render(self) -> str:
        checkbox_state = "☑" if self.checked else "☐"
        return f"Rendering a light-themed checkbox: {checkbox_state}"
    
    def toggle(self) -> str:
        self.checked = not self.checked
        status = "checked" if self.checked else "unchecked"
        return f"Light-themed checkbox {status}"


class LightTextInput(TextInput):
    def __init__(self):
        self.value = ""
    
    def render(self) -> str:
        return f"Rendering a light-themed text input with value: '{self.value}'"
    
    def get_value(self) -> str:
        return self.value
    
    def set_value(self, value: str) -> None:
        self.value = value


# Concrete Products for Dark Theme
class DarkButton(Button):
    def render(self) -> str:
        return "Rendering a dark-themed button"
    
    def click(self) -> str:
        return "Dark-themed button clicked"


class DarkCheckbox(Checkbox):
    def __init__(self):
        self.checked = False
    
    def render(self) -> str:
        checkbox_state = "☑" if self.checked else "☐"
        return f"Rendering a dark-themed checkbox: {checkbox_state}"
    
    def toggle(self) -> str:
        self.checked = not self.checked
        status = "checked" if self.checked else "unchecked"
        return f"Dark-themed checkbox {status}"


class DarkTextInput(TextInput):
    def __init__(self):
        self.value = ""
    
    def render(self) -> str:
        return f"Rendering a dark-themed text input with value: '{self.value}'"
    
    def get_value(self) -> str:
        return self.value
    
    def set_value(self, value: str) -> None:
        self.value = value


# Abstract Factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
    
    @abstractmethod
    def create_text_input(self) -> TextInput:
        pass


# Concrete Factories
class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()
    
    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()
    
    def create_text_input(self) -> TextInput:
        return LightTextInput()


class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()
    
    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()
    
    def create_text_input(self) -> TextInput:
        return DarkTextInput()


# Client
class Application:
    def __init__(self, factory: UIFactory):
        self.factory = factory
        self.button = None
        self.checkbox = None
        self.text_input = None
    
    def create_ui(self) -> None:
        self.button = self.factory.create_button()
        self.checkbox = self.factory.create_checkbox()
        self.text_input = self.factory.create_text_input()
    
    def render_ui(self) -> None:
        if not all([self.button, self.checkbox, self.text_input]):
            raise ValueError("UI components not created yet")
        
        print("\nRendering UI components:")
        print(f"- {self.button.render()}")
        print(f"- {self.checkbox.render()}")
        print(f"- {self.text_input.render()}")
    
    def simulate_user_interaction(self) -> None:
        if not all([self.button, self.checkbox, self.text_input]):
            raise ValueError("UI components not created yet")
        
        print("\nSimulating user interaction:")
        print(f"- {self.button.click()}")
        print(f"- {self.checkbox.toggle()}")
        
        self.text_input.set_value("User input")
        print(f"- Text input updated: {self.text_input.render()}")
        
        print(f"- {self.checkbox.toggle()}")


# Example usage
if __name__ == "__main__":
    # Create application with Light theme
    print("=== Light Theme Application ===")
    light_app = Application(LightThemeFactory())
    light_app.create_ui()
    light_app.render_ui()
    light_app.simulate_user_interaction()
    
    # Create application with Dark theme
    print("\n=== Dark Theme Application ===")
    dark_app = Application(DarkThemeFactory())
    dark_app.create_ui()
    dark_app.render_ui()
    dark_app.simulate_user_interaction()