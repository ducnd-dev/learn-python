'''
Exception Handling trong Python cho JavaScript Developers
====================================================

Python cung cấp một hệ thống Exception Handling mạnh mẽ và linh hoạt hơn
so với cấu trúc try-catch trong JavaScript.
'''

# =========== TRY-EXCEPT CƠ BẢN ===========
# Giống try-catch trong JavaScript nhưng mạnh mẽ hơn

# Cú pháp cơ bản
try:
    # Mã có thể gây lỗi
    result = 10 / 0  # ZeroDivisionError
except ZeroDivisionError:
    # Xử lý lỗi cụ thể
    print("Error: Không thể chia cho 0!")

# So sánh với JavaScript:
# try {
#   const result = 10 / 0;  // Infinity trong JS, không gây lỗi
# } catch (error) {
#   console.error("Error:", error.message);
# }

# =========== CATCHING SPECIFIC EXCEPTIONS ===========
# Python cho phép bắt nhiều loại exception khác nhau

def divide_numbers(a, b):
    try:
        # Nhiều lỗi có thể xảy ra
        result = a / b
        return f"Result: {result}"
    except ZeroDivisionError:
        # Bắt lỗi chia cho 0
        return "Error: Không thể chia cho 0!"
    except TypeError:
        # Bắt lỗi kiểu dữ liệu
        return "Error: Phải truyền vào số!"
    except Exception as e:
        # Bắt tất cả các lỗi khác
        return f"Error không xác định: {str(e)}"

# Thử các trường hợp khác nhau
print(divide_numbers(10, 2))       # Kết quả bình thường
print(divide_numbers(10, 0))       # ZeroDivisionError
print(divide_numbers(10, "abc"))   # TypeError
print(divide_numbers(10, [1, 2]))  # TypeError

# =========== ELSE VÀ FINALLY ===========
# Mở rộng của try-except không có trong JavaScript

def process_file(filename):
    try:
        file = open(filename, 'r')
        content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' không tồn tại!")
        return None
    else:
        # Chỉ chạy nếu không có lỗi (không có trong JS)
        print(f"Đọc file thành công, độ dài: {len(content)} ký tự")
        return content
    finally:
        # Luôn chạy, giống finally trong JavaScript
        print("Xử lý file kết thúc, dọn dẹp tài nguyên")
        # Đóng file nếu đã mở thành công
        if 'file' in locals() and not file.closed:
            file.close()
            print("Đã đóng file")

# Thử với file không tồn tại
print("\nThử mở file không tồn tại:")
process_file("nonexistent_file.txt")

# Thử với file có thực
print("\nThử mở file có thực:")
try:
    with open("test_file.txt", "w") as f:
        f.write("Test content for exception handling example.")
    process_file("test_file.txt")
except:
    print("Không thể tạo file test")

# =========== EXCEPTION HIERARCHY ===========
# Python có hệ thống phân cấp exception rõ ràng

def show_exception_hierarchy():
    print("\nHierarchy of some common exceptions:")
    print("BaseException")
    print("├── SystemExit")
    print("├── KeyboardInterrupt")
    print("├── GeneratorExit")
    print("└── Exception")
    print("    ├── StopIteration")
    print("    ├── ArithmeticError")
    print("    │   ├── FloatingPointError")
    print("    │   ├── OverflowError")
    print("    │   └── ZeroDivisionError")
    print("    ├── AssertionError")
    print("    ├── AttributeError")
    print("    ├── BufferError")
    print("    ├── EOFError")
    print("    ├── ImportError")
    print("    │   └── ModuleNotFoundError")
    print("    ├── LookupError")
    print("    │   ├── IndexError")
    print("    │   └── KeyError")
    print("    ├── MemoryError")
    print("    ├── NameError")
    print("    │   └── UnboundLocalError")
    print("    ├── OSError")
    print("    │   ├── BlockingIOError")
    print("    │   ├── ChildProcessError")
    print("    │   ├── ConnectionError")
    print("    │   ├── FileExistsError")
    print("    │   ├── FileNotFoundError")
    print("    │   ├── InterruptedError")
    print("    │   ├── IsADirectoryError")
    print("    │   ├── NotADirectoryError")
    print("    │   ├── PermissionError")
    print("    │   ├── ProcessLookupError")
    print("    │   └── TimeoutError")
    print("    ├── ReferenceError")
    print("    ├── RuntimeError")
    print("    │   ├── NotImplementedError")
    print("    │   └── RecursionError")
    print("    ├── SyntaxError")
    print("    │   └── IndentationError")
    print("    │       └── TabError")
    print("    ├── SystemError")
    print("    ├── TypeError")
    print("    ├── ValueError")
    print("    │   └── UnicodeError")
    print("    └── Warning")

