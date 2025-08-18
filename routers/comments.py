from fastapi import Depends, APIRouter ,HTTPException
from sqlalchemy.orm import Session
from schemas import CommentWithReplies, UserDetails,CommentCreate
from database import get_db
import models
from typing import List
from repository import comments
from oauth2 import get_current_user 
router = APIRouter(tags=['Comments']) 

@router.post('/comments') 
def create_comments(
    request: CommentCreate,  
    db:Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return comments.create_comment(request, current_user.id, db)

@router.get('/comments/{blog_id}')
def get_comments(blog_id: int, db: Session = Depends(get_db)):
    comments_list = comments.get_comments(blog_id, db)
    print(comments_list)
    # return comments_list 