import json
import requests

url = 'http://192.168.33.10:5001/api/quizzes'
headers = {'Content-Type': 'application/json'}

# Make a POST request to create a quiz in the database.
data = dict(title= 'Python Basics 2', difficulty_level='Moderate', text='Explanation 2')
#data = dict(title= 'Python Basics updated', difficulty_level = 'Easy updated')
response = requests.post(url, data=json.dumps(data), headers=headers)
'''
# Make a POST request to create a question in the database.
#data = dict(ques_text = "Is this new?", ans_text="This is it", anschoices=[{"answer":"a. New answer CHANGE", "correct":True}, {"answer":"b. Second choice mod", "correct":False}, {"answer":"c. Third modified mod", "correct":True}])                                
data = dict(ques_text = "Is this new?", ans_text="This is it", anschoices=[{"answer":"a. New answer CHANGE", "correct":True}, {"answer":"b. Second choice mod", "correct":False}, {"answer":"c. Third modified mod", "correct":True}])                                
response = requests.post(url, data=json.dumps(data), headers=headers)
'''

# Make a GET request for the entire collection.
#response = requests.get(url, headers=headers)
#response = requests.delete(url, headers=headers)
'''
# Make a DEL request for the entire collection.
response = requests.delete(url, headers=headers)
'''
print '\n_____________________Response received___________________\n'
print '\nJson response:\n==============\n Status code:%i  Reason: %s' %(response.status_code, response.reason)
print '\nResponse:\n==============\n%s' %(response.json())
print '\nHeader:\n==============\n%s\n' %(response.headers)
print '\n_________________________________________________________\n'
