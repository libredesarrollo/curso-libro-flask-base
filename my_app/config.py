import os

ALLOWED_EXTENSIONS_FILES = { 'pdf', 'jpg', 'jpeg', 'gif', 'png' }

def allowed_extensions_file(filename): #test.png
    # setting the rsplit:maxsplit parameter to 1, will return a list with 2 elements
    return '.' in filename and filename.lower().rsplit('.',1)[1] in ALLOWED_EXTENSIONS_FILES

class Config(object):
    UPLOAD_FOLDER=os.path.realpath('.') + '/my_app/uploads'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://sail:password@localhost:3306/testing" 
    SECRET_KEY='SECRET_KEY'
    # WTF_CSRF_ENABLED = False