'''
Python Optimization Techniques
=============================

Module này tập trung vào các kỹ thuật tối ưu hóa trong Python, 
giúp cải thiện hiệu suất mã nguồn Python cho các ứng dụng yêu cầu cao.

CẢNH BÁO: Khi tối ưu hóa, luôn đo lường trước và sau khi tối ưu để 
đảm bảo cải tiến thực sự hữu ích.
'''

print("=== Python Optimization Techniques ===")

# ====== CÔNG CỤ ĐO LƯỜNG ======
print("\n--- Công cụ đo lường hiệu suất ---")
print("""
Các công cụ quan trọng:

1. time module - đo thời gian thực thi cơ bản
2. timeit - đo lường thời gian thực thi chính xác hơn
3. cProfile - profiler đầy đủ cho Python
4. memory_profiler - đo lường sử dụng bộ nhớ
5. line_profiler - phân tích thời gian thực thi theo từng dòng
""")

# Ví dụ đơn giản với time module
import time

print("\nĐo lường với time module:")
start = time.time()
sum(range(10000000))
end = time.time()
print(f"Thời gian thực thi: {end - start:.4f} giây")

# Ví dụ với timeit
import timeit

print("\nĐo lường với timeit:")
list_creation_time = timeit.timeit("l = [i for i in range(100)]", number=100000)
set_creation_time = timeit.timeit("s = {i for i in range(100)}", number=100000)
print(f"List comprehension: {list_creation_time:.6f} giây")
print(f"Set comprehension: {set_creation_time:.6f} giây")

# Ví dụ với cProfile
import cProfile
import io
import pstats
from pstats import SortKey

def complex_calculation():
    total = 0
    for i in range(1000000):
        total += i * i
    return total

print("\nĐo lường với cProfile:")
profiler = cProfile.Profile()
profiler.enable()
complex_calculation()
profiler.disable()

s = io.StringIO()
ps = pstats.Stats(profiler, stream=s).sort_stats(SortKey.CUMULATIVE)
ps.print_stats(10)
print(s.getvalue())

# ====== TỐI ƯU THUẬT TOÁN ======
print("\n--- Tối ưu thuật toán ---")
print("""
1. Phức tạp tính toán (Big O):
   - O(1) - constant time: Thời gian không đổi, không phụ thuộc vào kích thước đầu vào
   - O(log n) - logarithmic: Tăng logarit theo kích thước đầu vào
   - O(n) - linear: Tăng tuyến tính theo kích thước đầu vào
   - O(n log n) - linearithmic: Thuật toán sắp xếp hiệu quả
   - O(n²), O(n³) - quadratic, cubic: Tăng nhanh với kích thước đầu vào
   - O(2ⁿ), O(n!) - exponential, factorial: Thuật toán kém hiệu quả

2. Lựa chọn cấu trúc dữ liệu phù hợp:
   - list: Truy cập ngẫu nhiên nhanh, chèn/xóa cuối nhanh
   - dict: Tìm kiếm, chèn, xóa nhanh (O(1))
   - set: Tìm kiếm, kiểm tra thành viên nhanh
   - collections.deque: Chèn/xóa hai đầu nhanh
""")

# Ví dụ: So sánh thuật toán
print("\nSo sánh hiệu suất thuật toán:")

# O(n) linear search
def linear_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

# O(log n) binary search
def binary_search(arr, x):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

# So sánh
import random
data = sorted(random.sample(range(1000000), 100000))
target = data[50000]

start = time.time()
linear_search(data, target)
linear_time = time.time() - start

start = time.time()
binary_search(data, target)
binary_time = time.time() - start

print(f"Linear search: {linear_time:.6f} giây")
print(f"Binary search: {binary_time:.6f} giây")
print(f"Binary search nhanh hơn {linear_time/binary_time:.1f} lần")

# Ví dụ: Lựa chọn cấu trúc dữ liệu
print("\nSo sánh hiệu suất cấu trúc dữ liệu:")
n = 100000

# List vs Set khi tìm kiếm
list_data = list(range(n))
set_data = set(range(n))
target = n - 1

list_search_time = timeit.timeit(lambda: target in list_data, number=100)
set_search_time = timeit.timeit(lambda: target in set_data, number=100)

print(f"Tìm kiếm trong list: {list_search_time:.6f} giây")
print(f"Tìm kiếm trong set: {set_search_time:.6f} giây")
print(f"Set nhanh hơn {list_search_time/set_search_time:.1f} lần cho tìm kiếm")

# ====== TỐI ƯU MÃ NGUỒN PYTHON ======
print("\n--- Tối ưu mã nguồn Python ---")
print("""
1. Sử dụng cấu trúc dữ liệu và phương thức bậc thấp
   - Ưu tiên list/dict/set comprehensions
   - Sử dụng các phương thức như map, filter, reduce

2. Tránh tính toán lặp lại
   - Sử dụng bộ nhớ đệm (caching)
   - Áp dụng memoization với functools.lru_cache

3. Tối ưu vòng lặp
   - Đưa điều kiện ra ngoài vòng lặp nếu có thể
   - Sử dụng itertools cho hiệu suất tốt hơn

4. String operations
   - Sử dụng join() thay vì + để nối chuỗi
   - String interpolation (f-strings) nhanh hơn concatenation
""")

# Ví dụ 1: List comprehension vs loops
print("\nList comprehension vs for loop:")

