from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Posts(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False )
    content = Column(String, nullable = False)
    published = Column (Boolean, nullable = False, server_default = 'True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable = False, primary_key = True) 
    email = Column(String, nullable =False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()')) 

class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable= False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)

class Announcement(Base):
    __tablename__ = 'announcement'

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    description = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)


class FeedBack(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key= True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    issue = Column(String, nullable=False)
    issue_to = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

 
    