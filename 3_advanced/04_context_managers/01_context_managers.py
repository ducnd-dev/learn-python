'''
Context Managers cho JavaScript Developers
===========================================

Context managers trong Python là một pattern tạo điều kiện cho 
việc quản lý tài nguyên như files, connections, và locks.

Chúng đảm bảo setup và teardown chính xác, ngay cả khi 
xảy ra lỗi, tương tự như try-finally trong JavaScript.

Context managers sử dụng cú pháp with, không có tương đương 
trực tiếp trong JavaScript (trước khi ES2022 giới thiệu tính năng "using").
'''

# =========== BASICS OF CONTEXT MANAGERS ===========
print("=== Context Manager Basics ===")

# Cách truyền thống để làm việc với file
print("\n--- Truyền thống vs With Statement ---")
print("Cách truyền thống:")
file = None
try:
    file = open('sample.txt', 'w')
    file.write('Hello, World!')
finally:
    if file:
        file.close()
        print("File closed manually in finally block")

# Cách sử dụng context manager (with statement)
print("\nSử dụng with statement:")
with open('sample.txt', 'w') as file:
    file.write('Hello with context manager!')
print("File tự động đóng sau khi thoát khỏi with block")

# Đọc file để kiểm tra
with open('sample.txt', 'r') as file:
    content = file.read()
    print(f"File content: {content}")

# So sánh với JavaScript:
print("\nJS equivalent (pre-ES2022):")
print("""
// Phương pháp truyền thống trong JavaScript
let file;
try {
  file = fs.openSync('sample.txt', 'w');
  fs.writeSync(file, 'Hello, World!');
} finally {
  if (file !== undefined) {
    fs.closeSync(file);
  }
}

// Javascript hiện đại với các hàm promise dễ dàng hơn
async function writeFile() {
  await fs.promises.writeFile('sample.txt', 'Hello, World!');
}
""")

print("\nJS equivalent (ES2022+) với 'using' declaration:")
print("""
{
  using file = getFile('sample.txt');
  // File tự động disposed khi thoát khỏi block
}
""")

# =========== CREATING CONTEXT MANAGERS ===========
print("\n\n=== Creating Context Managers ===")

# ===== USING CLASSES =====
print("\n--- Context Manager bằng Class ---")

class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
        
    def __enter__(self):
        """Được gọi khi bắt đầu with statement"""
        self.file = open(self.filename, self.mode)
        print(f"Opening {self.filename} in {self.mode} mode")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Được gọi khi kết thúc with statement hoặc có exception"""
        if self.file:
            self.file.close()
            print(f"Closing {self.filename}")
            
        # Xử lý exception nếu cần
        if exc_type is not None:
            print(f"Exception occurred: {exc_type}, {exc_val}")
            
        # Return False để cho phép exception lan truyền
        # Return True để chặn exception
        return False

# Sử dụng custom context manager
with FileManager('custom.txt', 'w') as file:
    file.write("Using custom context manager!")
    print("Writing to file...")
    
# Kiểm tra nội dung
with FileManager('custom.txt', 'r') as file:
    content = file.read()
    print(f"Custom file content: {content}")
    
# Thử context manager với exception
try:
    with FileManager('custom.txt', 'r') as file:
        print("About to raise an exception...")
        raise ValueError("Test exception")
except ValueError as e:
    print(f"Exception was propagated: {e}")

# ===== USING CONTEXTLIB =====
print("\n--- Context Manager bằng contextlib ---")

import contextlib

@contextlib.contextmanager
def file_manager(filename, mode):
    """Context manager using contextlib.contextmanager decorator"""
    try:
        file = open(filename, mode)
        print(f"Opening {filename} in {mode} mode")
        # Yield to give control back to the with block
        yield file
    finally:
        file.close()
        print(f"Closing {filename}")

# Sử dụng context manager từ decorator
with file_manager('contextlib_example.txt', 'w') as file:
    file.write("Created with contextlib.contextmanager!")
    print("Writing to file using contextlib...")

# Kiểm tra nội dung
with file_manager('contextlib_example.txt', 'r') as file:
    content = file.read()
    print(f"Contextlib file content: {content}")

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// JavaScript không có built-in decorator tương tự,
// nhưng có thể mô phỏng bằng cách sử dụng function và callback

function withFile(filename, mode, callback) {
  const file = fs.openSync(filename, mode);
  try {
    callback(file);
  } finally {
    fs.closeSync(file);
  }
}

// Sử dụng
withFile('example.txt', 'w', (file) => {
  fs.writeSync(file, 'Hello, World!');
});
""")

