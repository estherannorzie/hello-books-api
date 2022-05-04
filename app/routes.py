from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

# creating endpoint
books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

# endpoints decorated
# there is a comma near the methods arg since it's a tuple with one element. 
# else python thinks it's a string
@books_bp.route("", methods=("GET",))
def read_all_books():
    # the title query value is case sensitive in Postman
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
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


@books_bp.route("/<book_id>", methods=("PUT",))
def update_book(book_id):
    # get book id    
    book = validate_book(book_id)

    # turn the request body into a dictionary
    request_body = request.get_json()
    
    # update the book instance's title and description
    book.title = request_body["title"]
    book.description = request_body["description"]

    # commit the book instance into database
    db.session.commit()

    return make_response(f"Book #{book.id} successfully updated")


@books_bp.route("/<book_id>", methods=("DELETE",))
def delete_book(book_id):
    book = validate_book(book_id)
    
    db.session.delete(book)
    db.session.commit()

    return make_response(f"Book #{book.id} successfully deleted.")


def validate_book(book_id):
    try:
        book_id = int(book_id)
    # if the id is the wrong data type
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)
    # if the id is the right data type but does not exist
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