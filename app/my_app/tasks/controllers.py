import os

from flask import Blueprint, render_template, request, redirect, url_for

from werkzeug.utils import secure_filename

from my_app.tasks import operations
from my_app.tasks import forms

from my_app import config
from my_app import app

taskRoute = Blueprint('tasks',__name__,url_prefix='/tasks',)

@taskRoute.route('/')
def index():
    return render_template('dashboard/task/index.html', tasks=operations.getAll())

@taskRoute.route('/<int:id>')
def show(id:int):
    return 'Show '+str(id)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    operations.delete(id)
    return redirect(url_for('tasks.index'))

@taskRoute.route('/create', methods=('GET','POST'))
def create():
    
    form = forms.Task() #csrf_enabled=False
    if form.validate_on_submit():
        operations.create(form.name.data)
    
    return render_template('dashboard/task/create.html', form=form)

@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
def update(id:int):

    task = operations.getById(id, True)
    form = forms.Task()

    if request.method == 'GET':
        form.name.data = task.name

    if form.validate_on_submit():
        operations.update(id, form.name.data)
        f = form.file.data
        if f and config.allowed_extensions_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('tasks.index'))

    return render_template('dashboard/task/update.html', form=form, id=id)

