'''
Python Concurrency: Threading và Multiprocessing cho JavaScript Developers
=================================================================

Python hỗ trợ nhiều mô hình lập trình đồng thời (concurrency) khác nhau.
Trong khi JavaScript chỉ có một thread chính với event loop (Node.js),
Python cung cấp cả Threading và Multiprocessing cho các tác vụ song song.
'''

# =========== CONCURRENCY VS PARALLELISM ===========
# Concurrency (đồng thời): Xử lý nhiều tác vụ trong cùng một khoảng thời gian
# Parallelism (song song): Thực hiện nhiều tác vụ cùng một lúc

print("Python hỗ trợ cả Concurrency và Parallelism:")
print("- Threading: Concurrency với shared memory (GIL)")
print("- Multiprocessing: Parallelism với isolated memory")
print("- AsyncIO: Concurrency với event loop (giống Node.js)")

# =========== PYTHON'S GLOBAL INTERPRETER LOCK (GIL) ===========
# GIL là một cơ chế khóa trong CPython chỉ cho phép một thread thực thi Python bytecode tại một thời điểm
# GIL giúp quản lý memory đơn giản, nhưng hạn chế parallelism thực sự trong CPU-bound tasks

print("\nGIL lý giải tại sao:")
print("- Threading tốt cho I/O-bound tasks (network, file operations)")
print("- Multiprocessing tốt cho CPU-bound tasks (tính toán phức tạp)")

# =========== THREADING BASICS ===========
import threading
import time
import os

def worker(name, delay):
    """Hàm worker đơn giản cho thread."""
    print(f"{name} starting in process {os.getpid()}, thread {threading.get_ident()}")
    count = 0
    while count < 3:
        time.sleep(delay)
        count += 1
        print(f"{name} working: {count}")
    print(f"{name} finished")

def basic_threading_example():
    print("\n=== Threading Basic Example ===")
    # Tạo 2 threads
    thread1 = threading.Thread(target=worker, args=("Thread-1", 0.5))
    thread2 = threading.Thread(target=worker, args=("Thread-2", 1))

    # Start threads
    thread1.start()
    thread2.start()

    # Tiếp tục chạy main thread
    print("Main thread continues execution...")
    
    # Wait cho threads hoàn thành
    thread1.join()
    thread2.join()
    
    print("All threads have finished")

# Chạy ví dụ threading cơ bản
basic_threading_example()

# So sánh với JavaScript:
# JavaScript chỉ có một main thread, nhưng sử dụng event loop và callbacks
# // JavaScript trong Node.js:
# function worker(name, delay) {
#   console.log(`${name} starting`);
#   let count = 0;
#   const interval = setInterval(() => {
#     count++;
#     console.log(`${name} working: ${count}`);
#     if (count >= 3) {
#       clearInterval(interval);
#       console.log(`${name} finished`);
#     }
#   }, delay);
# }
# worker("Task-1", 500);
# worker("Task-2", 1000);
# console.log("Main thread continues execution...");

# =========== THREADING: SHARING DATA ===========
# Threads chia sẻ memory space, nên cần cẩn thận với race conditions

def thread_unsafe_counter():
    print("\n=== Thread Unsafe Counter Example ===")
    
    # Biến được chia sẻ giữa các threads
    counter = 0
    
    def increment():
        nonlocal counter
        for _ in range(1000000):
            counter += 1
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=increment)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Final counter value: {counter}")
    print("Expected value: 5000000")
    print("Note: Value is often less due to race conditions!")

# thread_unsafe_counter()  # Uncomment để chạy (có thể mất nhiều thời gian)

# =========== THREADING: SYNCHRONIZATION ===========
# Locks, Semaphores, và các cơ chế đồng bộ hóa khác

def thread_safe_counter():
    print("\n=== Thread Safe Counter Example ===")
    
    counter = 0
    counter_lock = threading.Lock()
    
    def increment():
        nonlocal counter
        for _ in range(100000):  # Reduced for speed
            with counter_lock:  # Use Lock as context manager
                counter += 1
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=increment)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Final counter value: {counter}")
    print("Expected value: 500000")
    print("With Lock, count is accurate!")

thread_safe_counter()

# =========== THREAD POOL ===========
# ThreadPoolExecutor từ Python 3.2+ giúp quản lý thread pool

from concurrent.futures import ThreadPoolExecutor
import random

def process_item(item):
    """Giả lập xử lý item với thời gian ngẫu nhiên."""
    process_time = random.uniform(0.1, 0.5)
    time.sleep(process_time)
    return f"Processed {item} in {process_time:.2f}s"

