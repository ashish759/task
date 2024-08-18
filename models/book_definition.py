from . import db  # Import the db instance from __init__.py
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    year_published = db.Column(db.Integer)
    summary = db.Column(db.Text)
    reviews = relationship("Review", backref="book", cascade="all, delete-orphan")

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer)    
