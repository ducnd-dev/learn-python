"""
Repository Design Pattern

The Repository pattern mediates between the domain and data mapping layers, acting like an
in-memory domain object collection. It provides a more object-oriented view of the persistence layer,
hiding data access complexity from the domain logic.

Key components:
1. Repository Interface: Defines methods for domain object access
2. Repository Implementation: Implements the repository interface using specific data storage technology
3. Entity: Domain objects that are persisted and retrieved by the repository
4. Data Mapper/ORM (optional): Maps between domain objects and database structures
5. Unit of Work (optional): Coordinates transactions and changes tracking

This pattern is commonly used in:
- Clean Architecture
- Domain-Driven Design (DDD)
- Microservices
- Applications with complex domain models
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, TypeVar, Generic
import json
import os
import sqlite3
from datetime import datetime


# Entity class
class User:
    def __init__(self, user_id: int = None, username: str = "", email: str = "", 
                 created_at: datetime = None):
        self.id = user_id
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.now()
    
    def __str__(self) -> str:
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"


# Generic type for entities
T = TypeVar('T')


# Repository Interface
class Repository(Generic[T], ABC):
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Retrieve an entity by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all entities"""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> bool:
        """Update an existing entity"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID"""
        pass


# In-Memory Repository Implementation
class InMemoryUserRepository(Repository[User]):
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
    
    def get_by_id(self, entity_id: int) -> Optional[User]:
        return self._users.get(entity_id)
    
    def get_all(self) -> List[User]:
        return list(self._users.values())
    
    def add(self, entity: User) -> User:
        # Assign ID if not provided
        if entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        
        self._users[entity.id] = entity
        return entity
    
    def update(self, entity: User) -> bool:
        if entity.id in self._users:
            self._users[entity.id] = entity
            return True
        return False
    
    def delete(self, entity_id: int) -> bool:
        if entity_id in self._users:
            del self._users[entity_id]
            return True
        return False
    
    # Additional methods specific to Users
    def find_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None
    
    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None


# JSON File Repository Implementation
class JsonFileUserRepository(Repository[User]):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
        self._next_id = self._calculate_next_id()
    
    def _ensure_file_exists(self) -> None:
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file)
    
    def _read_all_from_file(self) -> List[Dict]:
        with open(self.file_path, 'r') as file:
            return json.load(file)
    
    def _write_all_to_file(self, users_data: List[Dict]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(users_data, file, indent=2)
    
    def _calculate_next_id(self) -> int:
        users_data = self._read_all_from_file()
        if not users_data:
            return 1
        return max(user['id'] for user in users_data) + 1
    
    def _to_dict(self, user: User) -> Dict:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
    
    def _from_dict(self, user_dict: Dict) -> User:
        return User(
            user_id=user_dict['id'],
            username=user_dict['username'],
            email=user_dict['email'],
            created_at=datetime.fromisoformat(user_dict['created_at'])
        )
    
    def get_by_id(self, entity_id: int) -> Optional[User]:
        users_data = self._read_all_from_file()
        for user_data in users_data:
            if user_data['id'] == entity_id:
                return self._from_dict(user_data)
        return None
    
    def get_all(self) -> List[User]:
        users_data = self._read_all_from_file()
        return [self._from_dict(user_data) for user_data in users_data]
    
    def add(self, entity: User) -> User:
        users_data = self._read_all_from_file()
        
        # Assign ID if not provided
        if entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        
        users_data.append(self._to_dict(entity))
        self._write_all_to_file(users_data)
        return entity
    
    def update(self, entity: User) -> bool:
        users_data = self._read_all_from_file()
        
        for i, user_data in enumerate(users_data):
            if user_data['id'] == entity.id:
                users_data[i] = self._to_dict(entity)
                self._write_all_to_file(users_data)
                return True
        
        return False
    
    def delete(self, entity_id: int) -> bool:
        users_data = self._read_all_from_file()
        original_length = len(users_data)
        
        users_data = [user_data for user_data in users_data if user_data['id'] != entity_id]
        
        if len(users_data) < original_length:
            self._write_all_to_file(users_data)
            return True
        
        return False


# SQLite Repository Implementation
class SQLiteUserRepository(Repository[User]):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table_if_not_exists()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _create_table_if_not_exists(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.commit()
    
    def get_by_id(self, entity_id: int) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    user_id=row[0],
                    username=row[1],
                    email=row[2],
                    created_at=datetime.fromisoformat(row[3])
                )
            
            return None
    
    def get_all(self) -> List[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, created_at FROM users")
            rows = cursor.fetchall()
            
            return [
                User(
                    user_id=row[0],
                    username=row[1],
                    email=row[2],
                    created_at=datetime.fromisoformat(row[3])
                )
                for row in rows
            ]
    
    def add(self, entity: User) -> User:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            created_at_str = entity.created_at.isoformat()
            
            cursor.execute(
                "INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)",
                (entity.username, entity.email, created_at_str)
            )
            conn.commit()
            
            # Set the ID from the auto-increment value
            entity.id = cursor.lastrowid
            
            return entity
    
    def update(self, entity: User) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            created_at_str = entity.created_at.isoformat()
            
            cursor.execute(
                "UPDATE users SET username = ?, email = ?, created_at = ? WHERE id = ?",
                (entity.username, entity.email, created_at_str, entity.id)
            )
            conn.commit()
            
            return cursor.rowcount > 0
    
    def delete(self, entity_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (entity_id,))
            conn.commit()
            
            return cursor.rowcount > 0
    
    # Additional methods specific to users
    def find_by_username(self, username: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, created_at FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    user_id=row[0],
                    username=row[1],
                    email=row[2],
                    created_at=datetime.fromisoformat(row[3])
                )
            
            return None


# Service layer using the repository
class UserService:
    def __init__(self, user_repository: Repository[User]):
        self.user_repository = user_repository
    
    def register_user(self, username: str, email: str) -> User:
        # Business logic for user registration
        user = User(username=username, email=email)
        return self.user_repository.add(user)
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        return self.user_repository.get_all()
    
    def update_user_email(self, user_id: int, new_email: str) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if user:
            user.email = new_email
            return self.user_repository.update(user)
        return False
    
    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)


# Example usage
if __name__ == "__main__":
    # Choose which repository implementation to use
    # repository = InMemoryUserRepository()
    repository = JsonFileUserRepository("users.json")
    # repository = SQLiteUserRepository("users.db")
    
    # Create a service using the repository
    user_service = UserService(repository)
    
    # Register some users
    print("Registering users...")
    user1 = user_service.register_user("alice", "alice@example.com")
    user2 = user_service.register_user("bob", "bob@example.com")
    user3 = user_service.register_user("charlie", "charlie@example.com")
    
    # Get all users
    print("\nAll users:")
    for user in user_service.get_all_users():
        print(f"- {user}")
    
    # Update a user
    print("\nUpdating Bob's email...")
    success = user_service.update_user_email(user2.id, "bob.updated@example.com")
    print(f"Update {'successful' if success else 'failed'}")
    
    # Get a specific user
    print("\nGetting Bob's details:")
    bob = user_service.get_user(user2.id)
    if bob:
        print(f"- {bob}")
    
    # Delete a user
    print("\nDeleting Charlie's account...")
    success = user_service.delete_user(user3.id)
    print(f"Deletion {'successful' if success else 'failed'}")
    
    # Get all remaining users
    print("\nRemaining users:")
    for user in user_service.get_all_users():
        print(f"- {user}")