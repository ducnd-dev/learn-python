'''
Functional Programming trong Python cho JavaScript Developers
=========================================================

Lập trình hàm (Functional Programming) là một paradigm tập trung vào việc sử dụng
các hàm thuần túy (pure functions), tránh trạng thái thay đổi (mutable state),
và dữ liệu bất biến (immutable data). Python hỗ trợ các khái niệm functional
programming mặc dù không phải là ngôn ngữ functional thuần túy.

JavaScript cũng có khả năng functional nên nhiều khái niệm sẽ quen thuộc.
'''

# =========== FIRST-CLASS FUNCTIONS ===========
print("=== First-class Functions ===")

# Functions là first-class objects trong Python
def greet(name):
    return f"Hello, {name}!"

# Gán hàm cho biến
say_hello = greet
print(f"Function assigned to variable: {say_hello('Alice')}")

# Truyền hàm như tham số
def execute_function(func, arg):
    return func(arg)

result = execute_function(greet, "Bob")
print(f"Function as argument: {result}")

# Return hàm từ hàm khác
def create_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = create_multiplier(2)
triple = create_multiplier(3)

print(f"Returned function (double): {double(5)}")
print(f"Returned function (triple): {triple(5)}")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// JavaScript cũng có first-class functions
function greet(name) {
  return `Hello, ${name}!`;
}

const sayHello = greet;

function executeFunction(func, arg) {
  return func(arg);
}

function createMultiplier(factor) {
  return function(number) {
    return number * factor;
  };
}

const double = createMultiplier(2);
""")

# =========== PURE FUNCTIONS ===========
print("\n=== Pure Functions ===")

# Hàm thuần túy (Pure Function)
def add_pure(x, y):
    return x + y

print(f"Pure function: 3 + 5 = {add_pure(3, 5)}")

# Hàm không thuần túy (Impure Function)
total = 0

def add_impure(x):
    global total
    total += x
    return total

print(f"Impure function first call: {add_impure(3)}")
print(f"Impure function second call: {add_impure(5)}")  # Side effect: kết quả khác nhau với cùng input

print("\nĐặc điểm pure functions:")
print("1. Kết quả chỉ phụ thuộc vào input, không có side effects")
print("2. Cùng input luôn cho cùng output")
print("3. Không thay đổi trạng thái bên ngoài hàm")
print("4. Dễ test, debug, và tối ưu hóa")

# =========== HIGHER-ORDER FUNCTIONS ===========
print("\n=== Higher-Order Functions ===")

# Higher-order function: Nhận hàm làm tham số hoặc return một hàm
# Python có sẵn nhiều higher-order functions

# map: áp dụng hàm cho mỗi phần tử
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f"map() with lambda: {squared}")

# filter: lọc các phần tử theo điều kiện
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"filter() with lambda: {evens}")

# reduce: giảm list về một giá trị
from functools import reduce
sum_all = reduce(lambda acc, val: acc + val, numbers, 0)
print(f"reduce() with lambda: {sum_all}")

# Custom higher-order function
def apply_operation(numbers, operation):
    return [operation(x) for x in numbers]

result = apply_operation(numbers, lambda x: x * 10)
print(f"Custom higher-order function: {result}")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// JavaScript cũng có built-in higher-order functions
const numbers = [1, 2, 3, 4, 5];

// map
const squared = numbers.map(x => x ** 2);

// filter
const evens = numbers.filter(x => x % 2 === 0);

// reduce
const sumAll = numbers.reduce((acc, val) => acc + val, 0);
""")

# =========== LAMBDA FUNCTIONS ===========
print("\n=== Lambda Functions ===")

# Lambda functions: hàm ẩn danh, inline
# Cú pháp: lambda <params>: <expression>

# Lambda đơn giản
square = lambda x: x ** 2
print(f"Simple lambda: {square(5)}")

# Lambda với multiple parameters
multiply = lambda x, y: x * y
print(f"Multi-parameter lambda: {multiply(4, 5)}")

