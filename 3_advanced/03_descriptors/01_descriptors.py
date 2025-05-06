'''
Python Descriptors cho JavaScript Developers
=======================================

Descriptors là một tính năng nâng cao của Python cho phép bạn tùy chỉnh hành vi
của các thuộc tính (attributes) - cách chúng được truy cập, thiết lập và xóa.

Descriptors cung cấp nền tảng cho các tính năng như properties, methods, 
class methods, và static methods trong Python.
'''

# =========== TỔNG QUAN VỀ DESCRIPTORS ===========
# Descriptors là các objects có ít nhất một trong các magic methods: __get__, __set__, hoặc __delete__

print("=== Descriptors Overview ===")

# Một descriptor đơn giản
class MyDescriptor:
    def __get__(self, instance, owner_class):
        print(f"__get__ called. instance: {instance}, owner_class: {owner_class}")
        return 42
    
    def __set__(self, instance, value):
        print(f"__set__ called. instance: {instance}, value: {value}")
    
    def __delete__(self, instance):
        print(f"__delete__ called. instance: {instance}")

# Sử dụng descriptor
class MyClass:
    # descriptor được khai báo ở class level
    x = MyDescriptor()

# Truy cập, thiết lập và xóa thuộc tính
obj = MyClass()
print(f"Accessing obj.x: {obj.x}")  # Gọi __get__
obj.x = 100                         # Gọi __set__ 
del obj.x                           # Gọi __delete__

# Truy cập thông qua class cũng được xử lý bởi descriptor
print(f"Accessing MyClass.x: {MyClass.x}")  # Gọi __get__ với instance=None

# So sánh với JavaScript:
# JavaScript không có descriptor trực tiếp tương đương, nhưng ES5 giới thiệu Object.defineProperty
# // Tạo property tùy chỉnh trong JavaScript:
# class MyClass {}
# Object.defineProperty(MyClass.prototype, 'x', {
#   get() {
#     console.log('get called');
#     return 42;
#   },
#   set(value) {
#     console.log(`set called with value: ${value}`);
#   }
# });
# 
# const obj = new MyClass();
# console.log(obj.x);  // logs: get called, 42
# obj.x = 100;         // logs: set called with value: 100

# =========== CÁC LOẠI DESCRIPTORS ===========
# Data descriptor: Có __set__ và/hoặc __delete__
# Non-data descriptor: Chỉ có __get__ 

print("\n=== Types of Descriptors ===")

# Data descriptor
class DataDescriptor:
    def __get__(self, instance, owner):
        print("DataDescriptor.__get__ called")
        return 42
    
    def __set__(self, instance, value):
        print(f"DataDescriptor.__set__ called with value: {value}")

# Non-data descriptor
class NonDataDescriptor:
    def __get__(self, instance, owner):
        print("NonDataDescriptor.__get__ called")
        return 24

class TestClass:
    data_desc = DataDescriptor()
    non_data_desc = NonDataDescriptor()
    # Attribute thông thường
    regular_attr = 999

# Thứ tự ưu tiên:
# 1. Data descriptor
# 2. Instance attribute
# 3. Non-data descriptor
# 4. Class attribute

# Demo thứ tự ưu tiên
test = TestClass()

# Data descriptor luôn được gọi ngay cả khi có instance attribute trùng tên
test.__dict__['data_desc'] = "instance attribute"
print(f"test.data_desc: {test.data_desc}")  # Still calls DataDescriptor.__get__

# Non-data descriptor bị ghi đè bởi instance attribute
test.__dict__['non_data_desc'] = "instance attribute"
print(f"test.non_data_desc: {test.non_data_desc}")  # "instance attribute"

# =========== ỨNG DỤNG CƠ BẢN ===========
# Descriptor cho attribute với validation và conversion

