import enum

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from my_app import db

class LangChoices(enum.Enum):
    ES = 'ES'
    EN = 'EN'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    pwdhash = db.Column(db.String(500))
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_cofirmed_at = db.Column(db.DateTime())
    
    first_name=db.Column(db.String(100), nullable=False)
    last_name=db.Column(db.String(100), nullable=False)

    avatar_id= db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)
    address_id= db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    address = relationship('Address', lazy='joined')
    avatar = relationship('Document', lazy='joined')
    social_networks = db.relationship('SocialNetwork', lazy='joined', secondary='user_social_networks')

    lang = db.Column(db.Enum(LangChoices), default=LangChoices.EN)

    roles = db.relationship('Roles', lazy='joined', secondary='user_roles') #ROLES

    email_confirmed_at = db.Column(db.DateTime(), nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    def hash_password(self, password):
        self.pwdhash = generate_password_hash(password)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    @property
    def serialize(self):

        avatar = ''
        if self.avatar_id is not None:
            avatar = self.avatar.name
        
        lang = ''
        if self.lang is not None:
            lang = self.lang.value
        
        roles = ''
        if len(self.roles) > 0:
            for r in self.roles:
                roles += r.name+','
 
        return {
            'id' : self.id,
            'username' : self.username,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'email' : self.email,
            'avatar' : avatar,
            'avatar_id' : self.avatar_id,
            'lang' : lang,
            'email_confirmed_at' : self.email_confirmed_at,
            'roles' : roles
        }

class SocialNetwork(db.Model):
    __tablename__ = 'social_networks'
    id= db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(50), unique=True)

class UserSocialNetwork(db.Model):
    __tablename__ = 'user_social_networks'
    id= db.Column(db.Integer(), primary_key=True)
    user_id= db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    social_network_id= db.Column(db.Integer(), db.ForeignKey('social_networks.id', ondelete='CASCADE'))
    url=db.Column(db.String(500))

class Address(db.Model):
    __tablename__ = 'addresses'
    id= db.Column(db.Integer(), primary_key=True)
    address=db.Column(db.String(250))

# Roles
class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))