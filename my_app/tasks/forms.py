from flask_wtf import FlaskForm
from flask_babel import gettext

from wtforms import StringField, FileField, SelectField, HiddenField
from wtforms.validators import InputRequired

class Task(FlaskForm):
    name=StringField(gettext('Name'), validators=[InputRequired()], render_kw={"class":"form-control"})
    file=FileField(gettext('Document'),)
    category = SelectField(gettext('Category'), validate_choice=True) #choices=[(1, "Abc"), (2, "Def")]

class TaskTagAdd(FlaskForm):
    tag = SelectField(gettext('Tag'),)

class TaskTagRemove(FlaskForm):
    tag = HiddenField('Tag',)