class ValidString:
    def __init__(self, min_length=0, max_length=None):
        self.min_length = min_length
        self.max_length = max_length
        # Private name để lưu giá trị riêng cho mỗi instance
        self.private_name = f"_{id(self)}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Lấy giá trị từ instance.__dict__
        return getattr(instance, self.private_name, "")
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        
        if len(value) < self.min_length:
            raise ValueError(f"String must be at least {self.min_length} characters")
        
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"String cannot exceed {self.max_length} characters")
        
        # Lưu giá trị vào instance.__dict__
        setattr(instance, self.private_name, value)
    
    def __delete__(self, instance):
        # Xóa giá trị từ instance.__dict__ nếu có
        if hasattr(instance, self.private_name):
            delattr(instance, self.private_name)

# Sử dụng descriptor để tự động validate
class User:
    username = ValidString(min_length=3, max_length=20)
    email = ValidString()
    
    def __init__(self, username, email):
        self.username = username
        self.email = email

# Test descriptor với validation
print("\n=== Descriptor with Validation ===")
try:
    user = User("john_doe", "john@example.com")
    print(f"Created user: {user.username}, {user.email}")
    
    # Test validation
    user.username = "jd"  # Too short
except ValueError as e:
    print(f"Validation error: {e}")

# =========== PROPERTY VS DESCRIPTOR ===========
# Property là built-in descriptor để tạo getter/setter/deleter

print("\n=== Property vs Descriptor ===")

# Sử dụng property decorator
class Person:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        """Getter for name"""
        print("name getter called")
        return self._name
    
    @name.setter
    def name(self, value):
        """Setter for name"""
        print(f"name setter called with: {value}")
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        self._name = value
    
    @name.deleter
    def name(self):
        """Deleter for name"""
        print("name deleter called")
        del self._name

# Test property
person = Person("Alice")
print(f"Person's name: {person.name}")
person.name = "Bob"
print(f"Updated name: {person.name}")

try:
    person.name = ""  # Too short
except ValueError as e:
    print(f"Validation error: {e}")

# Property thực tế là một descriptor
print(f"person.name is a descriptor: {isinstance(Person.name, property)}")

# Tương đương với property, descriptor thủ công sẽ như sau:
class NameDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        print("name getter called (manual descriptor)")
        return instance._name
    
    def __set__(self, instance, value):
        print(f"name setter called (manual descriptor) with: {value}")
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        instance._name = value
    
    def __delete__(self, instance):
        print("name deleter called (manual descriptor)")
        del instance._name

class PersonWithDescriptor:
    name = NameDescriptor()
    
    def __init__(self, name):
        self._name = name

# Test descriptor thủ công
print("\n=== Manual Descriptor Implementation ===")
person2 = PersonWithDescriptor("Charlie")
print(f"Person's name: {person2.name}")
person2.name = "Dave"
print(f"Updated name: {person2.name}")

# =========== METHOD DESCRIPTOR ===========
# Method là một loại descriptor đặc biệt

print("\n=== Methods as Descriptors ===")

class Method:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Bind method với instance - tương tự Python thực hiện với methods
        return lambda *args, **kwargs: self.func(instance, *args, **kwargs)

class ClassMethod:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        # Bind method với class
        return lambda *args, **kwargs: self.func(owner, *args, **kwargs)

class StaticMethod:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        # Không bind với bất kỳ thứ gì
        return self.func

class MyClass:
    # Instance method thủ công với descriptor
    @Method
    def instance_method(self, x):
        return f"Instance method called with {x}, self={self}"
    
    # Class method thủ công với descriptor
    @ClassMethod
    def class_method(cls, x):
        return f"Class method called with {x}, class={cls.__name__}"
    
    # Static method thủ công với descriptor
    @StaticMethod
    def static_method(x):
        return f"Static method called with {x}"
    
    # Dùng built-in decorators của Python
    def normal_method(self, x):
        return f"Normal method called with {x}, self={self}"
    
    @classmethod
    def normal_class_method(cls, x):
        return f"Normal class method called with {x}, class={cls.__name__}"
    
    @staticmethod
    def normal_static_method(x):
        return f"Normal static method called with {x}"

# Test các loại methods
obj = MyClass()

print("\nCustom descriptor implementations:")
print(obj.instance_method("hello"))
print(MyClass.class_method("world"))
print(obj.static_method("python"))

