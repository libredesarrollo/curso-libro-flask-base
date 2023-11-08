from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager

from my_app.config import DevConfig

app = Flask(__name__) #template_folder='/pages'

#configurations
app.config.from_object(DevConfig)
# app.debug = True

#db
db=SQLAlchemy(app)
migrate = Migrate(app, db)

#login
login_manager = LoginManager()
login_manager.init_app(app)

#jwt
jwt = JWTManager()
jwt.init_app(app)

#restful
from my_app.api.task import TaskApi
from my_app.api.task_arg import TaskArgApi, TaskApiPagination, TaskArgUploadApi
from my_app.api.category_arg import CategoryArgApi
from my_app.api.tag_arg import TagArgApi
api = Api(app)
# api.add_resource(TaskApi, '/api/task', '/api/task/<int:id>')
api.add_resource(TaskArgApi, '/api/task', '/api/task/<int:id>')
api.add_resource(TaskApiPagination, '/api/task/<int:page>/<int:per_page>')
api.add_resource(TaskArgUploadApi, '/api/task/upload/<int:id>')
api.add_resource(CategoryArgApi, '/api/category', '/api/category/<int:id>')
api.add_resource(TagArgApi, '/api/tag', '/api/tag/<int:id>')
# api.add_resource(TaskApiSave, '/api/task/<int:id>')

#blueprints
from my_app.auth.controllers import authRoute
from my_app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)
app.register_blueprint(authRoute)

#create db
# with app.app_context():
#     db.create_all()

#route
@app.route('/')
def hello_world(): # -> str
    name = request.args.get('name','Desarrollolibre')
    return render_template('index.html',task=name,name=name)
    # return 'Hello Flask'