show_exception_hierarchy()

# =========== TẠO CUSTOM EXCEPTIONS ===========
# Tạo exception riêng bằng cách kế thừa từ Exception

class ValidationError(Exception):
    """Exception được ném ra khi xác thực đầu vào thất bại."""
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class User:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age
    
    @staticmethod
    def validate(username, email, age):
        if not username or len(username) < 3:
            raise ValidationError("Username phải có ít nhất 3 ký tự", "username")
        
        if not email or "@" not in email:
            raise ValidationError("Email không hợp lệ", "email")
        
        if not isinstance(age, (int, float)) or age < 18:
            raise ValidationError("Tuổi phải là số và >= 18", "age")

def create_user(username, email, age):
    try:
        User.validate(username, email, age)
        user = User(username, email, age)
        print(f"User created: {username}, {email}, {age}")
        return user
    except ValidationError as e:
        print(f"Validation error on field '{e.field}': {e.message}")
        return None

# Thử tạo user với dữ liệu hợp lệ và không hợp lệ
print("\nThử tạo user hợp lệ:")
user1 = create_user("john_doe", "john@example.com", 25)

print("\nThử tạo user với username không hợp lệ:")
user2 = create_user("jo", "john@example.com", 25)

print("\nThử tạo user với email không hợp lệ:")
user3 = create_user("john_doe", "john-example.com", 25)

print("\nThử tạo user với tuổi không hợp lệ:")
user4 = create_user("john_doe", "john@example.com", 16)

# =========== CONTEXT MANAGERS (WITH STATEMENT) ===========
# Context manager tự động xử lý cleanup (không có trong JavaScript)

# Sử dụng with để đọc file
def read_file_with_context_manager(filename):
    try:
        with open(filename, 'r') as file:  # file tự động đóng khi ra khỏi block with
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{filename}' không tồn tại")
        return None

# Tạo custom context manager
class TempFileManager:
    def __init__(self, filename, mode='w'):
        self.filename = filename
        self.mode = mode
    
    def __enter__(self):
        print(f"Creating temporary file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing and removing file: {self.filename}")
        self.file.close()
        import os
        if os.path.exists(self.filename):
            os.remove(self.filename)
        return False  # Re-raise exception nếu có

# Sử dụng custom context manager
def use_temp_file():
    print("\nSử dụng custom context manager:")
    try:
        with TempFileManager("temp_data.txt") as file:
            file.write("This is temporary data\n")
            file.write("It will be automatically deleted")
            print("Đã viết dữ liệu vào file tạm")
    except Exception as e:
        print(f"Error: {str(e)}")

use_temp_file()

# Context manager bằng contextlib
from contextlib import contextmanager

@contextmanager
def temporary_file(filename, mode='w'):
    try:
        print(f"Creating file: {filename}")
        file = open(filename, mode)
        yield file
    finally:
        file.close()
        print(f"Closing file: {filename}")
        import os
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Removed file: {filename}")

# Sử dụng context manager từ decorator
def use_contextlib_manager():
    print("\nSử dụng contextlib context manager:")
    try:
        with temporary_file("temp_data2.txt") as file:
            file.write("This is another temporary data file\n")
            print("Đã viết dữ liệu vào file tạm")
    except Exception as e:
        print(f"Error: {str(e)}")

