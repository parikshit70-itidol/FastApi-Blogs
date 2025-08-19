from sqlalchemy.orm import Session,joinedload
from schemas import CommentCreate,CommentWithReplies
import models
from fastapi import HTTPException

def create_comment(request: CommentCreate, user_id: int, db: Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == request.blog_id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        parent_id = request.parent_id if request.parent_id else None
        
        print(f"Creating comment for blog_id: {request.blog_id}, parent_id: {parent_id}")
        
        new_comment = models.Comment(
            description=request.description,
            blog_id=request.blog_id,
            user_id=user_id,
            parent_id=parent_id,
            is_reply= True if parent_id else False
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return {"message": "Comment created", "comment_id": new_comment.id,"parent_id": new_comment.parent_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create comment: {str(e)}") 
    
# def get_comments(id: int, db: Session):
#     try:
#         comments = db.query(models.Comment).join( models.Comment.user_id == models.User.id).join(models.Blog, models.Comment.blog_id == models.Blog.id).options(
#                 joinedload(models.Comment.author),  # load User
#                 joinedload(models.Comment.blog)     # load Blog
#             ).filter(models.Comment.blog_id == id,  models.Comment.is_reply == False).all()
        
#         if not comments:
#             raise HTTPException(status_code=404, detail="No comments found for this blog")
        
#         return comments
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to retrieve comments: {str(e)}") 
    
def get(id: int, db: Session):
    try:
        comment = db.query(models.Comment).filter(models.Comment.id == id).all()

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        return {
            "id": comment.id,
            "description": comment.description,
            "author": comment.author.name if comment.author else None,
            "replies": [
                {
                    "id": r.id,
                    "description": r.description,
                    "author": r.author.name if r.author else None,
                }
                for r in (comment.replies or [])   # ✅ Safe even if None
                if r.parent_id == comment.id
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve comment: {str(e)}")
