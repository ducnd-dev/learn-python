"""
Proxy Design Pattern

The Proxy pattern provides a surrogate or placeholder for another object to control
access to it. It is useful for:
1. Lazy initialization (Virtual Proxy)
2. Access control (Protection Proxy)
3. Remote access (Remote Proxy)
4. Logging (Logging Proxy)
5. Caching (Caching Proxy)
"""

from abc import ABC, abstractmethod
import time


# The Subject interface declares common operations for both RealSubject and Proxy
class Subject(ABC):
    @abstractmethod
    def request(self) -> None:
        pass


# RealSubject contains the core business logic
class RealSubject(Subject):
    def request(self) -> str:
        return "RealSubject: Handling request"


# The Proxy has a reference to a RealSubject object and controls access to it
class Proxy(Subject):
    def __init__(self, real_subject: RealSubject) -> None:
        self._real_subject = real_subject
        
    def request(self) -> str:
        if self._check_access():
            # Additional operations before the request
            result = self._real_subject.request()
            # Additional operations after the request
            self._log_access()
            return result
        else:
            return "Proxy: Access denied"
    
    def _check_access(self) -> bool:
        # Security check
        print("Proxy: Checking access prior to firing a real request.")
        return True
    
    def _log_access(self) -> None:
        print("Proxy: Logging the time of request.", end=" ")
        print(f"Time: {time.strftime('%H:%M:%S')}")


# Example of a Virtual Proxy that loads a heavy object only when necessary
class HeavyObject:
    def __init__(self):
        # Simulating a heavy initialization process
        print("HeavyObject: Loading lots of data...")
        time.sleep(1)
        self.data = "Large Dataset"
    
    def operation(self) -> str:
        return f"HeavyObject: Processing with {self.data}"


class VirtualProxy:
    def __init__(self):
        self._real_object = None
    
    def operation(self) -> str:
        print("VirtualProxy: First access, loading object...")
        if self._real_object is None:
            self._real_object = HeavyObject()
        return self._real_object.operation()


# Example of a Caching Proxy
class ExpensiveOperation:
    def perform_operation(self, a, b) -> int:
        print(f"ExpensiveOperation: Computing {a} * {b}...")
        time.sleep(0.5)  # Simulate complex computation
        return a * b


class CachingProxy:
    def __init__(self, operation: ExpensiveOperation):
        self._operation = operation
        self._cache = {}
    
    def perform_operation(self, a, b) -> int:
        key = f"{a}_{b}"
        if key not in self._cache:
            print("CachingProxy: Cache miss. Performing operation...")
            self._cache[key] = self._operation.perform_operation(a, b)
        else:
            print("CachingProxy: Cache hit. Returning cached result.")
        return self._cache[key]


# Example usage
if __name__ == "__main__":
    print("Client: Executing the client code with a real subject:")
    real_subject = RealSubject()
    print(real_subject.request())

    print("\nClient: Executing the same client code with a proxy:")
    proxy = Proxy(real_subject)
    print(proxy.request())
    
    print("\nExample of Virtual Proxy:")
    print("First access (will load the object):")
    virtual_proxy = VirtualProxy()
    print(virtual_proxy.operation())
    print("Second access (object already loaded):")
    print(virtual_proxy.operation())
    
    print("\nExample of Caching Proxy:")
    expensive_op = ExpensiveOperation()
    caching_proxy = CachingProxy(expensive_op)
    
    print("First computation of 5 * 10:")
    print(f"Result: {caching_proxy.perform_operation(5, 10)}")
    
    print("Second computation of 5 * 10 (should use cache):")
    print(f"Result: {caching_proxy.perform_operation(5, 10)}")
    
    print("Computation of 3 * 7 (should be a cache miss):")
    print(f"Result: {caching_proxy.perform_operation(3, 7)}")