'''
Python Modules & Packages cho JavaScript Developers
================================================

Module trong Python tương tự như modules trong JavaScript ES6.
Package trong Python tương tự như npm packages trong hệ sinh thái JavaScript.
'''

# =========== IMPORTING MODULES ===========

# Import toàn bộ module
import math

# Sử dụng module
radius = 5
circle_area = math.pi * radius ** 2
print(f"Area of circle with radius {radius}: {circle_area}")

# Dùng hàm từ module
print(f"Square root of 16: {math.sqrt(16)}")

# So sánh với JavaScript:
# import * as math from 'math';
# const radius = 5;
# const circleArea = math.PI * radius ** 2;

# =========== IMPORT RIÊNG LẺ ===========

# Import cụ thể
from math import pi, sqrt

# Sử dụng trực tiếp, không cần prefix
print(f"PI: {pi}")
print(f"Square root of 25: {sqrt(25)}")

# So sánh với JavaScript:
# import { PI, sqrt } from 'math';
# console.log(`PI: ${PI}`);
# console.log(`Square root of 25: ${sqrt(25)}`);

# Import với alias (đổi tên)
from math import sqrt as square_root
print(f"Square root of 36: {square_root(36)}")

# So sánh với JavaScript:
# import { sqrt as squareRoot } from 'math';
# console.log(`Square root of 36: ${squareRoot(36)}`);

# Import tất cả (không khuyến khích vì có thể gây xung đột tên)
from random import *
print(f"Random number between 0 and 1: {random()}")

# So sánh với JavaScript:
# import * from 'random'; // không hỗ trợ trực tiếp trong JS

# =========== MODULE CHUẨN PHỔ BIẾN ===========

# Module os - thao tác với hệ điều hành
import os
print(f"Current working directory: {os.getcwd()}")
print(f"List of files in current directory: {os.listdir('.')}")

# Module sys - System-specific parameters and functions
import sys
print(f"Python version: {sys.version}")
print(f"Path của Python: {sys.path}")  # Đường dẫn module search

# Module datetime - làm việc với ngày tháng
from datetime import datetime, timedelta
now = datetime.now()
print(f"Current date and time: {now}")
tomorrow = now + timedelta(days=1)
print(f"Tomorrow at this time: {tomorrow}")

# So sánh với JavaScript:
# const now = new Date();
# console.log(`Current date and time: ${now}`);
# const tomorrow = new Date(now);
# tomorrow.setDate(now.getDate() + 1);
# console.log(`Tomorrow at this time: ${tomorrow}`);

# Module random - làm việc với số ngẫu nhiên
import random
print(f"Random int between 1 and 10: {random.randint(1, 10)}")
print(f"Random choice from list: {random.choice(['apple', 'banana', 'orange'])}")

# So sánh với JavaScript:
# console.log(`Random int between 1 and 10: ${Math.floor(Math.random() * 10) + 1}`);
# const fruits = ['apple', 'banana', 'orange'];
# console.log(`Random choice from list: ${fruits[Math.floor(Math.random() * fruits.length)]}`);

# Module json - làm việc với JSON 
import json

# Object to JSON string (tương tự JSON.stringify trong JS)
person = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "languages": ["Python", "JavaScript"]
}
json_str = json.dumps(person, indent=2)
print(f"JSON string:\n{json_str}")

# JSON string to object (tương tự JSON.parse trong JS)
parsed_person = json.loads(json_str)
print(f"Parsed person name: {parsed_person['name']}")

# So sánh với JavaScript:
# const person = {
#    name: "John",
#    age: 30,
#    city: "New York",
#    languages: ["Python", "JavaScript"]
# };
# const jsonStr = JSON.stringify(person, null, 2);
# console.log(`JSON string:\n${jsonStr}`);
# const parsedPerson = JSON.parse(jsonStr);
# console.log(`Parsed person name: ${parsedPerson.name}`);

# =========== TẠO VÀ SỬ DỤNG MODULE ===========

# Tạo module: Lưu mã dưới đây vào file my_module.py
'''
# File: my_module.py
def greet(name):
    return f"Hello, {name}!"

def calculate_square(number):
    return number ** 2

PI = 3.14159

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def get_info(self):
        return f"{self.name}, {self.age} years old"
'''

# Sử dụng module:
# import my_module
# print(my_module.greet("Alice"))
# print(f"Square of 4: {my_module.calculate_square(4)}")
# print(f"PI value: {my_module.PI}")
# alice = my_module.Person("Alice", 25)
# print(alice.get_info())

# =========== PACKAGES ===========
# Package là tập hợp các module, tạo bằng cách tạo thư mục chứa file __init__.py

'''
my_package/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
'''

# Import từ package
# import my_package.module1
# from my_package.module2 import some_function
# from my_package.subpackage.module3 import SomeClass

# =========== PIP - PACKAGE MANAGER ===========
# pip là công cụ quản lý package của Python, tương tự npm trong JavaScript

# Cài đặt package
# pip install package_name

# Ví dụ: cài đặt requests package
# pip install requests

# Sử dụng package đã cài đặt
import requests  # Phải cài đặt trước khi sử dụng

try:
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    if response.status_code == 200:
        data = response.json()
        print(f"Todo title: {data['title']}")
except:
    print("Error making request or module not installed")

# So sánh với JavaScript:
# // In Node.js
# // npm install node-fetch
# const fetch = require('node-fetch');
# fetch('https://jsonplaceholder.typicode.com/todos/1')
#   .then(response => response.json())
#   .then(data => console.log(`Todo title: ${data.title}`))
#   .catch(error => console.error('Error:', error));

# =========== VIRTUAL ENVIRONMENTS ===========
# Virtual environment tương tự như Node.js projects với package.json riêng

'''
# Tạo virtual environment
python -m venv myenv

# Kích hoạt virtual environment
# Windows:
myenv\Scripts\activate
# macOS/Linux:
source myenv/bin/activate

# Cài đặt package trong virtual environment
pip install package_name

# Lưu danh sách package
pip freeze > requirements.txt

# Cài đặt từ requirements.txt
pip install -r requirements.txt

# Deactivate virtual environment
deactivate
'''

# So sánh với JavaScript:
# npm init
# npm install package_name
# Package được lưu trong package.json