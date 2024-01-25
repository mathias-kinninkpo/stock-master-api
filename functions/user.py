from sqlalchemy.orm import Session
from routes.auth import get_password_hash
from models.user import User
from fastapi import HTTPException, status
from schemas.user import UserCreate, User as UserResponse


def create_user(db: Session, username: str, password: str, full_name: str, email: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, password=hashed_password, full_name=full_name, email=email, role="user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None : 
        return None
    return UserResponse.from_orm(db_user)

def get_users(db: Session, skip: int = 0, limit: int = 10):
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.from_orm(user) for user in users]


def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return UserResponse.from_orm(db_user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return UserResponse.from_orm(db_user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
