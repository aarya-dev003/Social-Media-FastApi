from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import  get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import oauth2
from sqlalchemy import func


router = APIRouter(
    prefix='/feedback',
    tags=[
        'Feedback'
    ]
)


@router.post('', status_code= status.HTTP_201_CREATED, response_model= schemas.FeedBackOut)
def create_feedback(feedback : schemas.Feedback, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    usr_id = current_user.id
    new_feedback = models.FeedBack(user_id = usr_id, **feedback.model_dump()) 
    db.add(new_feedback)
    db.commit()

    db.refresh(new_feedback)

    return new_feedback


@router.get('', response_model= List[schemas.FeedBackOut])
def get_feedback_admin(db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    usr_id = current_user.id

    feedback = db.query(models.FeedBack).filter(models.FeedBack.issue_to == 'admin').all()

    if feedback == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No FeedBack Yet")
    # here define role


    return feedback




@router.get('/club', response_model= List[schemas.FeedBackOut])
def get_feedback_club(db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    usr_id = current_user.id

    feedback = db.query(models.FeedBack).filter(models.FeedBack.issue_to == 'club').all()

    if feedback == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No FeedBack Yet")
    # here define role


    return feedback