# Lambda trong sort
pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
pairs.sort(key=lambda pair: pair[1])  # Sort by second element 
print(f"Sorting with lambda: {pairs}")

# Lambda và list comprehension
cubes = [(lambda x: x**3)(i) for i in range(1, 6)]
print(f"Lambda in list comprehension: {cubes}")

# Giới hạn của lambda
print("\nGiới hạn của lambda:")
print("- Chỉ chứa một expression (không có statements)")
print("- Không thể chứa assignments hoặc multi-line code")
print("- Nên sử dụng def cho các hàm phức tạp")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// Arrow functions trong JavaScript tương tự lambda
const square = x => x ** 2;

const multiply = (x, y) => x * y;

// Sorting
const pairs = [[1, 'one'], [3, 'three'], [2, 'two']];
pairs.sort((a, b) => a[1].localeCompare(b[1]));

// JavaScript's arrow functions linh hoạt hơn lambda trong Python
// Arrow functions có thể có block body và multiple statements
const complex = x => {
  const temp = x * 2;
  return temp + 1;
};
""")

# =========== CLOSURES ===========
print("\n=== Closures ===")

# Closure: function "nhớ" môi trường nơi nó được tạo
def create_counter():
    count = 0
    def increment():
        nonlocal count  # Khai báo biến từ outer scope
        count += 1
        return count
    return increment

# Tạo các counters độc lập
counter1 = create_counter()
counter2 = create_counter()

print(f"Counter1: {counter1()}, {counter1()}, {counter1()}")  # 1, 2, 3
print(f"Counter2: {counter2()}")  # 1 (counter2 độc lập với counter1)

# Closure giữ tham chiếu đến biến, không phải giá trị
def create_multipliers():
    multipliers = []
    for i in range(1, 4):
        # Dùng default argument để "capture" giá trị hiện tại của i
        multipliers.append(lambda x, i=i: i * x)
    return multipliers

mult_functions = create_multipliers()
print(f"Multiplier results: {[fn(10) for fn in mult_functions]}")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// Closures in JavaScript
function createCounter() {
  let count = 0;
  return function() {
    count += 1;
    return count;
  };
}

// JavaScript closure "gotcha" với vòng lặp
// (khác với Python's default arguments)
function createMultipliers() {
  const multipliers = [];
  for (let i = 1; i < 4; i++) {
    // Trong ES6, let tạo một biến mới cho mỗi lần lặp
    multipliers.push(x => i * x);
  }
  return multipliers;
}
""")

# =========== PARTIAL APPLICATION & CURRYING ===========
print("\n=== Partial Application & Currying ===")

# Partial application: tạo hàm mới có một số arguments cố định
from functools import partial

def multiply(x, y):
    return x * y

# Tạo hàm mới với x=2
double = partial(multiply, 2)
print(f"Partial function: {double(5)}")  # 2 * 5 = 10

# Partial với keyword arguments
def log_message(level, message):
    return f"[{level.upper()}] {message}"

error_log = partial(log_message, level="ERROR")
print(f"Partial with keyword args: {error_log('Disk full')}")

# Currying: chuyển đổi hàm có nhiều tham số thành chuỗi hàm đơn tham số
def curried_multiply(x):
    def inner(y):
        return x * y
    return inner

triple = curried_multiply(3)
print(f"Curried function: {triple(4)}")  # 3 * 4 = 12

# Curry nhiều tham số
def curried_log(level):
    def add_message(message):
        def add_detail(detail):
            return f"[{level.upper()}] {message}: {detail}"
        return add_detail
    return add_message

error = curried_log("ERROR")
db_error = error("Database")
print(f"Multiple currying: {db_error('Connection failed')}")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// Currying in JavaScript
const curriedMultiply = x => y => x * y;
const triple = curriedMultiply(3);
console.log(triple(4));  // 12

