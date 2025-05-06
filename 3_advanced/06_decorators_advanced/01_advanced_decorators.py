'''
Advanced Decorators cho JavaScript Developers
=============================================

Decorators trong Python là một tính năng mạnh mẽ cho phép chỉnh sửa
hoặc mở rộng chức năng của các hàm và lớp mà không cần thay đổi code gốc.

Trong JavaScript, tính năng decorators chính thức (stage 3 proposal)
hoạt động tương tự nhưng có cú pháp và ngữ cảnh sử dụng khác.
'''

# ===== KIẾN THỨC CƠ BẢN VỀ DECORATORS =====
print("=== Kiến thức cơ bản về Decorators ===")

# Nhắc lại: Decorator là một hàm nhận vào một hàm và trả về một hàm
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Something is happening after the function is called.")
        return result
    return wrapper

@simple_decorator
def say_hello(name):
    return f"Hello, {name}!"

print(say_hello("World"))  # Output sẽ có các dòng "Something is happening..."

# Tương đương với:
# say_hello = simple_decorator(say_hello)

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// JavaScript decorators (Stage 3 proposal) sử dụng @ trước hàm/class
function simpleDecorator(target, context) {
  // target là hàm/phương thức được decorator
  return function(...args) {
    console.log("Something is happening before the function is called.");
    const result = target.apply(this, args);
    console.log("Something is happening after the function is called.");
    return result;
  };
}

class Example {
  @simpleDecorator
  sayHello(name) {
    return `Hello, ${name}!`;
  }
}
""")

# ===== DECORATORS VỚI THAM SỐ =====
print("\n\n=== Decorators với Tham số ===")

# Decorator với tham số yêu cầu thêm một lớp wrapper nữa
def repeat(n=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(n=5)
def say_hi():
    return "Hi!"

print(say_hi())  # Output: ['Hi!', 'Hi!', 'Hi!', 'Hi!', 'Hi!']

# Decorator với nhiều tham số
def route(path, methods=None):
    if methods is None:
        methods = ['GET']
    
    def decorator(func):
        func.path = path
        func.methods = methods
        return func
    return decorator

@route('/api/users', methods=['GET', 'POST'])
def get_users():
    return "List of users"

print(f"Function path: {get_users.path}, methods: {get_users.methods}")

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// Decorator với tham số trong JavaScript
function repeat(n = 3) {
  return function(target, context) {
    return function(...args) {
      const results = [];
      for (let i = 0; i < n; i++) {
        results.push(target.apply(this, args));
      }
      return results;
    };
  };
}

class Example {
  @repeat(5)
  sayHi() {
    return "Hi!";
  }
}

// Decorator cho route trong web framework
function route(path, methods = ['GET']) {
  return function(target, context) {
    target.path = path;
    target.methods = methods;
    return target;
  };
}

class Controller {
  @route('/api/users', ['GET', 'POST'])
  getUsers() {
    return "List of users";
  }
}
""")

# ===== CLASS DECORATORS =====
print("\n\n=== Class Decorators ===")

# Decorator cho class
def add_greeting(cls):
    # Thêm một phương thức mới vào class
    cls.greet = lambda self: f"Hello from {self.__class__.__name__}"
    return cls

@add_greeting
class Person:
    def __init__(self, name):
        self.name = name

person = Person("Alice")
print(person.greet())  # Output: "Hello from Person"

# Decorator định nghĩa lại các phương thức
def make_properties(cls):
    for key, value in vars(cls).items():
        # Chỉ xử lý các thuộc tính không đặc biệt
        if not key.startswith('__'):
            # Tạo một property getter đơn giản
            setattr(cls, key, property(lambda self, k=key: getattr(self, f"_{k}")))
    return cls

@make_properties
class User:
    name = None
    age = None
    
    def __init__(self, name, age):
        self._name = name
        self._age = age

user = User("Bob", 30)
print(f"User name: {user.name}, age: {user.age}")

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// Decorator cho class trong JavaScript
function addGreeting(target) {
  target.prototype.greet = function() {
    return `Hello from ${this.constructor.name}`;
  };
  return target;
}

