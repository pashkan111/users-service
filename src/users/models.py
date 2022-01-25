from db.db import Base
import sqlalchemy as sa


class Users(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer(), primary_key=True)
    first_name = sa.Column(sa.String(50))
    last_name = sa.Column(sa.String(50))
    other_name = sa.Column(sa.String(50))
    email = sa.Column(sa.String(50))
    phone = sa.Column(sa.String(12))
    birthday = sa.Column(sa.DateTime(timezone=True))
    is_admin = sa.Column(sa.Boolean(), default=False)
    