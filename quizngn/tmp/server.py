from flask import Flask
from flask import request
app = Flask(__name__)
from qzdb import *
import os
import json

@app.route('/')
def hello_world():
    return 'Welcome to the world of flask and sqlalchemy!'

"""
@app.route('/quizzes')
def process_quizzes():
    os.system('cls')
    if request.method == 'GET':
        print "Method = GET"
    L = db_get_quiz_list()
    import pdb; pdb.set_trace()
    for element in L:
        print element
    print   'Inside process quizzes after processing complete'
    return json.dumps(L)

@app.route('/quizzes/quizid')
def process_quiz_details():
    db_get_quiz_details()
    return 'Welcome to the world of flask and sqlalchemy!'

#@app.route('/quizzes/quizid/questions/qid', methods=['GET', 'POST','DELETE'])

    def process_add_ques(request):
    if request.method == 'GET'
        db_get_question_from_quiz(request)
    if request.method == 'POST'
        db_add_question_to_quiz(request)
    if request.method == 'DELETE'
        db_del_question_from_quiz(request)

    return 'Welcome to the world of flask and sqlalchemy!'
"""

if __name__ == '__main__':
    db_init()
    app.debug = True
    import pdb; pdb.set_trace()
    app.run('192.168.33.10',5001)
