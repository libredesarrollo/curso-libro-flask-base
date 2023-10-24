from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class ResgistrationForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Password must match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
