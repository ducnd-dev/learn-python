'''
Advanced OOP cho JavaScript Developers
======================================

Python hỗ trợ nhiều tính năng hướng đối tượng nâng cao mà JavaScript không có hoặc
triển khai khác. Hãy tìm hiểu các khái niệm OOP nâng cao trong Python.
'''

# =========== INHERITANCE (KẾ THỪA) ===========
print("=== Inheritance Patterns in Python ===")

# Single Inheritance (Kế thừa đơn)
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Some generic animal sound"

class Dog(Animal):  # Dog kế thừa từ Animal
    def speak(self):  # Ghi đè (override) phương thức speak
        return "Woof!"

# Multi-level Inheritance (Kế thừa nhiều cấp)
class Labrador(Dog):  # Labrador kế thừa từ Dog
    def speak(self):
        return super().speak() + " Loudly!"  # Gọi phương thức của lớp cha
    
    def fetch(self):
        return f"{self.name} is fetching the ball!"

# Multiple Inheritance (Kế thừa đa lớp)
class Swimmer:
    def swim(self):
        return "Swimming..."
    
    def speak(self):
        return "Splash!"

class FlyingDog(Dog, Swimmer):  # Kế thừa từ cả Dog và Swimmer
    def fly(self):
        return "Flying high!"

# Kiểm tra kế thừa
animal = Animal("Generic Animal")
dog = Dog("Buddy")
lab = Labrador("Max")
flying_dog = FlyingDog("SuperDog")

print(f"Animal: {animal.name}, Sound: {animal.speak()}")
print(f"Dog: {dog.name}, Sound: {dog.speak()}")
print(f"Lab: {lab.name}, Sound: {lab.speak()}, Action: {lab.fetch()}")
print(f"FlyingDog: {flying_dog.name}, Sound: {flying_dog.speak()}, Action: {flying_dog.fly()}, Also: {flying_dog.swim()}")

# Method Resolution Order (MRO) - Thứ tự giải quyết phương thức
print("\nMethod Resolution Order (MRO):")
print(f"MRO for FlyingDog: {[cls.__name__ for cls in FlyingDog.__mro__]}")
print("Python uses C3 Linearization algorithm for MRO")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// JavaScript chỉ hỗ trợ kế thừa đơn thông qua prototype
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    return "Some generic animal sound";
  }
}

class Dog extends Animal {
  speak() {
    return "Woof!";
  }
}

// Mô phỏng kế thừa đa lớp trong JavaScript là phức tạp hơn
// và thường được thực hiện bằng mixins hoặc composition
""")

# =========== ABSTRACT CLASSES & INTERFACES ===========
print("\n=== Abstract Classes and Interfaces ===")

from abc import ABC, abstractmethod

# Abstract class
class Shape(ABC):  # Kế thừa từ ABC (Abstract Base Class)
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    def describe(self):
        return f"This shape has area {self.area()} and perimeter {self.perimeter()}"

# Concrete classes
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius * self.radius
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Không thể khởi tạo một abstract class
try:
    shape = Shape()
except TypeError as e:
    print(f"Cannot instantiate abstract class: {e}")

# Sử dụng các concrete classes
circle = Circle(5)
rectangle = Rectangle(4, 6)

print(f"Circle - Area: {circle.area()}, Perimeter: {circle.perimeter()}")
print(f"Rectangle - Area: {rectangle.area()}, Perimeter: {rectangle.perimeter()}")
print(f"Circle description: {circle.describe()}")

# Protocol class (từ Python 3.8+) - Informal interfaces
try:
    from typing import Protocol, runtime_checkable
    
    @runtime_checkable
    class Drawable(Protocol):
        def draw(self) -> str:
            ...  # Ellipsis indicates abstract method
    
    class Canvas:
        def draw(self) -> str:
            return "Drawing on canvas"
    
    class Button:
        def draw(self) -> str:
            return "Drawing button"
        
        def click(self):
            return "Button clicked"
    
    # Check nếu class tuân thủ protocol
    print("\nProtocol checks:")
    print(f"Is Canvas drawable? {isinstance(Canvas(), Drawable)}")
    print(f"Is Button drawable? {isinstance(Button(), Drawable)}")
    
except ImportError:
    print("\nProtocol class requires Python 3.8 or newer")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// JavaScript không có built-in abstract classes, 
// nhưng có thể mô phỏng hành vi tương tự:

class Shape {
  constructor() {
    if (this.constructor === Shape) {
      throw new TypeError("Cannot instantiate abstract class");
    }
  }
  
  area() {
    throw new Error("Method 'area' must be implemented");
  }
  
  perimeter() {
    throw new Error("Method 'perimeter' must be implemented");
  }
}

// TypeScript cung cấp interfaces và abstract classes:
// abstract class Shape {
//   abstract area(): number;
//   abstract perimeter(): number;
// }
""")

