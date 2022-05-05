from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

# creating endpoint
books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

# decorating the endpoint
# there is a comma near the methods arg since it's a tuple with one element, 
# else python thinks it's a string
@books_bp.route("", methods=("GET",))
def read_all_books():
 # turns all instance of book into a list
        books = Book.query.all()
        books_response = [dict(id=book.id,
                               title=book.title, 
                               description=book.description) for book in books]
        
        return jsonify(books_response)


@books_bp.route("/<book_id>", methods=("GET",))
def read_one_book(book_id):
        book = validate_book(book_id)
        # technically, doesn't need jsonify because flask converts to dict
        return jsonify(dict(id=book.id,
                            title=book.title,
                            description=book.description))


def validate_book(book_id):
        try:
                book_id = int(book_id)
        except:
                abort(make_response({"message":f"book {book_id} invalid"}, 400))

        book = Book.query.get(book_id)

        if not book:
                abort(make_response({"message":f"book {book_id} not found"}, 404))

        return book
                

@books_bp.route("", methods=("POST",))
def create_book():
    # HTTP request body converted to a Python dictionary.
    request_body = request.get_json()

    # kwargs match model attributes and access request body
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])
        
    # db.session collects changes that need to be made for the database, 
    # we add then commit to save changes
    db.session.add(new_book)
    db.session.commit()
        
    return make_response(f"Book {new_book.title} successfully created", 201)