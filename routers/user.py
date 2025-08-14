from fastapi import APIRouter,Depends,HTTPException
from typing import List
from schemas import UserCreate,UserDetails
import models 
from sqlalchemy.orm import Session,joinedload
from database import get_db
from hashing import Hash 
from repository import user
router = APIRouter(tags=['User']) 

@router.post('/user') 
def create_user(request:UserCreate, db:Session = Depends(get_db)):
        return user.create(request,db) 

@router.get('/user/{id}',response_model = UserDetails) 
def get_user(id:int,db:Session = Depends(get_db)): 
    return user.get(id,db)
    
    