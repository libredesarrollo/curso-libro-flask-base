import json

from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with

from my_app import db
from my_app.tasks.models import Tag

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name cannot be blank!')

tag_fields = {
    'id': fields.Integer(),
    'name': fields.String()
}

class TagArgApi(Resource):

    @marshal_with(tag_fields)
    def get(self, id:int=None):

        if not id:
            return Tag.query.all()
        else:
            tag = Tag.query.get(id)
            if not tag:
                abort(404)
            return tag

    @marshal_with(tag_fields)
    def put(self, id:int):

        tag = Tag.query.get(id)
        if not tag:
            abort(400, {'message':'Tag not exits'})

        args = parser.parse_args()

        if len(args['name']) < 3:
            abort(403, {'message':'Name not valid'})

        tag.name = args['name']

        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)

        return tag

    # @marshal_with(tag_fields)
    def delete(self, id:int):
        tag = Tag.query.get(id)
        if not tag:
            abort(400, {'message':'Tag not exits'})

        db.session.delete(tag)
        db.session.commit()

        return json.dumps({'message':'Success'})

    @marshal_with(tag_fields)
    def post(self):

        args = parser.parse_args()

        if len(args['name']) < 3:
            abort(403, {'message':'Name not valid'})

        tag = Tag()
        tag.name = args['name']

        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)

        return tag