from fastapi import FastAPI
import models 
from database import engine
from routers import blog,user,authentication,comments
app = FastAPI() 

models.Base.metadata.create_all(engine) 
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(comments.router)
# def get_db():
#     db =  SessionLocal()
#     try:
#         yield db 
#     finally:
#         db.close()









