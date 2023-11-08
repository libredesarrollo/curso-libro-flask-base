import json

from flask import abort
from flask_restful import Resource, reqparse

from my_app import db
from my_app.tasks.models import Category

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name cannot be blank!')

class CategoryArgApi(Resource):

    def get(self, id:int=None):

        if not id:
            res = {}
            for category in Category.query.all():
                res[category.id] = category.serialize
            return res
        else:
            category = Category.query.get(id)
            if not category:
                abort(404)
            return category.serialize

    def put(self, id:int):

        category = Category.query.get(id)
        if not category:
            abort(400, {'message':'Category not exits'})

        args = parser.parse_args()

        if len(args['name']) < 3:
            abort(403, {'message':'Name not valid'})

        category.name = args['name']

        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)

        return category.serialize

    def delete(self, id:int):
        category = Category.query.get(id)
        if not category:
            abort(400, {'message':'Category not exits'})

        db.session.delete(category)
        db.session.commit()

        return json.dumps({'message':'Success'})

    def post(self):

        args = parser.parse_args()

        if len(args['name']) < 3:
            abort(403, {'message':'Name not valid'})

        category = Category()
        category.name = args['name']

        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)

        return category.serialize