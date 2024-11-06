from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import  get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    tags=['Announcement'],
    prefix="/announcement"
)

@router.get('', response_model = List[schemas.Announcement])
def get_announcement(db : Session= Depends(get_db)):
    results = db.query(models.Announcement).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Announcement Available")
    
    return results


@router.post('', response_model = schemas.Announcement, status_code=status.HTTP_201_CREATED)
def create_announcement(announcement: schemas.AnnouncementCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    role = current_user.role
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized For this Action")
    

    usr_id = current_user.id
    new_ann = models.Announcement(user_id = usr_id,**announcement.model_dump())
    try:
        db.add(new_ann)
        db.commit()
        db.refresh(new_ann)
    except Exception as e:
        db.rollback()  # Roll back the session in case of error
        raise HTTPException(status_code=500, detail="Failed to create announcement")

    return new_ann  

@router.put('/{id}', response_model=schemas.Announcement)
def update_announcement(id : int, announcement: schemas.AnnouncementCreate, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    
    role = current_user.role
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized For this Action")
    
    usr_id = current_user.id
    ann_query = db.query(models.Announcement).filter(models.Announcement.id == id)

    to_update = ann_query.first()

    if to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Announcement with id : {id} not Found')

    
    if to_update.user_id != usr_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized Action")

    ann_query.update(announcement.model_dump(),synchronize_session=False)
    # to_update.description = announcement.description
    db.commit()
    db.refresh(to_update)
    
    return to_update



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_announcement(id : int,  db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    role = current_user.role
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized For this Action")
    
    usr_id = current_user.id
    ann_query = db.query(models.Announcement).filter(models.Announcement.id == id)

    to_update = ann_query.first()

    if to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Announcement with id : {id} not Found')

    
    if to_update.user_id != usr_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized Action")

    # ann_query.update(announcement.model_dump(),synchronize_session=False)
    ann_query.delete(synchronize_session=False)
 
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
