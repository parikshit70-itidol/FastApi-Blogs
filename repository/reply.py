from sqlalchemy.orm import Session
from schemas import CommentCreate,CommentWithReplies
import models
from fastapi import HTTPException 


def get_reply(db: Session, comment_id: int):
    try:
        replies = db.query(models.Comment).filter(models.Comment.parent_id == comment_id).all()
        if not replies:
            raise HTTPException(status_code=404, detail="Comment not found")
        result = []
        for reply in replies:
            result.append(CommentWithReplies(
                description=reply.description,
                author=reply.user.name if reply.user else None  # only name instead of whole object
            ))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve replies: {str(e)}")