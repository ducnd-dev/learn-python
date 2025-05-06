'''
File Handling trong Python cho JavaScript Developers
================================================

Python có nhiều cách để làm việc với files và I/O operations.
So sánh với JavaScript, Python cung cấp cách xử lý file đơn giản
và linh hoạt hơn nhiều.
'''

# =========== ĐỌC VÀ GHI FILE CƠ BẢN ===========

# Mở và đọc toàn bộ file - Cách đơn giản nhất
def read_file_simple(file_path):
    try:
        # Tự động mở và đóng file khi ra khỏi block with
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File không tồn tại!"
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Viết nội dung vào file - ghi đè nội dung cũ
def write_file_simple(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Thêm nội dung vào cuối file
def append_to_file(file_path, content):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Ví dụ sử dụng 
test_file = 'example.txt'

# Ghi nội dung mới
write_file_simple(test_file, "Hello, this is line 1.\n")
append_to_file(test_file, "This is line 2.\n")
append_to_file(test_file, "This is line 3.\n")

# Đọc nội dung
content = read_file_simple(test_file)
print(f"File content:\n{content}")

# So sánh với JavaScript:
# // Đọc file trong Node.js
# const fs = require('fs');
# try {
#   const content = fs.readFileSync('example.txt', 'utf8');
#   console.log(content);
# } catch (err) {
#   console.error(err);
# }
#
# // Ghi file trong Node.js
# try {
#   fs.writeFileSync('example.txt', 'Hello, this is line 1.\n', 'utf8');
#   fs.appendFileSync('example.txt', 'This is line 2.\n', 'utf8');
# } catch (err) {
#   console.error(err);
# }

# =========== ĐỌC FILE THEO DÒNG ===========

def read_file_by_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Đọc tất cả các dòng vào list
            lines = file.readlines()
        return lines
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Hiệu quả hơn cho file lớn - xử lý từng dòng
def process_large_file(file_path, line_processor):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line_processor(line_number, line.strip())
        return True
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Đọc theo dòng
lines = read_file_by_lines(test_file)
print("\nLines as list:")
for i, line in enumerate(lines, 1):
    print(f"Line {i}: {line.strip()}")

# Xử lý từng dòng - hiệu quả cho file lớn
print("\nProcessing lines:")
process_large_file(test_file, lambda num, line: print(f"Processed line {num}: {line}"))

# =========== MODES VÀ FLAGS KHI MỞ FILE ===========

# Các mode mở file phổ biến:
# 'r' - Read (default) - Đọc
# 'w' - Write (tạo mới file nếu không tồn tại, xóa nội dung nếu đã tồn tại)
# 'a' - Append (thêm vào cuối file)
# 'r+' - Read and write (con trỏ ở đầu file)
# 'w+' - Write and read (xóa nội dung cũ)
# 'a+' - Append and read (con trỏ ở cuối file)
# 'x' - Create a new file and write to it (nếu file đã tồn tại sẽ báo lỗi)
# 'b' - Binary mode (thêm sau r, w, hoặc a)
# 't' - Text mode (default)

# Đọc và ghi binary data
def copy_binary_file(source_path, destination_path):
    try:
        with open(source_path, 'rb') as source:
            with open(destination_path, 'wb') as destination:
                destination.write(source.read())
        return True
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Tạo file ảnh đơn giản
def create_simple_image():
    with open('simple.bmp', 'wb') as f:
        # Header đơn giản cho BMP 10x10 pixel
        f.write(b'BM')
        f.write((54 + 10 * 10 * 3).to_bytes(4, byteorder='little'))  # File size
        f.write(b'\x00\x00\x00\x00')
        f.write((54).to_bytes(4, byteorder='little'))  # Pixel data offset
        f.write((40).to_bytes(4, byteorder='little'))  # Info header size
        f.write((10).to_bytes(4, byteorder='little'))  # Width
        f.write((10).to_bytes(4, byteorder='little'))  # Height
        f.write((1).to_bytes(2, byteorder='little'))   # Planes
        f.write((24).to_bytes(2, byteorder='little'))  # Bits per pixel
        f.write((0).to_bytes(4, byteorder='little'))   # Compression
        f.write((10 * 10 * 3).to_bytes(4, byteorder='little'))  # Image size
        f.write((0).to_bytes(4, byteorder='little'))   # X pixels per meter
        f.write((0).to_bytes(4, byteorder='little'))   # Y pixels per meter
        f.write((0).to_bytes(4, byteorder='little'))   # Colors used
        f.write((0).to_bytes(4, byteorder='little'))   # Important colors
        
        # Pixel data (10x10 red pixels)
        for _ in range(10):
            for _ in range(10):
                f.write(b'\xff\x00\x00')  # BGR color
    return 'simple.bmp'

# Uncomment để tạo file ảnh đơn giản
# image_file = create_simple_image()
# print(f"Created image file: {image_file}")

# Copy binary file
# copy_binary_file(image_file, 'simple_copy.bmp')
# print(f"Copied image file to: simple_copy.bmp")

# =========== FILE POSITIONS VÀ SEEKING ===========

def file_seek_example(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        # Đọc 5 ký tự đầu tiên
        start = file.read(5)
        print(f"First 5 chars: {start}")
        
        # Vị trí hiện tại
        position = file.tell()
        print(f"Current position: {position}")
        
        # Di chuyển con trỏ đến vị trí 0 (đầu file)
        file.seek(0)
        print(f"After seek(0), position: {file.tell()}")
        
        # Đọc lại từ đầu
        start_again = file.read(5)
        print(f"First 5 chars again: {start_again}")
        
        # Di chuyển đến vị trí cụ thể
        file.seek(7)
        print(f"After seek(7), reading 4 chars: {file.read(4)}")
        
        # Di chuyển tương đối từ vị trí hiện tại
        file.seek(3, 1)  # 1 là SEEK_CUR
        print(f"After seek(3, 1), reading 4 chars: {file.read(4)}")
        
        # Di chuyển tương đối từ cuối file
        file.seek(-10, 2)  # 2 là SEEK_END
        print(f"Last 10 chars: {file.read()}")

print("\nFile seeking example:")
file_seek_example(test_file)

# =========== XỬ LÝ FILE CSV ===========
import csv

# Tạo file CSV
def create_csv_example():
    with open('example.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Age', 'City'])
        writer.writerow(['Alice', 30, 'New York'])
        writer.writerow(['Bob', 25, 'Boston'])
        writer.writerow(['Charlie', 35, 'San Francisco'])
    return 'example.csv'

# Đọc file CSV
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Đọc header
        for row in reader:
            data.append(dict(zip(headers, row)))
    return data

# Đọc với DictReader (đọc trực tiếp thành dictionary)
def read_csv_dict(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Tạo và đọc CSV
csv_file = create_csv_example()
print(f"\nCreated CSV file: {csv_file}")

csv_data = read_csv_file(csv_file)
print("\nCSV data as list of dictionaries:")
for row in csv_data:
    print(row)

csv_dict_data = read_csv_dict(csv_file)
print("\nCSV data using DictReader:")
for row in csv_dict_data:
    print(row)

# =========== XỬ LÝ FILE JSON ===========
import json

# Tạo dữ liệu JSON
def create_json_example():
    data = {
        'name': 'John Doe',
        'age': 30,
        'is_active': True,
        'interests': ['programming', 'reading', 'hiking'],
        'contact': {
            'email': 'john@example.com',
            'phone': '123-456-7890'
        }
    }
    
    with open('example.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)
    return 'example.json'

# Đọc file JSON
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Tạo và đọc JSON
json_file = create_json_example()
print(f"\nCreated JSON file: {json_file}")

json_data = read_json_file(json_file)
print("\nJSON data:")
print(f"Name: {json_data['name']}")
print(f"Age: {json_data['age']}")
print(f"Interests: {', '.join(json_data['interests'])}")
print(f"Email: {json_data['contact']['email']}")

# =========== TEMPORARY FILES ===========
import tempfile
import os

def temp_file_example():
    # Tạo temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_name = temp.name
        temp.write(b"This is temporary data.\n")
        temp.write(b"It will be automatically deleted.\n")
    
    print(f"\nTemporary file created: {temp_name}")
    
    # Đọc lại temporary file
    with open(temp_name, 'r') as file:
        content = file.read()
    print(f"Temporary file content:\n{content}")
    
    # Xóa file sau khi sử dụng
    os.unlink(temp_name)
    print(f"Temporary file deleted: {temp_name}")

temp_file_example()

# =========== XỬ LÝ ĐƯỜNG DẪN VỚI PATHLIB ===========
from pathlib import Path

def pathlib_examples():
    # Tạo đối tượng Path
    current_file = Path(__file__)
    print(f"\nCurrent file: {current_file}")
    
    # Thư mục chứa file
    parent_dir = current_file.parent
    print(f"Parent directory: {parent_dir}")
    
    # Đường dẫn tuyệt đối
    absolute_path = current_file.absolute()
    print(f"Absolute path: {absolute_path}")
    
    # Tên file và phần mở rộng
    print(f"File name: {current_file.name}")
    print(f"File stem: {current_file.stem}")
    print(f"File suffix: {current_file.suffix}")
    
    # Tạo đường dẫn mới
    new_path = parent_dir / "new_folder" / "new_file.txt"
    print(f"New path: {new_path}")
    
    # Kiểm tra tồn tại
    print(f"File exists? {current_file.exists()}")
    print(f"New path exists? {new_path.exists()}")
    
    # Liệt kê file trong thư mục
    print("\nFiles in parent directory:")
    for file in parent_dir.iterdir():
        print(f" - {file.name} ({'directory' if file.is_dir() else 'file'})")
    
    # Tìm kiếm file với pattern
    print("\nPython files in parent directory:")
    for py_file in parent_dir.glob("*.py"):
        print(f" - {py_file.name}")
    
    # Recursive globbing
    print("\nAll Python files recursively:")
    for py_file in parent_dir.glob("**/*.py"):
        print(f" - {py_file.relative_to(parent_dir)}")

pathlib_examples()

# =========== FILE WATCHER ===========
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"File modified: {event.src_path}")
    
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"File created: {event.src_path}")
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"File deleted: {event.src_path}")

def watch_directory(path, duration=10):
    print(f"\nWatching directory: {path} for {duration} seconds")
    print("Make changes to files to see events...")
    
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

# Uncomment để chạy file watcher
# watch_directory(".", 30)  # Theo dõi thư mục hiện tại trong 30 giây