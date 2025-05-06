'''
Python OOP cho JavaScript Developers
=================================

Python là ngôn ngữ hướng đối tượng với nhiều tính năng mạnh mẽ.
Khái niệm OOP trong Python khá giống với JavaScript class (ES6+),
nhưng có nhiều tính năng phong phú hơn.
'''

# =========== CLASS VÀ OBJECT CƠ BẢN ===========

# Định nghĩa class trong Python
class Person:
    # Constructor - tương tự constructor trong JS
    def __init__(self, name, age):
        # Thuộc tính (attributes/properties)
        self.name = name
        self.age = age
    
    # Method (phương thức)
    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."
    
    # Method với tham số
    def celebrate_birthday(self):
        self.age += 1
        return f"Happy birthday! Now I'm {self.age} years old."

# Tạo object (instance) của class
john = Person("John", 30)
alice = Person("Alice", 25)

# Truy cập thuộc tính
print(f"Name: {john.name}, Age: {john.age}")

# Gọi phương thức
print(john.greet())
print(alice.celebrate_birthday())

# So sánh với JavaScript:
# class Person {
#   constructor(name, age) {
#     this.name = name;
#     this.age = age;
#   }
#
#   greet() {
#     return `Hello, my name is ${this.name} and I am ${this.age} years old.`;
#   }
#
#   celebrateBirthday() {
#     this.age += 1;
#     return `Happy birthday! Now I'm ${this.age} years old.`;
#   }
# }
#
# const john = new Person("John", 30);
# const alice = new Person("Alice", 25);

# =========== THUỘC TÍNH VÀ PHƯƠNG THỨC TĨNH (STATIC) ===========

class MathUtils:
    # Thuộc tính tĩnh (static attribute)
    PI = 3.14159
    
    # Phương thức tĩnh (static method)
    @staticmethod
    def square(number):
        return number ** 2
    
    # Phương thức lớp (class method) - truy cập được thuộc tính lớp
    @classmethod
    def get_circle_area(cls, radius):
        return cls.PI * radius ** 2

# Truy cập thuộc tính tĩnh
print(f"PI: {MathUtils.PI}")

# Gọi phương thức tĩnh
print(f"Square of 5: {MathUtils.square(5)}")

# Gọi class method
print(f"Area of circle with radius 5: {MathUtils.get_circle_area(5)}")

# So sánh với JavaScript:
# class MathUtils {
#   static PI = 3.14159;
#
#   static square(number) {
#     return number ** 2;
#   }
#
#   static getCircleArea(radius) {
#     return MathUtils.PI * radius ** 2;
#   }
# }

# =========== THUỘC TÍNH PRIVATE VÀ PROPERTY ===========

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner      # Thuộc tính public
        self._balance = balance  # Convention cho thuộc tính "private" (dấu gạch dưới _)
        self.__id = "12345"     # "Private" thực sự (name mangling với dấu 2 gạch dưới __)
    
    # Property - getter
    @property
    def balance(self):
        return self._balance
    
    # Property - setter
    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
    
    # Property không có setter (read-only)
    @property
    def account_info(self):
        return f"Owner: {self.owner}, Balance: ${self._balance}"
    
    # Method để truy cập thuộc tính "private"
    def get_id(self):
        return self.__id

# Tạo account
account = BankAccount("John", 1000)

# Truy cập thuộc tính public
print(f"Owner: {account.owner}")

# Sử dụng property
print(f"Balance: {account.balance}")  # Gọi getter

# Sử dụng setter
account.balance = 1500
print(f"New balance: {account.balance}")

# Sử dụng property read-only
print(account.account_info)

# Truy cập "private" attribute
print(f"ID: {account.get_id()}")

# Thử truy cập trực tiếp vào thuộc tính private bằng name mangling
try:
    print(account.__id)  # Raises AttributeError
except AttributeError:
    print("Cannot access __id directly")
    
# Truy cập bằng name mangling (không nên làm thế này trong thực tế)
print(f"ID (accessed with name mangling): {account._BankAccount__id}")

# So sánh với JavaScript:
# JavaScript không có thuộc tính private thực sự (trước ES2022)
# class BankAccount {
#   #id = "12345";  // Private field (from ES2022)
#   
#   constructor(owner, balance = 0) {
#     this.owner = owner;
#     this._balance = balance;
#   }
#   
#   get balance() {
#     return this._balance;
#   }
#   
#   set balance(value) {
#     if (value < 0) {
#       throw new Error("Balance cannot be negative");
#     }
#     this._balance = value;
#   }
#   
#   get accountInfo() {
#     return `Owner: ${this.owner}, Balance: $${this._balance}`;
#   }
#   
#   getId() {
#     return this.#id;
#   }
# }

# =========== KẾ THỪA (INHERITANCE) ===========

# Lớp cha (base class)
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return "Some generic animal sound"
    
    def get_info(self):
        return f"{self.name} is a {self.species}"

# Lớp con (derived class)
class Dog(Animal):
    def __init__(self, name, breed):
        # Gọi constructor của lớp cha
        super().__init__(name, "Dog")
        self.breed = breed
    
    # Override phương thức của lớp cha
    def make_sound(self):
        return "Woof!"
    
    # Thêm phương thức mới
    def fetch(self, item):
        return f"{self.name} is fetching the {item}!"

