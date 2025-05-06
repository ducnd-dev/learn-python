'''
Python Generators cho JavaScript Developers
========================================

Generator là một loại iterator đặc biệt trong Python, cho phép tạo ra giá trị
theo demand (khi cần) thay vì tạo sẵn tất cả trong bộ nhớ.

JavaScript từ ES6 cũng có khái niệm generator, và nó khá tương tự với Python.
'''

# =========== GENERATORS CƠ BẢN ===========
# Generator function trả về generator object

def count_up_to(max):
    """Generator đếm từ 1 đến max"""
    count = 1
    while count <= max:
        yield count  # yield tạm dừng hàm và trả về giá trị
        count += 1   # tiếp tục từ đây trong lần gọi next tiếp theo

# Tạo generator
counter = count_up_to(5)
print(f"Counter: {counter}")  # <generator object>

# Lấy giá trị từ generator
print(f"First value: {next(counter)}")  # 1
print(f"Second value: {next(counter)}")  # 2
print(f"Third value: {next(counter)}")  # 3

# Lặp qua các giá trị còn lại
print("Remaining values:")
for value in counter:
    print(value)  # 4, 5

# StopIteration được xử lý tự động trong vòng lặp for
# next(counter)  # Ném ra StopIteration exception

# So sánh với JavaScript:
# function* countUpTo(max) {
#   let count = 1;
#   while (count <= max) {
#     yield count;
#     count++;
#   }
# }
# const counter = countUpTo(5);
# console.log(counter.next().value);  // 1
# console.log(counter.next().value);  // 2

# =========== GENERATOR EXPRESSIONS ===========
# Generator expressions giống list comprehensions, nhưng dùng () thay vì []

# List comprehension - tạo toàn bộ list trong bộ nhớ
squares_list = [x*x for x in range(1, 6)]
print(f"\nSquares list: {squares_list}")

# Generator expression - tạo các giá trị theo demand
squares_gen = (x*x for x in range(1, 6))
print(f"Squares generator: {squares_gen}")

# Lặp qua generator expression
print("Generator expression values:")
for square in squares_gen:
    print(square, end=" ")
print()

# So sánh với JavaScript:
# // Không có generator expression trực tiếp trong JS
# // Nhưng có thể dùng generator function:
# const squaresGen = (function*() {
#   for (let i = 1; i <= 5; i++) {
#     yield i * i;
#   }
# })();

# =========== LƯỜI TÍNH TOÁN (LAZY EVALUATION) ===========
# Generator chỉ tính giá trị khi được yêu cầu

def compute_values(n):
    """Giả lập tính toán phức tạp"""
    print(f"Start computing values up to {n}")
    for i in range(1, n+1):
        print(f"Computing value {i}...")
        yield i * 10
    print("Computation complete!")

# Tạo generator - không thực hiện tính toán ngay
values = compute_values(5)
print(f"\nGenerator created: {values}")

# Khi truy cập giá trị thì mới tính toán
print("\nGetting first value:")
print(f"First value: {next(values)}")

print("\nGetting second value:")
print(f"Second value: {next(values)}")

print("\nGetting remaining values:")
for value in values:
    print(f"Value: {value}")

# =========== MEMORY EFFICIENCY ===========
# Generator tiết kiệm bộ nhớ khi làm việc với dữ liệu lớn

import sys

# So sánh kích thước bộ nhớ
big_list = [i for i in range(1000000)]  # Chiếm nhiều bộ nhớ
big_gen = (i for i in range(1000000))   # Chiếm ít bộ nhớ

print(f"\nMemory usage comparison:")
print(f"List size: {sys.getsizeof(big_list)} bytes")  
print(f"Generator size: {sys.getsizeof(big_gen)} bytes")

# Dùng generator với dữ liệu lớn
def process_large_file(filename):
    with open(filename, 'r') as file:
        for line in file:  # file là một generator lines
            yield line.strip()

# Ví dụ:
# for line in process_large_file('huge_log.txt'):
#     if 'ERROR' in line:
#         print(line)

# =========== GENERATOR VÀ CHAINING ===========
# Kết hợp nhiều generators với nhau

def numbers_up_to(n):
    for i in range(1, n+1):
        yield i

def squares(numbers):
    for n in numbers:
        yield n * n

