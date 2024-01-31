from flask_wtf import FlaskForm
from flask_babel import gettext

from wtforms import StringField, PasswordField, EmailField, TextAreaField, HiddenField, FileField, SelectField
from wtforms.validators import InputRequired, EqualTo, URL

class ResgistrationForm(FlaskForm):
    username = StringField(gettext('Username'), [InputRequired()])
    password = PasswordField(gettext('Password'), [InputRequired(), EqualTo('confirm', message=gettext('Password must match'))])
    confirm = PasswordField(gettext('Confirm')+' '+ gettext('Password'), [InputRequired()])

class LoginForm(FlaskForm):
    username = StringField(gettext('Username'), [InputRequired()])
    password = PasswordField(gettext('Password'), [InputRequired()])

class ChangeUserInformationForm(FlaskForm):
    firstname = StringField(gettext('First Name'), [InputRequired()])
    lastname = StringField(gettext('Last Name'), [InputRequired()])
    email = EmailField(gettext('Email'), [InputRequired()])

class ChangeUserAddressForm(FlaskForm):
    address = TextAreaField(gettext('Address'), [InputRequired()])

class ChangeUserPasswordForm(FlaskForm):
    password = PasswordField(gettext('Password'), [InputRequired(), EqualTo('confirm', message=gettext('Password must match'))])
    confirm = PasswordField(gettext('Confirm')+' '+ gettext('Password'), [InputRequired()])

class UserSocialNetworkForm(FlaskForm):
    name = StringField(gettext('Social Network'), [InputRequired(), URL()])
    social_network_id = HiddenField(gettext('Social Network ID'), [InputRequired()])

class AvatarForm(FlaskForm):
    avatar=FileField(gettext('Avatar'),)

class LangForm(FlaskForm):
    lang=SelectField(gettext('Lang'), choices=[("ES", "ES"), ("EN", "EN")])