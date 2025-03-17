from pydantic import BaseModel


class User(BaseModel):
    id: str = ""
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str = ""
    name: str
    email: str


class UserLoginRequest(BaseModel):
    email: str
    password: str
