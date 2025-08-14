from fastapi import APIRouter,Depends,HTTPException,status
import schemas
import models
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash 
from datetime import datetime, timedelta, timezone
from jwt_token import create_access_token 
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'],prefix="/authenticate")  


@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    try:
        user =  db.query(models.User).filter(models.User.email == request.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Invalid Credentials") 
        if not Hash.verify(user.password,request.password):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Invalid Password")
    
        access_token = create_access_token(data={"sub": request.username})
        return {"access_token":access_token, "token_type":"bearer"}    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Internal Server Error: {str(e)}") 
    
    