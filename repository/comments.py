from sqlalchemy.orm import Session
from schemas import CommentCreate
import models
from fastapi import HTTPException

def create_comment(request: CommentCreate, user_id: int, db: Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == request.blog_id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        new_comment = models.Comment(
            description=request.description,
            blog_id=request.blog_id,
            user_id=user_id,
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return {"message": "Comment created", "comment_id": new_comment.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create comment: {str(e)}")