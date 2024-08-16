from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Import the models to register them with the SQLAlchemy instance
from .book_definition import Book, Review