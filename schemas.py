from pydantic import BaseModel
from typing import List, Optional

class UserOut(BaseModel):
    name: str
    class Config:
        from_attributes = True

class ReplyOut(BaseModel):
    id: int
    description: str
    author: UserOut
    class Config:
        from_attributes = True
class CommentCreate(BaseModel):
    description: str
    blog_id: int

    class Config:
        from_attributes = True
class CommentWithReplies(BaseModel):
    id: int
    description: str
    author: UserOut
    replies: List[ReplyOut] = []
    class Config:
        from_attributes = True

class BlogBase(BaseModel):
    title: str
    description: str

class BlogCreate(BlogBase):
    pass

class BlogDetails(BlogBase):
    class Config:
        from_attributes = True

class BlogWithCommentsAndReplies(BlogDetails):
    author: UserOut
    comments: List[CommentWithReplies] = []
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    class Config:
        from_attributes = True

class UserDetails(BaseModel):
    name: str
    email: str
    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None