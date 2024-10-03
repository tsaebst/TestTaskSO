from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.authent import authenticate_user, create_access_token, decode_token
from app.crud import create_user, get_user, update_user, delete_user
from app.models import UserCreate, UserUpdate

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Аутентифікація користувача і генерація токену
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Перевірка токену
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

# CRUD операції
@app.post("/users/")
def api_create_user(user: UserCreate, current_user: str = Depends(get_current_user)):
    return create_user(user)

@app.get("/users/{username}")
def api_get_user(username: str, current_user: str = Depends(get_current_user)):
    return get_user(username)

@app.put("/users/{username}")
def api_update_user(username: str, user: UserUpdate, current_user: str = Depends(get_current_user)):
    return update_user(username, user.dict(exclude_unset=True))

@app.delete("/users/{username}")
def api_delete_user(username: str, current_user: str = Depends(get_current_user)):
    return delete_user(username)
