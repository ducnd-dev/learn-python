'''
itertools và functools cho JavaScript Developers
===============================================

itertools và functools là hai module quan trọng trong thư viện chuẩn của Python
cung cấp các công cụ hữu ích cho lập trình hàm và làm việc với iterators.

Những module này không có tương đương trực tiếp trong JavaScript, mặc dù
nhiều chức năng tương tự có thể đạt được bằng lodash hoặc Ramda.
'''

# =========== ITERTOOLS ===========
print("=== itertools Module ===")
print("itertools cung cấp các function tạo ra các iterators hiệu quả")

import itertools as it

# ===== INFINITE ITERATORS =====
print("\n--- Infinite Iterators ---")

# count() - Đếm từ n, tăng dần vô hạn
counter = it.count(10, 2)  # start=10, step=2
print("it.count(10, 2):", end=" ")
for i, val in enumerate(counter):
    print(val, end=" ")
    if i >= 4:  # Chỉ in 5 giá trị
        print("...")
        break

# cycle() - Lặp lại vô hạn
cycler = it.cycle(['A', 'B', 'C'])
print("\nit.cycle(['A', 'B', 'C']):", end=" ")
for i in range(8):  # In 8 giá trị
    print(next(cycler), end=" ")

# repeat() - Lặp lại một phần tử, có thể giới hạn số lần
repeater = it.repeat("X", 5)  # Lặp lại "X" 5 lần
print("\nit.repeat('X', 5):", end=" ")
for x in repeater:
    print(x, end=" ")

# So sánh với JavaScript:
print("\n\nJS equivalent:")
print("""
// count: Không có equivalent, cần triển khai thủ công
function* count(start = 0, step = 1) {
  let n = start;
  while (true) {
    yield n;
    n += step;
  }
}

// cycle: Cũng cần triển khai thủ công
function* cycle(iterable) {
  const saved = [...iterable];
  while (saved.length > 0) {
    yield* saved;
  }
}

// repeat: Có thể dùng Array(n).fill(x)
const repeater = Array(5).fill('X');
""")

# ===== TERMINATING ITERATORS =====
print("\n\n--- Terminating Iterators ---")

# accumulate() - Tính tổng tích lũy
nums = [1, 2, 3, 4, 5]
print("it.accumulate([1, 2, 3, 4, 5]):", list(it.accumulate(nums)))  # [1, 3, 6, 10, 15]

# Có thể dùng custom function
import operator
print("it.accumulate([1, 2, 3, 4, 5], operator.mul):", 
      list(it.accumulate(nums, operator.mul)))  # [1, 2, 6, 24, 120]

# chain() - Kết hợp nhiều iterables
print("it.chain('ABC', 'DEF'):", 
      list(it.chain('ABC', 'DEF')))  # ['A', 'B', 'C', 'D', 'E', 'F']

# compress() - Filter bằng selector
selectors = [1, 0, 1, 0, 1]
print("it.compress('ABCDE', [1, 0, 1, 0, 1]):", 
      list(it.compress('ABCDE', selectors)))  # ['A', 'C', 'E']

# dropwhile() và takewhile() - Lọc có điều kiện
def less_than_3(x):
    return x < 3

print("it.dropwhile(less_than_3, [1, 2, 3, 4, 1, 2]):", 
      list(it.dropwhile(less_than_3, [1, 2, 3, 4, 1, 2])))  # [3, 4, 1, 2]
print("it.takewhile(less_than_3, [1, 2, 3, 4, 1, 2]):", 
      list(it.takewhile(less_than_3, [1, 2, 3, 4, 1, 2])))  # [1, 2]

# filterfalse() - Giống filter() nhưng lấy các giá trị False
print("it.filterfalse(less_than_3, [1, 2, 3, 4, 1, 2]):", 
      list(it.filterfalse(less_than_3, [1, 2, 3, 4, 1, 2])))  # [3, 4]

# groupby() - Nhóm theo key function
animals = ['duck', 'dog', 'deer', 'cat', 'cow']
print("\nit.groupby() example:")
for key, group in it.groupby(sorted(animals), key=lambda x: x[0]):
    print(f"Key: {key}, Group: {list(group)}")

