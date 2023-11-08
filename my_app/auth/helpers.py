from my_app.auth.models import User

def authenticate(username, password):

    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    if user.check_password(password):
        return None

    return user