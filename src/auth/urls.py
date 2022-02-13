from typing import Optional

from datetime import datetime, timedelta
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from starlette.responses import RedirectResponse, Response, JSONResponse
from starlette.requests import Request
from .schemas import (
    LoginSchema, UserSchema, UsersListSchema
    )
from .auth_backend import (
    authenticate_user, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    register_user,
    get_full_user_info
    )
from fastapi_pagination import Page, add_pagination, paginate
from .services import get_users_from_db


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
def route_register(data: LoginSchema):
    """Route for register users"""
    
    user = register_user(data)
    if user:
        return {"login": user.login}
    return {"message": "user with such login already exists"}


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = Response('You have been successfully logged out')
    response.delete_cookie("Authorization")
    return response


@router.get("/users/current/")
async def read_users_me(response: Response, request: Request,  current_user: UserSchema = Depends(get_current_user)):
    user = get_full_user_info(current_user.login)
    if user:
        response.status_code = status.HTTP_200_OK
        return user
    response.status_code = status.HTTP_400_BAD_REQUEST


@router.get('/users', response_model=Page[UsersListSchema])
def route_get_users(response: Response, current_user: UserSchema = Depends(get_current_user)):
    users = get_users_from_db()
    response.status_code = status.HTTP_200_OK
    return paginate(users)
    
    
add_pagination(router)

