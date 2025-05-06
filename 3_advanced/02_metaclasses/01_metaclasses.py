'''
Python Metaclasses cho JavaScript Developers
========================================

Metaclasses là một trong những khái niệm nâng cao nhất trong Python,
cho phép bạn điều khiển cách class được tạo, giống như "class của class".

JavaScript thiếu khái niệm metaclasses trực tiếp, nhưng có thể mô phỏng một số
tính năng tương tự thông qua constructor functions và Proxy.
'''

# =========== CLASS VÀ TYPE TRONG PYTHON ===========
# Trong Python, mọi thứ đều là object, kể cả class

print("=== Classes và Types ===")

# Class trong Python là instance của metaclass 'type'
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, I'm {self.name}"

# Tạo instance từ class
john = Person("John")

# Kiểm tra type của các đối tượng
print(f"john is a: {type(john)}")               # <class '__main__.Person'>
print(f"Person is a: {type(Person)}")           # <class 'type'>
print(f"type is a: {type(type)}")               # <class 'type'> (type là metaclass của chính nó)

# So sánh với JavaScript:
# // JavaScript không có metaclass concept
# class Person {
#   constructor(name) {
#     this.name = name;
#   }
#   greet() {
#     return `Hello, I'm ${this.name}`;
#   }
# }
# const john = new Person("John");
# console.log(typeof john);      // "object"
# console.log(typeof Person);    // "function"

# =========== TẠO CLASS ĐỘNG ===========
# Class có thể được tạo "on-the-fly" bằng type

# Cách thông thường để tạo class
class Dog:
    species = "Canis familiaris"
    
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return "Woof!"

# Cách tương đương dùng type()
# Cú pháp: type(name, bases, attrs)
DogType = type(
    "DogType",                          # Tên class
    (),                                 # Class cha (tuple)
    {
        "species": "Canis familiaris",  # Class attribute
        "__init__": lambda self, name: setattr(self, "name", name),
        "bark": lambda self: "Woof!"    # Method
    }
)

# Test class được tạo từ type
rex = DogType("Rex")
print(f"\nDynamic class creation:")
print(f"Rex's class: {type(rex)}")
print(f"Rex's species: {rex.species}")
print(f"Rex says: {rex.bark()}")

# So sánh với JavaScript:
# // Tạo class động trong JavaScript
# function createClass(name, methods) {
#   // Tạo constructor function
#   const Class = function(...args) {
#     if (methods.constructor) {
#       methods.constructor.apply(this, args);
#     }
#   };
#   
#   // Thêm methods vào prototype
#   Object.entries(methods).forEach(([key, method]) => {
#     if (key !== 'constructor') {
#       Class.prototype[key] = method;
#     }
#   });
#   
#   return Class;
# }
#
# const DogClass = createClass('Dog', {
#   constructor: function(name) { this.name = name; },
#   bark: function() { return "Woof!"; }
# });

# =========== CUSTOM METACLASS ===========
# Metaclass giúp kiểm soát cách class được khởi tạo và tùy chỉnh

class Meta(type):
    # __new__ được gọi khi class được tạo
    def __new__(mcs, name, bases, attrs):
        print(f"\nCreating class: {name}")
        
        # Chuyển đổi tất cả method names thành uppercase
        uppercase_attrs = {}
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith('__'):
                uppercase_attrs[attr_name.upper()] = attr_value
            else:
                uppercase_attrs[attr_name] = attr_value
        
        # Thêm một method mới
        uppercase_attrs['VERSION'] = lambda self: "1.0"
        
        # Gọi __new__ của lớp cha (type) để thực sự tạo class
        return super().__new__(mcs, name, bases, uppercase_attrs)
    
    # __init__ được gọi sau khi class được tạo
    def __init__(cls, name, bases, attrs):
        print(f"Initializing class: {name}")
        super().__init__(name, bases, attrs)
    
    # __call__ được gọi khi class được instantiated
    def __call__(cls, *args, **kwargs):
        print(f"Creating instance of: {cls.__name__}")
        instance = super().__call__(*args, **kwargs)
        print(f"Instance created: {instance}")
        return instance

