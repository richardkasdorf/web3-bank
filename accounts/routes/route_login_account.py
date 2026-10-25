import os
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from accounts.models import User
from accounts.auth_model import create_access_token, verify_password


router = APIRouter(tags=["Authentication"])

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax").lower()

if COOKIE_SAMESITE == "none" and not COOKIE_SECURE:
    raise RuntimeError("SameSite=None exige Secure=True")

@router.post("/token")
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    try:
        account_id = int(form_data.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account number must be numeric"
        )

    user = db.query(User).filter(User.id == account_id).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect account number or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

#    IS_PRODUCTION = os.getenv("ENV") == "production" 
    # Token | Security
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=1800,
        path="/"
    )

    return {"message": "LogIn Successfully"}



@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        httponly=True,
    )
    return {"message": "Logged out"}