@addGreeting
class Person {
  constructor(name) {
    this.name = name;
  }
}

const person = new Person("Alice");
console.log(person.greet());  // "Hello from Person"

// Decorator đổi property
function makeProperties(target) {
  // Lấy tất cả static properties
  Object.getOwnPropertyNames(target).forEach(key => {
    if (!key.startsWith('__')) {
      const privateKey = `_${key}`;
      // Define property với getter
      Object.defineProperty(target.prototype, key, {
        get() { return this[privateKey]; }
      });
    }
  });
  return target;
}

@makeProperties
class User {
  static name = null;
  static age = null;
  
  constructor(name, age) {
    this._name = name;
    this._age = age;
  }
}
""")

# ===== METHOD DECORATORS =====
print("\n\n=== Method Decorators ===")

# Decorator cho phương thức
def log_method_call(func):
    def wrapper(self, *args, **kwargs):
        print(f"Calling {func.__name__} on {self.__class__.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class Calculator:
    @log_method_call
    def add(self, a, b):
        return a + b
    
    @log_method_call
    def multiply(self, a, b):
        return a * b

calc = Calculator()
print(f"2 + 3 = {calc.add(2, 3)}")
print(f"4 * 5 = {calc.multiply(4, 5)}")

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// Decorator cho phương thức trong JavaScript
function logMethodCall(target, context) {
  return function(...args) {
    console.log(`Calling ${context.name} on ${this.constructor.name}`);
    return target.apply(this, args);
  };
}

class Calculator {
  @logMethodCall
  add(a, b) {
    return a + b;
  }
  
  @logMethodCall
  multiply(a, b) {
    return a * b;
  }
}
""")

# ===== STACKING DECORATORS =====
print("\n\n=== Stacking Decorators (Xếp chồng) ===")

def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

def underline(func):
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper

# Xếp chồng decorators - thứ tự từ trong ra ngoài
@bold
@italic
@underline
def format_text(text):
    return text

print(format_text("Hello, World!"))  # Output: <b><i><u>Hello, World!</u></i></b>

# Thứ tự decorators rất quan trọng
@underline
@italic
@bold
def format_text2(text):
    return text

print(format_text2("Hello, World!"))  # Output: <u><i><b>Hello, World!</b></i></u>

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// Stacking decorators trong JavaScript
function bold(target, context) {
  return function(...args) {
    return `<b>${target.apply(this, args)}</b>`;
  };
}

function italic(target, context) {
  return function(...args) {
    return `<i>${target.apply(this, args)}</i>`;
  };
}

function underline(target, context) {
  return function(...args) {
    return `<u>${target.apply(this, args)}</u>`;
  };
}

class Formatter {
  @bold
  @italic
  @underline
  formatText(text) {
    return text;
  }
  
  @underline
  @italic
  @bold
  formatText2(text) {
    return text;
  }
}
""")

# ===== GIỮ METADATA CỦA HÀM GỐC =====
print("\n\n=== Giữ Metadata của Hàm Gốc ===")

import functools

# Decorator không dùng @functools.wraps
def decorator_without_wraps(func):
    def wrapper(*args, **kwargs):
        '''Wrapper docstring'''
        return func(*args, **kwargs)
    return wrapper

# Decorator sử dụng @functools.wraps
def decorator_with_wraps(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        '''Wrapper docstring'''
        return func(*args, **kwargs)
    return wrapper

@decorator_without_wraps
def hello_world():
    '''Say hello to the world.'''
    return "Hello, World!"

@decorator_with_wraps
def goodbye_world():
    '''Say goodbye to the world.'''
    return "Goodbye, World!"

# Kiểm tra metadata
print(f"hello_world.__name__: {hello_world.__name__}")  # wrapper
print(f"hello_world.__doc__: {hello_world.__doc__}")   # Wrapper docstring

print(f"goodbye_world.__name__: {goodbye_world.__name__}")  # goodbye_world
print(f"goodbye_world.__doc__: {goodbye_world.__doc__}")   # Say goodbye to the world.

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// JavaScript không có equivalent tích hợp sẵn
// Nhưng có thể tự triển khai

function preserveMetadata(originalFn, wrapperFn) {
  wrapperFn.name = originalFn.name;
  wrapperFn.displayName = originalFn.displayName;
  wrapperFn.length = originalFn.length;
  return wrapperFn;
}

function decoratorWithMetadata(target, context) {
  function wrapper(...args) {
    return target.apply(this, args);
  }
  return preserveMetadata(target, wrapper);
}
""")