# =========== CLASS COMPOSITION ===========
print("\n=== Class Composition ===")

# Ví dụ Composition
class Engine:
    def __init__(self, power):
        self.power = power
    
    def start(self):
        return f"Engine with {self.power}hp starting..."

class Wheels:
    def __init__(self, count):
        self.count = count
    
    def rotate(self):
        return f"{self.count} wheels rotating"

# Car sử dụng composition thay vì kế thừa
class Car:
    def __init__(self, engine_power, wheel_count):
        self.engine = Engine(engine_power)  # Composition
        self.wheels = Wheels(wheel_count)   # Composition
    
    def start_drive(self):
        return f"{self.engine.start()} and {self.wheels.rotate()}"

# Sử dụng composition
car = Car(150, 4)
print(f"Car starting: {car.start_drive()}")

# Dependency Injection - Một dạng composition
class ElectricEngine:
    def __init__(self, power):
        self.power = power
    
    def start(self):
        return f"Electric engine with {self.power}kW humming..."

# Car với dependency injection
class ModernCar:
    def __init__(self, engine, wheels):
        self.engine = engine    # Inject engine
        self.wheels = wheels    # Inject wheels
    
    def start_drive(self):
        return f"{self.engine.start()} and {self.wheels.rotate()}"

# Tạo các dependencies riêng biệt
electric_engine = ElectricEngine(100)
luxury_wheels = Wheels(4)

# Inject vào constructor
tesla = ModernCar(electric_engine, luxury_wheels)
print(f"Tesla starting: {tesla.start_drive()}")

print("\nComposition over Inheritance principle:")
print("- Kết hợp hành vi từ nhiều class mà không cần kế thừa đa lớp phức tạp")
print("- Tách biệt các khía cạnh riêng biệt của một hệ thống")
print("- Dễ dàng thay đổi hoặc mở rộng từng thành phần")
print("- 'Has-a' relationship thay vì 'is-a' relationship")

# =========== CLASS & STATIC METHODS ===========
print("\n=== Class Methods and Static Methods ===")

class MathUtils:
    # Class variable
    PI = 3.14159
    
    def __init__(self, value):
        # Instance variable
        self.value = value
    
    # Instance method
    def multiply(self, x):
        return self.value * x
    
    # Class method - có thể truy cập class variables và methods
    @classmethod
    def from_string(cls, string_value):
        value = float(string_value)
        return cls(value)  # Creates a new instance
    
    @classmethod
    def get_pi(cls):
        return cls.PI
    
    # Static method - không thể truy cập class hoặc instance variables
    @staticmethod
    def add(x, y):
        return x + y

# Sử dụng class và static methods
math = MathUtils(5)
print(f"Instance method: 5 * 3 = {math.multiply(3)}")
print(f"Class method (PI): {MathUtils.get_pi()}")
print(f"Static method: 10 + 7 = {MathUtils.add(10, 7)}")

# Alternative constructor with class method
math_from_string = MathUtils.from_string("10.5")
print(f"Created from string: {math_from_string.value}")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
class MathUtils {
  static PI = 3.14159;
  
  constructor(value) {
    this.value = value;
  }
  
  // Instance method
  multiply(x) {
    return this.value * x;
  }
  
  // Static method
  static add(x, y) {
    return x + y;
  }
  
