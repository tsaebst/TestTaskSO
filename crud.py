from typing import Dict
from fastapi import HTTPException

users_db: Dict[str, dict] = {}

def create_user(user):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user.dict()
    return user

def get_user(username: str):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(username: str, user_data):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(user_data)
    users_db[username] = user
    return user

def delete_user(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[username]