# islice() - Slice một iterator
print("it.islice('ABCDEFG', 2, 5):", 
      list(it.islice('ABCDEFG', 2, 5)))  # ['C', 'D', 'E']

# starmap() - Tương tự map() nhưng unpack arguments
operations = [(2, 5), (3, 2), (10, 3)]
print("it.starmap(pow, [(2, 5), (3, 2), (10, 3)]):", 
      list(it.starmap(pow, operations)))  # [32, 9, 1000]

# tee() - Split một iterator thành nhiều iterators
original_iter = iter([1, 2, 3])
iter1, iter2 = it.tee(original_iter, 2)
print("it.tee() demo - iter1:", list(iter1))  # [1, 2, 3]
print("it.tee() demo - iter2:", list(iter2))  # [1, 2, 3]

# zip_longest() - Giống zip() nhưng lấy phần tử dài nhất
print("it.zip_longest('ABCD', 'xy', fillvalue='-'):", 
      list(it.zip_longest('ABCD', 'xy', fillvalue='-')))  # [('A', 'x'), ('B', 'y'), ('C', '-'), ('D', '-')]

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// accumulate: Có thể dùng reduce
[1, 2, 3, 4, 5].reduce((acc, x, i, arr) => {
  if (i === 0) return [x];
  return [...acc, acc[acc.length-1] + x];
}, []);  // [1, 3, 6, 10, 15]

// chain: flat hoặc concat
[..."ABC", ..."DEF"];  // ['A', 'B', 'C', 'D', 'E', 'F']

// compress: filter với index
"ABCDE".split('').filter((x, i) => [1, 0, 1, 0, 1][i]);

// dropwhile: Không có built-in, có thể dùng lodash
// takewhile: Không có built-in, có thể dùng lodash
""")

# ===== COMBINATORIC ITERATORS =====
print("\n\n--- Combinatoric Iterators ---")

# product() - Tích Descartes (tất cả các tổ hợp)
print("it.product('AB', 'CD'):")
for p in it.product('AB', 'CD'):
    print(p, end=" ")  # ('A', 'C') ('A', 'D') ('B', 'C') ('B', 'D')

# permutations() - Hoán vị
print("\nit.permutations('ABC', 2):")
for p in it.permutations('ABC', 2):
    print(p, end=" ")  # ('A', 'B') ('A', 'C') ('B', 'A') ('B', 'C') ('C', 'A') ('C', 'B')

# combinations() - Tổ hợp
print("\nit.combinations('ABC', 2):")
for c in it.combinations('ABC', 2):
    print(c, end=" ")  # ('A', 'B') ('A', 'C') ('B', 'C')

# combinations_with_replacement() - Tổ hợp có lặp lại
print("\nit.combinations_with_replacement('ABC', 2):")
for c in it.combinations_with_replacement('ABC', 2):
    print(c, end=" ")  # ('A', 'A') ('A', 'B') ('A', 'C') ('B', 'B') ('B', 'C') ('C', 'C')

# So sánh với JavaScript:
print("\n\nJS equivalent:")
print("""
// Không có direct equivalent trong JS standard library
// Thường được triển khai bằng thư viện hoặc tự viết functions
""")

# ===== ITERTOOLS RECIPES =====
print("\n\n--- Itertools Recipes ---")
print("Python docs cung cấp một số 'recipes' hữu ích sử dụng itertools:")

# Take - Lấy n phần tử đầu tiên
def take(n, iterable):
    return list(it.islice(iterable, n))

print("take(3, range(10)):", take(3, range(10)))  # [0, 1, 2]

# Chunked - Chia thành các nhóm có kích thước cố định
def chunked(iterable, n):
    it1 = iter(iterable)
    while chunk := list(it.islice(it1, n)):
        yield chunk

print("chunked('ABCDEFG', 3):", list(chunked('ABCDEFG', 3)))  # [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]

# First True - Tìm phần tử đầu tiên thỏa mãn điều kiện
def first_true(iterable, default=False, pred=None):
    return next(filter(pred, iterable), default)

print("first_true([0, None, 0, 1, 2], default='not found'):", 
      first_true([0, None, 0, 1, 2], default='not found'))  # 1

# Roundrobin - Lấy phần tử từ mỗi iterable luân phiên
def roundrobin(*iterables):
    iterators = list(map(iter, iterables))
    active = len(iterators)
    while active:
        for i, it in enumerate(iterators):
            try:
                yield next(it)
            except StopIteration:
                active -= 1
                iterators[i] = None
                if not active:
                    break

print("roundrobin('ABC', 'D', 'EF'):", 
      list(roundrobin('ABC', 'D', 'EF')))  # ['A', 'D', 'E', 'B', 'F', 'C']

# =========== FUNCTOOLS ===========
print("\n\n=== functools Module ===")
print("functools cung cấp các higher-order functions và decorator")

import functools as ft

# ===== PARTIAL =====
print("\n--- partial() - Tạo hàm mới từ hàm có sẵn với arguments cố định ---")

def multiply(x, y):
    return x * y

# Tạo một hàm mới với y=10
times_ten = ft.partial(multiply, y=10)
print("ft.partial(multiply, y=10)(5):", times_ten(5))  # 50

# Tạo hàm mới với x=2
double = ft.partial(multiply, 2)
print("ft.partial(multiply, 2)(7):", double(7))  # 14

# partial với positional args
def tag(name, cls, content):
    return f'<{name} class="{cls}">{content}</{name}>'

# Tạo hàm div và p
div = ft.partial(tag, 'div')
p = ft.partial(tag, 'p')

print("div('alert', 'Hello'):", div('alert', 'Hello'))  # <div class="alert">Hello</div>
print("p('content', 'Text'):", p('content', 'Text'))  # <p class="content">Text</p>

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// Dùng bind hoặc closure
function multiply(x, y) {
  return x * y;
}

const timesTen = (x) => multiply(x, 10);
const double = multiply.bind(null, 2);
""")

