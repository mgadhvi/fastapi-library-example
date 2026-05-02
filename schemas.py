from pydantic import BaseModel
from typing import Optional, List

# Author Schemas
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None

class Author(AuthorBase):
    id: int
    
    class Config:
        from_attributes = True

# Book Schemas
class BookBase(BaseModel):
    title: str
    isbn: str
    description: Optional[str] = None
    published_year: Optional[int] = None

class BookCreate(BookBase):
    author_id: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    published_year: Optional[int] = None
    author_id: Optional[int] = None

class Book(BookBase):
    id: int
    author_id: int
    author: Author  # Nested author details

    class Config:
        from_attributes = True

# Schema for Author with their books
class AuthorWithBooks(Author):
    books: List[BookBase] = []
