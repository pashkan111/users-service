from db.db import session
from .models import AuthUser
from .schemas import UsersListSchemaORM
from typing import List

    
def get_serialized_users(users: List[AuthUser]) -> List[UsersListSchemaORM]:
    serialized_users = []
    for user in users:
        serialized_user = UsersListSchemaORM.from_orm(user)
        serialized_users.append(serialized_user)
    return serialized_users
        
    
def get_users_from_db():
    users = session.query(AuthUser).all()
    return get_serialized_users(users)
    
    
    