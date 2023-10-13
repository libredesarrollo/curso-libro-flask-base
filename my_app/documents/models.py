from sqlalchemy.orm import relationship

from my_app import db

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    ext = db.Column(db.String(8))