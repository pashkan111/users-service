from db.db import Base
import sqlalchemy as sa
from db.db import session
from .schemas import LoginSchema, PrivateCreateUserSchema


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = sa.Column(sa.Integer(), primary_key=True)
    login = sa.Column(sa.String(50), unique=True, index=True)
    password = sa.Column(sa.String(100))
    first_name = sa.Column(sa.String(50), nullable=True)
    last_name = sa.Column(sa.String(50), nullable=True)
    other_name = sa.Column(sa.String(50), nullable=True)
    email = sa.Column(sa.String(50), nullable=True)
    phone = sa.Column(sa.String(12), nullable=True)
    birthday = sa.Column(sa.Date, nullable=True)
    is_admin = sa.Column(sa.Boolean(), default=False)
    

    @classmethod
    def create_user(cls, data: LoginSchema):
        user = cls(login=data.login, password=data.password)
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def find_user(cls, login: str):
        user = session.query(cls).filter(cls.login==login).first()
        return user
    
    @classmethod
    def create_user_with_all_parameters(cls, data: PrivateCreateUserSchema):
        user = cls(**data.dict())
        session.add(user)
        session.commit()
        return user