# =========== NESTED CONTEXT MANAGERS ===========
print("\n\n=== Nested Context Managers ===")

# Sử dụng nhiều context managers cùng lúc
with open('file1.txt', 'w') as file1, open('file2.txt', 'w') as file2:
    file1.write("Content for file 1")
    file2.write("Content for file 2")
    print("Writing to multiple files simultaneously")

# Đọc nội dung để xác nhận
with open('file1.txt', 'r') as file1, open('file2.txt', 'r') as file2:
    content1 = file1.read()
    content2 = file2.read()
    print(f"File 1: {content1}, File 2: {content2}")

# Lồng các context managers
with open('outer.txt', 'w') as outer_file:
    outer_file.write("Outer content\n")
    with open('inner.txt', 'w') as inner_file:
        inner_file.write("Inner content")
    outer_file.write("More outer content")

print("Nested context managers completed")

# =========== PRACTICAL EXAMPLES ===========
print("\n\n=== Practical Examples ===")

# ===== 1. DATABASE CONNECTION =====
print("\n--- Database Connection Example ---")

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def __enter__(self):
        # In thực tế, đây sẽ là kết nối thực với database
        print(f"Connecting to database {self.database} on {self.host}")
        self.connection = f"Connection to {self.database} (simulated)"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # In thực tế, đây sẽ đóng kết nối
        print(f"Closing database connection to {self.database}")
        self.connection = None
        return False

# Sử dụng context manager cho database
with DatabaseConnection("localhost", "user", "password", "mydatabase") as conn:
    print(f"Performing database operations with {conn}")
    # In thực tế, đây sẽ là các hoạt động trên database
    
print("Database operations completed")

# So sánh với JavaScript:
print("\nJS equivalent:")
print("""
// JavaScript không có built-in context management, nhưng có thể mô phỏng
// với Promise và async/await

class DatabaseConnection {
  constructor(host, user, password, database) {
    this.host = host;
    this.user = user;
    this.password = password;
    this.database = database;
  }
  
  async connect() {
    console.log(`Connecting to database ${this.database}`);
    this.connection = `Connection to ${this.database}`;
    return this;
  }
  
  async close() {
    console.log(`Closing connection to ${this.database}`);
    this.connection = null;
  }
}

async function withDatabase(callback) {
  const db = new DatabaseConnection("localhost", "user", "password", "mydatabase");
  try {
    await db.connect();
    await callback(db);
  } finally {
    await db.close();
  }
}

// Sử dụng
await withDatabase(async (db) => {
  // Thực hiện các hoạt động trên database
});
""")

# ===== 2. LOCK (THREADING) =====
print("\n--- Lock Example ---")

import threading

# Tạo lock
lock = threading.Lock()

# Sử dụng context manager cho lock
def process_data():
    print("Waiting for lock...")
    with lock:  # Tự động acquire khi vào và release khi ra khỏi block
        print("Lock acquired, processing data...")
        # Giả lập xử lý dữ liệu
        
    print("Lock released")

# Tạo và chạy 2 threads
thread1 = threading.Thread(target=process_data)
thread2 = threading.Thread(target=process_data)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Threading example completed")

# ===== 3. TEMPORARY DIRECTORY =====
print("\n--- Temporary Directory Example ---")

import tempfile
import os
import shutil