use_contextlib_manager()

# =========== EXCEPTION CHAINING ===========
# Nối ngoại lệ (không có trong JavaScript)

def process_data(data):
    try:
        # Làm gì đó với data
        if not isinstance(data, dict):
            raise TypeError("Data phải là dictionary")
        
        if "value" not in data:
            raise KeyError("Key 'value' không tồn tại trong data")
        
        return data["value"] * 2
    except (TypeError, KeyError) as e:
        # Ném ra exception mới với exception gốc là cause
        raise ValueError("Không thể xử lý dữ liệu") from e

def run_process():
    test_data = [1, 2, 3]  # Không phải dict
    
    try:
        result = process_data(test_data)
        print(f"Kết quả: {result}")
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Caused by: {e.__cause__}")

print("\nException chaining example:")
run_process()

# =========== ASSERTIONS ===========
# Assertion là cách kiểm tra điều kiện, nếu sai sẽ ném ra AssertionError

def calculate_discount(price, discount_percent):
    # Đảm bảo giá trị hợp lệ
    assert price > 0, "Price must be positive"
    assert 0 <= discount_percent <= 100, "Discount must be between 0 and 100"
    
    discount = price * (discount_percent / 100)
    return price - discount

# Thử assertions
print("\nAssertions examples:")
try:
    print(f"Discounted price: {calculate_discount(100, 20)}")  # OK
    print(f"Discounted price: {calculate_discount(-100, 20)}")  # AssertionError
except AssertionError as e:
    print(f"Assertion failed: {e}")

try:
    print(f"Discounted price: {calculate_discount(100, 120)}")  # AssertionError
except AssertionError as e:
    print(f"Assertion failed: {e}")

# =========== TRACEBACK VÀ STACK INSPECTION ===========
# Truy xuất thông tin về call stack khi exception xảy ra

import traceback
import sys

def function_c():
    # Gây ra lỗi
    raise ValueError("Lỗi đã xảy ra trong function_c")

def function_b():
    try:
        function_c()
    except:
        print("\nTraceback information:")
        # In ra traceback thông tin
        traceback.print_exc()
        
        # Hoặc lấy traceback dưới dạng string
        traceback_str = traceback.format_exc()
        print("\nTraceback as string:")
        print(traceback_str[:150] + "..." if len(traceback_str) > 150 else traceback_str)
        
        # Lấy thông tin về exception hiện tại
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"\nException type: {exc_type.__name__}")
        print(f"Exception message: {exc_value}")
        
        # Trích xuất stack frames
        stack_frames = traceback.extract_tb(exc_traceback)
        print("\nStack frames:")
        for frame in stack_frames:
            print(f"File: {frame.filename}, Line: {frame.lineno}, Function: {frame.name}, Code: {frame.line}")

def function_a():
    function_b()

# Gọi stack functions
function_a()

# =========== HANDLING ASYNCHRONOUS EXCEPTIONS ===========
# Xử lý ngoại lệ trong asyncio (Python 3.5+)

import asyncio

async def fetch_data(url):
    print(f"Fetching data from {url}")
    # Giả lập network request
    await asyncio.sleep(1)
    
    # Giả lập lỗi cho một số URL
    if "error" in url:
        raise ConnectionError(f"Cannot connect to {url}")
    
    return f"Data from {url}"

async def process_url(url):
    try:
        data = await fetch_data(url)
        return data
    except ConnectionError as e:
        return f"Error: {e}"

async def main():
    urls = [
        "https://example.com/data",
        "https://example.com/error",
        "https://example.com/users"
    ]
    
    # Chạy các coroutines đồng thời
    tasks = [process_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    print("\nAsync exception handling results:")
    for url, result in zip(urls, results):
        print(f"{url} -> {result}")

# Run the async function
if hasattr(asyncio, 'run'):  # Python 3.7+
    print("\nRunning async functions:")
    asyncio.run(main())
else:
    # Python 3.5+
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()