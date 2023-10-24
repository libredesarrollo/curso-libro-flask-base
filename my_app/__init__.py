from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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


