'''
Python cho JavaScript Developers - Introduction
=============================================

Python là ngôn ngữ lập trình có cú pháp đơn giản, dễ đọc,
khác biệt đáng kể so với JavaScript.

Điểm khác biệt chính:
- Python sử dụng thụt lề (indentation) để xác định phạm vi code block, không dùng {}
- Python không cần dấu chấm phẩy (;) ở cuối câu lệnh
- Python có kiểu dữ liệu tĩnh, nhưng là dynamic typing (giống JavaScript)
- Python không có các từ khóa let, var, const
'''

# This is a comment in Python (giống // trong JavaScript)

"""
Đây là multi-line comment trong Python
Tương tự như /* */ trong JavaScript
Nhưng thực ra đây là docstring (chuỗi tài liệu)
"""

# In ra màn hình (tương tự console.log trong JavaScript)
print("Hello, Python World!")

# Trong Python 3, print là một function nên cần dấu ngoặc đơn ()
# Khác với Python 2 không cần dấu ngoặc

# Gán biến (không cần let, var, const như trong JavaScript)
message = "Welcome to Python!"
print(message)

# Python thường dùng snake_case thay vì camelCase trong JavaScript
user_name = "JSDeveloper"
print("Hello, " + user_name)

# Input từ người dùng (tương tự prompt trong JavaScript)
name = input("What is your name? ")
print("Nice to meet you, " + name)