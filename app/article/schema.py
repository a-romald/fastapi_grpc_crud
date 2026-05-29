from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Base Model: Common attributes
class ArticleBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=3, max_length=250)
    published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        model_config = ConfigDict(from_attributes=True)


# Create Model: Attributes required for creation
class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=3, max_length=250)
    published: bool = Field(...)


# Update Model: All fields optional for partial updates
class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=50)
    content: Optional[str] = Field(default=None, min_length=3, max_length=250)
    published: Optional[bool] = Field(default=None)


# Response Model: Attributes returned to the client
class Article(ArticleBase):
    id: int    
