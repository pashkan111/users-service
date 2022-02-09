from pydantic import BaseModel
import datetime 


class LoginSchema(BaseModel):
    login: str
    password: str
    
    
class LoginSchemaORM(LoginSchema):
    class Config:
        orm_mode = True


class TokenData(BaseModel):
    login: str


class UserSchema(BaseModel):
    first_name: str = None
    last_name: str = None
    other_name: str = None
    email: str = None
    phone: str = None
    birthday: datetime.date = None
    is_admin: bool = None


class UserSchemaORM(UserSchema):
    class Config:
        orm_mode = True