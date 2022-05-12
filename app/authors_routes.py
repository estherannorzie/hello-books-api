from app import db
from app.models.author import Author
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@authors_bp.route("/books", methods=("GET",))
def read_all_authors():
    authors = Author.query.all()
    authors_response = [{"name": author.name} for author in authors]

    return jsonify(authors_response)


@authors_bp.route("/<author_id>/books", methods=("GET",))
def read_books(author_id):

    author = validate_author(author_id)

    books_response = [
        {
            "id": book.id,
            "title": book.title,
            "description": book.description
    } for book in author.books]
    
    return jsonify(books_response)


@authors_bp.route("", methods=("POST",))
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

    
@authors_bp.route("/<author_id>/books", methods=("POST",))
def create_book(author_id):

    author = validate_author(author_id)

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author=author
    )
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)


def validate_author(author_id):
    try:
        author_id = int(author_id)
    except:
        abort(make_response({"message":f"author {author_id} invalid"}, 400))

    author = Author.query.get(author_id)

    if not author:
        abort(make_response({"message":f"author {author_id} not found"}, 404))

    return author