# Sử dụng metaclass
class Product(metaclass=Meta):
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def get_price(self):
        return f"${self.price:.2f}"
    
    def discount(self, percent):
        return self.price * (1 - percent/100)

# Tạo instance
laptop = Product("Laptop", 999.99)

# Method names đã được chuyển thành uppercase
print(f"\nProduct methods:")
print(f"Price: {laptop.GET_PRICE()}")  # Lưu ý: get_price() -> GET_PRICE()
print(f"15% discount: ${laptop.DISCOUNT(15):.2f}")
print(f"Version: {laptop.VERSION()}")

# So sánh với JavaScript:
# // JavaScript không có metaclasses nhưng có thể dùng Proxy
# function createClassWithProxy(classDefinition) {
#   // Create a proxy for the class
#   return new Proxy(classDefinition, {
#     // Trap for property access
#     get(target, prop, receiver) {
#       console.log(`Accessing ${prop} on class`);
#       return Reflect.get(target, prop, receiver);
#     },
#     
#     // Trap for instantiation
#     construct(target, args) {
#       console.log(`Creating instance of ${target.name}`);
#       const instance = Reflect.construct(target, args);
#       console.log(`Instance created`);
#       return instance;
#     }
#   });
# }
#
# const Product = createClassWithProxy(
#   class Product {
#     constructor(name, price) {
#       this.name = name;
#       this.price = price;
#     }
#     
#     getPrice() {
#       return `$${this.price.toFixed(2)}`;
#     }
#     
#     discount(percent) {
#       return this.price * (1 - percent/100);
#     }
#   }
# );

# =========== ỨNG DỤNG CỦA METACLASS ===========

# 1. SINGLETON PATTERN
print("\n=== Singleton Pattern with Metaclass ===")

class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        print(f"Database initialized with {connection_string}")

# Tạo "nhiều" instances
db1 = Database("mysql://localhost:3306")
db2 = Database("mysql://localhost:3306")  # Không khởi tạo lại

print(f"Same instance? {db1 is db2}")  # True

# 2. REGISTRY PATTERN
print("\n=== Registry Pattern with Metaclass ===")

class PluginRegistry(type):
    plugins = {}
    
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if bases:  # Chỉ đăng ký class con, không đăng ký class cha
            mcs.plugins[name] = cls
        return cls

class Plugin(metaclass=PluginRegistry):
    def run(self):
        raise NotImplementedError("Plugins must implement run()")

class TextPlugin(Plugin):
    def run(self):
        return "Processing text..."

class ImagePlugin(Plugin):
    def run(self):
        return "Processing image..."

# Tất cả plugins đã tự động đăng ký
print(f"Registered plugins: {', '.join(PluginRegistry.plugins.keys())}")

# Sử dụng plugin động
def process_file(file_type):
    plugin_name = f"{file_type.capitalize()}Plugin"
    if plugin_name in PluginRegistry.plugins:
        plugin = PluginRegistry.plugins[plugin_name]()
        return plugin.run()
    else:
        return f"No plugin for {file_type} files"

print(f"Processing text: {process_file('text')}")
print(f"Processing image: {process_file('image')}")
print(f"Processing video: {process_file('video')}")

# 3. AUTO PROPERTY CREATION
print("\n=== Auto Property Creation with Metaclass ===")

class AutoProperty(type):
    def __new__(mcs, name, bases, attrs):
        # Tìm tất cả các fields và tạo properties cho chúng
        for key, value in list(attrs.items()):
            if key.startswith('_') and not key.startswith('__'):
                property_name = key[1:]  # Bỏ dấu _ ở đầu
                
                # Tạo getter
                getter_name = f"get_{property_name}"
                if getter_name not in attrs:
                    attrs[getter_name] = lambda self, key=key: getattr(self, key)
                
                # Tạo setter
                setter_name = f"set_{property_name}"
                if setter_name not in attrs:
                    attrs[setter_name] = lambda self, value, key=key: setattr(self, key, value)
                
                # Tạo property
                attrs[property_name] = property(attrs[getter_name], attrs[setter_name])
        
        return super().__new__(mcs, name, bases, attrs)

