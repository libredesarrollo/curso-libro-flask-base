import os

from sqlalchemy.orm import Session

from my_app.documents import models
from my_app import db, app

def getById(id: int, show404=False):
    if show404:
        document = models.Document.query.get_or_404(id)
    else:
        document = db.session.query(models.Document).get(id)

    return document

def create(name: str, ext: str, folder='', file=None):
    document = models.Document(name=name, ext=ext)
    db.session.add(document)
    db.session.commit()
    db.session.refresh(document)

    if file is not None:
        file.save(os.path.join(app.instance_path, app.config['UPLOAD_FOLDER']+folder, name))

    return document

def delete(id: int, folder=''):
    document = getById(id=id)
    
    if document is not None:
        os.remove(app.config['UPLOAD_FOLDER']+folder+'/'+ document.name)
        db.session.delete(document)
        db.session.commit()
    