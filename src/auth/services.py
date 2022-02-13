from db.db import session
from .models import AuthUser
from .schemas import UsersListSchemaORM, UpdateUserModel, PrivateCreateUserSchemaORM, PrivateCreateUserSchema, PrivateDetailUserResponseModelORM
from typing import List
from fastapi import Depends, HTTPException
from starlette import status 

    
def get_serialized_users(users: List[AuthUser]) -> List[UsersListSchemaORM]:
    serialized_users = []
    for user in users:
        serialized_user = UsersListSchemaORM.from_orm(user)
        serialized_users.append(serialized_user)
    return serialized_users
        
    
def get_users_from_db():
    users = session.query(AuthUser).all()
    return get_serialized_users(users)
    
    
def update_user(login:str, data: UpdateUserModel):
    user = session.query(AuthUser).filter(AuthUser.login==login).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User has not been found'
        )
    for field, value in data.dict().items():
        setattr(user, field, value)
    
    session.add(user)
    session.commit()
    return user
    
    
def create_user(data: PrivateCreateUserSchema) -> PrivateCreateUserSchemaORM:
    user = AuthUser.create_user_with_all_parameters(data)
    return PrivateCreateUserSchemaORM.from_orm(user)
    
    
def get_user_by_id(id: int) -> PrivateDetailUserResponseModelORM:
    user = session.query(AuthUser).filter(AuthUser.id==id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User has not been found'
        )
    return PrivateDetailUserResponseModelORM.from_orm(user)


def update_user_by_id(id: int) -> PrivateDetailUserResponseModelORM:
    user = session.query(AuthUser).filter(AuthUser.id==id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User has not been found'
        )
    return PrivateDetailUserResponseModelORM.from_orm(user)


def delete_user_by_id(id: int) -> None:
    user = session.query(AuthUser).filter(AuthUser.id==id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User has not been found'
        ) 
    session.delete(user)
    session.commit()