class Person(metaclass=AutoProperty):
    def __init__(self, name, age):
        self._name = name
        self._age = age

# Test auto properties
person = Person("Alice", 30)
print(f"Name: {person.name}")  # Sử dụng property tự động
print(f"Age: {person.age}")

person.name = "Alicia"  # Sử dụng setter tự động
print(f"New name: {person.name}")

# 4. VALIDATION
print("\n=== Field Validation with Metaclass ===")

class ValidateMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Tìm tất cả các validators
        validators = {}
        for key, value in attrs.items():
            if key.startswith('validate_'):
                field_name = key[9:]  # Bỏ 'validate_'
                validators[field_name] = value
        
        # Lưu validators vào class
        attrs['_validators'] = validators
        
        # Ghi đè __setattr__ để validate khi set attribute
        original_setattr = attrs.get('__setattr__', object.__setattr__)
        
        def __setattr__(self, name, value):
            if name in self._validators:
                # Gọi validator
                validator = getattr(self, f'validate_{name}')
                value = validator(value)
            original_setattr(self, name, value)
        
        attrs['__setattr__'] = __setattr__
        
        return super().__new__(mcs, name, bases, attrs)

class User(metaclass=ValidateMeta):
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age
    
    def validate_username(self, value):
        if not isinstance(value, str) or len(value) < 3:
            raise ValueError("Username must be a string with at least 3 characters")
        return value
    
    def validate_email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise ValueError("Email must be a valid email address")
        return value
    
    def validate_age(self, value):
        if not isinstance(value, int) or value < 18:
            raise ValueError("Age must be an integer >= 18")
        return value

# Test validation
try:
    user = User("john_doe", "john@example.com", 25)
    print(f"Valid user created: {user.username}, {user.email}, {user.age}")
    
    # Test invalid values
    user.username = "jo"  # Too short
except ValueError as e:
    print(f"Validation error: {e}")

# =========== BEST PRACTICES VÀ CHÚ Ý ===========
print("\n=== Metaclass Best Practices ===")

print("1. Metaclasses rất mạnh mẽ nhưng cũng phức tạp - sử dụng khi thực sự cần thiết")
print("2. Class decorators thường là giải pháp đơn giản hơn cho nhiều trường hợp")
print("3. Cẩn thận với hiệu suất, metaclasses được gọi khi class được định nghĩa")
print("4. Khi sử dụng nhiều metaclasses, cần hiểu rõ về thứ tự gọi")
print("5. Để tương thích ngược, cân nhắc cung cấp cách khác cho các tính năng quan trọng")

# =========== CLASS DECORATORS VS METACLASSES ===========
print("\n=== Class Decorators vs Metaclasses ===")

# Class Decorator - Đơn giản hơn và thường đủ dùng
def add_repr(cls):
    """Class decorator để thêm __repr__ method"""
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    
    cls.__repr__ = __repr__
    return cls

@add_repr
class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role

employee = Employee("Bob", "Developer")
print(f"Employee repr: {employee}")

print("\nKhi nên dùng:")
print("- Class Decorators: Khi bạn cần sửa đổi class sau khi đã được tạo")
print("- Metaclasses: Khi bạn cần kiểm soát quá trình tạo class")

# =========== SO SÁNH VỚI JAVASCRIPT ===========
print("\n=== So sánh với JavaScript ===")

print("JavaScript không có metaclasses, nhưng có thể mô phỏng một số tính năng bằng:")
print("1. Object.defineProperty/defineProperties - để định nghĩa properties")
print("2. Proxies - để can thiệp vào truy cập thuộc tính")
print("3. Factory functions - để tạo objects và classes tùy chỉnh")
print("4. Class và function decorators (unofficial) - để mở rộng class behavior")
print("5. Reflection API - để truy cập metadata của objects")

print("\nHầu hết các vấn đề giải quyết bằng metaclass trong Python có thể giải quyết bằng:")
print("- Factory pattern")
print("- Higher-order components")
print("- Decorators")
print("- Dependency injection")
print("trong hệ sinh thái JavaScript.")