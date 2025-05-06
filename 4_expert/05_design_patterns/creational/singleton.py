"""
Singleton Design Pattern

The Singleton pattern ensures a class has only one instance and provides a global point
of access to it. This is useful when exactly one object is needed to coordinate actions
across the system.
"""

class Singleton:
    """
    A classic implementation of the Singleton pattern with a static instance variable.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        # This will be called every time an instance is "created"
        # but since __new__ returns the same instance, it's safe
        self.value = value if value is not None else self.value if hasattr(self, 'value') else None


# Alternative implementation using a metaclass
class SingletonMeta(type):
    """
    A metaclass that creates a Singleton base class when called.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonWithMeta(metaclass=SingletonMeta):
    """
    Example class that uses the SingletonMeta metaclass.
    """
    def __init__(self, value=None):
        self.value = value


# Example usage
if __name__ == "__main__":
    # Classic implementation
    s1 = Singleton("First instance")
    s2 = Singleton("Second instance - ignored")
    
    print(f"Classic singleton - Same instance: {s1 is s2}")
    print(f"Value of s1: {s1.value}")
    print(f"Value of s2: {s2.value}")  # Will be the same as s1.value
    
    # Metaclass implementation
    m1 = SingletonWithMeta("First meta instance")
    m2 = SingletonWithMeta("Second meta instance - ignored")
    
    print(f"Metaclass singleton - Same instance: {m1 is m2}")
    print(f"Value of m1: {m1.value}")
    print(f"Value of m2: {m2.value}")  # Will be the same as m1.value