print("\nPython's built-in implementations:")
print(obj.normal_method("hello"))
print(MyClass.normal_class_method("world"))
print(obj.normal_static_method("python"))

# =========== LAZY PROPERTIES ===========
# Sử dụng descriptor để tính toán giá trị chỉ khi cần

print("\n=== Lazy Properties with Descriptors ===")

class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Compute và cache giá trị 
        value = self.function(instance)
        # Lưu vào instance.__dict__ nên lần sau không cần tính lại
        setattr(instance, self.name, value)
        return value

class ExpensiveCalculation:
    def __init__(self, data):
        self.data = data
    
    @LazyProperty
    def processed_data(self):
        print("Processing data... (expensive operation)")
        # Giả lập một tính toán tốn thời gian
        import time
        time.sleep(1)
        return [x * 2 for x in self.data]
    
    @LazyProperty
    def data_sum(self):
        print("Calculating sum... (another expensive operation)")
        return sum(self.processed_data)

# Test lazy property
obj = ExpensiveCalculation([1, 2, 3, 4, 5])

print("Accessing processed_data first time:")
print(f"Processed data: {obj.processed_data}")

print("\nAccessing processed_data second time (should be cached):")
print(f"Processed data: {obj.processed_data}")

print("\nAccessing data_sum (uses processed_data):")
print(f"Sum: {obj.data_sum}")

# =========== DESCRIPTOR PROTOCOL CHI TIẾT ===========
print("\n=== Descriptor Protocol Details ===")

# __get__(self, instance, owner)
print("__get__(self, instance, owner):")
print("- self: descriptor instance")
print("- instance: object instance hoặc None khi gọi trên class")
print("- owner: class mà descriptor thuộc về")

# __set__(self, instance, value) 
print("\n__set__(self, instance, value):")
print("- self: descriptor instance")
print("- instance: object instance")
print("- value: giá trị được gán")

# __delete__(self, instance)
print("\n__delete__(self, instance):")
print("- self: descriptor instance")
print("- instance: object instance")

# __set_name__(self, owner, name)
print("\n__set_name__(self, owner, name) (Python 3.6+):")
print("- Được gọi khi descriptor được gán cho class attribute")
print("- self: descriptor instance")
print("- owner: class mà descriptor thuộc về")
print("- name: tên của attribute chứa descriptor")

# Demo __set_name__
class DescriptorWithSetName:
    def __set_name__(self, owner, name):
        print(f"__set_name__ called with owner={owner.__name__}, name={name}")
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)
    
    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)

class Demo:
    x = DescriptorWithSetName()
    y = DescriptorWithSetName()

print("\nDemo of __set_name__:")
d = Demo()
d.x = 10
d.y = 20
print(f"d.x: {d.x}, d.y: {d.y}")

# =========== DESCRIPTOR TRONG PYTHON STANDARD LIBRARY ===========
print("\n=== Descriptors in the Python Standard Library ===")

# 1. property
# 2. classmethod và staticmethod
# 3. __slots__ (giới hạn attribute names và sử dụng descriptors để truy cập)
# 4. ABC - Abstract Base Classes
# 5. Enum values

# Ví dụ với __slots__
class PersonWithSlots:
    __slots__ = ['name', 'age']
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Kiểm tra dạng của slot attributes
person_slots = PersonWithSlots("John", 30)
descriptor = type(PersonWithSlots).__dict__['name']
print(f"Slot 'name' is a descriptor: {hasattr(descriptor, '__get__')}")

# =========== ỨNG DỤNG THỰC TẾ ===========
print("\n=== Practical Applications ===")

# 1. Type Conversion & Validation
class TypedField:
    def __init__(self, field_type, default=None):
        self.field_type = field_type
        self.default = default
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, self.default)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.field_type):
            try:
                value = self.field_type(value)  # Attempt conversion
            except (TypeError, ValueError):
                raise TypeError(f"{self.name} must be of type {self.field_type.__name__}")
        setattr(instance, self.private_name, value)

