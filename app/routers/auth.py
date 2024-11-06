from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from datetime import timedelta
from ..config import settings

router = APIRouter(
    tags = ["Authentication"]
)

REFRESH_TOKEN_EXPIRY  = settings.refresh_token_expiration

@router.post('/login', response_model=schemas.Token)
# def login(user_credentials : schemas.UserLogin, db: Session = Depends(get_db)):
def login(user_credentials : OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    # oauth 2 password request form is a dictionary
    # {
        # "username" : user.name
        # "password" : user.password
    # }

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        user = db.query(models.Club).filter(models.Club.email == user_credentials.username).first()
    
    if not user:
        user = db.query(models.Admin).filter(models.Admin.email == user_credentials.username).first()

    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # print(user.role)
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #create a jwt token 
    access_token = oauth2.create_access_token(
        data = {"user_id" : user.id, "user_email" : user.email, "role" : user.role}
    )

    # refresh token 
    refresh_token = oauth2.create_access_token(
        data={"user_id" : user.id, "user_email" : user.email, "role" : user.role},
        refresh = True,
        expiry= timedelta(days=REFRESH_TOKEN_EXPIRY)
    )
    # return a token
    return JSONResponse(
        content = {
            "message" : "Login Successfull",
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            "token_type" : "bearer"
        }
    )
    

    # return {"access_token" : access_token, "token_type" : "bearer"}
    