# ===== DECORATOR CLASSES =====
print("\n\n=== Decorator Classes ===")

# Sử dụng class làm decorator
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
        
    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def say_whats_up():
    return "What's up?"

print(say_whats_up())
print(say_whats_up())
print(f"say_whats_up has been called {say_whats_up.count} times")

# Class decorator với tham số
class Retry:
    def __init__(self, max_retries=3, exceptions=None):
        if exceptions is None:
            exceptions = (Exception,)
        self.max_retries = max_retries
        self.exceptions = exceptions
        
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.max_retries:
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    attempts += 1
                    if attempts == self.max_retries:
                        raise
                    print(f"Attempt {attempts} failed: {e}, retrying...")
            return None
        return wrapper

# Giả lập hàm không ổn định (thỉnh thoảng sẽ lỗi)
@Retry(max_retries=3, exceptions=(ValueError,))
def unstable_function(should_fail=False):
    import random
    if should_fail or random.random() < 0.5:
        raise ValueError("Random failure")
    return "Success!"

print("\nTrying unstable_function(should_fail=False):")
try:
    print(unstable_function(should_fail=False))
except ValueError as e:
    print(f"Function failed after all retries: {e}")

print("\nTrying unstable_function(should_fail=True):")
try:
    print(unstable_function(should_fail=True))
except ValueError as e:
    print(f"Function failed after all retries: {e}")

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// Class decorator trong JavaScript
class CountCalls {
  constructor(target, context) {
    this.count = 0;
    this.original = target;
    
    return (...args) => {
      this.count++;
      return this.original.apply(this, args);
    };
  }
}

class Retry {
  constructor(maxRetries = 3, exceptions = [Error]) {
    this.maxRetries = maxRetries;
    this.exceptions = exceptions;
    
    return (target, context) => {
      return async function(...args) {
        let attempts = 0;
        while (attempts < this.maxRetries) {
          try {
            return await target.apply(this, args);
          } catch (e) {
            if (this.exceptions.some(ex => e instanceof ex)) {
              attempts++;
              if (attempts === this.maxRetries) throw e;
              console.log(`Attempt ${attempts} failed, retrying...`);
            } else {
              throw e;
            }
          }
        }
      };
    };
  }
}
""")

# ===== DECORATOR FACTORIES =====
print("\n\n=== Decorator Factories ===")

# Decorator factory
def permission_required(permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user', {})
            if permission in user.get('permissions', []):
                return func(*args, **kwargs)
            else:
                return "Permission denied"
        return wrapper
    return decorator

@permission_required('admin')
def delete_user(user_id, user=None):
    return f"User {user_id} deleted successfully"

# Test với user có quyền admin
admin_user = {'name': 'Admin', 'permissions': ['admin', 'edit']}
print(delete_user(123, user=admin_user))  # Thành công

# Test với user không có quyền admin
regular_user = {'name': 'User', 'permissions': ['view', 'edit']}
print(delete_user(123, user=regular_user))  # Permission denied

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// Decorator factory trong JavaScript
function permissionRequired(permission) {
  return function(target, context) {
    return function(userId, options = {}) {
      const user = options.user || {};
      const permissions = user.permissions || [];
      
      if (permissions.includes(permission)) {
        return target.call(this, userId, options);
      } else {
        return "Permission denied";
      }
    };
  };
}

class UserService {
  @permissionRequired('admin')
  deleteUser(userId, options = {}) {
    return `User ${userId} deleted successfully`;
  }
}
""")

