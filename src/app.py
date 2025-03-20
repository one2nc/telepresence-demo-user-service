import uuid
from typing import Dict

import jwt
from fastapi import FastAPI, HTTPException

from models import User, UserLoginRequest, UserResponse

SECRET_KEY = "mysecretkey"


def generate_token(user_id: str):
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


app = FastAPI()

# In-memory user store
users: Dict[str, User] = {}


@app.get("/healthz", status_code=201)
async def health():
    return {"message": "Hello from User Service!"}


@app.post("/users", response_model=UserResponse)
async def create_user(user: User):
    user.id = str(uuid.uuid4())
    if user.email in [u.email for u in users.values()]:
        raise HTTPException(status_code=400, detail="Email already registered")
    users[user.id] = user
    user = UserResponse.model_validate(
        {"id": user.id, "name": user.name, "email": user.email}
    )
    return user


@app.post("/login")
async def login(user: UserLoginRequest):
    user = next(
        (
            u
            for u in users.values()
            if user.email == u.email and user.password == u.password
        ),
        None,
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = generate_token(user.id)
    return {"access_token": token}


# @app.get("/users/{user_id}", response_model=UserResponse)
# async def get_user(user_id: str, token: str = Depends(verify_token)):
#     user = users.get(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user = UserResponse.model_validate(
#         {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email
#         }
#     )
#     return user
