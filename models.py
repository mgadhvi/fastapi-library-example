from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    bio = Column(Text, nullable=True)

    # Relationship to books
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    published_year = Column(Integer, nullable=True)
    
    # Foreign key to author
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    
    # Relationship to author
    author = relationship("Author", back_populates="books")
