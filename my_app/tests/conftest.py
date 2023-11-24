import pytest

from my_app import app as flask_app
from my_app.config import TestingConfig

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.config.from_object(TestingConfig)
    return app.test_client()

#Login
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='12345'):
        return self._client.post('/login', data={ 'username':username, 'password':password })
    
    def logout(self):
        return self._client.get('/logout')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)