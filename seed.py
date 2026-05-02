import argparse
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine, create_db_and_tables
from models import Book, Author, Base

def drop_tables():
    print("Dropping tables...")
    Base.metadata.drop_all(engine)

def seed_data(reset: bool = False):
    if reset:
        drop_tables()
    
    # Ensure tables exist
    create_db_and_tables()
    
    with Session(engine) as session:
        # Create Authors
        authors_data = [
            {"name": "F. Scott Fitzgerald", "bio": "American novelist and short story writer."},
            {"name": "George Orwell", "bio": "English novelist, essayist, and critic."},
            {"name": "J.R.R. Tolkien", "bio": "English writer, poet, and philologist."},
            {"name": "Harper Lee", "bio": "American novelist best known for To Kill a Mockingbird."},
            {"name": "Aldous Huxley", "bio": "English writer and philosopher."}
        ]
        
        author_map = {}
        for a_data in authors_data:
            stmt = select(Author).where(Author.name == a_data["name"])
            author = session.execute(stmt).scalar_one_or_none()
            if not author:
                author = Author(**a_data)
                session.add(author)
                session.flush() # Get ID
                print(f"Added author: {author.name}")
            author_map[author.name] = author.id

        # Create Books linked to Authors
        books_data = [
            {"title": "The Great Gatsby", "isbn": "9780743273565", "published_year": 1925, "author_name": "F. Scott Fitzgerald"},
            {"title": "1984", "isbn": "9780451524935", "published_year": 1949, "author_name": "George Orwell"},
            {"title": "The Hobbit", "isbn": "9780547928227", "published_year": 1937, "author_name": "J.R.R. Tolkien"},
            {"title": "To Kill a Mockingbird", "isbn": "9780061120084", "published_year": 1960, "author_name": "Harper Lee"},
            {"title": "Brave New World", "isbn": "9780060850524", "published_year": 1932, "author_name": "Aldous Huxley"}
        ]

        for b_data in books_data:
            stmt = select(Book).where(Book.isbn == b_data["isbn"])
            book = session.execute(stmt).scalar_one_or_none()
            if not book:
                author_id = author_map[b_data.pop("author_name")]
                book = Book(**b_data, author_id=author_id)
                session.add(book)
                print(f"Added book: {book.title}")
        
        session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database.")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate tables.")
    args = parser.parse_args()
    seed_data(reset=args.reset)