  // Factory method (tương tự class method Python)
  static fromString(stringValue) {
    return new MathUtils(parseFloat(stringValue));
  }
}
""")

# =========== PROPERTY DECORATORS ===========
print("\n=== Property Decorators ===")

class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    # Getter
    @property
    def celsius(self):
        print("Getting celsius value")
        return self._celsius
    
    # Setter
    @celsius.setter
    def celsius(self, value):
        print(f"Setting celsius value to {value}")
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible")
        self._celsius = value
    
    # Deleter
    @celsius.deleter
    def celsius(self):
        print("Deleting celsius value")
        self._celsius = 0
    
    # Property depending on another property
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# Sử dụng properties
temp = Temperature(25)
print(f"Celsius: {temp.celsius}")  # Gọi getter
print(f"Fahrenheit: {temp.fahrenheit}")  # Gọi getter của property mới

temp.celsius = 30  # Gọi setter
print(f"New celsius: {temp.celsius}, New fahrenheit: {temp.fahrenheit}")

temp.fahrenheit = 68  # Gọi setter của fahrenheit
print(f"New celsius: {temp.celsius}, New fahrenheit: {temp.fahrenheit}")

# Delete property value
del temp.celsius  # Gọi deleter
print(f"After delete: {temp.celsius}")

# Properties làm code pythonic hơn, không cần thông qua các method getter/setter
print("\nProperties cho phép gọi method như thuộc tính:")
print("temp.celsius thay vì temp.getCelsius()")
print("temp.celsius = 30 thay vì temp.setCelsius(30)")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
class Temperature {
  constructor(celsius = 0) {
    this._celsius = celsius;
  }
  
  // ES6 Getters and Setters
  get celsius() {
    console.log("Getting celsius value");
    return this._celsius;
  }
  
  set celsius(value) {
    console.log(`Setting celsius value to ${value}`);
    if (value < -273.15) {
      throw new Error("Temperature below absolute zero is not possible");
    }
    this._celsius = value;
  }
  
  get fahrenheit() {
    return (this._celsius * 9/5) + 32;
  }
  
  set fahrenheit(value) {
    this.celsius = (value - 32) * 5/9;
  }
}
""")

# =========== PRIVATE MEMBERS ===========
print("\n=== Private and Protected Members ===")

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner           # Public attribute
        self._balance = balance      # Protected attribute (convention)
        self.__transactions = []     # Private attribute (name mangling)
    
    def deposit(self, amount):
        self._balance += amount
        self.__transactions.append(f"Deposit: {amount}")
        return self._balance
    
    def withdraw(self, amount):
        if amount > self._balance:
            return "Insufficient funds"
        self._balance -= amount
        self.__transactions.append(f"Withdrawal: {amount}")
        return self._balance
    
    def get_balance(self):
        return self._balance
    
    def get_transaction_history(self):
        return self.__transactions
    
    # Private method
    def __calculate_interest(self):
        return self._balance * 0.05
    
    # Method calling private method
    def add_interest(self):
        interest = self.__calculate_interest()
        self.deposit(interest)
        return interest

# Sử dụng các conventions
account = Account("John Doe", 1000)
print(f"Owner: {account.owner}")
print(f"Initial balance: {account.get_balance()}")

account.deposit(500)
account.withdraw(200)
print(f"New balance: {account.get_balance()}")
print(f"Transaction history: {account.get_transaction_history()}")

# Truy cập interest
interest = account.add_interest()
print(f"Interest added: {interest}")
print(f"Balance after interest: {account.get_balance()}")

# Thử truy cập trực tiếp các thuộc tính protected và private
print("\nAccess modifiers in Python:")
print(f"Accessing protected attribute: account._balance = {account._balance}")
try:
    print(f"Accessing private attribute: account.__transactions = {account.__transactions}")
except AttributeError as e:
    print(f"Cannot access private attribute directly: {e}")

# Name mangling - Python đổi tên private attributes
print(f"Accessing private attribute with name mangling: account._Account__transactions = {account._Account__transactions}")

print("\nPython access modifiers:")
print("- Public: No prefix, accessible everywhere")
print("- Protected: Single underscore (_), convention only")
print("- Private: Double underscore (__), name mangling")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
class Account {
  constructor(owner, balance = 0) {
    this.owner = owner;         // Public
    this._balance = balance;    // Protected (convention)
    this.#transactions = [];    // Private (actual private field, ES2022)
  }
  
