'''
Advanced Python Functions cho JavaScript Developers
==============================================

Các tính năng hàm nâng cao trong Python so với JavaScript.
'''

# =========== CLOSURES VÀ HIGHER-ORDER FUNCTIONS ===========
# Tương tự JavaScript nhưng có một số điểm khác biệt

def create_counter(start=0):
    """Closure ví dụ - tạo một bộ đếm"""
    # Biến tự do (free variable) trong lexical scope
    count = start
    
    def increment(step=1):
        # Sử dụng từ khóa nonlocal để thay đổi biến bên ngoài
        nonlocal count
        count += step
        return count
    
    return increment

# Tạo counter
counter1 = create_counter(10)
print(f"Counter1: {counter1()}")  # 11
print(f"Counter1: {counter1()}")  # 12
print(f"Counter1: {counter1(5)}")  # 17

# Tạo counter khác
counter2 = create_counter()
print(f"Counter2: {counter2()}")  # 1
print(f"Counter2: {counter2()}")  # 2

# So sánh với JavaScript:
# function createCounter(start = 0) {
#   let count = start;
#   return function increment(step = 1) {
#     count += step;
#     return count;
#   };
# }

# =========== FUNCTION COMPOSITION ===========
# Kết hợp các hàm với nhau

def compose(*functions):
    """Kết hợp nhiều hàm thành một hàm duy nhất"""
    def composed_function(x):
        result = x
        # Áp dụng mỗi hàm theo thứ tự ngược (phải sang trái)
        for f in reversed(functions):
            result = f(result)
        return result
    return composed_function

# Các hàm để kết hợp
def double(x): return x * 2
def increment(x): return x + 1
def square(x): return x ** 2

# Tạo hàm kết hợp (double → increment → square)
transformed = compose(square, increment, double)
print(f"transformed(5): {transformed(5)}")  # square(increment(double(5))) = square(increment(10)) = square(11) = 121

# Thứ tự quan trọng
transformed2 = compose(double, increment, square)
print(f"transformed2(5): {transformed2(5)}")  # double(increment(square(5))) = double(increment(25)) = double(26) = 52

# So sánh với JavaScript:
# const compose = (...functions) => x => 
#   functions.reduceRight((result, f) => f(result), x);

# =========== PARTIAL APPLICATION VÀ CURRYING ===========
# Partial application - cung cấp một phần các đối số cho hàm

from functools import partial

def power(base, exponent):
    return base ** exponent

# Tạo hàm mới với base đã được cung cấp trước (partial application)
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(f"square(4): {square(4)}")  # 16
print(f"cube(3): {cube(3)}")  # 27

# Currying - chuyển đổi hàm nhận nhiều đối số thành chuỗi các hàm nhận đối số đơn
def curry_power(base):
    def with_exponent(exponent):
        return base ** exponent
    return with_exponent

# Sử dụng hàm đã curry
power_of_2 = curry_power(2)
print(f"2^8: {power_of_2(8)}")  # 256
print(f"2^10: {power_of_2(10)}")  # 1024

power_of_3 = curry_power(3)
print(f"3^3: {power_of_3(3)}")  # 27

# So sánh với JavaScript:
# // Currying
# const curryPower = base => exponent => base ** exponent;
# const powerOf2 = curryPower(2);
# console.log(`2^8: ${powerOf2(8)}`); // 256

# =========== DECORATORS NÂNG CAO ===========
# Decorator với tham số

