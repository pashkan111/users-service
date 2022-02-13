from codecs import strict_errors
from pydantic import BaseModel
import datetime 
from typing import List


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
        

class UsersListSchema(BaseModel):
    id: int = None
    first_name: str = None
    last_name: str = None
    email: str = None


class UsersListSchemaORM(UsersListSchema):
# class UsersListSchemaORM(UsersListSchema):
    # users: List[UsersListSchema] = []
    class Config:
        orm_mode = True
        

class UpdateUserModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: datetime.date
    
    
class UpdateUserResponseModel(UpdateUserModel):
    id: int
    
    
class UpdateUserResponseModelORM(UpdateUserResponseModel):
    class Config:
        orm_mode = True    
    