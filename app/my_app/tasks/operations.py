from sqlalchemy.orm import Session

from my_app.tasks import models
from my_app import db

def getById(id: int, show404=False):
    # task = db.session.query(models.Task).filter(models.Task.id == id).first()
    if show404:
        task = models.Task.query.get_or_404(id)
    else:
        task = db.session.query(models.Task).get(id)

    return task

def getAll():
    tasks = db.session.query(models.Task).all()
    return tasks

def create(name: str):
    taskdb = models.Task(name=name)
    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def update(id:int ,name: str):
    taskdb = getById(id=id)

    taskdb.name = name

    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def delete(id: int):
    taskdb = getById(id=id, show404=True)
    db.session.delete(taskdb)
    db.session.commit()

def pagination(page:int=1, per_page:int=10):
    return models.Task.query.paginate(page=page, per_page=per_page)