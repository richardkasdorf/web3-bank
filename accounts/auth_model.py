from pwdlib import PasswordHash
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import JWTError, jwt
from accounts.models import User
from fastapi import Cookie, Depends, HTTPException, status
from db.database import get_db
from sqlalchemy.orm import Session


password_hasher = PasswordHash.recommended()

## Generate HASH ---------
def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 90))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if access_token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if user is None:
        raise credentials_exception
    
    return user 




