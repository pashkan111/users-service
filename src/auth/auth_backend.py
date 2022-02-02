from typing import Optional
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request
from .schemas import LoginSchema, TokenData, UserInDB
# from configs import (
#     SECRET_KEY,
#     ALGORITHM,
#     ACCESS_TOKEN_EXPIRE_MINUTES
# )

SECRET_KEY='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30

fake_users_db = {
    "johndoe": {
        "login": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": '123',
        "disabled": False,
    }
}


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str = '/token',
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        cookie_authorization: str = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )
        print(cookie_scheme, cookie_param)

        if cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param
        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return True if plain_password == hashed_password else False
    # return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(OAuth2PasswordBearerCookie())):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)
    except PyJWTError:
        raise credentials_exception
    user = get_user(fake_users_db, login=token_data.login)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(login: str):
    if login in fake_users_db:
        user_dict = fake_users_db[login]
        return LoginSchema(**user_dict)


def authenticate_user(login: str, password: str):
    "Checks if user exists in db"
    user = get_user(login)
    if not user:
        return False
    if not verify_password(password, user.password):
    # if not verify_password(password, user.hashed_password):
        return False
    return user


def register_user(login: str, password: str):
    user = authenticate_user(login, password)
    if user:
        return user
    fake_users_db[login] = {'login': login, 'password': password}
    return get_user(login) 