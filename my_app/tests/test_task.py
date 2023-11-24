
# from my_app import app

from my_app.tasks import operations

def test_create(app, client):

    #get
    response = client.get('/tasks/create')
    assert response.status_code == 200
    assert  b'<input id="name" name="name" required type="text" value="">' in response.get_data()
    assert  '<input id="name" name="name" required type="text" value="">' in response.get_data(as_text=True)

    #post
    dataform = {
        "name" : "Task Test",
        "category" : 1,
    }

    taskCount = 0

    with app.app_context():
        taskCount = len(operations.getAll())
        response = client.post('/tasks/create', data=dataform)
        assert response.status_code == 200
        assert  '<input id="name" name="name" required type="text" value="'+dataform.get('name')+'">' in response.get_data(as_text=True)
        assert len(operations.getAll()) == taskCount+1

def test_update(app, client):

    #get
    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.get('/tasks/update/'+str(lastTask.id))
        assert response.status_code == 200
        assert  '<input id="name" name="name" required type="text" value="'+lastTask.name+'">' in response.get_data(as_text=True)

    #post
    dataform = {
        "name" : "Task Test 1.1",
        "category" : 1,
    }

    with app.app_context():
        response = client.post('/tasks/create', data=dataform)
        assert response.status_code == 200

        task = operations.getById(lastTask.id)
        assert  '<input id="name" name="name" required type="text" value="'+task.name+'">' in response.get_data(as_text=True)
        assert task.name == dataform.get('name')


def test_index(client, auth):
    auth.login()
    response = client.get('/tasks/')
    assert response.status_code == 200
    with app.app_context():
        tasks = operations.getAll()
        for t in tasks:
            assert '<li>'+t.name+'</li>' in response.get_data(as_text=True)

def test_delete(client):
    with app.app_context():
        lastTask = operations.getLastTask()
        response = client.get('/tasks/delete/'+str(lastTask.id))
        assert response.status_code == 302

        task = operations.getById(lastTask.id)
        assert task is None

