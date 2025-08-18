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
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_dict = {
        "title": blog.title,
        "description": blog.description,
        "author": blog.author.name if blog.author else None,
        "comments": [
            {
                "description": c.description,
                "author": c.author.name if c.author else None,
                "replies": [
                    {
                        "id": r.id,
                        "description": r.description,
                        "author": r.author.name if r.author else None,
                    }
                    for r in c.replies if r.parent_id is not None and r.parent_id == c.id and r.blog_id == blog.id
                ]
            }
            for c in blog.comments if c.parent_id is None
        ]
    }

    return BlogWithCommentsAndReplies.model_validate(blog_dict)

 