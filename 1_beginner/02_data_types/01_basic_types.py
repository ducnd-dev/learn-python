'''
Python Data Types cho JavaScript Developers
==========================================

Python và JavaScript có một số kiểu dữ liệu tương tự, nhưng cũng có nhiều điểm khác biệt.
'''

# =========== KIỂU DỮ LIỆU CƠ BẢN ===========

# Number - Số
# --------------------------
# Trong Python có int, float (không có số nguyên và số thực riêng biệt như JavaScript)
integer_number = 42          # int - số nguyên (tương tự Number trong JS)
float_number = 3.14          # float - số thập phân (tương tự Number trong JS)
complex_number = 1 + 2j      # complex - số phức (không có trong JS chuẩn)

print(f"Integer: {integer_number}, type: {type(integer_number)}")
print(f"Float: {float_number}, type: {type(float_number)}")
print(f"Complex: {complex_number}, type: {type(complex_number)}")

# String - Chuỗi
# --------------------------
# Tương tự như JavaScript, nhưng có nhiều tính năng hơn
single_quotes = 'Hello'              # Dùng dấu nháy đơn
double_quotes = "World"              # Dùng dấu nháy kép
triple_quotes = '''Multiple 
lines'''                             # Dùng để tạo chuỗi nhiều dòng

# f-string (từ Python 3.6+) - Tương tự template literal (`${}`) trong JavaScript
name = "Python"
greeting = f"Hello, {name}!"
print(greeting)

# Các phương thức chuỗi
print("hello world".capitalize())    # "Hello world"
print("hello world".title())         # "Hello World"
print("HELLO".lower())               # "hello"
print("hello".upper())               # "HELLO"
print("hello world".split())         # ['hello', 'world']
print("hello-world".split("-"))      # ['hello', 'world']

# Boolean - Logic
# --------------------------
# Giống JavaScript nhưng viết hoa: True, False (không phải true, false)
python_is_fun = True
javascript_is_hard = False

print(f"Python is fun? {python_is_fun}")
print(f"JavaScript is hard? {javascript_is_hard}")

# None - Null
# --------------------------
# Tương đương với null trong JavaScript (nhưng không giống undefined)
nothing = None
print(f"Value: {nothing}, type: {type(nothing)}")

# =========== TOÁN TỬ SO SÁNH ===========
print(10 > 5)            # True - Lớn hơn
print(10 >= 10)          # True - Lớn hơn hoặc bằng
print(10 < 5)            # False - Nhỏ hơn
print(10 <= 10)          # True - Nhỏ hơn hoặc bằng
print(10 == 10)          # True - Bằng nhau về giá trị
print(10 != 5)           # True - Khác nhau về giá trị

# Python không có === và !== như JavaScript
# Python so sánh kiểu dữ liệu tự động khi dùng == và !=
print(10 == "10")        # False - Khác với JavaScript (sẽ là true)
print(10 == int("10"))   # True - Sau khi chuyển đổi sang cùng kiểu

# is - Toán tử kiểm tra cùng đối tượng (tương tự Object.is trong JS)
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(a == b)    # True - Giá trị giống nhau
print(a is b)    # False - Không phải cùng một đối tượng
print(a is c)    # True - Cùng một đối tượng