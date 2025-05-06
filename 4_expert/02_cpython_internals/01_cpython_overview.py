'''
CPython Internals - Overview
============================

CPython là implementation phổ biến nhất của Python.
Module này giúp bạn hiểu cách CPython hoạt động bên trong.

CẢNH BÁO: Nội dung này khá nâng cao và đòi hỏi một số kiến thức về
hệ thống máy tính, compilers, và cấu trúc dữ liệu.
'''

print("=== CPython Internals ===")

# ====== TỔNG QUAN =======
print("\n--- Tổng quan về CPython ---")
print("""
CPython là implementation tiêu chuẩn của Python, viết bằng C.
Là implementation phổ biến nhất, được sử dụng khi bạn tải Python từ python.org.

Các implementation khác bao gồm:
- PyPy (sử dụng JIT compiler)
- Jython (chạy trên JVM)
- IronPython (chạy trên .NET)
""")

# ====== KIẾN TRÚC TỔNG THỂ =======
print("\n--- Kiến trúc tổng thể của CPython ---")
print("""
Quá trình thực thi Python code trong CPython:

1. Parser: Phân tích cú pháp code Python -> AST (Abstract Syntax Tree)
2. Compiler: Biên dịch AST -> Bytecode
3. Interpreter (PVM): Thực thi bytecode

Khi bạn chạy một file Python:
    Source Code (.py) -> AST -> Bytecode (.pyc) -> Execution
""")

# ====== BYTECODE =======
print("\n--- Python Bytecode ---")
print("Chúng ta có thể xem bytecode của một đoạn code bằng module 'dis':")

import dis

def example_function(x, y):
    z = x + y
    return z * 2

print("\nBytecode của example_function():")
dis.dis(example_function)

print("""
Mỗi dòng trong output dis:
- Offset trong bytecode
- Line number trong source code
- Operation name
- Các operation parameter
- Interpretation của instruction

Các bytecode instructions phổ biến:
- LOAD_*: Đẩy giá trị vào stack
- STORE_*: Lưu giá trị từ stack
- BINARY_*: Thực hiện các phép toán nhị phân
- COMPARE_*: So sánh giá trị
- CALL_*: Gọi hàm
- RETURN_*: Trả về giá trị
""")

# ====== REFERENCE COUNTING =======
print("\n--- Reference Counting & Garbage Collection ---")
print("""
CPython sử dụng hai cơ chế chính để quản lý bộ nhớ:

1. Reference Counting:
   - Mỗi object có một counter đếm số references tới nó
   - Khi counter = 0, object được giải phóng ngay lập tức
   - Có thể xem reference count bằng sys.getrefcount()

2. Garbage Collection:
   - Xử lý các reference cycles
   - Chạy định kỳ hoặc khi cần
   - Có thể điều khiển qua module 'gc'
""")

# Minh họa reference counting
import sys

print("\nReference Counting Demo:")
x = [1, 2, 3]  # Tạo list
print(f"x initial refcount: {sys.getrefcount(x) - 1}")  # -1 vì getrefcount() tạo ref tạm thời

y = x  # Tạo thêm reference
print(f"x refcount sau khi gán y = x: {sys.getrefcount(x) - 1}")

del y  # Xóa reference
print(f"x refcount sau khi del y: {sys.getrefcount(x) - 1}")

# Garbage collection
import gc

print("\nGarbage Collection Demo:")
print(f"GC thresholds hiện tại: {gc.get_threshold()}")
print(f"Objects đang theo dõi: {gc.get_count()}")

# Force garbage collection
gc.collect()
print(f"Sau gc.collect(): {gc.get_count()}")

# ====== OBJECT SYSTEM =======
print("\n--- Python Object System ---")
print("""
Trong CPython, mọi thứ đều là object và mỗi object có:
- type (xác định hành vi)
- reference count (cho memory management)
- value (giữ dữ liệu thực)

PyObject là struct C cơ bản đại diện cho mọi object:

struct PyObject {
    Py_ssize_t ob_refcnt;   // reference count
    PyTypeObject *ob_type;  // pointer to type
};

Object Types (PyTypeObject) xác định:
- Cách khởi tạo/giải phóng object
- Các phương thức của object
- Các attribute của object
""")