def repeat(times):
    """Decorator nhận tham số - để hàm chạy nhiều lần"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    return f"Hello, {name}!"

print(f"Greet 3 times: {greet('Alice')}")

# Nested decorators (stack nhiều decorator)
def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def format_text(text):
    return text

print(format_text("Python is fun"))  # <b><i>Python is fun</i></b>

# Thứ tự quan trọng
@italic
@bold
def format_text2(text):
    return text

print(format_text2("Python is fun"))  # <i><b>Python is fun</b></i>

# So sánh với JavaScript:
# // Decorator trong JS cần sử dụng các thư viện hoặc cài đặt babel
# function repeat(times) {
#   return function(target, name, descriptor) {
#     const original = descriptor.value;
#     descriptor.value = function(...args) {
#       const results = [];
#       for (let i = 0; i < times; i++) {
#         results.push(original.apply(this, args));
#       }
#       return results;
#     };
#     return descriptor;
#   };
# }

# =========== FUNCTION INTROSPECTION ===========
# Xem xét các thuộc tính của hàm

def add(a, b=0):
    """Add two numbers and return the result."""
    return a + b

# Xem doc string
print(f"Doc string: {add.__doc__}")

# Xem tên hàm
print(f"Function name: {add.__name__}")

# Xem mã nguồn (nếu có)
import inspect
print(f"Source code:\n{inspect.getsource(add)}")

# Xem signature (chữ ký hàm)
sig = inspect.signature(add)
print(f"Signature: {sig}")
print(f"Parameters: {list(sig.parameters.items())}")

# Kiểm tra giá trị mặc định
print(f"Default for b: {sig.parameters['b'].default}")

# =========== FUNCTION ANNOTATIONS ===========
# Type hints nâng cao (PEP 484)

from typing import List, Dict, Callable, TypeVar, Union, Optional

T = TypeVar('T')  # Kiểu generic

def filter_list(items: List[T], condition: Callable[[T], bool]) -> List[T]:
    """Filter a list using a condition function."""
    return [item for item in items if condition(item)]

# Sử dụng hàm với type hints
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = filter_list(numbers, lambda x: x % 2 == 0)
print(f"Even numbers: {even_numbers}")

# Union types (có thể là int hoặc str)
def process_id(user_id: Union[int, str]) -> str:
    if isinstance(user_id, int):
        return f"INT-{user_id}"
    else:
        return f"STR-{user_id}"

print(process_id(123))      # INT-123
print(process_id("abc"))    # STR-abc

# Optional - có thể là None
def get_user_name(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)  # None nếu user_id không tồn tại

print(f"User 1: {get_user_name(1)}")
print(f"User 3: {get_user_name(3)}")

# Kiểm tra type hints trong runtime
# pip install mypy
# Run: mypy your_file.py

# =========== FUNCTOOLS MODULE ===========
# Module functools cung cấp các công cụ hoạt động với hàm

from functools import lru_cache, reduce, wraps

# lru_cache - nhớ kết quả của các lần gọi trước (memoization)
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

import time

# Đo thời gian tính fibonacci
start = time.time()
print(f"fibonacci(35): {fibonacci(35)}")
end = time.time()
print(f"Time taken: {end - start:.6f} seconds")

# Thử lại - sẽ nhanh hơn vì kết quả được cache
start = time.time()
print(f"fibonacci(35) (cached): {fibonacci(35)}")
end = time.time()
print(f"Time taken: {end - start:.6f} seconds")

# reduce - tương tự Array.reduce trong JavaScript
product = reduce(lambda x, y: x * y, [1, 2, 3, 4, 5])
print(f"Product of numbers: {product}")  # 120

# wraps - bảo toàn thông tin của hàm gốc khi sử dụng decorator
def log_function_call(func):
    @wraps(func)  # Giữ nguyên metadata của func
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_function_call
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

print(calculate_sum(5, 3))
print(f"Function name: {calculate_sum.__name__}")      # Nếu không có @wraps, sẽ in ra "wrapper"
print(f"Documentation: {calculate_sum.__doc__}")       # Nếu không có @wraps, sẽ mất doc string

# =========== OPERATOR MODULE ===========
# Module operator cung cấp các hàm cho các toán tử

import operator

# Các toán tử số học
print(f"5 + 3 = {operator.add(5, 3)}")
print(f"5 - 3 = {operator.sub(5, 3)}")
print(f"5 * 3 = {operator.mul(5, 3)}")
print(f"5 / 3 = {operator.truediv(5, 3)}")

# Toán tử so sánh
print(f"5 > 3: {operator.gt(5, 3)}")
print(f"5 <= 3: {operator.le(5, 3)}")
print(f"5 == 3: {operator.eq(5, 3)}")

# Truy cập thuộc tính và item
user = {"name": "Alice", "age": 30}
print(f"User name: {operator.getitem(user, 'name')}")

class Person:
    def __init__(self, name):
        self.name = name

alice = Person("Alice")
print(f"Person name: {operator.attrgetter('name')(alice)}")

# Kết hợp với các hàm khác
items = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 35}]
# Sắp xếp theo tuổi
sorted_by_age = sorted(items, key=operator.itemgetter('age'))
print(f"Sorted by age: {sorted_by_age}")

# Sắp xếp theo tên
sorted_by_name = sorted(items, key=operator.itemgetter('name'))
print(f"Sorted by name: {sorted_by_name}")

# itemgetter và attrgetter trả về callable objects
get_name = operator.itemgetter('name')
print(f"Names: {list(map(get_name, items))}")  # ['Alice', 'Bob', 'Charlie']