// Partial application with bind
function multiply(x, y) {
  return x * y;
}
const double = multiply.bind(null, 2);
console.log(double(5));  // 10
""")

# =========== IMMUTABILITY ===========
print("\n=== Immutability ===")

# Python mutable vs immutable types
print("Immutable types: int, float, str, tuple, frozenset")
print("Mutable types: list, dict, set")

# Thay đổi state (cách không functional)
def add_to_list(lst, item):
    lst.append(item)  # Thay đổi list gốc (side effect)
    return lst

original_list = [1, 2, 3]
modified_list = add_to_list(original_list, 4)
print(f"Original list (mutated): {original_list}")  # [1, 2, 3, 4]
print(f"Modified list (same object): {modified_list}")  # [1, 2, 3, 4]
print(f"Are they the same object? {original_list is modified_list}")  # True

# Phong cách functional: không thay đổi input
def add_to_list_functional(lst, item):
    return lst + [item]  # Tạo list mới, không thay đổi list gốc

original_list = [1, 2, 3]
new_list = add_to_list_functional(original_list, 4)
print(f"Original list (unchanged): {original_list}")  # [1, 2, 3]
print(f"New list: {new_list}")  # [1, 2, 3, 4]
print(f"Are they the same object? {original_list is new_list}")  # False

# Đóng băng cấu trúc dữ liệu dùng tuple
mutable_point = [1, 2]  # Có thể thay đổi
immutable_point = (1, 2)  # Không thể thay đổi

try:
    immutable_point[0] = 3  # Raises TypeError
except TypeError as e:
    print(f"Tuples are immutable: {e}")

# namedtuple - immutable, nhưng có thể truy cập bằng tên
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(f"Named tuple: {p.x}, {p.y}")  # 1, 2

# Tạo phiên bản mới từ namedtuple cũ
p2 = p._replace(x=3)
print(f"Original point: {p}")  # Point(x=1, y=2)
print(f"New point: {p2}")  # Point(x=3, y=2)

# =========== RECURSION ===========
print("\n=== Recursion ===")

# Recursion là kỹ thuật phổ biến trong functional programming
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"Factorial of 5: {factorial(5)}")  # 120

# Fibonacci series
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"Fibonacci(7): {fibonacci(7)}")  # 13

# Recursion limitations
print("\nRecursion limitations:")
print("1. Python's default recursion limit is quite low (~1000)")
print("2. No tail-call optimization (có thể dẫn đến stack overflow)")
print("3. Usually slower than iteration in Python")

# Minh họa recursion limit
import sys
print(f"Default recursion limit: {sys.getrecursionlimit()}")

# =========== FUNCTION COMPOSITION ===========
print("\n=== Function Composition ===")

# Kết hợp các hàm để tạo hàm mới
def compose(f, g):
    return lambda x: f(g(x))

def double(x):
    return x * 2

def increment(x):
    return x + 1

# Compose: double after increment
double_after_increment = compose(double, increment)
print(f"double(increment(5)): {double_after_increment(5)}")  # double(5+1) = 12

# Nhiều hàm
def compose_multiple(*functions):
    def inner(x):
        result = x
        for f in reversed(functions):  # Áp dụng từ phải sang trái
            result = f(result)
        return result
    return inner

# Compose: double after increment after square
pipeline = compose_multiple(double, increment, lambda x: x**2)
print(f"double(increment(square(3))): {pipeline(3)}")  # double(increment(9)) = 20

# Pipe: Similar to compose but left-to-right
def pipe_multiple(*functions):
    def inner(x):
        result = x
        for f in functions:  # Áp dụng từ trái sang phải
            result = f(result)
        return result
    return inner

# Pipe: square after increment after double
pipeline = pipe_multiple(double, increment, lambda x: x**2)
print(f"square(increment(double(3))): {pipeline(3)}")  # square(double(3)+1) = 49

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// Compose trong JS
const compose = (f, g) => x => f(g(x));

// Pipe trong JS
const pipe = (...fns) => x => fns.reduce((y, f) => f(y), x);

// Sử dụng
const double = x => x * 2;
const increment = x => x + 1;
const square = x => x * x;

const result = pipe(double, increment, square)(3);
console.log(result);  // 49
""")

# =========== FUNCTIONAL TOOLS IN PYTHON ===========
print("\n=== Functional Tools in Python ===")

