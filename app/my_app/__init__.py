from flask import Flask, render_template, request

from my_app.tasks.controllers import taskRoute

from my_app.config import DevConfig

app = Flask(__name__) #template_folder='/pages'
app.register_blueprint(taskRoute)

app.config.from_object(DevConfig)
# app.debug = True

@app.route('/')
def hello_world(): # -> str
    name = request.args.get('name','Desarrollolibre')
    return render_template('index.html',task=name,name=name)
    return 'Hello Flask'


