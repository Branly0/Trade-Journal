from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc
from uuid import uuid4

from app.db.session import get_db
from app.core.security import hash_password, verify_password, create_access_token, authenticate_user, create_refresh_token, refresh_access_token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.models.user import User, UserTypeEnum
from app.models.token import Token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check for existing email
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.password)

        new_user = User(
            id=uuid4(),
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            user_type=UserTypeEnum(user.user_type)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException:
        raise
    except exc.IntegrityError as e:
        db.rollback()
        if "email" in str(e):
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Registration failed")

# @router.post("/logingin")
# def login_user(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token(data={"sub": db_user.email})
#     return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    new_token = Token(
        user_id=user.id,
        token=refresh_token,
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        new_access_token = refresh_access_token(refresh_token)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout_user(refresh_token: str, db: Session = Depends(get_db)):
    token = db.query(Token).filter(Token.token == refresh_token).first()
    if token:
        token.is_revoked = True
        db.commit()
        return {"detail": "Successfully logged out"}
    else:
        raise HTTPException(status_code=400, detail="Invalid refresh token")