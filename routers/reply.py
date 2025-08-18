from fastapi import Depends, APIRouter ,HTTPException
from sqlalchemy.orm import Session
from schemas import CommentWithReplies, UserDetails,CommentCreate
from database import get_db
import models
from typing import List
from repository import reply
from oauth2 import get_current_user 

router = APIRouter(tags=['Replies']) 

@router.get("/reply/{comment_id}", response_model=CommentWithReplies)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
   return reply.get_reply(db,comment_id)   
    