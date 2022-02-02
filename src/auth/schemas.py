from pydantic import BaseModel


class LoginSchema(BaseModel):
    login: str
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str


class User(BaseModel):
    login: str = None
    email: str = None
    full_name: str = None
    disabled: bool = None


class UserInDB(User):
    password: str