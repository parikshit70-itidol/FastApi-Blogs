from fastapi import Depends, APIRouter 
from sqlalchemy.orm import Session
from schemas import CommentWithReplies, UserDetails,CommentCreate
from database import get_db
import models
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

