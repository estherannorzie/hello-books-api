from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

# @authors_bp.route("/<book_id>", methods=("GET",))
# def read_author():
#     pass

# @authors_bp.route("", methods=("POST",))
# def create_author():
#     pass