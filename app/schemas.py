#pydantic classes
# pydantic is used to validate the data passed in post request similar to kotlin data class
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from pydantic.types import conint
from typing import Optional, Annotated, Literal


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    email: EmailStr
    id : int
    created_at : datetime

    class Config:
        # orm_mode = True
        from_attributes = True
        

class PostResponse(PostBase):
    id: int
    created_at : datetime
    user_id : int
    user: UserResponse

    class Config:
        # orm_mode = True
        from_attributes = True
        
    

class PostOut(BaseModel):
    post : PostResponse
    votes : int

    class Config:
        # orm_mode = True
        from_attributes = True



class UserCreate(BaseModel):
    email: EmailStr
    password : str




class UserLogin(BaseModel):
    email : EmailStr
    password : str

    class Config:
        orm_mode = True
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id : int
    # dir: Annotated[int, conint(le=1)]
    dir: Literal[0, 1] 

class AnnouncementCreate(BaseModel):
    description : str
    class Config:
        from_attributes =True

class Announcement(AnnouncementCreate):
    id : int
    created_at : datetime
    user_id : int
    # user : UserResponse

    class Config:
        from_attributes = True


class Feedback(BaseModel):
    issue : str
    issue_to : str
    class Config : 
        from_attributes = True

class FeedBackOut(Feedback):
    id : int
    user_id : int
    user : UserResponse
    created_at : datetime

    class Config : 
        from_attributes = True