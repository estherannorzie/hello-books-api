from app import db

class Book(db.Model):
    # attributes are mapped to columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    @staticmethod
    def to_dict():
        pass