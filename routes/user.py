# routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from functions.user import create_user, get_users, get_user, update_user, delete_user, password_forgot, password_forgot_verify
from schemas.user import UserCreate, LoginDataForm,  User as UserResponse
from .auth import get_current_user, get_db, verify_password, create_access_token


user_router = APIRouter(prefix="", tags=["Les actions sur les utilisateurs"]) # dependencies=[Depends(get_current_user)])


"""register_user - register a user

    Raises:
        HTTPException: if email is already exist
        
    Returns:
        dict: message of success
    """
@user_router.post("/register", response_model=dict)
def register_user(user : UserCreate,  db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already registered")
    user = create_user(db, username=user.username, password=user.password, full_name=user.full_name, email=user.email)
    if user:
        access_token = create_access_token(data={"sub": user.email})
        return {
            "message": "User registered successfully",
            "access_token": access_token, "token_type": "bearer"
        }
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured when creating user")


"""login_user

Raises:
    HTTPException: if user does not exist

Returns:
    dict: message if success
"""

@user_router.post("/login", response_model=dict)
def login_user(data : LoginDataForm, db: Session = Depends(get_db)):
    user = get_user(db, email=data.email)
    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



@user_router.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@user_router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return user
    

@user_router.put("/users/{user_id}", response_model=UserResponse)
def update(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)

@user_router.delete("/users/{user_id}", response_model=UserResponse)
def delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)




@user_router.post("/password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    user = password_forgot(db, email)
    _result = {'code': user.code}
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return  {
        "message" : "Email sent successfully",
        "code" :  _result
    }


@user_router.post("/password/verify")
async def verify_forgot_password(email: str, code: str, db: Session = Depends(get_db)):
    user = password_forgot_verify(db, email, code)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return   {
        "message" : "Email sent successfully",
        "user" :  user
    }


