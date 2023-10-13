from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from my_app.config import DevConfig

app = Flask(__name__) #template_folder='/pages'

#configurations
app.config.from_object(DevConfig)
# app.debug = True

#db
db=SQLAlchemy(app)
migrate = Migrate(app, db)

#blueprints
from my_app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)

#create db
# with app.app_context():
#     db.create_all()

#route
@app.route('/')
def hello_world(): # -> str
    name = request.args.get('name','Desarrollolibre')
    return render_template('index.html',task=name,name=name)
    # return 'Hello Flask'


