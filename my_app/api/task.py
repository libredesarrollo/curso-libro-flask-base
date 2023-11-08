import json

from flask import abort, request

from flask_restful import Resource, fields, marshal_with
from werkzeug.utils import secure_filename

from my_app import config

from my_app.tasks import operations
from my_app.documents import operations as doc_operations


task_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'category_id': fields.Integer(),
    'category': fields.String(attribute=lambda x: x.category.name)
}

class TaskApi(Resource):
    # def get(self, id=None):

    #     if not id:
    #         tasks = operations.getAll()
    #         res = {}
    #         for task in tasks:
    #             res[task.id] = task.serialize
    #     else:
    #         task = operations.getById(id)
    #         res = task.serialize
    #         if not task:
    #             abort(404)
    #         # res = json.dumps({
    #         #     'name': task.name,
    #         #     'category': task.category.name,
    #         # })
    #         # res = {
    #         #     'name': task.name,
    #         #     'category': task.category.name,
    #         # }

    #     return res

    @marshal_with(task_fields)
    def get(self, id=None):

        if not id:
            return operations.getAll()
        else:
            task = operations.getById(id)
            if not task:
                abort(404)
            return task

    def put(self, id:int):

        task = operations.getById(id)
        if not task:
            abort(400, {'message':'Task not exits'})

        if not request.form:
            abort(403, {'message':'Not Parameters'})

        if not "name" in request.form:
            abort(403, {'message':'Name not valid'})

        if len(request.form['name']) < 3:
            abort(403, {'message':'Name not valid'})

        if not "category_id" in request.form:
            abort(403, {'message':'Category not valid'})

        try:
            int(request.form['category_id'])
        except:
            abort(403, {'message':'Category not valid'})

        task = operations.update(id, request.form['name'],request.form['category_id'])

        f = request.files.get('file')
        if f and config.allowed_extensions_file(f.filename):
            filename = secure_filename(f.filename)
            document = doc_operations.create(filename, filename.lower().rsplit('.',1)[1],f)

            operations.update(id, task.name, task.category_id, document.id)

        return task.serialize

    def delete(self, id:int):
        task = operations.getById(id)
        if not task:
            abort(400, {'message':'Task not exits'})

        operations.delete(id)
        return json.dumps({'message':'Success'})

    def post(self):

        if not request.form:
            abort(403, {'message':'Not Parameters'})

        if not "name" in request.form:
            abort(403, {'message':'Name not valid'})

        if len(request.form['name']) < 3:
            abort(403, {'message':'Name not valid'})

        if not "category_id" in request.form:
            abort(403, {'message':'Category not valid'})

        try:
            int(request.form['category_id'])
        except:
            abort(403, {'message':'Category not valid'})

        task= operations.create(request.form['name'],request.form['category_id'])

        return task.serialize


            