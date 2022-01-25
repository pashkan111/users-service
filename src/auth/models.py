from db.db import Base
import sqlalchemy as sa


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = sa.Column(sa.Integer(), primary_key=True)
    login = sa.Column(sa.String(50), unique=True, index=True)
    password = sa.Column(sa.String(50))