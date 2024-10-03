from pydantic import BaseModel
from typing import List, Optional

# Схема для користувача
class User(BaseModel):
    username: str
    name: str
    age: int
    friends: List[str] = []

# Схема для створення та оновлення користувача
class UserCreate(BaseModel):
    username: str
    name: str
    age: int
    friends: Optional[List[str]] = []

class UserUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    friends: Optional[List[str]] = []