# Sử dụng context manager cho temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Created temporary directory: {temp_dir}")
    
    # Tạo một file trong directory này
    temp_file_path = os.path.join(temp_dir, "temp_file.txt")
    with open(temp_file_path, "w") as temp_file:
        temp_file.write("Temporary content")
    
    # Đọc file để xác nhận
    with open(temp_file_path, "r") as temp_file:
        content = temp_file.read()
        print(f"Temporary file content: {content}")
    
    print("Performing operations in temporary directory")
    
print("Temporary directory has been automatically cleaned up")

# Kiểm tra xem thư mục đã bị xóa chưa
try:
    os.listdir(temp_dir)
    print("Directory still exists")
except FileNotFoundError:
    print("Directory has been removed as expected")

# ===== 4. CHANGING DIRECTORY TEMPORARILY =====
print("\n--- Changing Directory Example ---")

@contextlib.contextmanager
def changed_directory(path):
    """Temporarily change working directory and then change back."""
    old_dir = os.getcwd()
    try:
        os.chdir(path)
        print(f"Changed directory to: {os.getcwd()}")
        yield
    finally:
        os.chdir(old_dir)
        print(f"Changed back to original directory: {os.getcwd()}")

# Sử dụng context manager để thay đổi directory tạm thời
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# Tạo thư mục tạm thời để thay đổi vào
os.makedirs("temp_dir", exist_ok=True)

with changed_directory("temp_dir"):
    # Tạo file trong thư mục mới
    with open("temp_file.txt", "w") as file:
        file.write("File in temporary directory")
    print(f"Files in temporary directory: {os.listdir()}")

print(f"Back in original directory: {os.getcwd()}")

# Dọn dẹp
shutil.rmtree("temp_dir")

# ===== 5. REDIRECTING STDOUT =====
print("\n--- Redirecting stdout Example ---")

import sys
from io import StringIO

@contextlib.contextmanager
def redirected_stdout():
    """Capture and redirect stdout temporarily."""
    original_stdout = sys.stdout
    temp_stdout = StringIO()
    try:
        sys.stdout = temp_stdout
        yield temp_stdout
    finally:
        sys.stdout = original_stdout

# Sử dụng context manager để redirect stdout
with redirected_stdout() as new_stdout:
    print("This will be captured instead of printed")
    print("More captured output")

# Output đã bị bắt vào new_stdout thay vì hiển thị ra console
captured_output = new_stdout.getvalue()
print(f"Captured output: {captured_output}")

# ===== 6. TIMER CONTEXT MANAGER =====
print("\n--- Timer Example ---")

import time

@contextlib.contextmanager
def timer(name):
    """Measure execution time of a code block."""
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"{name} took {elapsed:.6f} seconds to execute")

# Sử dụng context manager để đo thời gian
with timer("Sleeping operation"):
    time.sleep(1.5)  # Giả lập một thao tác tốn thời gian

with timer("Loop operation"):
    # Một thao tác tốn thời gian
    result = 0
    for i in range(1000000):
        result += i

# =========== CONTEXTLIB UTILITIES ===========
print("\n\n=== More contextlib Utilities ===")

# ===== SUPPRESS =====
print("\n--- suppress: Ignore specific exceptions ---")

# Giả sử chúng ta có một hàm có thể gây ra nhiều loại exception
def risky_operation(arg):
    if arg < 0:
        raise ValueError("Negative value")
    elif arg == 0:
        raise ZeroDivisionError("Zero division")
    else:
        return 10 / arg

# Bình thường
try:
    result = risky_operation(0)
except (ValueError, ZeroDivisionError) as e:
    print(f"Caught error: {e}")

# Với suppress - chỉ bỏ qua ZeroDivisionError
with contextlib.suppress(ZeroDivisionError):
    result = risky_operation(0)  # ZeroDivisionError được bỏ qua
    print("This won't execute")
print("Continued after suppressed ZeroDivisionError")

# Với ValueError sẽ vẫn gây crash
try:
    with contextlib.suppress(ZeroDivisionError):
        result = risky_operation(-1)  # ValueError không được bỏ qua
        print("This won't execute")