# ===== REDUCE =====
print("\n--- reduce() - Tổng hợp một iterable thành một giá trị duy nhất ---")

# Tính tổng
numbers = [1, 2, 3, 4, 5]
sum_nums = ft.reduce(lambda a, b: a + b, numbers)
print("ft.reduce(lambda a, b: a + b, [1, 2, 3, 4, 5]):", sum_nums)  # 15

# Tìm max
find_max = ft.reduce(lambda a, b: a if a > b else b, numbers)
print("ft.reduce(lambda a, b: a if a > b else b, [1, 2, 3, 4, 5]):", find_max)  # 5

# Flatten list of lists
nested = [[1, 2], [3, 4], [5, 6]]
flattened = ft.reduce(lambda a, b: a + b, nested)
print("ft.reduce(lambda a, b: a + b, [[1, 2], [3, 4], [5, 6]]):", flattened)  # [1, 2, 3, 4, 5, 6]

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// JavaScript có Array.prototype.reduce
[1, 2, 3, 4, 5].reduce((a, b) => a + b);  // 15

// Tìm max 
[1, 2, 3, 4, 5].reduce((a, b) => a > b ? a : b);  // 5

// Flatten
[[1, 2], [3, 4], [5, 6]].reduce((a, b) => a.concat(b), []);  // [1, 2, 3, 4, 5, 6]
""")

# ===== LRU_CACHE =====
print("\n--- lru_cache - Memoization decorator ---")

# Fibonacci không cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Fibonacci với cache
@ft.lru_cache(maxsize=None)
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

# Không chạy fibonacci(35) vì quá chậm
import time

print("Calculating fibonacci_cached(35)...")
start = time.time()
result = fibonacci_cached(35)
end = time.time()
print(f"Result: {result}, Time: {end - start:.6f} seconds")

# Kiểm tra cache stats
print("Cache info:", fibonacci_cached.cache_info())

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// Không có built-in, nhưng có thể triển khai memoization
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const fibCached = memoize(function(n) {
  if (n < 2) return n;
  return fibCached(n - 1) + fibCached(n - 2);
});
""")