# 2. Unit Conversion
class DistanceField:
    def __init__(self):
        # Private dict để lưu giá trị cho mỗi instance
        self.values = {}
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.values.get(id(instance), 0)
    
    def __set__(self, instance, value):
        self.values[id(instance)] = float(value)
    
    # Methods để truy cập với các đơn vị khác nhau
    def kilometers(self, instance):
        return self.__get__(instance, type(instance))
    
    def miles(self, instance):
        return self.__get__(instance, type(instance)) * 0.621371
    
    def feet(self, instance):
        return self.__get__(instance, type(instance)) * 3280.84

# Ví dụ sử dụng
class Product:
    id = TypedField(int)
    name = TypedField(str, "")
    price = TypedField(float, 0.0)
    
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Route:
    distance = DistanceField()  # km
    
    def __init__(self, distance_km):
        self.distance = distance_km
    
    def get_distance_km(self):
        return self.distance  # hoặc self.__class__.distance.kilometers(self)
    
    def get_distance_miles(self):
        return self.__class__.distance.miles(self)
    
    def get_distance_feet(self):
        return self.__class__.distance.feet(self)

# Test TypedField
print("Testing TypedField for automatic conversion:")
try:
    # Automatic conversion
    product = Product("100", "Laptop", "999.99")
    print(f"Product: ID={product.id} ({type(product.id).__name__}), "
          f"Name={product.name} ({type(product.name).__name__}), "
          f"Price={product.price} ({type(product.price).__name__})")
    
    # Type error
    product.price = "invalid"
except TypeError as e:
    print(f"Type Error: {e}")

# Test DistanceField
print("\nTesting DistanceField for unit conversion:")
route = Route(100)  # 100 km
print(f"Distance in km: {route.get_distance_km()}")
print(f"Distance in miles: {route.get_distance_miles():.2f}")
print(f"Distance in feet: {route.get_distance_feet():.2f}")

# =========== BEST PRACTICES ===========
print("\n=== Best Practices ===")

print("1. Sử dụng property cho mục đích đơn giản")
print("2. Dùng descriptor khi cần hành vi tương tự trên nhiều attributes")
print("3. Cẩn thận với các descriptor chia sẻ state - mỗi instance nên có state riêng")
print("4. Sử dụng __set_name__ (Python 3.6+) để lấy tên attribute tự động")
print("5. Consider weak references for caching to prevent memory leaks")
print("6. Kết hợp descriptors với metaclasses cho các use cases phức tạp")

# =========== SO SÁNH VỚI JAVASCRIPT ===========
print("\n=== So sánh với JavaScript ===")

print("JavaScript:")
print("- Sử dụng Object.defineProperty/ Object.defineProperties")
print("- Getters và setters với cú pháp get/set")
print("- Proxy objects để chặn và tùy chỉnh property access")
print("- Không có cơ chế nào tương đương với non-data descriptors")

print("\nVí dụ JavaScript getter/setter:")
print("""
class Person {
  constructor(name) {
    this._name = name;
  }
  
  get name() {
    console.log('getter called');
    return this._name;
  }
  
  set name(value) {
    console.log('setter called');
    if (typeof value !== 'string') {
      throw new TypeError('Name must be a string');
    }
    this._name = value;
  }
}
""")

print("\nVí dụ JavaScript Proxy:")
print("""
const handler = {
  get(target, prop) {
    console.log(`Getting ${prop}`);
    return target[prop];
  },
  set(target, prop, value) {
    console.log(`Setting ${prop} to ${value}`);
    target[prop] = value;
    return true;
  }
};

const person = new Proxy({}, handler);
person.name = 'John';  // logs: Setting name to John
console.log(person.name);  // logs: Getting name, John
""")

print("\nPython's descriptors thường mạnh mẽ và linh hoạt hơn JavaScript's property definitions:"
      "\n- Hoạt động ở class level, không chỉ instance level"
      "\n- Hỗ trợ tất cả các hoạt động (get, set, delete)"
      "\n- Dễ dàng tái sử dụng trên nhiều classes khác nhau"
      "\n- Tích hợp tốt hơn với mô hình OOP của Python")