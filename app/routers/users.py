from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import  get_db
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)  
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    #hash the password
    club_exits = db.query(models.User).filter(models.User.email == user.email).first()

    if club_exits:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= "User Already Exits")
    

    hash_pwd = utils.hash(user.password)
    user.password = hash_pwd
    new_user= models.User(role= 'user', **user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User with id: {id} does not exits')
    
    return user

@router.post('/club', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)  
def create_club(club: schemas.ClubCreate, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    #hash the password
    # print(current_user.role)
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Only Admin can Create Club")
    
    club_exits = db.query(models.Club).filter(models.Club.username == club.username).first()

    if club_exits:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= "Club Already Exits")
    
    hash_pwd = utils.hash(club.password)
    club.password = hash_pwd
    new_user= models.Club(role = 'club' ,**club.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 


@router.post('/admin', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)  
def create_admin(admin: schemas.ClubCreate, db : Session = Depends(get_db)):
    #hash the password
    club_exits = db.query(models.Admin).filter(models.Admin.username == admin.username).first()

    if club_exits:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= "Admin Already Exits")
    
    hash_pwd = utils.hash(admin.password)
    admin.password = hash_pwd
    new_user= models.Admin(role = 'admin' ,**admin.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 