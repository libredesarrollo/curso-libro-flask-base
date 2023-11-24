from flask_jwt_extended import create_access_token

from my_app.tasks import operations
from my_app.auth.models import User

def test_index(app, client):
    with app.app_context():
        response = client.get('/api/task')
        assert response.status_code == 200
        tasks = operations.getAll()
        for i in range(len(tasks)):
            assert tasks[i].name == response.get_json()[i]['name']

def test_show(app, client):
    with app.app_context():
        laskTask = operations.getLastTask()
        response = client.get('/api/task/'+str(laskTask.id))
        assert response.status_code == 200

        assert laskTask.name == response.get_json()['name']
        assert laskTask.id == response.get_json()['id']

def test_create(app, client):

    dataform = {
        "name" : "Task Test",
        "category_id" : 1,
    }
    with app.app_context():
        taskCount = len(operations.getAll())
        response = client.post('/api/task', json=dataform)
        assert response.status_code == 200

        assert len(operations.getAll()) == taskCount+1
        lastTask = operations.getLastTask()
        assert lastTask.name == response.get_json()['name']
        assert lastTask.id == response.get_json()['id']

def test_create_auth(app, client):

    dataform = {
        "name" : "Task Test",
        "category_id" : 1,
    }

    with app.app_context():
        tokenauth = create_access_token(identity=User.query.filter_by(username='admin').first().id)
        headers = { "Authorization": "Bearer "+tokenauth }

        taskCount = len(operations.getAll())
        response = client.post('/api/task', json=dataform, headers=headers)
        assert response.status_code == 200

        assert len(operations.getAll()) == taskCount+1
        lastTask = operations.getLastTask()
        assert lastTask.name == response.get_json()['name']
        assert lastTask.id == response.get_json()['id']

def test_update(app, client):

    dataform = {
        "name" : "Task Test 1.1",
        "category_id" : 1,
    }
    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.put('/api/task/'+str(lastTask.id), json=dataform)

        assert response.status_code == 200

        taskUpdate = operations.getById(lastTask.id)

        assert taskUpdate.name == response.get_json()['name']
        assert taskUpdate.id == response.get_json()['id']

def test_delete(app, client):

    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.delete('/api/task/'+str(lastTask.id))

        assert response.status_code == 200

        task = operations.getById(lastTask.id)

        assert task is None
