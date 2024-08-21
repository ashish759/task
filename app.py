from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List
from sqlalchemy import update, delete, func
from models.book_definition import Book, Review, Base  # Ensure models are imported correctly
from models.book_models import BookCreate, ReviewCreate

# JWT settings


# Database configuration
DATABASE_URL = "postgresql+asyncpg://postgres:Ashi%4012345678@localhost:5432/postgres"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# FastAPI app
app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)



# Dependency to get the session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# Event to create tables at startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/books", response_model=list[BookCreate])
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    return books

@app.post("/books", response_model=BookCreate, status_code=201)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    new_book = Book(**book.dict())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book

@app.get("/books/{id}", response_model=BookCreate)
async def get_book(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{id}", response_model=BookCreate)
async def update_book(id: int, book: BookCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == id))
    existing_book = result.scalars().first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book.dict().items():
        setattr(existing_book, key, value)
    
    session.add(existing_book)
    await session.commit()
    await session.refresh(existing_book)
    return existing_book

@app.delete("/books/{id}", status_code=204)
async def delete_book(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await session.execute(delete(Book).where(Book.id == id))
    await session.commit()
    return {"message": "Book deleted successfully"}

@app.post("/books/{id}/reviews", response_model=ReviewCreate, status_code=201)
async def add_review(id: int, review: ReviewCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    new_review = Review(book_id=id, **review.dict())
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review

@app.get("/books/{id}/reviews", response_model=List[ReviewCreate])
async def get_reviews(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Review).where(Review.book_id == id))
    reviews = result.scalars().all()
    return reviews

@app.get("/books/{id}/summary")
async def get_summary(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews = await session.execute(select(Review).where(Review.book_id == id))
    reviews = reviews.scalars().all()
    
    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / len(reviews) if reviews else None

    return {
        "title": book.title,
        "author": book.author,
        "summary": book.summary,
        "average_rating": average_rating,
        "reviews_count": len(reviews)
    }

@app.get("/")
async def hello():
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
