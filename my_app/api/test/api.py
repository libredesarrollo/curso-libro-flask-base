import requests

import json
# GET si auth
# res = requests.get('http://127.0.0.1:5000/api/task', headers= { 'Content-Type': 'application/json' })
# res = requests.get('http://127.0.0.1:5000/api/task', headers= { 'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTQzNjE0MiwianRpIjoiYzI0NDBkMDQtYzgwNy00MTIzLTkzYzgtYzEzMmIyOTk1NWRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk5NDM2MTQyLCJleHAiOjE2OTk1MjI1NDJ9.njnWWjDv2lriA3uN8A9-nygk45N1SsRQxdKsQUX-SC0' })


d={'name': 'Task Json', 'category_id':1}
# res = requests.post('http://127.0.0.1:5000/api/task', headers= { 'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTQzNjE0MiwianRpIjoiYzI0NDBkMDQtYzgwNy00MTIzLTkzYzgtYzEzMmIyOTk1NWRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk5NDM2MTQyLCJleHAiOjE2OTk1MjI1NDJ9.njnWWjDv2lriA3uN8A9-nygk45N1SsRQxdKsQUX-SC0' }, data=json.dumps(d))
# res = requests.post('http://127.0.0.1:5000/api/task', headers= { 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTQzNjE0MiwianRpIjoiYzI0NDBkMDQtYzgwNy00MTIzLTkzYzgtYzEzMmIyOTk1NWRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk5NDM2MTQyLCJleHAiOjE2OTk1MjI1NDJ9.njnWWjDv2lriA3uN8A9-nygk45N1SsRQxdKsQUX-SC0' }, json=d)

# res = requests.put('http://127.0.0.1:5000/api/task/14', headers= { 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTQzNjE0MiwianRpIjoiYzI0NDBkMDQtYzgwNy00MTIzLTkzYzgtYzEzMmIyOTk1NWRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk5NDM2MTQyLCJleHAiOjE2OTk1MjI1NDJ9.njnWWjDv2lriA3uN8A9-nygk45N1SsRQxdKsQUX-SC0' }, json=d)
res = requests.delete('http://127.0.0.1:5000/api/task/14', headers= { 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTQzNjE0MiwianRpIjoiYzI0NDBkMDQtYzgwNy00MTIzLTkzYzgtYzEzMmIyOTk1NWRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk5NDM2MTQyLCJleHAiOjE2OTk1MjI1NDJ9.njnWWjDv2lriA3uN8A9-nygk45N1SsRQxdKsQUX-SC0' })
# print(res)
print(res.json())