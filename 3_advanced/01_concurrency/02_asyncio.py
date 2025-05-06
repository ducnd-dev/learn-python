'''
Python AsyncIO cho JavaScript Developers
====================================

AsyncIO là một mô hình lập trình bất đồng bộ trong Python, tương tự như
mô hình sử dụng Promises và async/await trong JavaScript.

AsyncIO được giới thiệu trong Python 3.4 và hỗ trợ async/await từ Python 3.5.
'''

# =========== ASYNCIO vs JAVASCRIPT EVENT LOOP ===========
# AsyncIO trong Python và JavaScript's Event Loop có nhiều điểm tương đồng

import asyncio
import time
import random
import aiohttp
import sys

print("Python AsyncIO vs JavaScript Async Programming")
print("----------------------------------------------")
print("Tương đồng:")
print("- Cả hai đều là non-blocking I/O models")
print("- Cả hai đều sử dụng một event loop")
print("- Cả hai đều hỗ trợ async/await syntax")
print("- Cả hai đều xử lý tác vụ đồng thời không cần multithreading")

print("\nKhác biệt:")
print("- Python AsyncIO là một thư viện/module; JavaScript event loop được tích hợp sẵn")
print("- Python vẫn hỗ trợ threading và multiprocessing bên cạnh asyncio")
print("- Python asyncio thường phải dùng thư viện async-aware (như aiohttp thay vì requests)")

# =========== COROUTINES CƠ BẢN ===========
# Coroutines đóng vai trò tương tự như Promises trong JavaScript

async def hello_world():
    """Coroutine đơn giản"""
    print("Hello...")
    await asyncio.sleep(1)  # Non-blocking sleep, tương tự setTimeout() trong JS
    print("...World!")
    return "Completed"

# Trong Python 3.7+
if sys.version_info >= (3, 7):
    print("\n=== Basic Coroutine Example (Python 3.7+) ===")
    asyncio.run(hello_world())  # Đơn giản nhất để chạy coroutine

# Trong tất cả các phiên bản python 3.5+
print("\n=== Basic Coroutine Example (All Python 3.5+) ===")
loop = asyncio.get_event_loop()
result = loop.run_until_complete(hello_world())
print(f"Result: {result}")

# So sánh với JavaScript:
# async function helloWorld() {
#   console.log("Hello...");
#   await new Promise(resolve => setTimeout(resolve, 1000));
#   console.log("...World!");
#   return "Completed";
# }
# 
# helloWorld().then(result => console.log(`Result: ${result}`));

# =========== CHẠY NHIỀU COROUTINES ===========
# Tương tự Promise.all() trong JavaScript

async def fetch_data(delay, value):
    """Giả lập một network request"""
    print(f"Fetching data {value}...")
    await asyncio.sleep(delay)  # Giả lập độ trễ network
    print(f"Data {value} fetched after {delay}s")
    return f"Data{value}"

async def main_gather():
    # asyncio.gather() tương tự như Promise.all() trong JavaScript
    print("\n=== Running multiple coroutines with gather ===")
    start = time.time()
    
    # Tạo 3 coroutines
    coro1 = fetch_data(1, 1)
    coro2 = fetch_data(2, 2)
    coro3 = fetch_data(3, 3)
    
    # Chạy chúng đồng thời
    results = await asyncio.gather(coro1, coro2, coro3)
    
    end = time.time()
    print(f"Results: {results}")
    print(f"Total time: {end - start:.2f}s (thay vì 6s nếu chạy tuần tự)")

loop.run_until_complete(main_gather())

# So sánh với JavaScript:
# async function fetchData(delay, value) {
#   console.log(`Fetching data ${value}...`);
#   await new Promise(resolve => setTimeout(resolve, delay * 1000));
#   console.log(`Data ${value} fetched after ${delay}s`);
#   return `Data${value}`;
# }
# 
# async function main() {
#   const start = Date.now();
#   
#   const results = await Promise.all([
#     fetchData(1, 1),
#     fetchData(2, 2),
#     fetchData(3, 3)
#   ]);
#   
#   const end = Date.now();
#   console.log(`Results: ${results}`);
#   console.log(`Total time: ${(end - start) / 1000}s`);
# }
# 
# main();

