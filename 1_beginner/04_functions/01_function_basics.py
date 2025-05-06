'''
Python Functions cho JavaScript Developers
========================================

Hàm trong Python tương tự như JavaScript, nhưng có một số khác biệt đáng chú ý.
'''

# =========== ĐỊNH NGHĨA HÀM CƠ BẢN ===========
# Định nghĩa hàm trong Python dùng từ khóa def

def greet():
    print("Hello, World!")

# Gọi hàm
greet()  # Hello, World!

# So sánh với JavaScript:
# function greet() {
#     console.log("Hello, World!");
# }
# greet();

# =========== HÀM CÓ THAM SỐ ===========
# Tham số hàm tương tự như JavaScript

def greet_person(name):
    print(f"Hello, {name}!")

greet_person("John")  # Hello, John!

# Tham số với giá trị mặc định (tương tự default parameters trong JS)
def greet_with_time(name, time="morning"):
    print(f"Good {time}, {name}!")

greet_with_time("Alice")         # Good morning, Alice!
greet_with_time("Bob", "evening")  # Good evening, Bob!

# So sánh với JavaScript:
# function greetWithTime(name, time = "morning") {
#     console.log(`Good ${time}, ${name}!`);
# }

# =========== RETURN VALUE ===========
# Trả về giá trị từ hàm

def sum_numbers(a, b):
    return a + b

result = sum_numbers(5, 3)
print(f"Sum: {result}")  # Sum: 8

# Return nhiều giá trị (không có trong JavaScript)
def get_user_info():
    name = "John"
    age = 30
    return name, age  # Trả về tuple

# Unpacking kết quả
username, user_age = get_user_info()
print(f"Name: {username}, Age: {user_age}")  # Name: John, Age: 30

# So sánh với JavaScript:
# function getUserInfo() {
#     const name = "John";
#     const age = 30;
#     return [name, age]; // Hoặc return {name, age};
# }
# const [username, userAge] = getUserInfo();

# =========== THAM SỐ POSITIONAL VÀ KEYWORD ===========

def display_info(name, age, city):
    print(f"Name: {name}, Age: {age}, City: {city}")

# Gọi với tham số positional (vị trí)
display_info("John", 30, "New York")

# Gọi với tham số keyword (tên)
display_info(age=30, name="John", city="New York")  # Thứ tự không quan trọng khi dùng keyword

# Kết hợp cả hai (positional phải đặt trước keyword)
display_info("John", city="New York", age=30)

# =========== *ARGS VÀ **KWARGS ===========
# Tương tự rest parameters và spread operators trong JavaScript

# *args - nhận vào nhiều tham số positional
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(f"Sum of 1, 2, 3: {sum_all(1, 2, 3)}")          # 6
print(f"Sum of 1, 2, 3, 4, 5: {sum_all(1, 2, 3, 4, 5)}") # 15

# So sánh với JavaScript:
# function sumAll(...args) {
#     return args.reduce((total, num) => total + num, 0);
# }

# **kwargs - nhận vào nhiều tham số keyword
def display_user_data(**kwargs):
    print("User data:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

display_user_data(name="John", age=30, city="New York", job="Developer")

# So sánh với JavaScript:
# function displayUserData(userData) {
#     console.log("User data:");
#     for (const [key, value] of Object.entries(userData)) {
#         console.log(`${key}: ${value}`);
#     }
# }
# displayUserData({name: "John", age: 30, city: "New York", job: "Developer"});

# Kết hợp *args và **kwargs
def combined_example(required_arg, *args, **kwargs):
    print(f"Required: {required_arg}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

combined_example("Hello", 1, 2, 3, name="John", age=30)

# =========== LAMBDA FUNCTIONS ===========
# Tương tự arrow functions trong JavaScript, nhưng ngắn gọn hơn

# Lambda cơ bản
square = lambda x: x * x
print(f"Square of 5: {square(5)}")  # 25

# So sánh với JavaScript:
# const square = x => x * x;

# Lambda với nhiều tham số
add = lambda x, y: x + y
print(f"5 + 3 = {add(5, 3)}")  # 8

# So sánh với JavaScript:
# const add = (x, y) => x + y;

# Lambda thường dùng trong các hàm như map, filter
numbers = [1, 2, 3, 4, 5]

# Map với lambda
squared = list(map(lambda x: x * x, numbers))
print(f"Squared: {squared}")  # [1, 4, 9, 16, 25]

# So sánh với JavaScript:
# const squared = numbers.map(x => x * x);

# Filter với lambda
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")  # [2, 4]

# So sánh với JavaScript:
# const evens = numbers.filter(x => x % 2 === 0);

# =========== SCOPE (PHẠM VI) ===========
# Python có global scope và local scope, nhưng không có block scope như JS

global_var = "I'm global"

def test_scope():
    local_var = "I'm local"
    print(global_var)  # Có thể truy cập biến global
    print(local_var)   # Có thể truy cập biến local

test_scope()
# print(local_var)  # Error: local_var không tồn tại ngoài hàm

# Thay đổi biến global từ trong hàm
def modify_global():
    global global_var
    global_var = "Modified global"

modify_global()
print(global_var)  # "Modified global"

# So sánh với JavaScript:
# let globalVar = "I'm global";
# function testScope() {
#     let localVar = "I'm local";
#     console.log(globalVar);
#     console.log(localVar);
# }

# =========== NESTED FUNCTIONS ===========
# Hàm lồng nhau và closure tương tự JavaScript

def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

add_five = outer_function(5)
print(f"5 + 3 = {add_five(3)}")  # 8

# So sánh với JavaScript:
# function outerFunction(x) {
#     return function innerFunction(y) {
#         return x + y;
#     };
# }
# const addFive = outerFunction(5);

# =========== DECORATORS ===========
# Decorators là một tính năng đặc biệt của Python, tương tự Higher-order functions trong JS

# Định nghĩa decorator
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

# Sử dụng decorator
@my_decorator
def say_hello():
    print("Hello!")

say_hello()

# Tương đương với:
# def say_hello():
#     print("Hello!")
# say_hello = my_decorator(say_hello)

# So sánh với JavaScript:
# function myDecorator(func) {
#     return function() {
#         console.log("Something is happening before the function is called.");
#         func();
#         console.log("Something is happening after the function is called.");
#     };
# }
# const sayHello = myDecorator(function() {
#     console.log("Hello!");
# });

# =========== TYPE HINTS (từ Python 3.5+) ===========
# Tương tự TypeScript trong hệ sinh thái JavaScript

def calculate_area(radius: float) -> float:
    """Tính diện tích hình tròn."""
    return 3.14 * radius * radius

area = calculate_area(5.0)
print(f"Area: {area}")

# Nhiều kiểu dữ liệu phức tạp hơn
from typing import List, Dict, Tuple, Optional

def process_users(users: List[Dict[str, str]]) -> Tuple[int, List[str]]:
    count = len(users)
    names = [user["name"] for user in users]
    return count, names

def get_user(user_id: int) -> Optional[Dict[str, str]]:
    # Optional nghĩa là có thể trả về None hoặc Dict
    users = {1: {"name": "John"}, 2: {"name": "Alice"}}
    return users.get(user_id)

# So sánh với TypeScript:
# function calculateArea(radius: number): number {
#     return 3.14 * radius * radius;
# }
# 
# function processUsers(users: {name: string}[]): [number, string[]] {
#     const count = users.length;
#     const names = users.map(user => user.name);
#     return [count, names];
# }
# 
# function getUser(userId: number): {name: string} | null {
#     const users = {1: {name: "John"}, 2: {name: "Alice"}};
#     return users[userId] || null;
# }