except ValueError as e:
    print(f"ValueError wasn't suppressed: {e}")

# ===== REDIRECT_STDOUT AND REDIRECT_STDERR =====
print("\n--- redirect_stdout and redirect_stderr ---")

# Chuyển hướng stdout và stderr sang một file object khác
with StringIO() as buffer, contextlib.redirect_stdout(buffer):
    print("This is redirected to the buffer")
    print("And so is this")
    captured = buffer.getvalue()

print(f"Captured with redirect_stdout: {captured}")

# Cả stderr
with StringIO() as buffer, contextlib.redirect_stderr(buffer):
    print("This goes to normal stdout")
    sys.stderr.write("This error message goes to the buffer\n")
    captured = buffer.getvalue()

print(f"Captured with redirect_stderr: {captured}")

# ===== EXITSTACK =====
print("\n--- ExitStack: Manage a dynamic number of context managers ---")

@contextlib.contextmanager
def debug_context(name):
    print(f"Entering {name} context")
    yield
    print(f"Exiting {name} context")

# Sử dụng ExitStack để quản lý nhiều context managers
with contextlib.ExitStack() as stack:
    # Thêm các context managers vào stack
    stack.enter_context(debug_context("first"))
    stack.enter_context(debug_context("second"))
    
    # Thêm một callback sẽ được gọi khi thoát khỏi ExitStack
    stack.callback(print, "This is a callback")
    
    # Mô phỏng thêm context managers một cách linh hoạt
    if True:  # có thể là điều kiện thời gian chạy
        stack.enter_context(debug_context("conditional"))
    
    print("Inside ExitStack block")

# ===== CLOSING =====
print("\n--- closing: Ensure close() is called ---")

class Resource:
    def __init__(self, name):
        self.name = name
        print(f"Resource {name} initialized")
    
    def close(self):
        print(f"Resource {self.name} closed")
    
    def operation(self):
        print(f"Performing operation on {self.name}")

# Sử dụng closing để đảm bảo close() được gọi
resource = Resource("example")
with contextlib.closing(resource) as r:
    r.operation()
print("Resource should be closed now")

# ===== NULLCONTEXT =====
print("\n--- nullcontext: Dummy context manager ---")

# Hàm sử dụng optional context manager
def process_with_optional_transaction(data, transaction=None):
    # Sử dụng transaction nếu có, nếu không thì dùng nullcontext
    with transaction or contextlib.nullcontext():
        print(f"Processing {data}")
        # Trong thực tế, đây có thể là thao tác DB cần transaction

# Sử dụng với transaction thật
class DummyTransaction:
    def __enter__(self):
        print("Starting transaction")
        return self
    
    def __exit__(self, *args):
        print("Committing transaction")
        return False

# Với transaction
process_with_optional_transaction("data 1", DummyTransaction())

# Không có transaction
process_with_optional_transaction("data 2")  # Sử dụng nullcontext

# =========== ADVANCED PATTERNS ===========
print("\n\n=== Advanced Context Manager Patterns ===")

# ===== REENTRANT CONTEXT MANAGERS =====
print("\n--- Reentrant Context Managers ---")

class ReentrantLock:
    def __init__(self):
        self._lock = threading.RLock()  # Reentrant lock
    
    def __enter__(self):
        print("Acquiring lock")
        self._lock.acquire()
        return self
    
    def __exit__(self, *args):
        print("Releasing lock")
        self._lock.release()
        return False
    
    def locked_operation(self):
        print("Performing locked operation")
        # Có thể an toàn gọi lại __enter__ và __exit__
        with self:
            print("Nested operation with same lock")

# Sử dụng reentrant context manager
with ReentrantLock() as lock:
    print("First level operation")
    lock.locked_operation()  # Sẽ lấy lock lần nữa một cách an toàn

# ===== CONTEXT MANAGER WITH STATE =====
print("\n--- Context Manager with State ---")

