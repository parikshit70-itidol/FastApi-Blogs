from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas import BlogBase, BlogCreate, BlogWithCommentsAndReplies

from models import Blog, Comment
from sqlalchemy.orm import Session, joinedload
from database import get_db
from oauth2 import get_current_user

def get_all(db: Session):
    blogs = db.query(Blog).all()
    return blogs

def create(request: BlogCreate, db: Session, current_user: get_current_user):
    new_blog = Blog(title=request.title, description=request.description, username=current_user.name)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id: int, db: Session):
    blogs = db.query(Blog).filter(Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=404, detail="Blogs not Found")
    db.delete(blogs)
    db.commit()
    return {"message": 'Blogs Deleted'}

def update(id, blog: BlogCreate, db: Session):
    try:
        update_blog = db.query(Blog).filter(Blog.id == id)
        if not update_blog.first():
            raise HTTPException(status_code=404, detail="Blogs are not Updated")
        update_blog.update(blog.dict())
        db.commit()
        return {"message": "Updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update blog: {str(e)}"
        )

def get(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blogs not Found")

    # Load comments and replies with authors
    for comment in blog.comments:
        _ = comment.user  # author for comment
        for reply in comment.replies:
            _ = reply.user  # author for reply

    return BlogWithCommentsAndReplies.model_validate(blog) 
 
 