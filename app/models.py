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
    image = Column(String, nullable = False)
    published = Column (Boolean, nullable = False, server_default = 'True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    club_id = Column(Integer, ForeignKey("club.id", ondelete="CASCADE"), nullable=False)
    club = relationship("Club")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable = False, primary_key = True) 
    email = Column(String, nullable =False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()')) 
    role = Column(String, nullable=False, server_default='user')

class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable= False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)

class Announcement(Base):
    __tablename__ = 'announcement'

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    description = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey("admin.id", ondelete="CASCADE"), nullable=False)
    admin = relationship("Admin")


class FeedBack(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key= True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    issue = Column(String, nullable=False)
    issue_to = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")


class Club(Base):
    __tablename__ = 'club'
    id = Column(Integer, nullable = False, primary_key = True) 
    email = Column(String, nullable =False, unique=True)
    username = Column(String, nullable = False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()')) 
    role = Column(String, nullable=False, server_default='club') 
 


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, nullable = False, primary_key = True) 
    email = Column(String, nullable =False, unique=True)
    username = Column(String, nullable = False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()')) 
    role = Column(String, nullable=False, server_default='admin') 