# Tạo object của lớp con
rex = Dog("Rex", "German Shepherd")

# Truy cập phương thức từ lớp cha
print(rex.get_info())  # Từ Animal

# Truy cập phương thức bị override
print(f"Sound: {rex.make_sound()}")  # Từ Dog, không phải Animal

# Truy cập phương thức mới
print(rex.fetch("ball"))

# Kiểm tra kiểu
print(f"Rex is a Dog: {isinstance(rex, Dog)}")
print(f"Rex is an Animal: {isinstance(rex, Animal)}")

# So sánh với JavaScript:
# class Animal {
#   constructor(name, species) {
#     this.name = name;
#     this.species = species;
#   }
#   
#   makeSound() {
#     return "Some generic animal sound";
#   }
#   
#   getInfo() {
#     return `${this.name} is a ${this.species}`;
#   }
# }
#
# class Dog extends Animal {
#   constructor(name, breed) {
#     super(name, "Dog");
#     this.breed = breed;
#   }
#   
#   makeSound() {
#     return "Woof!";
#   }
#   
#   fetch(item) {
#     return `${this.name} is fetching the ${item}!`;
#   }
# }

# =========== ĐA KẾ THỪA VÀ MIXINS ===========
# Python hỗ trợ đa kế thừa, JavaScript không hỗ trợ

class Swimmer:
    def swim(self):
        return "Swimming"

class Flyer:
    def fly(self):
        return "Flying"

# Đa kế thừa
class Duck(Animal, Swimmer, Flyer):
    def __init__(self, name):
        super().__init__(name, "Duck")
    
    def make_sound(self):
        return "Quack!"

# Tạo Duck
duck = Duck("Donald")
print(duck.get_info())      # Từ Animal
print(duck.make_sound())    # Từ Duck
print(duck.swim())          # Từ Swimmer
print(duck.fly())           # Từ Flyer

# Trong JavaScript, có thể dùng mixins để mô phỏng:
# // JavaScript không hỗ trợ đa kế thừa trực tiếp
# const SwimmerMixin = (superclass) => class extends superclass {
#   swim() {
#     return "Swimming";
#   }
# };
#
# const FlyerMixin = (superclass) => class extends superclass {
#   fly() {
#     return "Flying";
#   }
# };
#
# class Duck extends FlyerMixin(SwimmerMixin(Animal)) { ... }

# =========== PHƯƠNG THỨC MAGIC __METHODS__ ===========
# Phương thức đặc biệt trong Python bắt đầu và kết thúc bằng __

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # String representation
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    # Representation for developers
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    # Addition operator overloading (+)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # Equality operator overloading (==)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    # Length operator overloading (len())
    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
    
    # Make the object callable
    def __call__(self, scale):
        return Vector(self.x * scale, self.y * scale)

# Tạo vector
v1 = Vector(3, 4)
v2 = Vector(1, 2)

# __str__ & __repr__
print(v1)

# __add__
v3 = v1 + v2
print(f"v1 + v2 = {v3}")

# __eq__
print(f"v1 == v2: {v1 == v2}")
print(f"v1 == Vector(3, 4): {v1 == Vector(3, 4)}")

# __len__
print(f"Length of v1: {len(v1)}")

# __call__
v4 = v1(2)  # Double the vector
print(f"v1 scaled by 2: {v4}")

# So sánh với JavaScript:
# JavaScript không hỗ trợ operator overloading
# class Vector {
#   constructor(x, y) {
#     this.x = x;
#     this.y = y;
#   }
#   
#   toString() {
#     return `Vector(${this.x}, ${this.y})`;
#   }
#   
#   add(other) {
#     return new Vector(this.x + other.x, this.y + other.y);
#   }
#   
#   equals(other) {
#     return this.x === other.x && this.y === other.y;
#   }
#   
#   length() {
#     return Math.floor(Math.sqrt(this.x ** 2 + this.y ** 2));
#   }
#   
#   scale(factor) {
#     return new Vector(this.x * factor, this.y * factor);
#   }
# }

# =========== ABSTRACT CLASSES ===========
# Lớp trừu tượng trong Python cần import module abc

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    # Phương thức không trừu tượng
    def description(self):
        return "This is a shape"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Không thể tạo instance của abstract class
try:
    shape = Shape()
except TypeError as e:
    print(f"Cannot instantiate abstract class: {e}")

# Tạo instance của class con
circle = Circle(5)
rectangle = Rectangle(4, 6)

print(f"Circle area: {circle.area()}")
print(f"Circle perimeter: {circle.perimeter()}")
print(f"Circle description: {circle.description()}")

print(f"Rectangle area: {rectangle.area()}")
print(f"Rectangle perimeter: {rectangle.perimeter()}")

# So sánh với JavaScript:
# JavaScript không có abstract class tích hợp sẵn
# class Shape {
#   constructor() {
#     if (this.constructor === Shape) {
#       throw new Error("Abstract class cannot be instantiated");
#     }
#   }
#   
#   area() {
#     throw new Error("Method must be implemented");
#   }
#   
#   perimeter() {
#     throw new Error("Method must be implemented");
#   }
#   
#   description() {
#     return "This is a shape";
#   }
# }