# ===== DECORATOR FOR ASYNCHRONOUS FUNCTIONS =====
print("\n\n=== Decorator cho Async Functions ===")

import asyncio

# Decorator cho async function
def log_async_call(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Calling async function: {func.__name__}")
        start_time = asyncio.get_event_loop().time()
        result = await func(*args, **kwargs)
        end_time = asyncio.get_event_loop().time()
        print(f"Async function {func.__name__} completed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@log_async_call
async def fetch_data(delay):
    await asyncio.sleep(delay)
    return f"Data fetched after {delay} seconds"

# Chạy coroutine
try:
    # Python 3.7+
    result = asyncio.run(fetch_data(0.5))
    print(result)
except (AttributeError, RuntimeError):
    print("asyncio.run() requires Python 3.7+. Using alternative method.")
    # Phương thức thay thế cho phiên bản Python cũ hơn
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_data(0.5))
    print(result)

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// Decorator cho async function trong JavaScript
function logAsyncCall(target, context) {
  return async function(...args) {
    console.log(`Calling async function: ${context.name}`);
    const startTime = performance.now();
    const result = await target.apply(this, args);
    const endTime = performance.now();
    console.log(`Async function ${context.name} completed in ${(endTime - startTime).toFixed(4)} ms`);
    return result;
  };
}

class DataService {
  @logAsyncCall
  async fetchData(delay) {
    await new Promise(resolve => setTimeout(resolve, delay * 1000));
    return `Data fetched after ${delay} seconds`;
  }
}
""")

# ===== CONTEXT MANAGER AS DECORATOR =====
print("\n\n=== Context Manager as Decorator ===")

from contextlib import contextmanager

# Context manager
@contextmanager
def timer():
    import time
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"Time elapsed: {end_time - start_time:.5f} seconds")

# Sử dụng context manager làm decorator
def with_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with timer():
            return func(*args, **kwargs)
    return wrapper

@with_timer
def do_computation():
    import time
    # Giả lập tác vụ nặng
    time.sleep(0.3)
    return "Computation done!"

print(do_computation())

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// JavaScript không có direct equivalent cho context managers
// Nhưng có thể mô phỏng bằng đối tượng với methods enter/exit

class Timer {
  constructor() {
    this.startTime = 0;
  }
  
  enter() {
    this.startTime = performance.now();
    return this;
  }
  
  exit() {
    const endTime = performance.now();
    console.log(`Time elapsed: ${((endTime - this.startTime)/1000).toFixed(5)} seconds`);
  }
}

function withTimer(target, context) {
  return function(...args) {
    const timer = new Timer().enter();
    try {
      return target.apply(this, args);
    } finally {
      timer.exit();
    }
  };
}

class ComputationService {
  @withTimer
  doComputation() {
    // Simulate heavy task
    const start = Date.now();
    while (Date.now() - start < 300) {} // Block for 300ms
    return "Computation done!";
  }
}
""")

# ===== DESCRIPTOR AS DECORATOR =====
print("\n\n=== Descriptor as Decorator ===")

# Descriptor class
class TypedProperty:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_
    
    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f"Expected {self.type}, got {type(value)}")
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

# Chuyển descriptor thành decorator
def typed_property(type_):
    def decorator(func):
        prop_name = func.__name__
        
        # Tạo một descriptor để kiểm tra kiểu dữ liệu
        descriptor = TypedProperty(prop_name, type_)
        
        # Định nghĩa getter và setter
        def getter(self):
            return descriptor.__get__(self, type(self))
        
        def setter(self, value):
            descriptor.__set__(self, value)
        
        # Trả về property với getter và setter
        return property(getter, setter)
    
    return decorator

# Sử dụng typed_property
class Person:
    @typed_property(str)
    def name(self):
        """Name property."""
        pass
    
    @typed_property(int)
    def age(self):
        """Age property."""
        pass
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Test typed_property
person = Person("Alice", 30)
print(f"Person: {person.name}, {person.age}")

try:
    person.age = "thirty"  # Sẽ gây ra TypeError
except TypeError as e:
    print(f"Error: {e}")

