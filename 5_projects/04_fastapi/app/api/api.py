"""
API router configuration.
"""

from fastapi import APIRouter

from app.api.routes import auth, todos, users

api_router = APIRouter()

# Include router for authentication
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include router for users
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Include router for todos
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])