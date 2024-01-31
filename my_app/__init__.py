from functools import wraps

from flask import Flask, render_template, request, session

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_babel import Babel

from my_app.config import DevConfig

app = Flask(__name__, static_folder='assets') #template_folder='/pages'

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

#babel
def get_locale():
    # return 'es'

    if session['user'] and session['user']['lang']:
        return session['user']['lang']
    
    return request.accept_languages.best_match(['es','en'])

babel = Babel(app,locale_selector=get_locale)

def roles_required(*role_names):
    def wrapper(f):
        @wraps(f)   
        def wrap(*args, **kwargs):
            for r in role_names:
                if session['user']['roles'].find(r) < 0:
                    return "You do not have the role to perform this operation", 401
                
            return f(*args, **kwargs)
        return wrap
    return wrapper

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
from my_app.tasks.models import Task
from my_app.auth.models import User
from sqlalchemy.sql.expression import or_
#route

from my_app.util.template_filter import text_to_upper
app.add_template_filter(text_to_upper)

@app.route('/')
def hello_world(): # -> str
    name = request.args.get('name','Desarrollolibre')
    # return {'hello': 'world'}

    print(db.session.query(Task.name.distinct().label("title")).all())

    return render_template('index.html',task=name,name=name)
    # return 'Hello Flask'