def thread_pool_example():
    print("\n=== Thread Pool Example ===")
    items = list(range(1, 11))
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Cách 1: map() - Kết quả theo thứ tự đầu vào
        results = executor.map(process_item, items)
        print("Results with map() (ordered):")
        for result in results:
            print(f"  {result}")
            
        # Cách 2: submit() + as_completed() - Kết quả theo thứ tự hoàn thành
        print("\nResults with submit() + as_completed() (as completed):")
        futures = [executor.submit(process_item, item) for item in items]
        
        from concurrent.futures import as_completed
        for future in as_completed(futures):
            print(f"  {future.result()}")

thread_pool_example()

# So sánh với JavaScript:
# // Trong Node.js, Promise.all() giống như map()
# const processItem = async (item) => { /* ... */ };
# const items = Array.from({length: 10}, (_, i) => i + 1);
# 
# // Ordered results (like map())
# const results = await Promise.all(items.map(processItem));
# 
# // As completed (no direct equivalent, requires custom implementation)
# const futures = items.map(item => processItem(item));
# for (const result of await Promise.allSettled(futures)) {
#   if (result.status === 'fulfilled') console.log(result.value);
# }

# =========== MULTIPROCESSING BASICS ===========
# Multiprocessing khắc phục giới hạn của GIL bằng cách tạo nhiều processes

import multiprocessing as mp

def cpu_bound_task(n):
    """Một tác vụ tốn nhiều CPU."""
    count = 0
    for i in range(n):
        count += i
    return count

def basic_multiprocessing():
    print("\n=== Basic Multiprocessing Example ===")
    
    # Tạo pool với 4 processes
    with mp.Pool(processes=4) as pool:
        results = pool.map(cpu_bound_task, [10000000, 20000000, 30000000, 40000000])
        
    print(f"Results: {results}")

if __name__ == "__main__":  # Quan trọng cho multiprocessing
    basic_multiprocessing()

# =========== MEASURING PERFORMANCE: THREADING VS MULTIPROCESSING ===========

import concurrent.futures
import math

# CPU-bound task: Tính toán số nguyên tố
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_primes(numbers):
    return [n for n in numbers if is_prime(n)]

def measure_performance():
    print("\n=== Performance Comparison ===")
    
    # Tạo range of numbers để kiểm tra
    NUMBERS = list(range(100000, 101000))  # 1000 số lớn để kiểm tra
    
    # Sequential execution
    start_time = time.time()
    sequential_result = find_primes(NUMBERS)
    sequential_time = time.time() - start_time
    
    # Threading
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Chia numbers thành 4 chunks
        chunk_size = len(NUMBERS) // 4
        chunks = [NUMBERS[i:i + chunk_size] for i in range(0, len(NUMBERS), chunk_size)]
        thread_result = list(executor.map(find_primes, chunks))
        # Flat list of lists
        thread_result = [item for sublist in thread_result for item in sublist]
    threading_time = time.time() - start_time
    
    # Multiprocessing
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        # Tương tự như threading
        chunk_size = len(NUMBERS) // 4
        chunks = [NUMBERS[i:i + chunk_size] for i in range(0, len(NUMBERS), chunk_size)]
        mp_result = list(executor.map(find_primes, chunks))
        mp_result = [item for sublist in mp_result for item in sublist]
    multiprocessing_time = time.time() - start_time
    
    # Print results
    print(f"Found {len(sequential_result)} prime numbers")
    print(f"Sequential time: {sequential_time:.4f}s")
    print(f"Threading time: {threading_time:.4f}s")
    print(f"Multiprocessing time: {multiprocessing_time:.4f}s")
    
    print("\nObservations:")
    print("- For CPU-bound tasks (prime calculation), multiprocessing is faster")
    print("- Threading may even be slower than sequential due to GIL and overhead")
    print("- Results may vary based on your CPU cores and system load")

if __name__ == "__main__":
    measure_performance()

# =========== PROCESS COMMUNICATION ===========
# Processes không chia sẻ memory, nên cần cơ chế giao tiếp

def process_communication_example():
    print("\n=== Process Communication Example ===")
    
    # 1. Sử dụng Queue
    def producer(queue):
        print(f"Producer process {os.getpid()}")
        for i in range(5):
            item = f"Item {i}"
            queue.put(item)
            print(f"Produced: {item}")
            time.sleep(0.1)
    
    def consumer(queue):
        print(f"Consumer process {os.getpid()}")
        while True:
            if queue.empty():
                time.sleep(0.1)
                continue
            
            item = queue.get()
            if item is None:  # Poison pill
                break
            print(f"Consumed: {item}")
            time.sleep(0.2)
    
    # Tạo shared queue
    queue = mp.Queue()
    
    # Start processes
    prod = mp.Process(target=producer, args=(queue,))
    cons = mp.Process(target=consumer, args=(queue,))
    
    prod.start()
    cons.start()
    
    # Wait for producer
    prod.join()
    
    # Send poison pill và đợi consumer
    queue.put(None)
    cons.join()
    
    print("Process communication completed")

