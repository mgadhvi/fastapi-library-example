from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from database import create_db_and_tables, get_db
import models, schemas

app = FastAPI(title="Library API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- Author Endpoints ---

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/authors/", response_model=List[schemas.AuthorWithBooks])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # joinedload for efficient relationship fetching
    stmt = select(models.Author).options(joinedload(models.Author.books)).offset(skip).limit(limit)
    authors = db.execute(stmt).unique().scalars().all()
    return authors

@app.get("/authors/{author_id}", response_model=schemas.AuthorWithBooks)
def read_author(author_id: int, db: Session = Depends(get_db)):
    stmt = select(models.Author).options(joinedload(models.Author.books)).where(models.Author.id == author_id)
    author = db.execute(stmt).unique().scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

# --- Book Endpoints ---

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Verify author exists
    author = db.get(models.Author, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
        
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Use joinedload to fetch author info in the same query
    stmt = select(models.Book).options(joinedload(models.Book.author)).offset(skip).limit(limit)
    books = db.execute(stmt).scalars().all()
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    stmt = select(models.Book).options(joinedload(models.Book.author)).where(models.Book.id == book_id)
    book = db.execute(stmt).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.patch("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    stmt = select(models.Book).where(models.Book.id == book_id)
    db_book = db.execute(stmt).scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"ok": True}