# ===== SINGLEDISPATCH =====
print("\n--- singledispatch - Lựa chọn hàm dựa trên type của tham số ---")

@ft.singledispatch
def process_data(data):
    raise NotImplementedError(f"Cannot process data of type {type(data)}")

@process_data.register
def _(data: list):
    return f"Processing list with {len(data)} items"

@process_data.register
def _(data: str):
    return f"Processing string of length {len(data)}"

@process_data.register
def _(data: int):
    return f"Processing integer: {data}"

# Sử dụng singledispatch
print("process_data([1, 2, 3]):", process_data([1, 2, 3]))
print("process_data('hello'):", process_data('hello'))
print("process_data(42):", process_data(42))

try:
    process_data({1: 'a'})  # dict không được đăng ký
except NotImplementedError as e:
    print(f"Error: {e}")

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// JavaScript không có built-in feature tương tự
// Thường sử dụng type checking thủ công
function processData(data) {
  if (Array.isArray(data)) {
    return `Processing list with ${data.length} items`;
  } else if (typeof data === 'string') {
    return `Processing string of length ${data.length}`;
  } else if (typeof data === 'number') {
    return `Processing integer: ${data}`;
  } else {
    throw new Error(`Cannot process data of type ${typeof data}`);
  }
}
""")

# ===== WRAPS =====
print("\n--- wraps - Preserves metadata của hàm gốc khi decorating ---")

def my_decorator(func):
    @ft.wraps(func)  # Giữ nguyên metadata của func
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example_function(x):
    """This is the docstring for example_function."""
    return x * 2

# Gọi hàm đã được decorator
print(example_function(5))

# Kiểm tra metadata có được giữ lại không
print(f"Function name: {example_function.__name__}")
print(f"Docstring: {example_function.__doc__}")

print("\nWithout @wraps, metadata would show function name as 'wrapper'")

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// JavaScript không có built-in decorator, nhưng có thể
// triển khai tương tự với các hàm bậc cao

function myDecorator(func) {
  function wrapper(...args) {
    console.log(`Calling ${func.name}`);
    return func(...args);
  }
  // Preserve metadata manually
  Object.defineProperties(wrapper, {
    name: { value: func.name },
    length: { value: func.length }
  });
  return wrapper;
}

const exampleFunction = myDecorator(function exampleFunction(x) {
  return x * 2;
});
""")

# ===== TOTAL_ORDERING =====
print("\n--- total_ordering - Chỉ cần thực hiện một vài phương thức so sánh ---")

@ft.total_ordering
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age
    
    def __lt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age

# Tạo đối tượng để test
alice = Person("Alice", 30)
bob = Person("Bob", 25)

