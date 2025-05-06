'''
Python Comprehensions cho JavaScript Developers
=============================================

Comprehensions là một tính năng độc đáo của Python, cho phép tạo các
collection (list, dict, set) một cách ngắn gọn và hiệu quả.

JavaScript (từ ES6+) có cách tương tự với map, filter, reduce, 
nhưng comprehensions trong Python thường ngắn gọn và dễ đọc hơn.
'''

# =========== LIST COMPREHENSIONS ===========
# Cách ngắn gọn để tạo list từ một sequence

# Cách truyền thống trong nhiều ngôn ngữ
numbers = []
for i in range(1, 6):
    numbers.append(i * i)
print(f"Squaress (traditional): {numbers}")

# Sử dụng list comprehension
squares = [i * i for i in range(1, 6)]
print(f"Squares (comprehension): {squares}")

# So sánh với JavaScript:
# // Cách truyền thống
# const numbers = [];
# for (let i = 1; i <= 5; i++) {
#    numbers.push(i * i);
# }
#
# // Với Array.map
# const squares = Array.from({length: 5}, (_, i) => (i+1) * (i+1));
# // Hoặc
# const squares = [...Array(5)].map((_, i) => (i+1) * (i+1));

# =========== LIST COMPREHENSION VỚI ĐIỀU KIỆN ===========
# Thêm điều kiện để lọc (filter) kết quả

# Lấy các số chẵn từ 1-10
even_numbers = [i for i in range(1, 11) if i % 2 == 0]
print(f"Even numbers: {even_numbers}")

# Lấy các số chia hết cho 3 hoặc chia hết cho 5, trong khoảng 1-20
divisible_by_3_or_5 = [i for i in range(1, 21) if i % 3 == 0 or i % 5 == 0]
print(f"Divisible by 3 or 5: {divisible_by_3_or_5}")

# So sánh với JavaScript:
# // Dùng filter
# const evenNumbers = Array.from({length: 10}, (_, i) => i+1).filter(n => n % 2 === 0);
# const divisibleBy3Or5 = Array.from({length: 20}, (_, i) => i+1).filter(n => n % 3 === 0 || n % 5 === 0);

# =========== NESTED LIST COMPREHENSIONS ===========
# List comprehension lồng nhau

# Tạo ma trận 3x4
matrix = [[j for j in range(4)] for i in range(3)]
print(f"3x4 Matrix: {matrix}")

# Flatten một ma trận 2D
flat_matrix = [cell for row in matrix for cell in row]
print(f"Flattened matrix: {flat_matrix}")

# So sánh với JavaScript:
# // Tạo ma trận
# const matrix = Array.from({length: 3}, () => Array.from({length: 4}, (_, j) => j));
# // Flatten
# const flatMatrix = matrix.flat();

# =========== IF-ELSE TRONG LIST COMPREHENSION ===========
# Sử dụng if-else (toán tử bậc ba) trong list comprehension

# Thay thế số chẵn bằng 'even', số lẻ bằng 'odd'
number_types = ['even' if i % 2 == 0 else 'odd' for i in range(1, 11)]
print(f"Number types: {number_types}")

# So sánh với JavaScript:
# const numberTypes = Array.from({length: 10}, (_, i) => (i+1) % 2 === 0 ? 'even' : 'odd');

# =========== DICTIONARY COMPREHENSIONS ===========
# Tương tự list comprehension nhưng tạo dictionary

# Tạo dictionary với key là số, value là bình phương
squares_dict = {i: i*i for i in range(1, 6)}
print(f"Squares dict: {squares_dict}")

# Dictionary với điều kiện
even_squares = {i: i*i for i in range(1, 11) if i % 2 == 0}
print(f"Even squares: {even_squares}")

# So sánh với JavaScript:
# // Tạo object
# const squaresDict = Object.fromEntries(Array.from({length: 5}, (_, i) => [i+1, (i+1) * (i+1)]));
# const evenSquares = Object.fromEntries(Array.from({length: 10}, (_, i) => [i+1, (i+1) * (i+1)]).filter(([k]) => k % 2 === 0));

# =========== SET COMPREHENSIONS ===========
# Tạo set (tập hợp không trùng lặp) bằng comprehension

# Tạo set các số bình phương từ list
numbers = [1, 2, 3, 2, 4, 3, 5]
squares_set = {x*x for x in numbers}
print(f"Squares set: {squares_set}")  # Không có phần tử trùng lặp

# So sánh với JavaScript:
# const numbers = [1, 2, 3, 2, 4, 3, 5];
# const squaresSet = new Set(numbers.map(x => x * x));

# =========== GENERATOR EXPRESSIONS ===========
# Giống list comprehension nhưng dùng () thay vì [], tạo generator

# Tạo generator biểu thức
squares_gen = (i*i for i in range(1, 6))
print(f"Squares generator: {squares_gen}")  # In ra generator object

# Lặp qua generator
print("Iterating over generator:")
for sq in squares_gen:
    print(sq, end=" ")
print()

