'''
Python Collections cho JavaScript Developers
=========================================

Python có các cấu trúc dữ liệu tập hợp tương tự JavaScript nhưng phong phú hơn.
So sánh với JavaScript:
- List ~ Array 
- Dictionary ~ Object/Map
- Set ~ Set
- Tuple - không có tương đương trực tiếp trong JavaScript (có thể coi là readonly array)
'''

# =========== LIST (MẢNG) ===========
# Tương tự Array trong JavaScript, nhưng mạnh mẽ hơn

# Khởi tạo list
my_list = [1, 2, 3, 4, 5]
mixed_list = [1, "hello", True, 3.14]
nested_list = [1, [2, 3], [4, 5, 6]]

print(f"List: {my_list}")
print(f"List có thể chứa nhiều kiểu dữ liệu: {mixed_list}")
print(f"List có thể lồng nhau: {nested_list}")

# Truy cập phần tử của list (giống JavaScript)
print(f"Phần tử đầu tiên: {my_list[0]}")               # 1
print(f"Phần tử cuối cùng: {my_list[-1]}")             # 5 (cách viết gọn của Python)
print(f"Phần tử [-2] (từ cuối đếm lên): {my_list[-2]}")  # 4

# Slicing - cắt list (không có trong JavaScript)
print(f"my_list[1:3]: {my_list[1:3]}")                # [2, 3] - lấy từ index 1 đến 2 (không bao gồm 3)
print(f"my_list[:3]: {my_list[:3]}")                  # [1, 2, 3] - lấy từ đầu đến index 2
print(f"my_list[2:]: {my_list[2:]}")                  # [3, 4, 5] - lấy từ index 2 đến hết
print(f"my_list[::2]: {my_list[::2]}")                # [1, 3, 5] - lấy cách 2 phần tử

# Thay đổi giá trị của list
my_list[0] = 100
print(f"Sau khi thay đổi: {my_list}")                # [100, 2, 3, 4, 5]

# Các phương thức của list (nhiều phương thức giống Array trong JavaScript)
my_list.append(6)                                    # Thêm vào cuối (giống push)
print(f"Sau khi append: {my_list}")                  # [100, 2, 3, 4, 5, 6]

my_list.insert(1, 200)                               # Thêm vào vị trí index
print(f"Sau khi insert: {my_list}")                  # [100, 200, 2, 3, 4, 5, 6]

last_item = my_list.pop()                            # Lấy và xóa phần tử cuối (giống pop)
print(f"Phần tử bị pop: {last_item}")               # 6
print(f"Sau khi pop: {my_list}")                     # [100, 200, 2, 3, 4, 5]

my_list.remove(200)                                  # Xóa phần tử có giá trị 200
print(f"Sau khi remove 200: {my_list}")              # [100, 2, 3, 4, 5]

my_list.sort()                                       # Sắp xếp list (tương tự sort trong JS nhưng không trả về mảng mới)
print(f"Sau khi sort: {my_list}")                    # [2, 3, 4, 5, 100]

my_list.reverse()                                    # Đảo ngược list
print(f"Sau khi reverse: {my_list}")                 # [100, 5, 4, 3, 2]

print(f"Độ dài của list: {len(my_list)}")           # 5 (tương đương array.length trong JS)

# List comprehension - cách viết tạo list gọn hơn (không có trong JS)
squares = [x**2 for x in range(1, 6)]
print(f"List các số bình phương: {squares}")         # [1, 4, 9, 16, 25]

# Với điều kiện if (filter)
even_squares = [x**2 for x in range(1, 10) if x % 2 == 0]
print(f"List các số bình phương chẵn: {even_squares}") # [4, 16, 36, 64]

# =========== DICTIONARY (OBJECT, MAP) ===========
# Tương tự Object trong JavaScript hoặc Map

# Khởi tạo dictionary
user = {
    "name": "John",
    "age": 30,
    "is_admin": True,
    "skills": ["Python", "JavaScript"]
}

print(f"Dictionary: {user}")

# Truy cập phần tử của dictionary
print(f"Tên người dùng: {user['name']}")             # John
print(f"Tuổi: {user.get('age')}")                    # 30 (get là phương thức an toàn hơn)
print(f"Email: {user.get('email', 'Không có')}")     # Không có (giá trị mặc định nếu key không tồn tại)

# Thêm/thay đổi phần tử (giống JavaScript)
user["email"] = "john@example.com"
user["age"] = 31
print(f"Sau khi thay đổi: {user}")

# Xóa phần tử
del user["is_admin"]
removed_value = user.pop("age")
print(f"Giá trị bị xóa: {removed_value}")            # 31
print(f"Sau khi xóa: {user}")

# Các phương thức của dictionary
print(f"Các keys: {list(user.keys())}")              # ['name', 'skills', 'email']
print(f"Các values: {list(user.values())}")          # ['John', ['Python', 'JavaScript'], 'john@example.com']
print(f"Các cặp key-value: {list(user.items())}")    # [('name', 'John'), ('skills', ['Python', 'JavaScript']), ('email', 'john@example.com')]

# Dictionary comprehension
squares_dict = {x: x**2 for x in range(1, 6)}
print(f"Dictionary các số bình phương: {squares_dict}")  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# =========== TUPLE ===========
# Giống list nhưng immutable (không thể thay đổi sau khi tạo)

# Khởi tạo tuple
coordinates = (10, 20)
person = ("John", 30, True)

print(f"Tuple coordinates: {coordinates}")
print(f"Tuple person: {person}")

# Truy cập phần tử (giống list)
print(f"X coordinate: {coordinates[0]}")             # 10
print(f"Tên: {person[0]}")                           # John

# Tuple unpacking (tương tự destructuring trong JavaScript)
name, age, is_active = person
print(f"Đã unpack - Tên: {name}, Tuổi: {age}")

# Tuple không thể thay đổi phần tử sau khi tạo
# coordinates[0] = 100  # Lỗi: TypeError: 'tuple' object does not support item assignment

# Tuple methods
print(f"Số lần xuất hiện của 'John': {person.count('John')}")  # 1
print(f"Vị trí của 'John': {person.index('John')}")           # 0

# =========== SET ===========
# Tương tự Set trong JavaScript - tập hợp các phần tử không trùng lặp

# Khởi tạo set
fruits = {"apple", "banana", "orange", "apple"}
print(f"Set fruits: {fruits}")                        # {'orange', 'banana', 'apple'} - không có phần tử trùng lặp

# Thêm phần tử
fruits.add("grape")
print(f"Sau khi add: {fruits}")

# Xóa phần tử
fruits.remove("banana")  # Raise lỗi nếu không tìm thấy
print(f"Sau khi remove: {fruits}")

fruits.discard("kiwi")   # Không raise lỗi nếu không tìm thấy
print(f"Sau khi discard phần tử không tồn tại: {fruits}")

# Các phép toán tập hợp
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

print(f"Union (hợp): {set_a | set_b}")              # {1, 2, 3, 4, 5, 6, 7, 8}
print(f"Intersection (giao): {set_a & set_b}")       # {4, 5}
print(f"Difference (hiệu): {set_a - set_b}")         # {1, 2, 3}
print(f"Symmetric diff: {set_a ^ set_b}")            # {1, 2, 3, 6, 7, 8}