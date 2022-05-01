from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

# creating endpoint
books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

# decorating the endpoint
@books_bp.route("", methods=["POST", "GET"])
def handle_books():
    # "Pythonifies" the JSON HTTP request body by converting it to a Python dictionary.
    request_body = request.get_json()

    if request.method == "POST"
        # kwargs match model attributes and access request body
        new_book = Book(title=request_body["title"],
                        description=request_body["description"])
        
        # db.session collects changes that need to be made for the database, we add then commit to save changes
        db.session.add(new_book)
        db.session.commit()
        
        return make_response(f"Book {new_book.title} successfully created", 201)

    elif request.method == "GET":
        # turns all instance of book into a list
        books = Book.query.all()
        books_response = [dict(title=book.title, 
                               description=book.description) for book in books]
        
        return jsonify(books_response)

    