  // Private method (ES2022)
  #calculateInterest() {
    return this._balance * 0.05;
  }
  
  deposit(amount) {
    this._balance += amount;
    this.#transactions.push(`Deposit: ${amount}`);
    return this._balance;
  }
  
  // remaining methods...
}
""")

# =========== DUNDER (MAGIC) METHODS ===========
print("\n=== Dunder (Magic) Methods ===")

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # String representation
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    # Operator overloading
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        else:
            raise TypeError("Unsupported operand type")
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        else:
            raise TypeError("Unsupported operand type")
    
    # Right-side operations
    def __radd__(self, other):
        return self.__add__(other)
    
    # Comparison operations
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y
    
    # Container behavior
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector index out of range")
    
    def __len__(self):
        return 2
    
    # Context manager protocol
    def __enter__(self):
        print("Vector context manager: Entering")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Vector context manager: Exiting")
        return False

# Sử dụng dunder methods
v1 = Vector(3, 4)
v2 = Vector(1, 2)

# String representation
print(f"v1: {v1}")  # __str__
print(f"repr: {repr(v2)}")  # __repr__

# Operator overloading
v3 = v1 + v2  # __add__
print(f"v1 + v2 = {v3}")

v4 = v1 - v2  # __sub__
print(f"v1 - v2 = {v4}")

v5 = 5 + v1  # __radd__
print(f"5 + v1 = {v5}")

# Comparison
print(f"v1 == v2: {v1 == v2}")  # __eq__
print(f"v1 == Vector(3, 4): {v1 == Vector(3, 4)}")  # __eq__

# Container behavior
print(f"v1[0]: {v1[0]}, v1[1]: {v1[1]}")  # __getitem__
print(f"len(v1): {len(v1)}")  # __len__

# Context manager
with Vector(10, 20) as v:  # __enter__, __exit__
    print(f"Within context manager: {v}")

print("\nHowto use magic methods:")
print("1. __str__/__repr__: Hiển thị đại diện chuỗi của object")
print("2. Arithmetic: __add__, __sub__, __mul__, __truediv__, etc.")
print("3. Comparison: __eq__, __lt__, __gt__, etc.")
print("4. Container: __getitem__, __setitem__, __len__, __contains__, etc.")
print("5. Context management: __enter__, __exit__")
print("6. Iteration: __iter__, __next__")
print("7. Attribute access: __getattr__, __setattr__, __delattr__")
print("8. Callable objects: __call__")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
class Vector {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
  
  // String representation
  toString() {
    return `Vector(${this.x}, ${this.y})`;
  }
  
  // Custom methods for operations
  add(other) {
    if (other instanceof Vector) {
      return new Vector(this.x + other.x, this.y + other.y);
    } else if (typeof other === 'number') {
      return new Vector(this.x + other, this.y + other);
    }
    throw new TypeError("Unsupported operand type");
  }
  
  // No true operator overloading in JavaScript
  // Must use methods like add(), subtract() instead of + and -
}
""")

# =========== MIXINS (MULTIPLE INHERITANCE) ===========
print("\n=== Mixins and Multiple Inheritance ===")

# Mixin classes
class Loggable:
    def log(self, message):
        print(f"[LOG] {message}")

class Serializable:
    def serialize(self):
        return {"classname": self.__class__.__name__, **self.__dict__}
    
    def deserialize(self, data):
        for key, value in data.items():
            if key != "classname":
                setattr(self, key, value)

# Sử dụng mixins thông qua multiple inheritance
class User(Loggable, Serializable):
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def display(self):
        self.log(f"Displaying user: {self.name}")
        return f"User: {self.name}, Email: {self.email}"

# Sử dụng người dùng với các tính năng được thêm vào từ mixins
user = User("Alice", "alice@example.com")
user.log("User created")  # Từ Loggable mixin
print(f"User display: {user.display()}")

# Serialization
serialized = user.serialize()  # Từ Serializable mixin
print(f"Serialized user: {serialized}")

# Deserialization
new_user = User("", "")
new_user.deserialize(serialized)
print(f"Deserialized user: {new_user.display()}")

print("\nMixin benefits:")
print("1. Code reuse không cần deep inheritance hierarchy")
print("2. Composition của behaviors thay vì inheritance")
print("3. Dễ dàng thêm chức năng mà không cần thay đổi nhiều code")
print("4. Solution cho diamond inheritance problem")