def even_numbers(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n

# Kết hợp generators
nums = numbers_up_to(10)
squared = squares(nums)
filtered = even_numbers(squared)

print("\nChained generators:")
for num in filtered:
    print(num, end=" ")  # 4, 16, 36, 64, 100
print()

# Cách ngắn gọn hơn với generator expression
result = (
    n * n
    for n in range(1, 11)
    if (n * n) % 2 == 0
)
print("\nChained generator expressions:")
for num in result:
    print(num, end=" ")
print()

# So sánh với JavaScript:
# function* numbersUpTo(n) {
#   for (let i = 1; i <= n; i++) yield i;
# }
# function* squares(numbers) {
#   for (const n of numbers) yield n * n;
# }
# function* evenNumbers(numbers) {
#   for (const n of numbers) if (n % 2 === 0) yield n;
# }
# const result = evenNumbers(squares(numbersUpTo(10)));

# =========== SENDING VALUES TO GENERATORS (COROUTINES) ===========
# Generator có thể nhận giá trị từ bên ngoài qua phương thức send()

def echo():
    """Coroutine nhận và echo lại giá trị"""
    print("Starting echo generator")
    while True:
        received = yield  # Nhận giá trị từ bên ngoài, không trả về gì
        print(f"Received: {received}")

def simple_coroutine():
    """Coroutine nhận và trả về giá trị"""
    print("Starting simple coroutine")
    while True:
        received = yield "Ready for input"  # Trả về + nhận vào
        print(f"Received: {received}")

# Dùng echo generator
print("\nUsing echo generator:")
echo_gen = echo()
next(echo_gen)  # Khởi tạo generator (chạy đến yield đầu tiên)
echo_gen.send("Hello")
echo_gen.send(42)
echo_gen.send({"key": "value"})

# Dùng coroutine trả về giá trị
print("\nUsing simple coroutine:")
coro = simple_coroutine()
response = next(coro)  # Khởi tạo và lấy giá trị đầu tiên
print(f"First response: {response}")
response = coro.send("First message")
print(f"Second response: {response}")
response = coro.send("Second message")
print(f"Third response: {response}")

# So sánh với JavaScript:
# // JavaScript không có send() method nhưng có thể dùng .next(value)
# function* simpleCoroutine() {
#   console.log("Starting simple coroutine");
#   let received;
#   while (true) {
#     received = yield "Ready for input";
#     console.log(`Received: ${received}`);
#   }
# }
# const coro = simpleCoroutine();
# console.log(coro.next().value);  // "Ready for input"
# console.log(coro.next("Hello").value);  // logs "Received: Hello", returns "Ready for input"

# =========== GENERATORS VỚI THROW VÀ CLOSE ===========
# Generator có thể xử lý exceptions và dọn dẹp tài nguyên

def generator_with_exception():
    try:
        yield 1
        yield 2
        yield 3
    except ValueError as e:
        print(f"Caught exception: {e}")
        yield "After exception"
    finally:
        print("Generator cleanup code")

print("\nGenerator with exception handling:")
gen = generator_with_exception()
print(next(gen))  # 1
print(next(gen))  # 2
print(gen.throw(ValueError("Custom error")))  # "After exception"
try:
    next(gen)  # Raises StopIteration
except StopIteration:
    print("Generator is done")

# Dùng close() để dừng generator
def generator_with_close():
    try:
        yield 1
        yield 2
        yield 3
    finally:
        print("Cleanup when generator is closed")

print("\nClosing a generator:")
gen = generator_with_close()
print(next(gen))  # 1
gen.close()  # Kích hoạt finally block

# =========== RECURSIVE GENERATORS ===========
# Generator có thể gọi đệ quy (yield from)

def countdown(n):
    if n <= 0:
        return
    yield n
    yield from countdown(n-1)  # Delegate to another generator

print("\nRecursive generator:")
for i in countdown(5):
    print(i, end=" ")  # 5 4 3 2 1
print()

# Khám phá cấu trúc dữ liệu lồng nhau
def flatten(lst):
    """Làm phẳng list có thể chứa các list con"""
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)  # Gọi đệ quy với flatten
        else:
            yield item

nested_list = [1, [2, [3, 4], 5], 6, [7, 8]]
print("\nFlattening nested list:")
for item in flatten(nested_list):
    print(item, end=" ")  # 1 2 3 4 5 6 7 8
print()

# So sánh với JavaScript:
# function* flatten(arr) {
#   for (const item of arr) {
#     if (Array.isArray(item)) {
#       yield* flatten(item);
#     } else {
#       yield item;
#     }
#   }
# }

# =========== PIPELINE VỚI GENERATOR ===========
# Tạo pipeline xử lý dữ liệu với generators

def read_data():
    """Giả lập đọc dữ liệu từ nguồn"""
    data = [
        {"name": "Alice", "age": 30, "salary": 50000},
        {"name": "Bob", "age": 25, "salary": 45000},
        {"name": "Charlie", "age": 35, "salary": 60000},
        {"name": "Dave", "age": 40, "salary": 70000}
    ]
    for item in data:
        yield item

def filter_by_age(items, min_age):
    """Lọc theo tuổi"""
    for item in items:
        if item["age"] >= min_age:
            yield item

def calculate_tax(items):
    """Tính thuế 20%"""
    for item in items:
        item = item.copy()  # Tránh thay đổi item gốc
        item["tax"] = item["salary"] * 0.2
        item["net_income"] = item["salary"] - item["tax"]
        yield item

def format_output(items):
    """Format dữ liệu đầu ra"""
    for item in items:
        yield f"{item['name']}: ${item['net_income']:.2f} (tax: ${item['tax']:.2f})"

# Tạo và chạy pipeline xử lý
print("\nData processing pipeline:")
pipeline = format_output(
    calculate_tax(
        filter_by_age(
            read_data(), 30
        )
    )
)

for result in pipeline:
    print(result)

# So sánh với JavaScript:
# // Pipeline trong JavaScript tương tự
# function* readData() { /* ... */ }
# function* filterByAge(items, minAge) { /* ... */ }
# function* calculateTax(items) { /* ... */ }
# function* formatOutput(items) { /* ... */ }
# 
# const pipeline = formatOutput(
#   calculateTax(
#     filterByAge(readData(), 30)
#   )
# );
# 
# for (const result of pipeline) {
#   console.log(result);
# }

# =========== ASYNCHRONOUS GENERATORS (PYTHON 3.6+) ===========
# Kết hợp generators với async/await

import asyncio

async def async_range(count):
    """Async generator mô phỏng range()"""
    for i in range(count):
        await asyncio.sleep(0.1)  # Giả lập I/O operation
        yield i

async def process_async_data():
    print("\nAsync generator example:")
    async for i in async_range(5):
        print(f"Got {i}")

# Uncomment để chạy với Python 3.7+
# asyncio.run(process_async_data())

# So sánh với JavaScript:
# // Async generators trong JavaScript
# async function* asyncRange(count) {
#   for (let i = 0; i < count; i++) {
#     await new Promise(resolve => setTimeout(resolve, 100));
#     yield i;
#   }
# }
# 
# async function processAsyncData() {
#   for await (const i of asyncRange(5)) {
#     console.log(`Got ${i}`);
#   }
# }
# 
# processAsyncData();