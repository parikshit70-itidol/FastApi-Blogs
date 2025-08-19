from pydantic import BaseModel,Field
from typing import List, Optional

class UserOut(BaseModel):
    name: str

    class Config:
        from_attributes = True





class CommentCreate(BaseModel):
    description: str
    blog_id: int
    parent_id: Optional[int] = None
    class Config:
        from_attributes = True


class CommentWithReplies(BaseModel):
    id: int
    description: str
    author: Optional[str] = None
    replies: List["CommentWithReplies"] = Field(default_factory=list)  # self-referencing

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class BlogBase(BaseModel):
    title: str
    description: str


class BlogCreate(BlogBase):
    pass


class BlogDetails(BlogBase):
    class Config:
        from_attributes = True


class BlogWithCommentsAndReplies(BlogDetails):
    author: str   
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


CommentWithReplies.model_rebuild()