# Một số công cụ quan trọng để lập trình hàm trong Python
print("Key functional tools in Python:")
print("- map(), filter(), reduce()")
print("- lambda")
print("- list/dict/set comprehensions")
print("- functools module")
print("- itertools module")
print("- operator module")

from functools import lru_cache, partial, reduce

# Example: lru_cache for memoization
@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n-1) + fib_memo(n-2)

print(f"fibonacci(30) with memoization: {fib_memo(30)}")  # Much faster than naive recursion

# operator module provides function versions of operators
import operator

numbers = [1, 2, 3, 4, 5]
product = reduce(operator.mul, numbers, 1)
print(f"Product of numbers using operator.mul: {product}")  # 120

# itemgetter, attrgetter for extracting data
from operator import itemgetter, attrgetter

people = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
names = list(map(itemgetter('name'), people))
print(f"Names extracted with itemgetter: {names}")

# =========== LIST COMPREHENSIONS ===========
print("\n=== List/Dict/Set Comprehensions ===")

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
print(f"List comprehension: {squares}")

# Dict comprehension
square_map = {x: x**2 for x in range(5)}
print(f"Dict comprehension: {square_map}")

# Set comprehension
unique_squares = {x**2 for x in range(-5, 5)}
print(f"Set comprehension: {unique_squares}")

# Nested comprehensions
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [x for row in matrix for x in row]
print(f"Flattened matrix using nested comprehension: {flattened}")

# Comprehensions vs functional tools
print("\nComprehensions often replace map/filter in Python:")
print("- [x**2 for x in range(10)]  # list comprehension")
print("- list(map(lambda x: x**2, range(10)))  # map")
print("- [x for x in range(10) if x%2==0]  # filter in comprehension")
print("- list(filter(lambda x: x%2==0, range(10)))  # filter")

# So sánh với JavaScript:
print("\nSo sánh với JavaScript:")
print("""
// JavaScript array methods
const squares = Array.from({length: 10}, (_, i) => i).filter(x => x % 2 === 0).map(x => x**2);

// ES2023 introduced "array comprehensions" nhưng bị loại bỏ
// Có thể dùng array methods chaining thay thế
""")

# =========== GENERATORS & LAZY EVALUATION ===========
print("\n=== Generators & Lazy Evaluation ===")

# Lazy evaluation: evaluation chỉ diễn ra khi cần thiết
# Generators là cách Python triển khai lazy evaluation

# Generator function with yield
def count_up_to(n):
    i = 0
    while i < n:
        yield i
        i += 1

# Using generator - values generated on-demand
counter = count_up_to(5)
print(f"Generator object: {counter}")
print(f"Next value: {next(counter)}")  # 0
print(f"Next value: {next(counter)}")  # 1

# Consuming all values
print(f"All remaining values: {list(counter)}")  # [2, 3, 4]

# Generator expressions: like list comprehensions but lazy
even_squares = (x**2 for x in range(10) if x % 2 == 0)
print(f"Generator expression: {even_squares}")
print(f"First 3 even squares: {next(even_squares)}, {next(even_squares)}, {next(even_squares)}")

# Infinite sequences with generators
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib_gen = fibonacci_generator()
print("First 10 Fibonacci numbers:")
for _ in range(10):
    print(next(fib_gen), end=" ")
print()

# Benefits of lazy evaluation:
print("\nBenefits of lazy evaluation:")
print("1. Memory efficiency - only process what's needed")
print("2. Ability to work with infinite sequences")
print("3. Processing large datasets without loading all into memory")
print("4. Separation of generation and consumption logic")

# =========== IMMUTABLE DATA STRUCTURES ===========
print("\n=== Third-party Immutable Data Structures ===")

print("Python has libraries for immutable data structures:")
print("- pyrsistent: Efficient persistent data structures")
print("- immutables: High-performance immutable mappings")