# Test các phương thức so sánh
print(f"alice == bob: {alice == bob}")  # False
print(f"alice != bob: {alice != bob}")  # True
print(f"alice < bob: {alice < bob}")    # False
print(f"alice > bob: {alice > bob}")    # True
print(f"alice <= bob: {alice <= bob}")  # False
print(f"alice >= bob: {alice >= bob}")  # True

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// JavaScript không có built-in decorator hoặc tính năng tương tự
// Cần triển khai tất cả các phương thức so sánh thủ công
""")

# ===== CACHE (Python 3.9+) =====
if hasattr(ft, 'cache'):
    print("\n--- cache - Phiên bản đơn giản hóa của lru_cache (Python 3.9+) ---")
    
    @ft.cache
    def expensive_computation(n):
        print(f"Computing {n}...")
        return n * n
    
    print("First call:", expensive_computation(10))  # Sẽ tính toán
    print("Second call:", expensive_computation(10))  # Sẽ dùng cache
    
    # Clear cache
    expensive_computation.cache_clear()
    print("After clearing cache:", expensive_computation(10))  # Sẽ tính toán lại
else:
    print("\n--- cache decorator requires Python 3.9+ ---")

# =========== COMBINING ITERTOOLS AND FUNCTOOLS ===========
print("\n\n=== Combining itertools and functools ===")

# Đếm số lần xuất hiện của mỗi ký tự
def char_frequency(text):
    text = text.lower()
    # Sắp xếp để nhóm các ký tự giống nhau
    sorted_text = sorted(text)
    # Nhóm các ký tự giống nhau
    grouped = {k: list(g) for k, g in it.groupby(sorted_text)}
    # Tính số lần xuất hiện
    return {k: len(v) for k, v in grouped.items()}

text = "Hello World"
print(f"Character frequency in '{text}':", char_frequency(text))

# Hệ thống hình ảnh: Nhóm hình ảnh theo kích thước
images = [
    {"name": "img1.jpg", "size": "small", "width": 100, "height": 100},
    {"name": "img2.jpg", "size": "medium", "width": 200, "height": 150},
    {"name": "img3.jpg", "size": "small", "width": 100, "height": 100},
    {"name": "img4.jpg", "size": "large", "width": 500, "height": 300},
    {"name": "img5.jpg", "size": "medium", "width": 250, "height": 150}
]

def group_by_size(images):
    # Sắp xếp theo kích thước
    sorted_images = sorted(images, key=lambda img: img["size"])
    # Nhóm theo kích thước
    grouped = {k: list(g) for k, g in it.groupby(sorted_images, key=lambda img: img["size"])}
    return grouped

grouped_images = group_by_size(images)
print("\nImages grouped by size:")
for size, imgs in grouped_images.items():
    print(f"Size: {size}, Count: {len(imgs)}")
    for img in imgs:
        print(f"  - {img['name']} ({img['width']}x{img['height']})")

# Tạo pipeline cho xử lý dữ liệu
def pipeline(*funcs):
    def process(data):
        result = data
        for func in funcs:
            result = func(result)
        return result
    return process

# Các bước xử lý
def only_even(numbers):
    return list(filter(lambda x: x % 2 == 0, numbers))

def square(numbers):
    return list(map(lambda x: x * x, numbers))

def sum_all(numbers):
    return ft.reduce(lambda a, b: a + b, numbers, 0)

# Tạo pipeline
process_numbers = pipeline(only_even, square, sum_all)

numbers = list(range(1, 11))  # 1-10
result = process_numbers(numbers)
print(f"\nProcessed numbers: {numbers}")
print(f"Result after filtering even, squaring, and summing: {result}")

# =========== BEST PRACTICES ===========
print("\n\n=== Best Practices ===")

print("1. Sử dụng itertools cho các thao tác lặp để cải thiện hiệu suất và khả năng đọc")
print("2. Sử dụng lru_cache cho các hàm tốn thời gian tính toán với input lặp lại")
print("3. Kết hợp các iterator thay vì tạo list trung gian để tiết kiệm bộ nhớ")
print("4. Sử dụng @wraps khi viết decorators để giữ metadata")
print("5. Tận dụng partial để tạo các phiên bản chuyên biệt của hàm")
print("6. Sử dụng singledispatch cho các hàm xử lý nhiều loại dữ liệu")

# Các pattern phổ biến với itertools và functools
print("\n--- Common Patterns ---")

# 1. Flatten a nested structure
nested_lists = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flattened = list(it.chain.from_iterable(nested_lists))
print("Flattening lists:", flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 2. Get unique items while preserving order
def unique_everseen(iterable):
    seen = set()
    return [x for x in iterable if not (x in seen or seen.add(x))]

print("Unique items:", unique_everseen([1, 2, 3, 1, 2, 4, 5, 3]))  # [1, 2, 3, 4, 5]

# 3. Create a sliding window iterator
def sliding_window(seq, n):
    it = iter(seq)
    window = list(it.islice(it, n))
    yield tuple(window)
    for x in it:
        window = window[1:] + [x]
        yield tuple(window)

print("Sliding windows of size 3:")
for window in sliding_window([1, 2, 3, 4, 5, 6], 3):
    print(window, end=" ")  # (1, 2, 3) (2, 3, 4) (3, 4, 5) (4, 5, 6) 

# =========== REAL-WORLD APPLICATIONS ===========
print("\n\n=== Real-World Applications ===")

# 1. Data Processing Pipeline
print("\n--- Data Processing Pipeline ---")

# Mẫu dữ liệu thô
raw_data = [
    {"name": "Alice", "age": "30", "active": "yes"},
    {"name": "Bob", "age": "25", "active": "no"},
    {"name": "Charlie", "age": "35", "active": "yes"},
    {"name": "David", "age": "40", "active": "yes"},
    {"name": "Eve", "age": "22", "active": "no"}
]

# Các hàm xử lý
def parse_age(record):
    record["age"] = int(record["age"])
    return record

def convert_active_status(record):
    record["active"] = record["active"].lower() == "yes"
    return record

def filter_active(records):
    return filter(lambda r: r["active"], records)

def extract_name_age(record):
    return {"name": record["name"], "age": record["age"]}

# Xây dựng pipeline
process_data = ft.partial(map, parse_age)
process_data = ft.partial(map, convert_active_status)
filter_active_users = ft.partial(filter, lambda r: r["active"])
extract_info = ft.partial(map, extract_name_age)

# Chạy pipeline
processed_data = list(extract_info(filter_active_users(process_data(raw_data))))
print("Processed data:")
for item in processed_data:
    print(f"  {item}")

# 2. Task Scheduler với priority
print("\n--- Task Scheduler ---")

tasks = [
    {"id": 1, "name": "Task A", "priority": "high"},
    {"id": 2, "name": "Task B", "priority": "medium"},
    {"id": 3, "name": "Task C", "priority": "low"},
    {"id": 4, "name": "Task D", "priority": "high"},
    {"id": 5, "name": "Task E", "priority": "medium"}
]

# Priority mapper
priority_map = {"high": 3, "medium": 2, "low": 1}

# Sắp xếp tasks theo priority
sorted_tasks = sorted(tasks, key=lambda t: priority_map[t["priority"]], reverse=True)

# Nhóm tasks theo priority
grouped_tasks = {k: list(g) for k, g in it.groupby(sorted_tasks, key=lambda t: t["priority"])}

print("Tasks by priority:")
for priority, task_list in grouped_tasks.items():
    print(f"  {priority.upper()} priority tasks:")
    for task in task_list:
        print(f"    - Task {task['id']}: {task['name']}")

# 3. Caching API Results
print("\n--- Caching API Results ---")

# Giả lập API call
@ft.lru_cache(maxsize=100)
def fetch_user_data(user_id):
    print(f"Fetching data for user {user_id}...")
    # Trong thực tế, đây sẽ là API call
    return {"id": user_id, "name": f"User {user_id}", "data": f"Some data for {user_id}"}

# Test cache
print("First request for user 1:")
data1 = fetch_user_data(1)
print("Second request for user 1 (should use cache):")
data1_again = fetch_user_data(1)
print("Request for user 2:")
data2 = fetch_user_data(2)

print("Cache info:", fetch_user_data.cache_info())

# =========== SUMMARY ===========
print("\n\n=== Summary ===")

print("itertools:")
print("- Cung cấp các iterators hiệu quả và tiết kiệm bộ nhớ")
print("- Bao gồm infinite iterators, combinatoric generators")
print("- Cho phép function chaining để tạo data pipelines")
print("- Không có tương đương đầy đủ trong JavaScript")

print("\nfunctools:")
print("- Cung cấp các higher-order functions và decorators")
print("- Bao gồm partial, reduce, lru_cache, singledispatch")
print("- Hỗ trợ functional programming trong Python")
print("- Một số tính năng tương tự trong JavaScript (reduce) nhưng nhiều tính năng là độc đáo")

print("\nKết hợp itertools và functools:")
print("- Tạo data processing pipelines mạnh mẽ")
print("- Cải thiện performance và khả năng đọc code")
print("- Giảm memory footprint khi làm việc với large datasets")
print("- Mẫu thiết kế functional tạo ra code dễ test và maintain")