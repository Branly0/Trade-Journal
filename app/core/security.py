### --------------password hashing and verification utilities using argon2
from passlib import context as passlib_context

pwd_context = passlib_context.CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using Argon2."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using Argon2."""
    return pwd_context.verify(plain_password, hashed_password)

### --------------JWT token generation and verification utilities using PyJWT

from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

"""the env virable for security settings are now in app/core/config.py, so we import them from there"""
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"type": "access", "exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"type": "refresh", "exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        email: str = payload.get("sub")

        #for the refresh check, we can also verify if the token exists in the database and is valid (not revoked)
        from app.db.session import SessionLocal
        from app.models.token import Token
        db = SessionLocal()
        token = db.query(Token).filter(Token.token == refresh_token).first()

        if token.is_revoked:
            raise ValueError("Token has been revoked, you are logged out")

        if email is None:
            raise ValueError("Invalid token")
        return create_access_token(data={"sub": email})
    except jwt.JWTError:
        raise ValueError("Invalid token")

def authenticate_user(email: str, password: str):
    """Authenticate user by email and password."""
    from app.db.session import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    if not user or not verify_password(password, user.hashed_password):
        return None
    return user