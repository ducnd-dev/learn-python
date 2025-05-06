"""
Factory Method Design Pattern

The Factory Method pattern defines an interface for creating an object, but lets subclasses
decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.
"""
from abc import ABC, abstractmethod


# Product interface
class Document(ABC):
    @abstractmethod
    def create(self):
        pass


# Concrete Products
class PDFDocument(Document):
    def create(self):
        return "Creating PDF document"


class WordDocument(Document):
    def create(self):
        return "Creating Word document"


class HTMLDocument(Document):
    def create(self):
        return "Creating HTML document"


# Creator abstract class
class DocumentCreator(ABC):
    @abstractmethod
    def factory_method(self) -> Document:
        pass

    def operation(self) -> str:
        # Call the factory method to create a Document object
        document = self.factory_method()
        # Now use the document
        result = f"DocumentCreator: {document.create()}"
        return result


# Concrete Creators override the factory method to change the resulting product type
class PDFCreator(DocumentCreator):
    def factory_method(self) -> Document:
        return PDFDocument()


class WordCreator(DocumentCreator):
    def factory_method(self) -> Document:
        return WordDocument()


class HTMLCreator(DocumentCreator):
    def factory_method(self) -> Document:
        return HTMLDocument()


# Client code
def client_code(creator: DocumentCreator) -> None:
    print(f"Client: I'm not aware of the creator's class, but it still works.\n"
          f"{creator.operation()}")


# Example usage
if __name__ == "__main__":
    print("App: Launched with the PDFCreator.")
    client_code(PDFCreator())
    print("\n")

    print("App: Launched with the WordCreator.")
    client_code(WordCreator())
    print("\n")
    
    print("App: Launched with the HTMLCreator.")
    client_code(HTMLCreator())