# models/api_models.py

from flask_restx import fields, Namespace

# Create a namespace to use with API models
api = Namespace('api_models')

book_model = api.model('Book', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True, description='The book title'),
    'author': fields.String(required=True, description='The book author'),
    'genre': fields.String(description='The book genre'),
    'year_published': fields.Integer(description='The year the book was published'),
    'summary': fields.String(description='A summary of the book'),
})

review_model = api.model('Review', {
    'id': fields.Integer(readOnly=True),
    'book_id': fields.Integer(required=True, description='The ID of the book'),
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'review_text': fields.String(description='The review text'),
    'rating': fields.Integer(description='The rating given to the book'),
})