class DBTransaction:
    def __init__(self, connection):
        self.connection = connection
        self.transaction_level = 0
        print("Transaction object created")
    
    def __enter__(self):
        self.transaction_level += 1
        if self.transaction_level == 1:
            # Chỉ bắt đầu transaction thật sự ở level đầu tiên
            print("BEGIN TRANSACTION")
        else:
            print(f"SAVEPOINT level_{self.transaction_level}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Rollback nếu có exception
            print(f"ROLLBACK TO SAVEPOINT level_{self.transaction_level}")
        else:
            # Commit nếu không có exception
            print(f"RELEASE SAVEPOINT level_{self.transaction_level}")
        
        self.transaction_level -= 1
        if self.transaction_level == 0:
            # Chỉ commit/rollback thật sự ở transaction gốc
            if exc_type is not None:
                print("ROLLBACK TRANSACTION")
            else:
                print("COMMIT TRANSACTION")
        
        return False  # Cho phép exception lan truyền

# Sử dụng nested transactions
db_connection = "Database connection (simulated)"
transaction = DBTransaction(db_connection)

with transaction:
    print("Performing operation 1")
    
    with transaction:
        print("Performing nested operation 2")
        
        with transaction:
            print("Performing deeply nested operation 3")
            # Uncomment để xem rollback
            # raise ValueError("Oops")

# ===== ASYNC CONTEXT MANAGERS =====
print("\n--- Async Context Managers (Python 3.7+) ---")

import asyncio

class AsyncResource:
    async def __aenter__(self):
        print("Async setup - acquiring resource")
        await asyncio.sleep(0.1)  # Simulate async setup
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Async teardown - releasing resource")
        await asyncio.sleep(0.1)  # Simulate async teardown
        return False
    
    async def use_resource(self):
        print("Using the async resource")
        await asyncio.sleep(0.2)  # Simulate async operation

@contextlib.asynccontextmanager
async def async_resource_manager():
    print("Setting up async resource")
    await asyncio.sleep(0.1)
    try:
        yield "resource"
    finally:
        print("Cleaning up async resource")
        await asyncio.sleep(0.1)

async def use_async_context_manager():
    # Sử dụng async with
    async with AsyncResource() as resource:
        await resource.use_resource()
    
    # Sử dụng decorator
    async with async_resource_manager() as res:
        print(f"Using {res}")
        await asyncio.sleep(0.2)

# Chạy coroutine
print("Running async context manager demo")
asyncio.run(use_async_context_manager())

# =========== BEST PRACTICES ===========
print("\n\n=== Best Practices ===")

print("1. Luôn đảm bảo cleanup trong __exit__ hoặc finally block")
print("2. Sử dụng contextlib.contextmanager khi có thể để code ngắn gọn hơn")
print("3. Xử lý exceptions trong __exit__ cẩn thận")
print("4. Tránh code phức tạp trong __enter__ và __exit__")
print("5. Sử dụng ExitStack cho dynamic context management")

# =========== SUMMARY ===========
print("\n\n=== Summary ===")

print("Context Managers trong Python:")
print("- Đơn giản hóa quản lý tài nguyên với cú pháp with")
print("- Đảm bảo cleanup code được thực thi ngay cả khi có exceptions")
print("- Có thể triển khai bằng class với __enter__/__exit__ hoặc decorator")
print("- contextlib cung cấp nhiều utilities hữu ích")
print("- Sử dụng cho files, locks, transactions, và nhiều tài nguyên khác")
print("- Async context managers mở rộng pattern cho asynchronous code")
print("- Không có tương đương trực tiếp trong JavaScript (trước ES2022)")

# Dọn dẹp files tạo ra trong ví dụ
import os
files_to_remove = [
    'sample.txt', 'custom.txt', 'contextlib_example.txt',
    'file1.txt', 'file2.txt', 'outer.txt', 'inner.txt'
]

for file in files_to_remove:
    try:
        os.remove(file)
        print(f"Removed {file}")
    except FileNotFoundError:
        pass

print("\nCleanup completed")