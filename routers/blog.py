from fastapi import APIRouter,Depends,HTTPException
from typing import List
from schemas import BlogBase,UserDetails,BlogDetails,BlogWithCommentsAndReplies 
import models 
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user 
from repository import blog
router = APIRouter(tags=['Blogs']) 


@router.get('/blogs', response_model = List[BlogDetails])
def all(db:Session = Depends(get_db), current_user:UserDetails = Depends(get_current_user)):
    return blog.get_all(db)

@router.post('/blog/') 
def create_blog(request: BlogBase, db:Session = Depends(get_db),current_user:UserDetails = Depends(get_current_user) ):
    return blog.create(request, db,current_user)


@router.get('/blog/{blog_id}', response_model= BlogWithCommentsAndReplies) 
def get_blog(id:int,db:Session= Depends(get_db)):
    return blog.get(id,db)


@router.delete('/blogs/{id}')
def delete_blog(id,db:Session = Depends(get_db)):
    return blog.delete(id,db)

@router.put('/blogs/{id}') 
def update_blogs(id,db:Session = Depends(get_db)):
    return blog.update()