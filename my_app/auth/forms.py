from flask_wtf import FlaskForm
from flask_babel import gettext

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class ResgistrationForm(FlaskForm):
    username = StringField(gettext('Username'), [InputRequired()])
    password = PasswordField(gettext('Password'), [InputRequired(), EqualTo('confirm', message=gettext('Password must match'))])
    confirm = PasswordField(gettext('Confirm')+' '+ gettext('Password'), [InputRequired()])

class LoginForm(FlaskForm):
    username = StringField(gettext('Username'), [InputRequired()])
    password = PasswordField(gettext('Password'), [InputRequired()])
