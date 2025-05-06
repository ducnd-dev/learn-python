"""
Command Design Pattern

The Command pattern encapsulates a request as an object, allowing you to parameterize
clients with different requests, queue or log requests, and support undoable operations.

Key components:
1. Command: Interface declaring an execution method
2. ConcreteCommand: Implements execution by invoking the corresponding operations on Receiver
3. Client: Creates a ConcreteCommand instance and sets its receiver
4. Invoker: Asks the command to carry out the request
5. Receiver: Knows how to perform the operations

This pattern is used in queue management, undo functionality, and macro recording.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass


# Receiver
class TextEditor:
    def __init__(self):
        self.text = ""
    
    def insert_text(self, text: str) -> None:
        self.text += text
        print(f"Inserted: '{text}'")
        print(f"Current text: '{self.text}'")
    
    def delete_text(self, length: int) -> str:
        if length <= 0 or length > len(self.text):
            return ""
        
        deleted_text = self.text[-length:]
        self.text = self.text[:-length]
        print(f"Deleted: '{deleted_text}'")
        print(f"Current text: '{self.text}'")
        return deleted_text
    
    def replace_text(self, old: str, new: str) -> bool:
        if old not in self.text:
            return False
        
        self.text = self.text.replace(old, new, 1)
        print(f"Replaced '{old}' with '{new}'")
        print(f"Current text: '{self.text}'")
        return True


# Concrete Commands
class InsertTextCommand(Command):
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text
    
    def execute(self) -> None:
        self.editor.insert_text(self.text)
    
    def undo(self) -> None:
        self.editor.delete_text(len(self.text))


class DeleteTextCommand(Command):
    def __init__(self, editor: TextEditor, length: int):
        self.editor = editor
        self.length = length
        self.deleted_text = ""
    
    def execute(self) -> None:
        self.deleted_text = self.editor.delete_text(self.length)
    
    def undo(self) -> None:
        if self.deleted_text:
            self.editor.insert_text(self.deleted_text)


class ReplaceTextCommand(Command):
    def __init__(self, editor: TextEditor, old_text: str, new_text: str):
        self.editor = editor
        self.old_text = old_text
        self.new_text = new_text
        self.replaced = False
    
    def execute(self) -> None:
        self.replaced = self.editor.replace_text(self.old_text, self.new_text)
    
    def undo(self) -> None:
        if self.replaced:
            self.editor.replace_text(self.new_text, self.old_text)


# Invoker
class CommandManager:
    def __init__(self):
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
    
    def execute_command(self, command: Command) -> None:
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()  # Clear redo stack when a new command is executed
    
    def undo(self) -> None:
        if not self.history:
            print("Nothing to undo")
            return
        
        command = self.history.pop()
        command.undo()
        self.redo_stack.append(command)
    
    def redo(self) -> None:
        if not self.redo_stack:
            print("Nothing to redo")
            return
        
        command = self.redo_stack.pop()
        command.execute()
        self.history.append(command)


# Example usage
if __name__ == "__main__":
    # Create receiver
    editor = TextEditor()
    
    # Create invoker
    command_manager = CommandManager()
    
    # Execute commands
    print("\n--- Executing commands ---")
    command_manager.execute_command(InsertTextCommand(editor, "Hello "))
    command_manager.execute_command(InsertTextCommand(editor, "World!"))
    command_manager.execute_command(ReplaceTextCommand(editor, "World", "Python"))
    command_manager.execute_command(DeleteTextCommand(editor, 1))
    
    # Undo operations
    print("\n--- Undoing operations ---")
    command_manager.undo()  # Undo delete
    command_manager.undo()  # Undo replace
    
    # Redo operation
    print("\n--- Redoing operations ---")
    command_manager.redo()  # Redo replace
    
    # Execute another command
    print("\n--- Execute new command ---")
    command_manager.execute_command(InsertTextCommand(editor, " is great!"))
    
    # Try to redo after executing a new command
    print("\n--- Try to redo ---")
    command_manager.redo()  # Nothing to redo