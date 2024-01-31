# import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from flask_login import login_required
# from flask_babel import gettext

from werkzeug.utils import secure_filename

from my_app.tasks import operations, forms, models
from my_app.documents import operations as doc_operations
from my_app import config, roles_required

# from my_app.util.user.confirmation import generate_confirmation_token

taskRoute = Blueprint('tasks',__name__,url_prefix='/tasks',)

@taskRoute.before_request
@login_required
def before():
    pass

@taskRoute.route('/')
@roles_required('READ_TASK')
def index():
    # token = generate_confirmation_token(session['user']['email'])
    # print(token)

    print(html)
    if session['user']['roles'].find('ADMIN') >= 0:
        tasks = operations.pagination(request.args.get('page', 1, type=int))
    else:
        tasks = operations.pagination(request.args.get('page', 1, type=int), user_id=session['user']['id'])

    return render_template('dashboard/task/index.html', tasks=tasks)

@taskRoute.route('/<int:id>')
@roles_required('READ_TASK')
def show(id:int):
    return 'Show '+str(id)

@taskRoute.route('/delete/<int:id>')
@roles_required('SAVE_TASK')
def delete(id:int):
    task=operations.getById(id,True)
    operations.delete(task.id)
    doc_operations.delete(task.document_id)
    flash('The registry has been removed successfully')
    return redirect(url_for('tasks.index'))

@taskRoute.route('/create', methods=('GET','POST'))
@roles_required('SAVE_TASK')
def create():
    form = forms.Task() #csrf_enabled=False
    form.category.choices = [ (c.id, c.name) for c in models.Category.query.all()]
    if form.validate_on_submit():
        operations.create(form.name.data, form.category.data, session['user']['id'])
        flash('The registry has been created successfully')
    
    return render_template('dashboard/task/create.html', form=form)

@taskRoute.route('/update/<int:id>', methods=['GET','POST'])
@roles_required('SAVE_TASK')
def update(id:int):

    task = operations.getById(id, True)

    form = forms.Task()
    form.category.choices = [ (c.id, c.name) for c in models.Category.query.all()]

    #tags
    formTag = forms.TaskTagAdd()
    formTag.tag.choices = [ (t.id, t.name) for t in models.Tag.query.all()]

    formTagRemove = forms.TaskTagRemove()
    #tags

    if request.method == 'GET':
        form.name.data = task.name
        form.category.default = task.category_id

    if form.validate_on_submit():
        operations.update(id, form.name.data, form.category.data,)
        f = form.file.data
        if f and config.allowed_extensions_file(f.filename):
            filename = secure_filename(f.filename)
            document = doc_operations.create(filename, filename.lower().rsplit('.',1)[1],'',f)
            operations.update(id, form.name.data, form.category.data, document.id)
            
        flash('The registry has been updated successfully','info')

        # return redirect(url_for('tasks.index'))

    return render_template('dashboard/task/update.html', form=form, formTag=formTag,formTagRemove=formTagRemove, task=task, id=id)

#tag

@taskRoute.route('/<int:id>/tag/add', methods=['POST'])
def tagAdd(id:int):
    formTag = forms.TaskTagAdd()
    formTag.tag.choices = [ (t.id, t.name) for t in models.Tag.query.all()]

    if(formTag.validate_on_submit()):
        operations.addTag(id,formTag.tag.data)
        flash('The registry has been created successfully')

    return redirect(url_for('tasks.update', id=id))

@taskRoute.route('/<int:id>/tag/remove', methods=['POST'])
def tagRemove(id:int):
    formTag = forms.TaskTagRemove()

    if(formTag.validate_on_submit()):
        operations.removeTag(id,formTag.tag.data)
        flash('The registry has been removed successfully')

    return redirect(url_for('tasks.update', id=id))

#tag