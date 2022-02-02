from typing import Optional

from datetime import datetime, timedelta
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, Response, JSONResponse
from starlette.requests import Request
from .schemas import LoginSchema, User, TokenData
from .auth_backend import (
    authenticate_user, 
    fake_users_db, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    register_user,
    )


router = APIRouter()


@router.post("/login")
# @router.post("/register", response_model=Token)
async def route_login(form_data: LoginSchema):
    user = authenticate_user(form_data.login, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    response = Response('You have been successfully registered')
    response.set_cookie(
            "Authorization",
            value=f"Bearer {access_token}",
            httponly=True
        )
    return response

@router.post('/register')
def route_register(form_data: LoginSchema):
    data = form_data.dict()

    user = register_user(**data)
    print(user.login)
    return TokenData(login=user.login).json()


# @router.post("/register", response_model=Token)
# async def route_register(form_data: LoginSchema):
#     user = authenticate_user(fake_users_db, form_data.login, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect login or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.login}, expires_delta=access_token_expires
#     )
#     # return {"access_token": access_token, "token_type": "bearer"}
#     response = Response('Hello')
#     response.set_cookie(
#             "Authorization",
#             value=f"Bearer {access_token}",
#             # domain="localtest.me",
#             httponly=True,
#             # max_age=1800,
#             # expires=1800,
#         )
#     return response


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain="localtest.me")
    return response


@router.get("/users/me/")
# @router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# @router.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.login}]

