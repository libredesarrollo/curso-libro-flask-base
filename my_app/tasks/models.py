from sqlalchemy import Table
from sqlalchemy.orm import relationship

from my_app import db
# tables

task_tag = db.Table('task_tag', 
                    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                    )

# models
class Task(db.Model):
    __tablename__='tasks'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))

    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)
    document = relationship('Document', lazy='joined')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', lazy='joined')

    tags = relationship('Tag', secondary=task_tag)

class Category(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))

class Tag(db.Model):
    __tablename__='tags'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))

    # tasks = relationship('Task', secondary=task_tag)
