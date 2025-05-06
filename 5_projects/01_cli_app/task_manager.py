"""
Task Manager CLI Application

A command-line interface application for managing tasks.
Features:
- Add, view, update, and delete tasks
- Mark tasks as complete
- Filter tasks by status, priority, or due date
- Save tasks to a JSON file
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Any


class Priority(Enum):
    """Enum for task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    
    def __str__(self) -> str:
        return self.name


class Status(Enum):
    """Enum for task status"""
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    
    def __str__(self) -> str:
        return self.name


class Task:
    """Represents a task in the task manager"""
    
    def __init__(self, 
                 title: str, 
                 description: str = "", 
                 priority: Priority = Priority.MEDIUM,
                 due_date: Optional[datetime] = None,
                 status: Status = Status.PENDING,
                 task_id: Optional[int] = None):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.created_at = datetime.now()
        self.id = task_id  # Will be set when added to the task manager
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.name,
            "status": self.status.name,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task object from a dictionary"""
        due_date = datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority[data["priority"]],
            due_date=due_date,
            status=Status[data["status"]],
            task_id=data["id"]
        )
    
    def __str__(self) -> str:
        """String representation of a task"""
        due_str = f"Due: {self.due_date.strftime('%Y-%m-%d')}" if self.due_date else "No due date"
        return f"[{self.id}] {self.title} ({self.priority}) - {self.status} - {due_str}"


class TaskManager:
    """Manages the collection of tasks"""
    
    def __init__(self, storage_file: str = "tasks.json"):
        self.tasks: List[Task] = []
        self.storage_file = storage_file
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, task: Task) -> Task:
        """Add a new task to the manager"""
        if task.id is None:
            task.id = self.next_id
            self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update a task with the provided attributes"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        if "title" in kwargs:
            task.title = kwargs["title"]
        if "description" in kwargs:
            task.description = kwargs["description"]
        if "priority" in kwargs:
            task.priority = kwargs["priority"]
        if "due_date" in kwargs:
            task.due_date = kwargs["due_date"]
        if "status" in kwargs:
            task.status = kwargs["status"]
        
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def list_tasks(self, 
                  status: Optional[Status] = None, 
                  priority: Optional[Priority] = None,
                  due_date_filter: Optional[str] = None) -> List[Task]:
        """List tasks with optional filtering"""
        filtered_tasks = self.tasks
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
        
        if due_date_filter:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            if due_date_filter == "today":
                tomorrow = today + timedelta(days=1)
                filtered_tasks = [t for t in filtered_tasks if t.due_date and today <= t.due_date < tomorrow]
            elif due_date_filter == "week":
                next_week = today + timedelta(days=7)
                filtered_tasks = [t for t in filtered_tasks if t.due_date and today <= t.due_date < next_week]
            elif due_date_filter == "overdue":
                filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date < today]
        
        return filtered_tasks
    
    def save_tasks(self) -> None:
        """Save tasks to the storage file"""
        with open(self.storage_file, 'w') as f:
            data = {
                "next_id": self.next_id,
                "tasks": [task.to_dict() for task in self.tasks]
            }
            json.dump(data, f, indent=2)
    
    def load_tasks(self) -> None:
        """Load tasks from the storage file"""
        if not os.path.exists(self.storage_file):
            return
        
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                
                # Load the next ID
                self.next_id = data.get("next_id", 1)
                
                # Load tasks
                task_data = data.get("tasks", [])
                self.tasks = [Task.from_dict(t) for t in task_data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.tasks = []
            self.next_id = 1


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse a date string in the format YYYY-MM-DD"""
    if not date_str:
        return None
    
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def main():
    """Main entry point for the CLI application"""
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description")
    add_parser.add_argument(
        "-p", "--priority", 
        choices=["LOW", "MEDIUM", "HIGH"],
        default="MEDIUM",
        help="Task priority"
    )
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    
    # 'list' command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-s", "--status", 
        choices=["PENDING", "IN_PROGRESS", "COMPLETED"],
        help="Filter by status"
    )
    list_parser.add_argument(
        "-p", "--priority", 
        choices=["LOW", "MEDIUM", "HIGH"],
        help="Filter by priority"
    )
    list_parser.add_argument(
        "--due", 
        choices=["today", "week", "overdue"],
        help="Filter by due date"
    )
    
    # 'update' command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("-t", "--title", help="New task title")
    update_parser.add_argument("-d", "--description", help="New task description")
    update_parser.add_argument(
        "-p", "--priority", 
        choices=["LOW", "MEDIUM", "HIGH"],
        help="New task priority"
    )
    update_parser.add_argument("--due", help="New due date (YYYY-MM-DD)")
    update_parser.add_argument(
        "-s", "--status", 
        choices=["PENDING", "IN_PROGRESS", "COMPLETED"],
        help="New task status"
    )
    
    # 'delete' command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")
    
    # 'view' command
    view_parser = subparsers.add_parser("view", help="View a task details")
    view_parser.add_argument("id", type=int, help="Task ID")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize task manager
    task_manager = TaskManager()
    
    if args.command == "add":
        due_date = parse_date(args.due)
        priority = Priority[args.priority]
        
        task = Task(
            title=args.title,
            description=args.description or "",
            priority=priority,
            due_date=due_date
        )
        
        task = task_manager.add_task(task)
        print(f"Added task: {task}")
    
    elif args.command == "list":
        status = Status[args.status] if args.status else None
        priority = Priority[args.priority] if args.priority else None
        
        tasks = task_manager.list_tasks(
            status=status,
            priority=priority,
            due_date_filter=args.due
        )
        
        if not tasks:
            print("No tasks found.")
        else:
            print(f"Found {len(tasks)} tasks:")
            for task in tasks:
                print(task)
    
    elif args.command == "update":
        kwargs = {}
        
        if args.title:
            kwargs["title"] = args.title
        
        if args.description:
            kwargs["description"] = args.description
        
        if args.priority:
            kwargs["priority"] = Priority[args.priority]
        
        if args.due:
            kwargs["due_date"] = parse_date(args.due)
        
        if args.status:
            kwargs["status"] = Status[args.status]
        
        task = task_manager.update_task(args.id, **kwargs)
        if task:
            print(f"Updated task: {task}")
        else:
            print(f"Task with ID {args.id} not found.")
    
    elif args.command == "delete":
        if task_manager.delete_task(args.id):
            print(f"Deleted task with ID {args.id}.")
        else:
            print(f"Task with ID {args.id} not found.")
    
    elif args.command == "view":
        task = task_manager.get_task(args.id)
        if task:
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Priority: {task.priority}")
            print(f"Status: {task.status}")
            print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
            if task.due_date:
                print(f"Due: {task.due_date.strftime('%Y-%m-%d')}")
            else:
                print("Due: No due date")
        else:
            print(f"Task with ID {args.id} not found.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()