# =========== DATACLASSES (PYTHON 3.7+) ===========
try:
    from dataclasses import dataclass, field
    print("\n=== Dataclasses (Python 3.7+) ===")
    
    @dataclass
    class Product:
        name: str
        price: float
        quantity: int = 0
        tags: list = field(default_factory=list)
        
        def total_cost(self):
            return self.price * self.quantity
    
    # Sử dụng dataclass
    laptop = Product("Laptop", 1299.99, 5, ["electronics", "computers"])
    print(f"Product: {laptop}")
    print(f"Total cost: ${laptop.total_cost()}")
    
    # Comparing dataclasses
    laptop2 = Product("Laptop", 1299.99, 5, ["electronics", "computers"])
    print(f"laptop == laptop2: {laptop == laptop2}")  # True, dataclasses implement __eq__
    
    print("\nDataclass benefits:")
    print("1. Automatically generates __init__, __repr__, __eq__, etc.")
    print("2. Immutable dataclasses with frozen=True")
    print("3. Specify default values easily")
    print("4. Type annotations provide clarity")
    print("5. Reduces boilerplate code")
    
except ImportError:
    print("\nDataclasses require Python 3.7 or newer")

# =========== NAMED TUPLES ===========
from collections import namedtuple

print("\n=== Named Tuples ===")

# Creating a named tuple type
Person = namedtuple("Person", ["name", "age", "city"])

# Creating instances
alice = Person("Alice", 30, "New York")
bob = Person(name="Bob", age=25, city="Boston")

print(f"Person: {alice}")
print(f"Name: {alice.name}, Age: {alice.age}, City: {alice.city}")

# Unpacking
name, age, city = bob
print(f"Unpacked: Name={name}, Age={age}, City={city}")

# Converting to dictionary
alice_dict = alice._asdict()
print(f"As dictionary: {alice_dict}")

# Creating a new instance with a modified field
alice_older = alice._replace(age=31)
print(f"Modified: {alice_older}")

print("\nNamed tuple benefits:")
print("1. Immutable data structure like regular tuples")
print("2. Accessible by name (obj.name) or position (obj[0])")
print("3. Memory-efficient")
print("4. Lightweight alternative to classes for data containers")
print("5. Compatible with tuple unpacking")

# =========== SLOTS ===========
print("\n=== __slots__ for Memory Efficiency ===")

class RegularClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedClass:
    __slots__ = ['x', 'y']  # Define allowed attributes
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Create instances
regular = RegularClass(1, 2)
slotted = SlottedClass(1, 2)

# Memory comparison (this is simplistic, actual memory savings are larger)
import sys
regular_size = sys.getsizeof(regular.__dict__)
# Slotted classes don't have __dict__
slotted_size = sys.getsizeof(slotted) if hasattr(slotted, '__slots__') else 0

print(f"Regular instance __dict__ size: {regular_size} bytes")
print(f"Slotted instance size: {slotted_size} bytes (not accurate, but usually smaller)")

# Try adding a new attribute
regular.z = 3  # Works fine
try:
    slotted.z = 3  # Will raise AttributeError
except AttributeError as e:
    print(f"Cannot add new attribute to slotted class: {e}")

print("\n__slots__ benefits:")
print("1. Reduced memory usage")
print("2. Slightly faster attribute access")
print("3. Prevents accidental creation of new attributes")

print("\n__slots__ limitations:")
print("1. No __dict__ attribute (by default)")
print("2. No dynamic attribute assignment")
print("3. More complex to use with inheritance")

# =========== BEST PRACTICES ===========
print("\n=== OOP Best Practices in Python ===")

print("1. Prefer composition over inheritance when possible")
print("2. Use properties instead of getter/setter methods")
print("3. Follow Python naming conventions:")
print("   - Class names: PascalCase")
print("   - Method/attribute names: snake_case")
print("   - Constants: UPPERCASE_WITH_UNDERSCORES")
print("4. Use @classmethod for alternative constructors")
print("5. Use @staticmethod for utility functions related to the class")
print("6. Take advantage of dunder methods for operator overloading")
print("7. Use type hints for better documentation and tooling support")
print("8. Apply mixins for reusable behaviors")
print("9. Consider dataclasses for data container classes")
print("10. Use __slots__ for memory-critical applications")