loop_time = timeit.timeit("""
result = []
for i in range(1000):
    if i % 2 == 0:
        result.append(i*i)
""", number=1000)

comprehension_time = timeit.timeit("""
result = [i*i for i in range(1000) if i % 2 == 0]
""", number=1000)

print(f"For loop: {loop_time:.6f} giây")
print(f"List comprehension: {comprehension_time:.6f} giây")

# Ví dụ 2: Memoization
from functools import lru_cache

print("\nDemo memoization với lru_cache:")

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@lru_cache(maxsize=None)
def fibonacci_cached(n):
    if n <= 1:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

start = time.time()
fibonacci(30)
uncached_time = time.time() - start

start = time.time()
fibonacci_cached(30)
cached_time = time.time() - start

print(f"Fibonacci không cache: {uncached_time:.6f} giây")
print(f"Fibonacci với cache: {cached_time:.6f} giây")
print(f"Cache nhanh hơn {uncached_time/cached_time:.1f} lần")

# Ví dụ 3: String concatenation
print("\nSo sánh phương pháp nối chuỗi:")

concat_time = timeit.timeit("""
s = ""
for i in range(1000):
    s += str(i)
""", number=1000)

join_time = timeit.timeit("""
s = "".join(str(i) for i in range(1000))
""", number=1000)

print(f"Concatenation (+): {concat_time:.6f} giây")
print(f"join(): {join_time:.6f} giây")
print(f"join() nhanh hơn {concat_time/join_time:.1f} lần")

# ====== PYTHON SIÊU TỐI ƯU ======
print("\n--- Siêu tối ưu Python ---")
print("""
Khi cần hiệu suất cực cao:

1. NumPy - cho tính toán số học mảng
   - Vectorization cho phép tính toán nhanh với dữ liệu lớn
   - Thực hiện bằng C tốc độ cao

2. Numba - JIT compiler cho Python
   - Biên dịch hàm Python thành mã máy
   - Sử dụng @numba.jit decorator

3. Cython - kết hợp Python và C
   - Compile Python thành C extension
   - Static typing cho tốc độ cao hơn

4. Multiprocessing - xử lý song song
   - Giúp vượt qua giới hạn GIL
   - Tận dụng nhiều CPU cores
""")

# Ví dụ NumPy Vectorization
print("\nNumPy vectorization vs Python loops:")
import numpy as np

size = 10000000

# Python pure
start = time.time()
result = [i*i for i in range(size)]
python_time = time.time() - start

# NumPy vectorized
start = time.time()
numpy_array = np.arange(size)
result = numpy_array * numpy_array
numpy_time = time.time() - start

print(f"Python list: {python_time:.6f} giây")
print(f"NumPy vectorized: {numpy_time:.6f} giây")
print(f"NumPy nhanh hơn {python_time/numpy_time:.1f} lần")

# Multiprocessing example
from multiprocessing import Pool
import os

def process_chunk(chunk):
    return [i*i for i in chunk]

print("\nSingle process vs multiprocessing:")

def split_into_chunks(data, n):
    chunk_size = len(data) // n
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

data = list(range(10000000))

# Single process
start = time.time()
result = [i*i for i in data]
single_time = time.time() - start

# Multi process
start = time.time()
chunks = split_into_chunks(data, os.cpu_count())
with Pool(processes=os.cpu_count()) as pool:
    result = pool.map(process_chunk, chunks)
    result = [item for sublist in result for item in sublist]
multi_time = time.time() - start

print(f"Single process: {single_time:.6f} giây")
print(f"Multiprocessing: {multi_time:.6f} giây")
print(f"Multiprocessing nhanh hơn {single_time/multi_time:.1f} lần với {os.cpu_count()} cores")

# ====== QUAN TRỌNG ======
print("\n--- Quy tắc tối ưu ---")
print("""
1. Profile trước, tối ưu sau:
   - "Premature optimization is the root of all evil" - Donald Knuth
   - 80% thời gian thực thi thường nằm trong 20% mã nguồn

2. Ba cấp độ tối ưu:
   - Thuật toán: Thay đổi cách giải quyết vấn đề
   - Mã nguồn: Viết Python hiệu quả hơn
   - Siêu tối ưu: Sử dụng Numpy, Numba, Cython, C extensions

3. Khả năng bảo trì vs Hiệu suất:
   - Cân nhắc độ phức tạp tăng thêm
   - Viết code rõ ràng, tối ưu nơi cần thiết

4. Tài nguyên học thêm:
   - "High Performance Python" - Micha Gorelick & Ian Ozsvald
   - "Python Cookbook" - David Beazley & Brian K. Jones
   - "Effective Python" - Brett Slatkin
""")

# ====== TÓM TẮT ======
print("\n--- Tóm tắt ---")
print("""
Tối ưu Python theo các bước:

1. Đo lường và xác định điểm nghẽn (bottlenecks)
2. Cải thiện thuật toán và cấu trúc dữ liệu
3. Tối ưu mã nguồn Python thuần
4. Sử dụng thư viện chuyên dụng (NumPy, Pandas...)
5. Nếu vẫn cần tối ưu hơn nữa: Numba, Cython, C extensions

Tối ưu là quá trình lặp đi lặp lại:
1. Đo lường (Measure)
2. Tối ưu (Optimize)
3. Đo lường lại (Measure again)
4. Đánh giá tradeoffs (Evaluate)
""")