# Minh họa object system
print("\nObject System Demo:")
a = 42
b = "Hello"
c = [1, 2, 3]

objects = [a, b, c]
for obj in objects:
    print(f"Object: {obj}")
    print(f"  Type: {type(obj)}")
    print(f"  ID: {id(obj)}")
    print(f"  Size in memory: {sys.getsizeof(obj)} bytes")
    print(f"  __dict__: {getattr(obj, '__dict__', 'không có __dict__')}")
    print()

# ====== EXTENSION MODULES =======
print("\n--- Extension Modules ---")
print("""
Extension Modules là modules viết bằng C/C++ để tối ưu hoặc
tích hợp với các thư viện khác.

Cách tạo Python C Extensions:
1. Sử dụng Python C API trực tiếp
2. Dùng công cụ như Cython, SWIG, ctypes, cffi

Ưu điểm:
- Hiệu suất cao hơn cho các tác vụ tính toán nặng
- Tích hợp với thư viện C/C++ hiện có
- Kiểm soát sâu hơn đối với tài nguyên hệ thống

Ví dụ về các Extension Modules phổ biến:
- numpy: Array operations
- pandas: Data analysis
- tensorflow: Machine learning
""")

# ====== GIL (GLOBAL INTERPRETER LOCK) =======
print("\n--- Global Interpreter Lock (GIL) ---")
print("""
GIL là một mutex cho phép chỉ một thread thực thi Python bytecode tại một thời điểm.

Tại sao cần GIL?
- Bảo vệ internal data structures của CPython
- Đơn giản hóa memory management
- Làm cho code C extension an toàn hơn

Tác động của GIL:
- CPU-bound threads không chạy song song thực sự
- I/O-bound có thể chạy đồng thời vì GIL được giải phóng trong I/O operations
- Các process riêng biệt không bị ảnh hưởng bởi GIL

Cách làm việc với GIL:
- Dùng multiprocessing thay vì threading cho CPU-bound tasks
- Sử dụng asyncio cho I/O-bound concurrency
- Giải phóng GIL trong C extensions khi an toàn
""")

# Tạo ví dụ minh họa tác động của GIL
import threading
import time

def cpu_bound_task(n):
    # Một task đơn giản sử dụng nhiều CPU
    count = 0
    for i in range(n):
        count += i
    return count

print("\nVí dụ minh họa tác động của GIL:")

# Single-threaded
start = time.time()
cpu_bound_task(10000000)
cpu_bound_task(10000000)
end = time.time()
print(f"Single-threaded time: {end - start:.4f} seconds")

# Multi-threaded (2 threads)
start = time.time()
t1 = threading.Thread(target=cpu_bound_task, args=(10000000,))
t2 = threading.Thread(target=cpu_bound_task, args=(10000000,))
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print(f"Multi-threaded time: {end - start:.4f} seconds")
print("Notice how multi-threading may not improve performance for CPU-bound tasks due to GIL")

# ====== TÓM TẮT =======
print("\n--- Tóm tắt ---")
print("""
Hiểu CPython Internals giúp bạn:
1. Viết code Python hiệu quả hơn
2. Debug các vấn đề phức tạp
3. Tối ưu hiệu suất code
4. Đóng góp cho Python hoặc extension modules
5. Hiểu những hạn chế và cách khắc phục

Lộ trình học sâu hơn:
- Đọc source code: https://github.com/python/cpython
- "CPython Internals" book by Anthony Shaw
- "Inside the Python Virtual Machine" book by Obi Ike-Nwosu
""")

# Note: Running this file will demonstrate the concepts but won't
# show the internal C code or actual memory structures.
print("\nLưu ý: File này chỉ minh họa khái niệm, không thể hiển thị code C nội bộ hoặc cấu trúc bộ nhớ thực.")