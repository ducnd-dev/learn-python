"""
Composite Design Pattern

The Composite pattern composes objects into tree structures to represent part-whole hierarchies.
It lets clients treat individual objects and compositions of objects uniformly.

Key components:
1. Component: Interface or abstract class for all components (both leaf and composite)
2. Leaf: Represents individual objects with no children
3. Composite: Represents a component that has children (other components)
4. Client: Manipulates objects in the composition through the Component interface

This pattern is used when clients need to treat individual objects and compositions
of objects uniformly, or when you want to represent part-whole hierarchies of objects.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# Component
class FileSystemComponent(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def display(self, indent: int = 0) -> None:
        pass
    
    @abstractmethod
    def get_size(self) -> int:
        pass
    
    def get_name(self) -> str:
        return self.name


# Leaf
class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size
    
    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"- File: {self.name} ({self._size} bytes)")
    
    def get_size(self) -> int:
        return self._size


# Composite
class Directory(FileSystemComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)
    
    def remove(self, component: FileSystemComponent) -> None:
        self._children.remove(component)
    
    def get_child(self, index: int) -> Optional[FileSystemComponent]:
        if 0 <= index < len(self._children):
            return self._children[index]
        return None
    
    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"+ Directory: {self.name} ({self.get_size()} bytes)")
        for child in self._children:
            child.display(indent + 4)
    
    def get_size(self) -> int:
        total_size = 0
        for child in self._children:
            total_size += child.get_size()
        return total_size


# Extended Composite with search functionality
class SearchableDirectory(Directory):
    def search(self, name: str) -> List[FileSystemComponent]:
        results = []
        if name in self.name:
            results.append(self)
        
        for child in self._children:
            if name in child.get_name():
                results.append(child)
            
            # If it's a directory, search recursively
            if isinstance(child, SearchableDirectory):
                results.extend(child.search(name))
        
        return results


# Client code
if __name__ == "__main__":
    # Create a file structure
    root = SearchableDirectory("root")
    
    # Add files to root
    root.add(File("file1.txt", 100))
    root.add(File("file2.txt", 200))
    
    # Create subdirectories
    documents = SearchableDirectory("documents")
    documents.add(File("doc1.pdf", 500))
    documents.add(File("doc2.pdf", 750))
    
    # Create nested subdirectory
    reports = SearchableDirectory("reports")
    reports.add(File("report1.docx", 300))
    reports.add(File("report2.docx", 400))
    reports.add(File("data.xlsx", 250))
    
    # Add nested directories
    documents.add(reports)
    root.add(documents)
    
    # Create another subdirectory
    images = SearchableDirectory("images")
    images.add(File("image1.jpg", 1024))
    images.add(File("image2.jpg", 2048))
    root.add(images)
    
    # Display the file structure
    print("\n=== File Structure ===")
    root.display()
    
    # Display the size of specific components
    print(f"\nSize of documents: {documents.get_size()} bytes")
    print(f"Size of root: {root.get_size()} bytes")
    
    # Search for components
    print("\n=== Search Results ===")
    print("Searching for 'report':")
    results = root.search("report")
    for item in results:
        print(f"- Found: {item.get_name()}")
    
    print("\nSearching for 'doc':")
    results = root.search("doc")
    for item in results:
        print(f"- Found: {item.get_name()}")