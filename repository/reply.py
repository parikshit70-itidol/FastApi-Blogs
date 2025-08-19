from sqlalchemy.orm import Session
from schemas import CommentCreate,CommentWithReplies
import models
from fastapi import HTTPException 



# utils/reply.py
def get_reply(db: Session, comment_id: int):
    try:
        comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        def get_reply_utils(parent_id: int):
            replie = db.query(models.Comment).filter(models.Comment.parent_id == parent_id).all()
            print(f"Replies for comment_id {parent_id}: {replie}")
            if not replie:
                return []
            replies = []
            for rep in replie:
                replies.append({
                    "id": rep.id,
                    "description": rep.description,
                    "author": rep.author.name if rep.author else None,
                    "replies": get_reply_utils(rep.id)  # Recursive
                })
            return replies

        # include parent + recursive children
        return  get_reply_utils(comment.id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve replies: {str(e)}")
