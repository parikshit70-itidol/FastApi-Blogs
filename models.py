from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from sqlalchemy.orm import relationship, backref

class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    username = Column(String, ForeignKey('user.name'))
    comments = relationship("Comment", back_populates="blog")
    author = relationship("User", back_populates="blogs")
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    comments = relationship("Comment", back_populates="author")
    blogs = relationship("Blog", back_populates="author")
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    blog_id = Column(Integer, ForeignKey('blog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    author = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    

    
    