if __name__ == "__main__":
    # process_communication_example()  # Uncomment to run
    pass

# =========== SHARED MEMORY TRONG MULTIPROCESSING ===========

def shared_memory_example():
    print("\n=== Shared Memory Example ===")
    
    # Shared Value và Array
    counter = mp.Value('i', 0)  # Shared integer
    array = mp.Array('i', range(5))  # Shared array of integers
    
    def increment_counter(counter, array, index):
        # Lấy lock cho counter
        with counter.get_lock():
            counter.value += 1
        
        # Sửa array
        array[index] = index * 2
        print(f"Process {os.getpid()}: counter = {counter.value}, array[{index}] = {array[index]}")
    
    # Tạo processes
    processes = []
    for i in range(5):
        p = mp.Process(target=increment_counter, args=(counter, array, i))
        processes.append(p)
        p.start()
    
    # Đợi tất cả processes hoàn thành
    for p in processes:
        p.join()
    
    print(f"Final counter value: {counter.value}")
    print(f"Final array: {list(array)}")

if __name__ == "__main__":
    # shared_memory_example()  # Uncomment to run
    pass

# =========== PROCESS POOL VS THREAD POOL ===========

def compare_pools():
    print("\n=== Process Pool vs Thread Pool ===")
    
    # I/O-bound task: simulate network request
    def io_bound_task(url):
        print(f"Fetching: {url}")
        time.sleep(1)  # Simulate network delay
        return f"Result from {url}"
    
    # CPU-bound task: calculate primes
    def cpu_bound_task(n):
        return len([i for i in range(2, n) if is_prime(i)])
    
    # Test data
    urls = [f"https://example.com/{i}" for i in range(10)]
    numbers = [100000 + i * 1000 for i in range(10)]
    
    print("Processing I/O-bound tasks...")
    
    # Thread Pool for I/O-bound
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(io_bound_task, urls))
    thread_time = time.time() - start
    
    # Process Pool for I/O-bound
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(io_bound_task, urls))
    process_time = time.time() - start
    
    print(f"I/O-bound tasks:")
    print(f"- Thread Pool: {thread_time:.2f}s")
    print(f"- Process Pool: {process_time:.2f}s")
    
    print("\nProcessing CPU-bound tasks...")
    
    # Thread Pool for CPU-bound
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, numbers))
    thread_time = time.time() - start
    
    # Process Pool for CPU-bound
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, numbers))
    process_time = time.time() - start
    
    print(f"CPU-bound tasks:")
    print(f"- Thread Pool: {thread_time:.2f}s")
    print(f"- Process Pool: {process_time:.2f}s")
    
    print("\nConclusions:")
    print("- For I/O-bound tasks: Thread Pool is usually more efficient")
    print("- For CPU-bound tasks: Process Pool is usually more efficient")
    print("- Process Pool has higher startup overhead")

if __name__ == "__main__":
    # compare_pools()  # Uncomment to run
    pass

# =========== BEST PRACTICES ===========

print("\n=== Best Practices for Concurrency in Python ===")
print("1. Use threading for I/O-bound tasks, multiprocessing for CPU-bound tasks")
print("2. Always protect shared resources with locks in threading")
print("3. Use 'if __name__ == \"__main__\":' guard for multiprocessing code")
print("4. Consider using ThreadPoolExecutor and ProcessPoolExecutor for easy pool management")
print("5. Avoid sharing complex mutable objects between processes when possible")
print("6. For complex parallel tasks, consider libraries like Dask or Joblib")
print("7. Understand that more threads/processes isn't always better (diminishing returns)")
print("8. When using locks, be aware of deadlock possibilities")
print("9. Consider asyncio for I/O-bound concurrent tasks as an alternative to threading")
print("10. Profile your code to ensure concurrency actually improves performance")

# =========== SO SÁNH VỚI JAVASCRIPT ===========

print("\n=== Python vs JavaScript Concurrency ===")
print("JavaScript:")
print("- Single-threaded with event loop")
print("- Promises, async/await for non-blocking I/O")
print("- Worker threads (in Node.js) for CPU-bound tasks")
print("- No true parallelism in the main JS runtime")

print("\nPython:")
print("- Threading for concurrent I/O tasks")
print("- Multiprocessing for parallel CPU tasks")
print("- AsyncIO for event-loop based concurrency (similar to JS)")
print("- More flexible model but also more complex")
print("- GIL can be a limitation in CPython")