# Chuyển đổi thành list (nếu cần)
numbers = [1, 2, 3, 4, 5]
squares_gen = (i*i for i in numbers)
squares_list = list(squares_gen)
print(f"Generator converted to list: {squares_list}")

# So sánh với JavaScript:
# // Generator trong JS dùng function*
# function* squaresGenerator() {
#   for (let i = 1; i <= 5; i++) {
#     yield i * i;
#   }
# }
# const gen = squaresGenerator();
# // Hoặc dùng generator expression từ ES6
# const numbers = [1, 2, 3, 4, 5];
# const squaresGen = function*(arr) { for (const n of arr) yield n * n; }(numbers);

# =========== SO SÁNH HIỆU NĂNG ===========
# Đôi khi comprehensions nhanh hơn các cách truyền thống

import time

def measure_time(func):
    """Decorator đo thời gian thực thi của hàm"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{func.__name__}' took {(end - start) * 1000:.2f} ms")
        return result
    return wrapper

@measure_time
def traditional_way(n):
    """Cách truyền thống để tạo list các số bình phương"""
    result = []
    for i in range(1, n+1):
        result.append(i * i)
    return result

@measure_time
def using_comprehension(n):
    """Dùng list comprehension để tạo list các số bình phương"""
    return [i * i for i in range(1, n+1)]

@measure_time
def using_map(n):
    """Dùng map() để tạo list các số bình phương"""
    return list(map(lambda x: x * x, range(1, n+1)))

# So sánh hiệu năng với n lớn
n = 1000000
print("\nPerformance comparison:")
traditional = traditional_way(n)
comprehension = using_comprehension(n)
map_result = using_map(n)

# Kiểm tra kết quả (đầu và cuối)
print(f"Traditional result (first 3): {traditional[:3]}, (last 3): {traditional[-3:]}")
print(f"Comprehension result (first 3): {comprehension[:3]}, (last 3): {comprehension[-3:]}")
print(f"Map result (first 3): {map_result[:3]}, (last 3): {map_result[-3:]}")

# =========== ỨNG DỤNG THỰC TẾ ===========

# Xử lý dữ liệu từ dictionary
users = [
    {"id": 1, "name": "Alice", "age": 30, "active": True},
    {"id": 2, "name": "Bob", "age": 25, "active": False},
    {"id": 3, "name": "Charlie", "age": 35, "active": True},
    {"id": 4, "name": "Dave", "age": 40, "active": True},
    {"id": 5, "name": "Eve", "age": 28, "active": False}
]

# Lấy tên các user đang active
active_names = [user["name"] for user in users if user["active"]]
print(f"\nActive users: {active_names}")

# Tạo dictionary id -> name
id_to_name = {user["id"]: user["name"] for user in users}
print(f"ID to name mapping: {id_to_name}")

# Phân nhóm users theo trạng thái active
status_groups = {
    "active": [user["name"] for user in users if user["active"]],
    "inactive": [user["name"] for user in users if not user["active"]]
}
print(f"Status groups: {status_groups}")

# Tăng tuổi mỗi người lên 1 và tạo list mới
users_aged = [{**user, "age": user["age"] + 1} for user in users]
print(f"Users with increased age:")
for user in users_aged:
    print(f"  {user['name']}: {user['age']} years old")

# =========== NHỮNG ĐIỀU CẦN TRÁNH ===========

# 1. Không nên dùng comprehension quá phức tạp, khó đọc
# BAD: Comprehension phức tạp
complex_comp = [x for x in 
                [y for y in 
                 [z for z in range(1, 5)]
                if y % 2 == 0]
               if x > 0]
print(f"\nComplex comprehension (avoid this): {complex_comp}")

# GOOD: Chia nhỏ để dễ đọc
step1 = [z for z in range(1, 5)]
step2 = [y for y in step1 if y % 2 == 0]
step3 = [x for x in step2 if x > 0]
print(f"Better approach (step by step): {step3}")

# 2. Không nên dùng comprehension khi có side-effects
# BAD: Using comprehension for side effects only
[print(f"Side effect {i}") for i in range(3)]  # Không nên làm điều này

# GOOD: Dùng vòng lặp for bình thường
print("\nBetter approach for side effects:")
for i in range(3):
    print(f"Side effect {i}")

# 3. Tránh dùng comprehension với quá nhiều điều kiện
# Simpler is better
too_many_conditions = [x for x in range(30) if x % 2 == 0 if x % 3 == 0 if x > 10 if x < 25]
print(f"Too many conditions (hard to read): {too_many_conditions}")

# Better with combined conditions
better_conditions = [x for x in range(30) if x % 2 == 0 and x % 3 == 0 and 10 < x < 25]
print(f"Better with combined conditions: {better_conditions}")

# =========== TIP CUỐI CÙNG ===========
print("\nFinal tips:")
print("1. Prioritize readability over brevity")
print("2. Use comprehensions for transforming data, not for side effects")
print("3. Break complex comprehensions into multiple steps")
print("4. Remember that generators (parentheses) are memory-efficient for large datasets")
print("5. Dictionary comprehensions are great for transforming and filtering key-value pairs")