# So sánh với JavaScript:
print("\nJS comparison:")
print("""
// JavaScript không có direct equivalent cho descriptors
// Nhưng có thể mô phỏng bằng decorators và Object.defineProperty

function typedProperty(type) {
  return function(target, context) {
    const propertyName = context.name;
    const privatePropName = `_${propertyName}`;
    
    function getter() {
      return this[privatePropName];
    }
    
    function setter(value) {
      if (!(value instanceof type) && 
          typeof value !== type.name.toLowerCase()) {
        throw new TypeError(`Expected ${type.name}, got ${typeof value}`);
      }
      this[privatePropName] = value;
    }
    
    return {
      get: getter,
      set: setter
    };
  };
}

class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  
  @typedProperty(String)
  name;
  
  @typedProperty(Number)
  age;
}
""")

# ===== BEST PRACTICES =====
print("\n\n=== Best Practices ===")

print("1. Sử dụng @functools.wraps để giữ nguyên metadata của hàm gốc")
print("2. Đảm bảo decorator thông qua đúng tham số và kết quả trả về")
print("3. Viết decorator dễ đọc, dễ bảo trì, và có thể tái sử dụng")
print("4. Test decorator riêng biệt trước khi áp dụng vào code thực tế")
print("5. Cẩn thận với thứ tự khi xếp chồng nhiều decorator")
print("6. Sử dụng class decorator khi cần lưu trữ trạng thái")
print("7. Định nghĩa rõ ràng về phạm vi, mục đích và hành vi của decorator")

# ===== REAL-WORLD USE CASES =====
print("\n\n=== Real-World Use Cases ===")

# 1. Caching (Memoization)
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Sử dụng args và frozen set của kwargs làm cache key
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@memoize
def fibonacci(n):
    """Tính số Fibonacci thứ n (không hiệu quả nếu không có memoization)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("\n1. Caching (Memoization)")
print(f"fibonacci(30) = {fibonacci(30)}")
print(f"fibonacci(35) = {fibonacci(35)}") # Nhanh hơn nhờ có caching

# 2. Authentication và Authorization
def requires_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Trong thực tế, sẽ kiểm tra session, JWT, etc.
        auth_token = kwargs.get('auth_token')
        if auth_token == 'valid_token':
            return func(*args, **kwargs)
        return "Authentication required"
    return wrapper

@requires_auth
def get_sensitive_data(data_id, auth_token=None):
    return f"Sensitive data for ID {data_id}"

print("\n2. Authentication")
print(get_sensitive_data(123, auth_token="valid_token"))  # Thành công
print(get_sensitive_data(123, auth_token="invalid_token"))  # Thất bại

# 3. Logging và Monitoring
def log_function_call(logger=None):
    if logger is None:
        import logging
        logger = logging.getLogger()
        
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            
            logger.info(f"Calling {func.__name__}({signature})")
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} returned {result!r}")
                return result
            except Exception as e:
                logger.exception(f"Exception in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

import logging
logging.basicConfig(level=logging.INFO)

@log_function_call()
def divide(a, b):
    return a / b

print("\n3. Logging")
print(divide(10, 2))  # Log thành công
try:
    divide(10, 0)  # Log exception
except ZeroDivisionError:
    print("Caught division by zero")

# 4. Rate Limiting
def rate_limit(max_calls, period):
    """Hạn chế số lần gọi hàm trong một khoảng thời gian."""
    import time
    
    def decorator(func):
        calls = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Loại bỏ các lần gọi cũ hơn period
            calls[:] = [call for call in calls if now - call < period]
            
            if len(calls) >= max_calls:
                raise Exception(f"Rate limit exceeded: {max_calls} calls per {period} seconds")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=3, period=1)
def limited_function():
    return "Function called successfully"

print("\n4. Rate Limiting")
print(limited_function())
print(limited_function())
print(limited_function())
try:
    print(limited_function())  # Exceeds rate limit
except Exception as e:
    print(f"Error: {e}")

# 5. Validation
def validate_args(*types, **kw_types):
    """Kiểm tra kiểu dữ liệu cho tham số."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Kiểm tra args
            for arg, type_ in zip(args, types):
                if not isinstance(arg, type_):
                    raise TypeError(f"Argument {arg} should be {type_}")
            
            # Kiểm tra kwargs
            for key, value in kwargs.items():
                if key in kw_types and not isinstance(value, kw_types[key]):
                    raise TypeError(f"Argument {key}={value} should be {kw_types[key]}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_args(int, int, operation=str)
def calculate(a, b, operation="add"):
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    else:
        return None

print("\n5. Validation")
print(calculate(5, 10))  # Valid args
print(calculate(5, 10, operation="multiply"))  # Valid kwargs
try:
    print(calculate("5", 10))  # Invalid arg type
except TypeError as e:
    print(f"Error: {e}")

# ===== DEBUGGING DECORATORS =====
print("\n\n=== Debugging Decorators ===")

def debug_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"Calling {func.__name__}({signature})")
        
        try:
            result = func(*args, **kwargs)
            print(f"{func.__name__} returned: {result!r}")
            return result
        except Exception as e:
            print(f"Exception in {func.__name__}: {e}")
            raise
    return wrapper

