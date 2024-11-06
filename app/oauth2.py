from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
# import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET key
#Algo
#Expiration token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiration


#  Jose library used
def create_access_token(data: dict,refresh : bool = False, expiry : timedelta = None):
    payload = {}
    expire = datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload['user'] = data
    # payload['user_id'] = data['user_id']
    payload['exp']= expire.timestamp()
    payload['refresh'] = refresh


    jwt_token = jwt.encode(
        claims = payload, 
        key = SECRET_KEY, 
        algorithm=ALGORITHM
    )

    return jwt_token


# def create_access_token(data: dict):
#     payload = {}
#     expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     payload['user'] = data
#     payload['exp']= expire

#     # to_encode = data.copy()

#     # to_encode.update({'exp' : expire})

#     jwt_token = jwt.encode(
#         claims = payload, 
#         key = SECRET_KEY, 
#         algorithm=ALGORITHM
#     )

#     return jwt_token
 

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user : dict = payload.get("user")
        # id: str = str(payload.get("user_id"))
        id: str = str(user['user_id'])
        role : str = str(user['role'])
        
        

        if id is None:
            raise credential_exception

        # token_data = schemas.TokenData(id=user.user_id)
        token_data = schemas.TokenData(id=id, role=role)
    except JWTError:
        raise credential_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could Not Validate Credentials', headers={'WWW-Authenticate': "Bearer"})

    token = verify_access_token(token, credential_exception) 
    role = token.role
    

    if role == 'club':
        user = db.query(models.Club).filter(models.Club.id == token.id, models.Club.role == role).first()
    elif role == 'admin':
        user = db.query(models.Admin).filter(models.Admin.id == token.id, models.Admin.role == role).first()
    else:
        user = db.query(models.User).filter(models.User.id == token.id, models.User.role == role).first()
    
    if not user:
        raise credential_exception


    return user  