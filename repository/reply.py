from sqlalchemy.orm import Session
from schemas import CommentCreate,CommentWithReplies
import models
from fastapi import HTTPException 


# utils/reply.py
def get_reply(db, comment_id: int):
    try:
        # Fetch all comments once 
        comments = db.query(models.Comment).all()

        if not comments:
            raise HTTPException(status_code=404, detail="No comments found")

        # Build dictionary: parent_id -> {child_id: child_object}
        db_data = {}
        for c in comments:
            if c.parent_id not in db_data:
                db_data[c.parent_id] = {}
            # unique key per child = its id
            db_data[c.parent_id][c.id] = c

        # Find the root comment
        root = next((c for c in comments if c.id == comment_id), None)
        if not root:
            raise HTTPException(status_code=404, detail="Comment not found")

        # Recursive function using db_data only
        def get_reply_utils(parent_id: int):
            children = db_data.get(parent_id, {})
            if not children:
                return []
            replies = []
            for rep in children.values():  # values() ensures no duplicate keys
                replies.append({
                    "id": rep.id,
                    "description": rep.description,
                    "author": rep.author.name if rep.author else None,
                    "replies": get_reply_utils(rep.id)  # recursion
                })
            return replies

        # Start recursion from this comment id
        return [{
            "id": root.id,
            "description": root.description,
            "author": root.author.name if root.author else None,
            "replies": get_reply_utils(root.id)
        }]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve replies: {str(e)}")

