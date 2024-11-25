from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class UserAuth(UserLogin):
    repeat_password: str

