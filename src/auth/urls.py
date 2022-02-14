from typing import Optional

from datetime import timedelta
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette import status
from starlette.responses import Response
from starlette.requests import Request
from .schemas import (
    LoginSchema, UsersListSchema, UpdateUserModel, UpdateUserResponseModelORM, PrivateCreateUserSchema
    )
from .auth_backend import (
    authenticate_user, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    register_user,
    get_full_user_info,
    check_user_permission
    )
from fastapi_pagination import Page, add_pagination, paginate
from .services import (
    get_users_from_db, update_user, create_user, get_user_by_id, delete_user_by_id, update_user_by_id
    )
from fastapi import HTTPException


router = APIRouter()


@router.post("/login")
async def route_login(data: LoginSchema):
    """Route for login user"""
    
    user = authenticate_user(data)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"login": user.login}, expires_delta=access_token_expires
    )
    response = Response()
    response.set_cookie(
            "Authorization",
            value=f"Bearer {access_token}",
            httponly=True
        )
    return response


@router.post('/register')
def route_register(response: Response, data: LoginSchema):
    """Route for register users"""
    
    user = register_user(data)
    if user:
        response.status_code = status.HTTP_200_OK
        return {"login": user.login}
    response.status_code = status.HTTP_403_FORBIDDEN
    return {"message": "user with such login already exists"}


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = Response('You have been successfully logged out')
    response.delete_cookie("Authorization")
    return response


@router.get("/users/current/")
async def read_users_me(response: Response, request: Request,  current_user: LoginSchema = Depends(get_current_user)):
    user = get_full_user_info(current_user.login)
    if user:
        response.status_code = status.HTTP_200_OK
        return user
    response.status_code = status.HTTP_400_BAD_REQUEST


@router.get('/users', response_model=Page[UsersListSchema])
def route_get_users(response: Response, current_user: LoginSchema = Depends(get_current_user)):
    users = get_users_from_db()
    response.status_code = status.HTTP_200_OK
    return paginate(users)
    

@router.patch('/users')
def route_update_user(data: UpdateUserModel, response: Response, current_user: LoginSchema = Depends(get_current_user)):
    try:
        user = update_user(current_user.login, data)
    except HTTPException as e:
        response.status_code = e.status_code
        return e.detail
    return UpdateUserResponseModelORM.from_orm(user)


@router.get('/private/users', response_model=Page[UsersListSchema])
def private_route_users(response: Response, current_user: LoginSchema = Depends(get_current_user)):
    is_admin = check_user_permission(current_user)
    if is_admin:
        users = get_users_from_db()
        response.status_code = status.HTTP_200_OK
        return paginate(users)
    response.status_code = status.HTTP_403_FORBIDDEN
    return 'Only for private users'


@router.post('/private/users')
def private_route_create_user(response: Response, data: PrivateCreateUserSchema, current_user: LoginSchema = Depends(get_current_user)):
    is_admin = check_user_permission(current_user)
    if is_admin:
        user = create_user(data)
        response.status_code = status.HTTP_201_CREATED
        return user
    response.status_code = status.HTTP_403_FORBIDDEN
    return 'Only for private users'


@router.get('/private/users/{id}')
def private_route_get_user(id: int, response: Response, current_user: LoginSchema = Depends(get_current_user)):
    is_admin = check_user_permission(current_user)
    if is_admin:
        try:
            user = get_user_by_id(id)
            return user
        except HTTPException as e:
            response.status_code = e.status_code
            return e.detail
    response.status_code = status.HTTP_403_FORBIDDEN
    return 'Only for private users'  


@router.delete('/private/users/{id}')
def private_route_delete_user(id: int, response: Response, current_user: LoginSchema = Depends(get_current_user)):
    is_admin = check_user_permission(current_user)
    if is_admin:
        try:
            delete_user_by_id(id)
            return 'Successfully deleted'
        except HTTPException as e:
            response.status_code = e.status_code
            return e.detail
    response.status_code = status.HTTP_403_FORBIDDEN
    return 'Only for private users' 


@router.patch('/private/users/{id}')
def private_route_update_user(id: int, response: Response, current_user: LoginSchema = Depends(get_current_user)):
    is_admin = check_user_permission(current_user)
    if is_admin:
        try:
            user = update_user_by_id(id)
            return user
        except HTTPException as e:
            response.status_code = e.status_code
            return e.detail
    response.status_code = status.HTTP_403_FORBIDDEN
    return 'Only for private users' 
    

add_pagination(router)

