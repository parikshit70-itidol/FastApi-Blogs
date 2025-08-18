from fastapi import APIRouter,Depends,HTTPException
from typing import List
from schemas import UserCreate,UserDetails
import models 
from sqlalchemy.orm import Session,joinedload
from database import get_db
from hashing import Hash 




def create(request:UserCreate,db:Session):
    try:
        new_user = models.User(name = request.name, email = request.email,password = Hash.bcrypt(request.password))  
        db.add(new_user) 
        db.commit()
        db.refresh(new_user) 
        return new_user 
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Data has not been stored:{str(e)}")  
    
def get(id:int,db:Session): 
    try: 
        get_user = db.query(models.User).filter(models.User.id == id).first() 
        if not get_user:
            raise HTTPException(status_code=404,detail="Users not found") 
        return get_user 
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Unable to Connect to Database: {str(e)}") 
