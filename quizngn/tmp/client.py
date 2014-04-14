import json
import requests

url = 'http://192.168.33.10:5001/api/quizzes/2'
headers = {'Content-Type': 'application/json'}

# Make a PATCH request to create a question in the database.
#data = dict(title= 'New', difficulty_level='Easy', text='None', no_ques = 1)
#response = requests.post(url, data=json.dumps(data), headers=headers)
#assert response.status_code == 201
"""
# Make a POST request to create a quiz in the database.
data = dict(ques="This question", ans="This is answer")
response = requests.post(url, data=json.dumps(data), headers=headers)
"""
# Make a GET request for the entire collection.
response = requests.get(url, headers=headers)
#assert response.status_code == 200
'''
# Make a DEL request for the entire collection.
response = requests.delete(url, headers=headers)
assert response.status_code == 200
'''
#import pdb; pdb.set_trace()
print(response.json())
