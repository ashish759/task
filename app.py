from flask import Flask
from flask_restx import Api
from models import db  # Import the db instance
from routes import book_ns

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ashi%4012345678@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Initialize the API
api = Api(app, version='1.0', title='Books API', description='A simple Books API')
api.add_namespace(book_ns)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
