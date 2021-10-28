from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from .. import models, utils
from ..database import get_db
from ..schemas import UserLogin
from .. import oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_info = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential."
        )

    if not utils.verify(user.password, user_info.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential."
        )

    # Create a token and return it
    access_token = oauth2.create_access_token(data={"user_id": user_info.id})
    return {"access_token": access_token, "token_type": "bearer"}
