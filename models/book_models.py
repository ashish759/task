from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str = None
    year_published: int = None
    summary: str = None

class ReviewCreate(BaseModel):
    user_id: int
    review_text: str
    rating: int