# =========== ASYNCIO.TASK ===========
# Task tương tự như Promise đã được kích hoạt

async def main_task():
    print("\n=== Running with asyncio.Task ===")
    start = time.time()
    
    # Tạo task object (Promise được kích hoạt ngay)
    task1 = asyncio.create_task(fetch_data(1, "A"))
    task2 = asyncio.create_task(fetch_data(1.5, "B"))
    
    # Lúc này, task đã bắt đầu chạy trong background
    print("Tasks created and started running...")
    
    # Làm việc khác trong khoảng thời gian này
    await asyncio.sleep(0.5)
    print("Did some other work while tasks are running...")
    
    # Đợi tasks hoàn thành
    result1 = await task1
    result2 = await task2
    
    end = time.time()
    print(f"Results: {result1}, {result2}")
    print(f"Total time: {end - start:.2f}s")

# Chạy với asyncio.Task 
if sys.version_info >= (3, 7):
    asyncio.run(main_task())
else:
    loop.run_until_complete(main_task())

# So sánh với JavaScript:
# // Trong JavaScript, Promise start ngay khi tạo
# const task1 = fetchData(1, "A");  // Đã bắt đầu chạy
# const task2 = fetchData(1.5, "B");  // Đã bắt đầu chạy
# 
# // Đợi kết quả sau
# const [result1, result2] = await Promise.all([task1, task2]);

# =========== ASYNCIO.WAIT vs PROMISE.RACE ===========
# asyncio.wait cho phép đợi khi một tập hợp coroutines hoàn thành

async def main_wait():
    print("\n=== Running with asyncio.wait ===")
    
    # Tạo các task với thời gian hoàn thành ngẫu nhiên
    tasks = [
        asyncio.create_task(fetch_data(random.uniform(0.5, 2), i))
        for i in range(5)
    ]
    
    # Đợi cho ít nhất 2 task hoàn thành
    done, pending = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_COMPLETED, timeout=2
    )
    
    print(f"\n{len(done)} tasks completed, {len(pending)} still pending")
    
    # Xem kết quả của các task đã hoàn thành
    for task in done:
        print(f"Completed task result: {task.result()}")
    
    # Hủy các task còn lại
    for task in pending:
        task.cancel()
    
    # Đợi các task còn lại xử lý hủy
    await asyncio.gather(*pending, return_exceptions=True)
    print("Remaining tasks have been canceled")

if sys.version_info >= (3, 7):
    asyncio.run(main_wait())
else:
    loop.run_until_complete(main_wait())

# So sánh với JavaScript:
# // Promise.race chỉ trả về Promise đầu tiên hoàn thành
# const promises = Array.from({length: 5}, (_, i) => 
#   fetchData(Math.random() * 1.5 + 0.5, i)
# );
# 
# const winner = await Promise.race(promises);
# console.log(`First completed: ${winner}`);
#
# // Không có tương đương trực tiếp cho asyncio.wait
# // Nhưng có thể dùng Promise.race kết hợp với setTimeout

# =========== XỬ LÝ LỖI ===========
# Xử lý exception trong async code

async def might_fail(fail=False):
    await asyncio.sleep(1)
    if fail:
        raise ValueError("Operation failed!")
    return "Success"

