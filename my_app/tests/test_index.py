import json

def test_index(app, client):
    response=client.get('/')
    
    assert response.status_code == 200
    expected = {'hello': 'world'}
    assert expected == json.loads(response.get_data(as_text=True))

