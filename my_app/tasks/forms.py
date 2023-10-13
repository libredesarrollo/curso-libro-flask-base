from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, HiddenField
from wtforms.validators import InputRequired

class Task(FlaskForm):
    name=StringField('Name', validators=[InputRequired()])
    file=FileField('Document',)
    category = SelectField('Category', validate_choice=True) #choices=[(1, "Abc"), (2, "Def")]

class TaskTagAdd(FlaskForm):
    tag = SelectField('Tag',)

class TaskTagRemove(FlaskForm):
    tag = HiddenField('Tag',)