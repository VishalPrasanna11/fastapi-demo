from fastapi import FastAPI, HTTPException, status
from typing import List, Dict
from app.models import User, UserCreate, UserUpdate

app = FastAPI(title="FastAPI Demo", version="1.0.0")

# In-memory storage for users
users_db: Dict[int, User] = {}
next_user_id = 1


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users():
    """Get all users"""
    return list(users_db.values())


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    """Get a user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return users_db[user_id]


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    global next_user_id
    new_user = User(id=next_user_id, **user.model_dump())
    users_db[next_user_id] = new_user
    next_user_id += 1
    return new_user


@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdate):
    """Update an existing user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    updated_user = User(id=user_id, **user.model_dump())
    users_db[user_id] = updated_user
    return updated_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    del users_db[user_id]