# Khi decorator không hoạt động như mong đợi
@debug_decorator
def problematic_function(x, y):
    return x / y

print("Debugging a problematic function:")
try:
    problematic_function(10, 0)
except ZeroDivisionError:
    pass  # Bắt exception để chương trình tiếp tục chạy

# Kiểm tra decorator với functools.wraps
print("\nChecking decorator with functools.wraps:")
print(f"Function name: {problematic_function.__name__}")
print(f"Function docstring: {problematic_function.__doc__}")
print(f"Function annotations: {problematic_function.__annotations__}")

# Làm sao để hủy decorator
print("\nUnwrapping a decorator:")
original_function = problematic_function.__wrapped__
print(f"Original function: {original_function.__name__}")

# ===== DECORATOR WITH INTROSPECTION =====
print("\n\n=== Decorator with Introspection ===")
import inspect

def describe(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Thêm metadata về function
    wrapper.signature = inspect.signature(func)
    wrapper.params = list(wrapper.signature.parameters.keys())
    wrapper.docstring = func.__doc__
    wrapper.source = inspect.getsource(func)
    
    return wrapper

@describe
def complex_function(a, b=1, *, c=None, **kwargs):
    """This is a complex function with multiple parameter types."""
    return a + b

print("Function introspection:")
print(f"Signature: {complex_function.signature}")
print(f"Parameters: {complex_function.params}")
print(f"Docstring: {complex_function.docstring}")
print(f"Source code: \n{complex_function.source}")

# ===== SUMMARY =====
print("\n\n=== Summary ===")

print("Advanced Decorators trong Python:")
print("1. Decorator cơ bản: Hàm nhận hàm, trả về hàm")
print("2. Decorator với tham số: Thêm một lớp wrapper")
print("3. Class decorators: Thay đổi hành vi của class")
print("4. Method decorators: Áp dụng cho phương thức của class")
print("5. Stacking decorators: Áp dụng nhiều decorators theo thứ tự")
print("6. Giữ metadata: Sử dụng functools.wraps")
print("7. Decorator classes: Sử dụng __call__")
print("8. Decorator factories: Tạo decorators với tham số")
print("9. Async decorators: Cho các hàm bất đồng bộ")
print("10. Context managers as decorators: Kết hợp context với decorator")
print("11. Descriptors as decorators: Tạo property được kiểm soát")
print("12. Use cases: Caching, authentication, logging, rate limiting, validation")

print("\nDecorators trong JavaScript:")
print("1. JavaScript cũng có decorators (Stage 3 proposal)")
print("2. Tương tự về ý tưởng nhưng khác về cú pháp và ngữ cảnh")
print("3. Một số tính năng như descriptors không có equivalent trực tiếp")
print("4. Không có một số tiện ích như functools.wraps")
print("5. Decorators trong JavaScript chủ yếu áp dụng cho class và class methods")