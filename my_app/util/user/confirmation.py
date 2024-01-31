from itsdangerous import URLSafeTimedSerializer

from my_app import app

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECURITY_PASSWORD_SALT'])

    return serializer.dumps(email,salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token,expiration=360):
    serializer = URLSafeTimedSerializer(app.config['SECURITY_PASSWORD_SALT'])

    try:
        email = serializer.loads(token,
                                 salt=app.config['SECURITY_PASSWORD_SALT'],
                                 max_age=expiration
                                 )
    except:
        return False
    return email