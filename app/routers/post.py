from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import  get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import oauth2
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('', response_model=List[schemas.PostOut])
def get_posts(db : Session = Depends(get_db), limit :int = 10, skip:int = 0, search: Optional[str] = ""):
    
    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    results =( 
                db.query(
                    models.Posts, 
                    func.count(models.Votes.post_id).label("votes")
                )
                .join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True)
                .group_by(models.Posts.id)
                .filter(models.Posts.title.contains(search)).limit(limit).offset(skip)
                .all()
            )   

    results_with_votes = [
        {"post": post, "votes": votes} for post, votes in results
    ]

    return results_with_votes

#user specific posts
@router.get('/user', response_model=List[schemas.PostResponse])
def get_posts(db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Posts).filter(models.Posts.club_id == current_user.id).all()
    return posts



@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Posts(title=post.title, content=post.content, published=post.published)
    # to make it cleaner we use pydantic model
    usr_id = current_user.id
    role = current_user.role

    if role != 'club':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized For this Action")
    
    new_post = models.Posts(club_id = usr_id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
#title : string, content : String, category, bool published



#  get a single post
@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id:int, db : Session = Depends(get_db)):
    # post = db.query(models.Posts).filter(models.Posts.id == id).first()
    result =( 
                db.query(
                    models.Posts, 
                    func.count(models.Votes.post_id).label("votes")
                )
                .join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True)
                .group_by(models.Posts.id)
                .filter(models.Posts.id == id)
                .first()
            )   



    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id : {id} not found')
    
    post, votes = result

    return schemas.PostOut(
        post = schemas.PostResponse.from_orm(post),
        votes= votes
    )



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    role = current_user.role
    if role != 'club':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized For this Action")
    
    post_query = db.query(models.Posts).filter(models.Posts.id==id)
    
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exits")
    

    if post.club_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform Requested Action")

    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id : int, post: schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    role = current_user.role
    if role != 'club':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized For this Action")
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    update_post = post_query.first()

    # print(current_user.email)
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id= {id} not found")
    
    if update_post.club_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized Action")

    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()
    db.refresh(update_post)

    return update_post


# for user queries