async def error_handling_example():
    print("\n=== Error Handling Example ===")
    
    # 1. Sử dụng try/except (giống try/catch trong JavaScript)
    try:
        result = await might_fail(fail=True)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Caught error: {e}")
    
    # 2. Xử lý lỗi với gather
    results = await asyncio.gather(
        might_fail(fail=False),
        might_fail(fail=True),
        return_exceptions=True  # Quan trọng: exception được trả về, không ném
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed with: {result}")
        else:
            print(f"Task {i} succeeded with: {result}")

if sys.version_info >= (3, 7):
    asyncio.run(error_handling_example())
else:
    loop.run_until_complete(error_handling_example())

# So sánh với JavaScript:
# // Try/catch
# try {
#   const result = await mightFail(true);
#   console.log(`Result: ${result}`);
# } catch (error) {
#   console.log(`Caught error: ${error.message}`);
# }
#
# // Promise.allSettled() tương tự asyncio.gather với return_exceptions=True
# const results = await Promise.allSettled([
#   mightFail(false),
#   mightFail(true)
# ]);
#
# results.forEach((result, i) => {
#   if (result.status === 'fulfilled') {
#     console.log(`Task ${i} succeeded with: ${result.value}`);
#   } else {
#     console.log(`Task ${i} failed with: ${result.reason}`);
#   }
# });

# =========== ASYNC FOR VÀ ASYNC WITH ===========
# Xử lý iterators và context managers một cách bất đồng bộ

# Async generator (tương tự như async generator trong JS)
async def async_range(count):
    for i in range(count):
        await asyncio.sleep(0.5)
        yield i

# Async context manager
class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource asynchronously...")
        await asyncio.sleep(1)
        print("Resource acquired")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource asynchronously...")
        await asyncio.sleep(0.5)
        print("Resource released")
    
    async def work(self):
        await asyncio.sleep(1)
        return "Work completed"

async def for_and_with_example():
    print("\n=== Async For and Async With Example ===")
    
    # Async for
    print("Async for example:")
    async for i in async_range(3):
        print(f"Got value: {i}")
    
    # Async with
    print("\nAsync with example:")
    async with AsyncResource() as resource:
        result = await resource.work()
        print(f"Result: {result}")

if sys.version_info >= (3, 7):
    asyncio.run(for_and_with_example())
else:
    loop.run_until_complete(for_and_with_example())

# So sánh với JavaScript:
# // Async generator
# async function* asyncRange(count) {
#   for (let i = 0; i < count; i++) {
#     await new Promise(resolve => setTimeout(resolve, 500));
#     yield i;
#   }
# }
#
# // Sử dụng async generator
# for await (const i of asyncRange(3)) {
#   console.log(`Got value: ${i}`);
# }
#
# // JavaScript không có async with chính thức, nhưng có thể giả lập:
# class AsyncResource {
#   async acquire() {
#     console.log("Acquiring resource asynchronously...");
#     await new Promise(resolve => setTimeout(resolve, 1000));
#     console.log("Resource acquired");
#     return this;
#   }
#
#   async release() {
#     console.log("Releasing resource asynchronously...");
#     await new Promise(resolve => setTimeout(resolve, 500));
#     console.log("Resource released");
#   }
#
#   async work() {
#     await new Promise(resolve => setTimeout(resolve, 1000));
#     return "Work completed";
#   }
# }
#
# // Sử dụng đối tượng này
# const resource = new AsyncResource();
# try {
#   await resource.acquire();
#   const result = await resource.work();
#   console.log(`Result: ${result}`);
# } finally {
#   await resource.release();
# }

# =========== HTTP REQUESTS ===========
# Ví dụ sử dụng aiohttp (thư viện HTTP async cho Python)

async def fetch_url(session, url):
    """Fetch data from url asynchronously."""
    print(f"Fetching {url}")
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return f"Error: {response.status} for {url}"
            
            data = await response.text()
            return f"Data from {url}: {len(data)} bytes"
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

async def http_example():
    print("\n=== HTTP Requests Example ===")
    urls = [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.github.com"
    ]
    
    # aiohttp là thư viện HTTP async của Python (không phải thư viện tiêu chuẩn)
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            for url, result in zip(urls, results):
                print(f"{url} -> {result}")
    except ImportError:
        print("aiohttp package not installed. Install with: pip install aiohttp")
        print("Example code for reference only.")

# Chỉ chạy nếu aiohttp được cài đặt
try:
    import aiohttp
    if sys.version_info >= (3, 7):
        asyncio.run(http_example())
    else:
        loop.run_until_complete(http_example())
except ImportError:
    print("\n=== HTTP Requests Example (aiohttp not installed) ===")
    print("aiohttp package not installed. Install with: pip install aiohttp")
    print("Example code for reference only.")

# So sánh với JavaScript:
# // Fetch API trong browser hoặc Node.js với node-fetch
# async function fetchUrl(url) {
#   console.log(`Fetching ${url}`);
#   try {
#     const response = await fetch(url);
#     if (!response.ok) {
#       return `Error: ${response.status} for ${url}`;
#     }
#     const data = await response.text();
#     return `Data from ${url}: ${data.length} bytes`;
#   } catch (error) {
#     return `Error fetching ${url}: ${error.message}`;
#   }
# }
#
# async function httpExample() {
#   const urls = [
#     "https://www.example.com",
#     "https://www.python.org",
#     "https://www.github.com"
#   ];
#
#   const results = await Promise.all(urls.map(url => fetchUrl(url)));
#
#   urls.forEach((url, i) => {
#     console.log(`${url} -> ${results[i]}`);
#   });
# }
#
# httpExample();

# =========== TIMEOUTS VÀ CANCELLATION ===========
# Xử lý timeout và hủy task

async def long_operation():
    print("Starting long operation...")
    try:
        await asyncio.sleep(10)  # Giả lập tác vụ kéo dài
        return "Long operation completed"
    except asyncio.CancelledError:
        print("Long operation was cancelled!")
        raise  # Re-raise để thông báo cancellation

async def timeout_and_cancel_example():
    print("\n=== Timeout and Cancellation Example ===")
    
    # 1. Sử dụng asyncio.wait_for để timeout
    try:
        print("Waiting for long operation with timeout...")
        result = await asyncio.wait_for(long_operation(), timeout=2)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out after 2 seconds!")
    
    # 2. Sử dụng asyncio.shield để tránh cancel
    task = asyncio.create_task(long_operation())
    
    # Đợi một chút
    await asyncio.sleep(1)
    
    # Hủy task
    print("Cancelling task...")
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task was successfully cancelled")

if sys.version_info >= (3, 7):
    asyncio.run(timeout_and_cancel_example())
else:
    loop.run_until_complete(timeout_and_cancel_example())

# So sánh với JavaScript:
# // Timeout với Promise.race và setTimeout
# async function longOperation() {
#   console.log("Starting long operation...");
#   try {
#     await new Promise(resolve => setTimeout(resolve, 10000));
#     return "Long operation completed";
#   } catch (error) {
#     console.log("Long operation was aborted!");
#     throw error;  // Re-throw
#   }
# }
#
# // Timeout implementation
# async function withTimeout(promise, timeoutMs) {
#   const timeout = new Promise((_, reject) => 
#     setTimeout(() => reject(new Error("Timeout")), timeoutMs)
#   );
#   return Promise.race([promise, timeout]);
# }
#
# // Cancellation with AbortController
# async function withCancellation() {
#   const controller = new AbortController();
#   const { signal } = controller;
#
#   // In modern fetch
#   const fetchPromise = fetch('https://example.com', { signal });
#
#   // Cancel after 1 second
#   setTimeout(() => {
#     console.log("Cancelling...");
#     controller.abort();
#   }, 1000);
#
#   try {
#     const response = await fetchPromise;
#     // ...
#   } catch (error) {
#     if (error.name === 'AbortError') {
#       console.log("Fetch was cancelled");
#     } else {
#       console.error("Fetch error:", error);
#     }
#   }
# }

# =========== ASYNCIO ĐỂ XỬ LÝ BLOCKING I/O ===========
# Chạy blocking I/O trong thread pool

import concurrent.futures

def blocking_io():
    """Một function thực hiện blocking I/O operation."""
    print(f"Blocking I/O operation running in thread: {threading.current_thread().name}")
    # Giả lập file I/O
    time.sleep(2)
    return "Blocking operation result"

async def run_blocking_in_thread_pool():
    print("\n=== Running Blocking I/O in Thread Pool ===")
    
    # Lấy default executor
    loop = asyncio.get_running_loop()
    
    # 1. Sử dụng run_in_executor để chạy blocking function
    print("Running blocking I/O in default thread pool...")
    result = await loop.run_in_executor(None, blocking_io)
    print(f"Result: {result}")
    
    # 2. Sử dụng custom thread pool
    print("\nRunning blocking I/O in custom thread pool...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        result1 = loop.run_in_executor(pool, blocking_io)
        result2 = loop.run_in_executor(pool, blocking_io)
        result3 = loop.run_in_executor(pool, blocking_io)
        
        # Đợi tất cả hoàn thành
        results = await asyncio.gather(result1, result2, result3)
        print(f"Results: {results}")

if sys.version_info >= (3, 7):
    import threading
    asyncio.run(run_blocking_in_thread_pool())
else:
    import threading
    loop.run_until_complete(run_blocking_in_thread_pool())

# So sánh với JavaScript:
# JavaScript xử lý blocking I/O khác:
# // Node.js sử dụng libuv event loop và sẵn có một thread pool
# // cho các operations như file I/O, DNS lookup, etc.
#
# // Để chạy CPU-intensive code, Node.js cung cấp Worker Threads
# const { Worker } = require('worker_threads');
#
# function runWorker(code) {
#   return new Promise((resolve, reject) => {
#     const worker = new Worker(
#       `const { parentPort } = require('worker_threads');
#        const result = (${code})();
#        parentPort.postMessage(result);`,
#       { eval: true }
#     );
#     worker.on('message', resolve);
#     worker.on('error', reject);
#   });
# }
#
# // Sử dụng
# async function main() {
#   const result = await runWorker(() => {
#     // Blocking code here
#     let sum = 0;
#     for (let i = 0; i < 1000000000; i++) {
#       sum += i;
#     }
#     return sum;
#   });
#   console.log(result);
# }

# =========== BEST PRACTICES ===========

print("\n=== AsyncIO Best Practices ===")
print("1. Không trộn lẫn sync và async code - I/O nên đồng nhất hoàn toàn async")
print("2. Sử dụng asyncio.run() (Python 3.7+) để chạy top-level coroutine")
print("3. Dùng async với thay vì chỉ await để quản lý tài nguyên đúng cách")
print("4. Cẩn thận với CPU-bound tasks - có thể block event loop")
print("5. Dùng asyncio.create_task() để chạy coroutines trong background")
print("6. Xử lý error và cancellation trong coroutines của bạn")
print("7. Dùng thư viện native async (aiohttp, asyncpg, ...) để đạt hiệu suất tốt nhất")
print("8. Đặt timeout cho tất cả network operations")
print("9. Dùng asyncio.run_in_executor() nếu phải gọi blocking functions")
print("10. Debug với asyncio.get_event_loop().set_debug(True)")

# =========== SO SÁNH TỔNG QUAN VỚI JAVASCRIPT ===========

print("\n=== Python AsyncIO vs JavaScript Async Programming: Tóm tắt ===")
print("Python:")
print("- Coroutines (async def / await)")
print("- asyncio.gather() ~ Promise.all()")
print("- asyncio.wait() ~ không có tương đương trực tiếp")
print("- asyncio.wait_for() ~ Promise.race() + timeout")
print("- asyncio.create_task() ~ kích hoạt Promise")
print("- Không có .then()/.catch() chains - dùng try/except")
print("- Nhiều options cho concurrency: threading, multiprocessing, asyncio")
print("- Cần thư viện async-aware riêng (aiohttp, asyncpg, ...)")

print("\nJavaScript:")
print("- Promises và async/await")
print("- Promise.all() ~ asyncio.gather()")
print("- Promise.race() ~ một phần của asyncio.wait()")
print("- Promise.allSettled() ~ asyncio.gather(return_exceptions=True)")
print("- Xây dựng hoàn toàn dựa trên event loop")
print("- Có .then()/.catch()/.finally() chains")
print("- Mọi APIs đều async theo mặc định (Browser & Node.js)")
print("- Callback hell đã được thay thế bằng Promises và async/await")