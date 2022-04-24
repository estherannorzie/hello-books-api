from flask import Blueprint, jsonify

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

# decorating function using endpoint
@books_bp.route("", methods=["GET"])
def get_all_books():
    return jsonify([
                    {"id": book.id, 
                    "title": book.title, 
                    "description": book.description} 
                    for book in books
        ])