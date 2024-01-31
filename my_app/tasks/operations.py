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

def getLastTask():
    task = models.Task.query.order_by(models.Task.id.desc()).first()
    return task

def getAll():
    tasks = db.session.query(models.Task).all()
    return tasks

def create(name: str, category_id:int, user_id:int):
    taskdb = models.Task(name=name, category_id=category_id, user_id=user_id)
    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def update(id:int ,name: str, category_id:int, document_id: int = None):
    taskdb = getById(id=id)

    taskdb.name = name
    taskdb.category_id = category_id
    if document_id is not None:
        taskdb.document_id = document_id

    db.session.add(taskdb)
    db.session.commit()
    db.session.refresh(taskdb)
    return taskdb

def delete(id: int):
    taskdb = getById(id=id, show404=True)
    db.session.delete(taskdb)
    db.session.commit()

def pagination(page:int=1, per_page:int=10, user_id=None):
    if user_id is None:
        return models.Task.query.paginate(page=page, per_page=per_page)
    
    return models.Task.query.filter(models.Task.user_id==user_id).paginate(page=page, per_page=per_page)

#tags
def addTag(id: int, tagid:int):
    task = getById(id=id)
    tag = models.Tag.query.get_or_404(tagid)
    task.tags.append(tag)

    db.session.add(task)
    db.session.commit()
    db.session.refresh(task)

    return task
def removeTag(id: int, tagid:int):
    task = getById(id=id)
    tag = models.Tag.query.get_or_404(tagid)
    task.tags.remove(tag)

    db.session.add(task)
    db.session.commit()
    db.session.refresh(task)

    return task
#tags