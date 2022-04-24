from flask import Blueprint

# create class
class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

# create instances of class
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
    # must convert book id into integer
    book_id = int(book_id)
    for book in books:
        if book_id == book.id:
            return (dict(id = book.id, 
                        title = book.title, 
                        description = book.description))