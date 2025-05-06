"""
Event Loop Internals trong asyncio
==================================

Phần này đi sâu vào cách hoạt động nội bộ của event loop trong module asyncio,
giúp hiểu các cơ chế bên dưới lập trình bất đồng bộ trong Python.
"""

import asyncio
import time
import inspect
import os
import selectors
import threading
from contextlib import contextmanager

# ====== Event Loop là gì? ======
print("==== Event Loop là gì? ====")
print("Event loop là một cơ chế lập trình cho phép một chương trình chờ và phản hồi các sự kiện.")
print("Trong Python asyncio, event loop quản lý và thực thi các coroutines, callbacks, tasks...")

# ===== Kiến trúc event loop trong asyncio =====
print("\n==== Kiến trúc event loop trong asyncio ====")
print("1. Selector event loop: Dựa trên selector module (epoll, kqueue, IOCP)")
print("2. ProactorEventLoop: Windows-specific, dùng Proactor I/O completion")

# Lấy event loop theo cách khác nhau
print("\nCác cách lấy event loop:")
print("1. asyncio.get_event_loop(): Lấy loop hiện tại hoặc tạo một loop mới")
print("2. asyncio.new_event_loop(): Tạo một event loop mới")
print("3. asyncio.set_event_loop(loop): Đặt một loop làm event loop hiện tại")

# ==== Xem xét các lớp event loop ====
print("\n==== Cấu trúc các lớp event loop ====")
print("Tất cả event loop thực thi giao diện AbstractEventLoop")

# Hiện thị một số method quan trọng của AbstractEventLoop
loop = asyncio.new_event_loop()
methods = [m for m in dir(loop) if not m.startswith('_') and callable(getattr(loop, m))]
selected_methods = [
    'run_forever', 'run_until_complete', 'stop', 'is_running', 
    'create_task', 'create_future', 'call_soon', 'call_later', 
    'call_at', 'create_connection'
]

print("\nMột số method quan trọng của event loop:")
for method in selected_methods:
    if method in methods:
        print(f"- {method}: {inspect.signature(getattr(loop, method))}")

# ==== Tìm hiểu sâu về các internal components ====
print("\n==== Internal Components ====")

# 1. Selector - nền tảng của I/O multiplexing
print("\n1. Selector - nền tảng của I/O không đồng bộ")
print("Các event loop dựa trên selectors để theo dõi các file descriptor I/O")

# Hiển thị các implementation của selector
selector_impls = ", ".join([cls for cls in dir(selectors) if 'Selector' in cls and not cls.startswith('_')])
print(f"Selector implementations: {selector_impls}")

# Phát hiện selector tốt nhất cho hệ thống
print(f"Selector tốt nhất cho hệ thống này: {selectors.DefaultSelector.__name__}")

# 2. Event Loop Policies
print("\n2. Event Loop Policies")
print("Policies quyết định cách tạo và quản lý event loop cho mỗi thread")
print(f"Current policy: {asyncio.get_event_loop_policy().__class__.__name__}")

# Kiểm tra event loop policy khác nhau trên các hệ thống
if os.name == 'nt':
    print("Trên Windows có ProactorEventLoop và SelectorEventLoop")
    print("Mặc định Windows Python 3.8+ sẽ dùng ProactorEventLoop")
else:
    print("Trên Unix-like systems, SelectorEventLoop là mặc định")
    print("Sử dụng selector tốt nhất cho mỗi nền tảng (epoll trên Linux, kqueue trên BSD)")

# ==== Cách Event Loop thực thi các Tasks ====
print("\n==== Cách Event Loop thực thi các Tasks ====")
print("Event loop sử dụng các cơ chế sau để thực thi code bất đồng bộ:")

# 1. Call Queue
print("\n1. Call Queue")
print("Loop duy trì một hàng đợi (_ready) các callbacks để thực thi")

# Minh họa call queue với call_soon
@contextmanager
def show_callbacks(loop):
    # Đây là giả lập để minh họa, không truy cập trực tiếp thuộc tính nội bộ trong code thực
    current_ready = list(getattr(loop, '_ready', []))
    print(f"  Ban đầu: {len(current_ready)} callbacks trong hàng đợi")
    yield
    new_ready = list(getattr(loop, '_ready', []))
    print(f"  Sau khi thêm: {len(new_ready)} callbacks trong hàng đợi")

# Sử dụng call_soon để thêm callbacks vào hàng đợi
with show_callbacks(loop):
    loop.call_soon(print, "Callback 1")
    loop.call_soon(print, "Callback 2")
    loop.call_soon(print, "Callback 3")

# 2. Coroutines và Task Execution
print("\n2. Coroutines và Task Execution")
print("Event loop thực thi coroutines bằng cách wrap chúng trong Task objects")

# Hiển thị cách tạo task
async def demo_coroutine():
    await asyncio.sleep(0.1)
    return "Coroutine đã hoàn thành"

task = loop.create_task(demo_coroutine())
print(f"Task được tạo: {task}")
print(f"Task state: {task._state}")

# ==== Chi tiết về event loop execution ====
print("\n==== Chi tiết về event loop execution ====")

# Minh họa flow thực thi bên trong event loop
def simulate_event_loop_iteration():
    print("\nMô phỏng một lần lặp (iteration) của event loop:")
    print("1. Xử lý các callbacks đã sẵn sàng trong _ready queue")
    print("2. Tính toán thời gian chờ tối đa cho selector")
    print("3. Gọi selector để đợi các sự kiện (I/O readiness)")
    print("4. Xử lý các sự kiện I/O đã sẵn sàng và lập lịch callbacks")
    print("5. Kiểm tra các timers và thực thi callbacks đã đến hạn")
    print("6. Lặp lại quá trình này cho đến khi stop() được gọi")

