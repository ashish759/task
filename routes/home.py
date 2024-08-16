# routes/book_routes.py

from flask_restx import Namespace, Resource
from models.book_definition import Book, Review, db
from models.book_models import book_model, review_model
 

api = Namespace('books', description='Books operations')

@api.route('/books')
class BookList(Resource):
    @api.marshal_list_with(book_model)
    def get(self):
        '''List all books'''
        return Book.query.all()

    @api.expect(book_model)
    @api.marshal_with(book_model, code=201)
    def post(self):
        '''Create a new book'''
        data = api.payload
        new_book = Book(
            title=data['title'],
            author=data['author'],
            genre=data.get('genre'),
            year_published=data.get('year_published'),
            summary=data.get('summary')
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book, 201

@api.route('/review')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        '''List all reviews'''
        return Review.query.all()

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        '''Create a new review'''
        data = api.payload
        new_review = Review(
            book_id=data['book_id'],
            user_id=data['user_id'],
            review_text=data.get('review_text'),
            rating=data.get('rating')
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review, 201