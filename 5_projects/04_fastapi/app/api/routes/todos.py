"""
Todo routes for task management.
"""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.models import Todo, User
from app.schemas.schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter()


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_in: TodoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new todo.
    """
    todo = Todo(
        **todo_in.dict(),
        user_id=current_user.id,
    )
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    
    return todo


@router.get("/", response_model=List[TodoResponse])
async def read_todos(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    completed: Optional[bool] = None,
) -> Any:
    """
    Retrieve todos.
    """
    query = select(Todo).where(Todo.user_id == current_user.id)
    
    if completed is not None:
        query = query.where(Todo.completed == completed)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    
    return result.scalars().all()


@router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(
    todo_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get todo by ID.
    """
    todo = await get_todo_by_id(db, todo_id, current_user)
    
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a todo.
    """
    todo = await get_todo_by_id(db, todo_id, current_user)
    
    # Update only fields that are provided
    update_data = todo_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    await db.commit()
    await db.refresh(todo)
    
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a todo.
    """
    todo = await get_todo_by_id(db, todo_id, current_user)
    
    await db.delete(todo)
    await db.commit()


async def get_todo_by_id(db: AsyncSession, todo_id: int, current_user: User) -> Todo:
    """
    Get a todo by ID, verifying it belongs to the current user.
    """
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    )
    todo = result.scalars().first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todo