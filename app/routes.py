from flask import Blueprint, abort, make_response

# create Book class
class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description


# create instances of Book
books = [
    Book(1, "Introductory Python", "Introductory programming for students"),

    Book(2,"Intermediate Python","Intermediate programming for students"),

    Book(3, "Advanced Python", "Advanced programming for students")
]


# creating endpoint
books_bp = Blueprint("books_bp", __name__, url_prefix="/books")


# "/<book_id>" is a route parameter
@books_bp.route("/<book_id>", methods=["GET"])

# parameter of book_id must match the route parameter in decorator
def get_book(book_id):
    book = validate_book(book_id)

    return (dict(id = book.id, 
                title = book.title, 
                description = book.description))
    

def validate_book(book_id):
    try:
        book = int(book_id)
    except ValueError:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    for book in books:
            if book_id == book.id:
                return book
    
    # 404 + response body is returned if no book is found
    abort(make_response({"message": f"book {book_id} not found"}, 404))