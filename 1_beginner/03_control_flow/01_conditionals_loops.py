'''
Python Control Flow cho JavaScript Developers
=========================================

Python có các cấu trúc điều khiển tương tự JavaScript,
nhưng cú pháp và cách thể hiện có sự khác biệt.
'''

# =========== IF-ELIF-ELSE ===========
# Tương tự if-else trong JavaScript, nhưng dùng elif thay vì else if
# và dùng thụt lề thay vì dấu ngoặc nhọn {}

age = 20

# Cú pháp if trong Python
if age < 18:
    print("Bạn chưa đủ tuổi trưởng thành")
elif age >= 18 and age < 60:
    print("Bạn là người trưởng thành")
else:
    print("Bạn là người cao tuổi")

# So sánh với JavaScript:
# if (age < 18) {
#     console.log("Bạn chưa đủ tuổi trưởng thành");
# } else if (age >= 18 && age < 60) {
#     console.log("Bạn là người trưởng thành");
# } else {
#     console.log("Bạn là người cao tuổi");
# }

# Toán tử 3 ngôi trong Python (tương tự ternary operator trong JavaScript)
is_adult = "Người lớn" if age >= 18 else "Trẻ em"
print(f"Status: {is_adult}")

# So sánh với JavaScript:
# let isAdult = age >= 18 ? "Người lớn" : "Trẻ em";
# console.log(`Status: ${isAdult}`);

# =========== LOOP (VÒNG LẶP) ===========

# For loop trong Python khác JavaScript nhiều nhất
# Python dùng for-in, không có for(;;) như JavaScript

# For loop với range
print("\nFor loop với range:")
for i in range(5):  # range(5) tạo ra dãy từ 0 đến 4
    print(f"Số: {i}")

# So sánh với JavaScript:
# for (let i = 0; i < 5; i++) {
#     console.log(`Số: ${i}`);
# }

# For loop với range có start, stop
print("\nFor loop với range có start, stop:")
for i in range(1, 6):  # range(1, 6) tạo ra dãy từ 1 đến 5
    print(f"Số: {i}")

# So sánh với JavaScript:
# for (let i = 1; i < 6; i++) {
#     console.log(`Số: ${i}`);
# }

# For loop với range có step (bước nhảy)
print("\nFor loop với range có step:")
for i in range(0, 10, 2):  # range(0, 10, 2) tạo ra dãy 0, 2, 4, 6, 8
    print(f"Số: {i}")

# So sánh với JavaScript:
# for (let i = 0; i < 10; i += 2) {
#     console.log(`Số: ${i}`);
# }

# For loop với collection (tương tự for...of trong JavaScript)
print("\nFor loop với list:")
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"Fruit: {fruit}")

# So sánh với JavaScript:
# const fruits = ["apple", "banana", "orange"];
# for (const fruit of fruits) {
#     console.log(`Fruit: ${fruit}`);
# }

# For loop với enumerate (để lấy index và giá trị)
print("\nFor loop với enumerate:")
for index, fruit in enumerate(fruits):
    print(f"Fruit {index}: {fruit}")

# So sánh với JavaScript:
# fruits.forEach((fruit, index) => {
#     console.log(`Fruit ${index}: ${fruit}`);
# });

# For loop với dictionary (tương tự for...in trong JavaScript nhưng khác về mặt cú pháp)
print("\nFor loop với dictionary:")
user = {"name": "John", "age": 30, "city": "New York"}

# Lặp qua các keys
for key in user:
    print(f"Key: {key}, Value: {user[key]}")

# Lặp qua cả key và value
for key, value in user.items():
    print(f"Key: {key}, Value: {value}")

# So sánh với JavaScript:
# const user = {name: "John", age: 30, city: "New York"};
# for (const key in user) {
#     console.log(`Key: ${key}, Value: ${user[key]}`);
# }
# Object.entries(user).forEach(([key, value]) => {
#     console.log(`Key: ${key}, Value: ${value}`);
# });

# =========== WHILE LOOP ===========
# While loop trong Python tương tự JavaScript

print("\nWhile loop:")
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# Break và Continue
print("\nBreak và Continue:")
for i in range(10):
    if i == 3:
        continue  # Bỏ qua iteration hiện tại
    if i == 7:
        break  # Thoát khỏi loop
    print(f"Số: {i}")

# =========== MATCH-CASE (từ Python 3.10+) ===========
# Tương tự switch-case trong JavaScript

print("\nMatch-case (Switch-case):")
status_code = 404

# Chỉ chạy trên Python 3.10 trở lên
# match status_code:
#     case 200 | 201:
#         print("Success")
#     case 400:
#         print("Bad Request")
#     case 404:
#         print("Not Found")
#     case 500:
#         print("Server Error")
#     case _:  # Default case (giống default trong switch-case của JS)
#         print("Unknown status code")

# So sánh với JavaScript:
# switch (statusCode) {
#     case 200:
#     case 201:
#         console.log("Success");
#         break;
#     case 400:
#         console.log("Bad Request");
#         break;
#     case 404:
#         console.log("Not Found");
#         break;
#     case 500:
#         console.log("Server Error");
#         break;
#     default:
#         console.log("Unknown status code");
#         break;
# }

# =========== TRY-EXCEPT (TRY-CATCH) ===========
# Tương tự try-catch trong JavaScript

print("\nTry-except:")
try:
    # Gây ra lỗi
    result = 10 / 0
    print(result)  # Dòng này không được thực thi
except ZeroDivisionError:
    print("Không thể chia cho 0!")
except Exception as e:
    print(f"Lỗi không xác định: {e}")
else:
    # Chỉ chạy nếu không có lỗi (không có trong JavaScript)
    print("Phép chia thành công!")
finally:
    # Luôn chạy, giống finally trong JavaScript
    print("Phép tính kết thúc!")