simulate_event_loop_iteration()

# ==== Handle và TimerHandle ====
print("\n==== Handle và TimerHandle ====")
print("asyncio sử dụng các đối tượng Handle để đại diện cho callbacks trong hàng đợi")

# Tạo một handle bằng call_soon
handle = loop.call_soon(print, "Handle callback")
print(f"Handle: {handle}")
print(f"Handle cancelled: {handle.cancelled()}")

# Tạo một timer handle với call_later
timer_handle = loop.call_later(1, print, "Timer handle callback")
print(f"TimerHandle: {timer_handle}")
print(f"TimerHandle when: {timer_handle.when()}")

# ==== Future internals ====
print("\n==== Future internals ====")
print("Futures là placeholders cho kết quả sẽ sẵn sàng trong tương lai")

# Tạo và kiểm tra một future
future = loop.create_future()
print(f"Future: {future}")
print(f"Future done: {future.done()}")

# Thêm một callback vào future
future.add_done_callback(lambda f: print(f"Future callback with result: {f.result()}"))

# Thiết lập kết quả cho future
print("Thiết lập kết quả cho future...")
future.set_result("Future result")
print(f"Future done: {future.done()}")
print(f"Future result: {future.result()}")

# ==== Tương tác giữa event loop và thread ====
print("\n==== Tương tác giữa event loop và thread ====")
print("asyncio event loops là thread-specific, mỗi thread có một current loop")

# Hiển thị thread-specific event loops
def show_thread_loop():
    try:
        thread_loop = asyncio.get_event_loop()
        print(f"Thread {threading.current_thread().name} có event loop: {thread_loop}")
    except RuntimeError as e:
        print(f"Thread {threading.current_thread().name} không có event loop: {e}")

# Kiểm tra loop trong thread chính
show_thread_loop()

# Tạo thread mới và kiểm tra loop
thread = threading.Thread(target=show_thread_loop, name="CustomThread")
thread.start()
thread.join()

# ==== Thread Safety ====
print("\n==== Thread Safety ====")
print("asyncio event loop KHÔNG thread-safe nói chung")
print("Để gọi từ thread khác, hãy dùng call_soon_threadsafe hoặc run_coroutine_threadsafe")

# ==== Event Loop và Network I/O ====
print("\n==== Event Loop và Network I/O ====")
print("event loop thực hiện I/O không đồng bộ thông qua selectors và transport/protocol")

# Transport và Protocol
print("\nTransport và Protocol:")
print("- Transport: Trừu tượng hóa cách dữ liệu được truyền (TCP, UDP, pipes)")
print("- Protocol: Xác định cách dữ liệu được xử lý")

# ==== Debug Mode ====
print("\n==== Debug Mode ====")
print("asyncio có debug mode giúp phát hiện vấn đề")

# Kiểm tra debug mode
old_debug = loop.get_debug()
print(f"Debug mode: {old_debug}")

# Bật debug mode và kiểm tra
loop.set_debug(True)
print(f"Debug mode sau khi bật: {loop.get_debug()}")

# Các tính năng debug mode
print("\nCác tính năng debug mode:")
print("- Slow callback warnings (>100ms)")
print("- Resource warnings cho tasks/futures bị hủy")
print("- Log khi exception không được xử lý")

# Đặt lại trạng thái debug
loop.set_debug(old_debug)

# ==== Ví dụ thực tế ====
print("\n==== Ví dụ thực tế ====")

# Tạo một ứng dụng client-server đơn giản
print("\nMô phỏng client-server bất đồng bộ:")

async def echo_server(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    
    print(f"Server nhận được: {message!r} từ {addr}")
    
    print(f"Server gửi: {message!r}")
    writer.write(data)
    await writer.drain()
    
    print("Server đóng kết nối")
    writer.close()
    await writer.wait_closed()

async def echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)
    
    print(f'Client gửi: {message!r}')
    writer.write(message.encode())
    await writer.drain()
    
    data = await reader.read(100)
    print(f'Client nhận được: {data.decode()!r}')
    
    print('Client đóng kết nối')
    writer.close()
    await writer.wait_closed()

async def example_application():
    # Khởi động server
    server = await asyncio.start_server(
        echo_server, '127.0.0.1', 8888)
    
    addr = server.sockets[0].getsockname()
    print(f'Server đang chạy trên {addr}')
    
    # Chạy client
    await echo_client("Hello World!")
    
    # Đóng server
    server.close()
    await server.wait_closed()

# Chúng ta không thực sự chạy ứng dụng ở đây vì sẽ chặn output
print("Ví dụ mô phỏng echo server/client với asyncio")
print("Chi tiết thực thi có thể xem trong mã nguồn")

# ==== Tóm tắt ====
print("\n==== Tóm tắt ====")
print("1. Event loop là trung tâm của asyncio, điều khiển thực thi các coroutines")
print("2. Dựa trên selectors để thực hiện I/O multiplexing hiệu quả")  
print("3. Quản lý callbacks và tasks thông qua các hàng đợi và handles")
print("4. Theo dõi thời gian để thực thi timer callbacks")
print("5. Mỗi thread có một event loop riêng")
print("6. Để sử dụng asyncio hiệu quả, hiểu về event loop rất quan trọng")

# Đóng loop
loop.close()

print("\nTài liệu tham khảo:")
print("1. https://docs.python.org/3/library/asyncio-eventloop.html")
print("2. https://github.com/python/cpython/blob/main/Lib/asyncio/base_events.py")
print("3. https://github.com/python/cpython/blob/main/Lib/asyncio/selector_events.py")
print("4. https://github.com/python/cpython/blob/main/Lib/asyncio/proactor_events.py")