print("""
# Example with pyrsistent
from pyrsistent import pvector, pmap, s

# Immutable vector
v1 = pvector([1, 2, 3])
v2 = v1.append(4)  # v1 is unchanged, new vector returned
print(f"v1: {v1}, v2: {v2}")

# Immutable map
m1 = pmap({"a": 1, "b": 2})
m2 = m1.set("c", 3)  # m1 is unchanged
print(f"m1: {m1}, m2: {m2}")
""")

# =========== FUNCTIONAL PROGRAMMING STYLE ===========
print("\n=== Functional Programming Style in Python ===")

# Putting it all together - functional style

# Input data
transactions = [
    {"type": "purchase", "amount": 10.0, "currency": "USD"},
    {"type": "sale", "amount": 5.0, "currency": "EUR"},
    {"type": "purchase", "amount": 7.0, "currency": "EUR"},
    {"type": "purchase", "amount": 15.0, "currency": "USD"},
    {"type": "sale", "amount": 3.0, "currency": "USD"},
]

# Currency conversion rates
conversion_rates = {"USD": 1.0, "EUR": 1.09}

# Step 1: Pure function to convert amount to USD
def to_usd(transaction):
    currency = transaction["currency"]
    amount = transaction["amount"]
    rate = conversion_rates.get(currency, 1.0)
    return {**transaction, "amount_usd": amount * rate}

# Step 2: Pure function to categorize transaction
def categorize(transaction):
    amount = transaction["amount_usd"]
    if amount < 5.0:
        category = "small"
    elif amount < 10.0:
        category = "medium"
    else:
        category = "large"
    return {**transaction, "category": category}

# Step 3: Filter to purchases only
def is_purchase(transaction):
    return transaction["type"] == "purchase"

# Functional pipeline
def analyze_transactions(transactions):
    # Convert to USD
    transactions_usd = map(to_usd, transactions)
    
    # Filter to purchases
    purchases = filter(is_purchase, transactions_usd)
    
    # Categorize transactions
    categorized = map(categorize, purchases)
    
    return list(categorized)

# Execute pipeline
result = analyze_transactions(transactions)
print("Analyzed transactions (functional style):")
for transaction in result:
    print(f" - {transaction['category']} purchase of {transaction['amount_usd']:.2f} USD (original: {transaction['amount']} {transaction['currency']})")

# Alternative with composition
def analyze_with_composition(transactions):
    pipeline = compose_multiple(
        lambda txs: list(map(categorize, txs)),
        lambda txs: filter(is_purchase, txs),
        lambda txs: map(to_usd, txs)
    )
    return pipeline(transactions)

# =========== BEST PRACTICES FOR FUNCTIONAL PYTHON ===========
print("\n=== Best Practices for Functional Programming in Python ===")

print("1. Prefer pure functions whenever possible")
print("2. Use list/dict/set comprehensions for clarity")
print("3. Leverage built-in functions like map, filter, sorted")
print("4. Use immutable data structures (tuples, frozensets)")
print("5. Use higher-order functions for abstraction")
print("6. Use generators for lazy evaluation and memory efficiency")
print("7. Consider tools like itertools and functools")
print("8. Avoid overusing lambda for complex logic")
print("9. Remember Python is multi-paradigm - use the approach that fits best")
print("10. Use type hints to clarify function contracts")

# =========== TRADEOFFS: FUNCTIONAL VS IMPERATIVE ===========
print("\n=== Tradeoffs: Functional vs Imperative ===")

print("Advantages of Functional Programming:")
print("1. More predictable, easier to test and debug")
print("2. Easier to reason about and understand")
print("3. Better for concurrent and parallel execution")
print("4. Less prone to side effects and bugs")
print("5. Often more declarative and concise")

print("\nDisadvantages in Python:")
print("1. Can be less performant (copying vs. mutating)")
print("2. Python lacks tail-call optimization")
print("3. Can be less intuitive for some problems")
print("4. Functional style can be verbose in Python")
print("5. Python's standard library is often imperative")

print("\nConclusion:")
print("Python supports a functional style but isn't a functional language.")
print("Use functional concepts where they improve your code, but don't")
print("force functional patterns where imperative or OOP approaches work better.")