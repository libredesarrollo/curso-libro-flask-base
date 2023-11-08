import json
import werkzeug

from flask import abort

from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from my_app import config

from my_app.tasks import operations
from my_app.documents import operations as doc_operations

nested_tag_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
}

task_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'category_id': fields.Integer(),
    'category': fields.String(attribute=lambda x: x.category.name),
    'tags': fields.List(fields.Nested(nested_tag_fields))
}

parser = reqparse.RequestParser()

parser.add_argument('name', required=True, help='Name cannot be blank!')
parser.add_argument('category_id', type=int, required=True, help='Category cannot be blank!')

class TaskArgApi(Resource):

    @marshal_with(task_fields)
    @jwt_required()
    def get(self, id:int=None):

        # user_id = get_jwt_identity()
        # print(user_id)
        
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

        args = parser.parse_args()

        if len(args['name']) < 3:
            abort(403, {'message':'Name not valid'})

        task= operations.update(id, args['name'],args['category_id'])

        return task.serialize

    @jwt_required()
    def delete(self, id:int):
        task = operations.getById(id)
        if not task:
            abort(400, {'message':'Task not exits'})

        operations.delete(id)
        return json.dumps({'message':'Success'})

    @jwt_required()
    def post(self):

        args = parser.parse_args()

        if len(args['name']) < 3:
            abort(403, {'message':'Name not valid'})

        task= operations.create(args['name'],args['category_id'])

        return task.serialize

class TaskApiPagination(Resource):

    @jwt_required()
    def get(self, page:int, per_page:int):
        tasks = operations.pagination(page,per_page)
        res = {}
        for task in tasks:
            res[task.id] = task.serialize

        return res
    
class TaskArgUploadApi(Resource):
    def put(self, id):
        task = operations.getById(id)
        if not task:
            abort(400, {'message':'Task not exits'})
        
        parserUpload = reqparse.RequestParser()
        parserUpload.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')

        args = parserUpload.parse_args()

        if args['file']:
            f = args['file']
            if f and config.allowed_extensions_file(f.filename):
                filename = secure_filename(f.filename)
                document = doc_operations.create(filename, filename.lower().rsplit('.',1)[1],f)

                operations.update(id, task.name, task.category_id, document.id)
                
        return task.serialize