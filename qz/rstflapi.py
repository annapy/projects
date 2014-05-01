from flask import Flask, request
from flask import json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

import qzdb 
import utls 

class InvalidUsage(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

class QuizzesAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type = str, required = True,
                             help = "No title given for quiz", location = 'json')
        self.reqparse.add_argument("difficulty_level", type = str, required = True,
                             help = "No difficulty level given for quiz", location = 'json')
        self.reqparse.add_argument("text", type = str, required = True,
                             help = "Quiz text not provided", location = 'json')
        super(QuizzesAPI, self).__init__()


    #GET /api/quizzes
    def get(self):
        '''Get all quizzes'''
        print "_______________________________________________"
        print "QuizzesAPI get fn: %s" %(request)

        '''Query from quiz table'''
        Query_obj = qzdb.Quiz.query.order_by(qzdb.Quiz.qzid).all()
        if Query_obj == []:
            response = handle_invalid_usage(InvalidUsage('Error: No quizzes found',status_code=404))
            return response

        '''Return response'''
        resp_fields = ['qzid','title', 'difficulty_level', 'text','no_ques']
        relnshp_flag = 0
        quizzes = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'quizzes\':%s}\n' %(quizzes)
        response = jsonify(quizzes=quizzes)
        response.status_code = 200
        utls.display_tables()
        return response

    #POST /api/quizzes
    def post(self):
        '''Add new quiz'''
        print "_________________________________________________"
        print "QuizzesAPI post fn: %s\nJson Request\n=============\n %s" %(request, request.json)

        '''Get values from request'''
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value != None:
                if (key == 'title'):
                    title = request.json['title']
                if (key == 'difficulty_level'):
                    difficulty_level = request.json['difficulty_level']
                if (key == 'text'):
                    text = request.json['text']

        #print args.help
        '''Update tables'''
        Quiz_obj = qzdb.Quiz(title, difficulty_level, text)
        qzdb.db.session.add(Quiz_obj)
        qzdb.db.session.commit()
        
        '''Return response'''
        location = "/api/quizzes/"+str(Quiz_obj.qzid)
        Query_obj = qzdb.Quiz.query.filter_by(qzid=Quiz_obj.qzid).all()
        resp_fields = ['qzid','title', 'difficulty_level', 'text','no_ques']
        relnshp_flag = 0
        quiz = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'quiz\':%s\n}' %(quiz)
        response = jsonify(quiz=quiz)
        response.status_code = 201
        response.location = location
        utls.display_tables()
        return response

class QuizAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type = str, 
                             help = "*********No title given********", location = 'json')
        self.reqparse.add_argument("difficulty_level", type = str,
                             help = "No difficulty level set", location = 'json')
        self.reqparse.add_argument("text", type = str, 
                             help = "text", location = 'json')
        super(QuizAPI, self).__init__()


    #GET  /api/quizzes/{qzid}
    def get(self, qzid):
        '''Get quiz details'''
        print "_________________________________________________"
        print "QuizAPI get fn: %s" %(request)

        '''Query from quiz table'''
        Query_obj = qzdb.Quiz.query.filter_by(qzid = qzid).all()
        if Query_obj == []:
            response = handle_invalid_usage(InvalidUsage('Error: Quiz not found',status_code=404))
            return response

        '''Return response'''
        resp_fields = ['qzid','title', 'difficulty_level', 'text','no_ques']
        relnshp_flag = 0
        quiz = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'quiz\':%s}\n' %(quiz)
        response = jsonify(quiz=quiz)
        utls.display_tables()
        response.status_code = 200
        return response


    #PATCH /api/quizzes/{qzid}
    def patch(self, qzid):
        '''Edit quiz details'''
        print "_________________________________________________"
        print "QuizAPI patch fn: %s \nJson Request\n=============\n %s" %(request, request.json) 

        '''Get values from req'''
        args = self.reqparse.parse_args()
        cols = {}
        no_data = True
        for key, value in args.iteritems():
            if value != None:
                no_data = False
                cols[key] = request.json[key]

        '''If no input in patch request, return 400'''
        if no_data:
            response = handle_invalid_usage(InvalidUsage('Error: No input data provided in Patch req',status_code=400))
            return response

        '''Update tables'''
        qzdb.Quiz.query.filter_by(qzid = qzid).update(cols)
        qzdb.db.session.commit()

        '''Return response'''
        Query_obj = qzdb.Quiz.query.filter_by(qzid=qzid).all()
        resp_fields = ['qzid','title', 'difficulty_level', 'text','no_ques']
        relnshp_flag = 0
        quiz = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'quiz\':%s\n}' %(quiz)
        response = jsonify(quiz=quiz)
        response.status_code = 200
        utls.display_tables()
        return response

    #DELETE  /api/quizzes/{qzid}
    def delete(self, qzid):
        '''Delete quiz'''
        print "_________________________________________________"
        print "QuizAPI delete fn: %s" %(request)
        '''delete all questions table entries for the quiz'''
        qzdb.Question.query.join(qzdb.Quiz).filter(qzdb.Question.qzid == qzid).delete()
        
        '''delete all Ans choices table entries for quiz'''
        qzdb.Anschoice.query.join(qzdb.Quiz).filter(qzdb.Anschoice.qzid == qzid).delete()

        '''delete quiz'''
        qzdb.Quiz.query.filter(qzdb.Quiz.qzid == qzid).delete()
        qzdb.db.session.commit()
        
        '''Return response'''
        utls.display_tables()
        return 204

class QuestionsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("ques_text", type = str, required = True,
                             help = "No ques text provided", location = 'json')
        self.reqparse.add_argument("ans_text", type = str, required = True,
                             help = "No ans given", location = 'json')
        super(QuestionsAPI, self).__init__()

        relnshp_flag = 0

    #GET /api/questions/{qzid}/questions
    def get(self, qzid):
        '''Get all questions for quiz'''
        print "_________________________________________________"
        print "QuestionisAPI get fn: %s" %(request)

        '''Query from quetsions table'''
        Query_obj = qzdb.Question.query.join(qzdb.Quiz).join(qzdb.Anschoice).filter(qzdb.Quiz.qzid == qzid).all()
        if Query_obj == []:
            response = handle_invalid_usage(InvalidUsage('Error: No question for quiz found',status_code=404))
            return response

        '''Return response'''
        resp_fields = ['qid', 'qzid','ques_text', 'ans_text', 'anschoices'] 
        relnshp_flag = resp_fields.index('anschoices')
        questions = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'questions\':%s}\n' %(questions)
        response = jsonify(questions = questions)
        response.status_code = 200
        utls.display_tables()
        return response

    #POST /api/quizzes/{qzid}/questions
    def post(self, qzid):
        '''Add question to quiz'''
        print "_________________________________________________"
        print "QuestionsAPI post fn: %s \nJson Request\n=============\n %s" %(request, request.json)

        '''Get data from req'''
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value != None:
                if (key == 'ques_text'):
                    ques_text = request.json['ques_text']
                if (key == 'ans_text'):
                    ans_text = request.json['ans_text']
                if (key == 'anschoices'):
                    anschoices = request.json['anschoices']

        '''Post new data to table'''
        qn_obj = qzdb.Question(ques_text, ans_text, qzid)
        qzdb.db.session.add(qn_obj)

        '''Update correspnoding relationship tables '''
        #Quiz table
        L = qzdb.Quiz.query.filter_by(qzid = qzid).first()
        qzdb.Quiz.query.filter_by(qzid = qzid).update(dict(no_ques= (L.no_ques+1)))

        #Ans choices table 
        ansidL = []
        for i in range(len(anschoices)):
            ans_obj = qzdb.Anschoice(qzid,
                                     qn_obj.qid,
                                     anschoices[i]["answer"], 
                                     anschoices[i]["correct"]
                                    )
            qzdb.db.session.add(ans_obj)
        qzdb.db.session.commit()

        '''Return response'''
        location = "/api/quizzes/"+str(qzid)+"/questions/"+str(qn_obj.qid)
        Query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qn_obj.qid).all()
        resp_fields = ['qid', 'qzid','ques_text', 'ans_text', 'anschoices'] 
        relnshp_flag = resp_fields.index('anschoices')
        question = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)

        print "Json response"
        print "=============\n"
        print '{\'question\':%s}\n' %(question)
        response = jsonify(question = question)
        response.location = location
        response.status_code = 201
        utls.display_tables()
        return response

class QuestionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ques_text', type = str, required = True,
                             help = 'No title given', location = 'json')
        self.reqparse.add_argument('ans_text', type = str, default = "",
                             help = 'No ans provided', location = 'json')
        super(QuestionAPI, self).__init__()

    #GET  /api/quizzes/{qzid}/questions/{qid}
    def get(self, qzid, qid):
        '''Get question qid for quiz'''
        print "_________________________________________________"
        print "QuestionAPI get fn: %s" %(request)

        '''Query Question table'''
        Query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).all()
        if Query_obj == []:
            response = handle_invalid_usage(InvalidUsage('Error: Question not found',status_code=404))
            return response

        '''Return response'''
        resp_fields = ['qid', 'qzid','ques_text', 'ans_text', 'anschoices'] 
        relnshp_flag = resp_fields.index('anschoices')
        question = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'question\':%s}\n' %(question)
        response = jsonify(question = question)
        response.status_code = 200
        utls.display_tables()
        return response

    #PATCH /api/quizzes/{qzid}/questions/{qid}
    def patch(self, qzid, qid):
        '''Add question to quiz'''
        print "_________________________________________________"
        print "QuestionAPI patch fn: %s \nJson Request\n=============\n %s" %(request, request.json)

        '''Check if question qid exists for qzid, raise error'''
        Query_obj = qzdb.Question.query.filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).all()
        if Query_obj == []:
            response = handle_invalid_usage(InvalidUsage('Error: Question to edit not found for quiz',status_code=400))
            return response

        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value != None:
                if (key == 'ques_text'):
                    ques_text = request.json['ques_text']
                if (key == 'ans_text'):
                    ans_text = request.json['ans_text']
                if (key == 'anschoices'):
                    anschoices = request.json['anschoices']

        '''Update all table entries with input data'''
        qzdb.Question.query.filter_by(qid = qid).update(cols)

        '''Updating correspnoding relationship tables '''
        #Ans choices table 
        Q_obj = qzdb.Anschoice.query.filter_by(qid = qid)
        index = 0
        for i in Q_obj:
            ansid = Q_obj[index].ansid
            ans_choice = anschoices[index]["answer"]
            correct    = anschoices[index]["correct"]
            qzdb.Anschoice.query.filter_by(ansid = ansid).update(dict(ans_choice = ans_choice, correct = correct))  
            index += 1
        qzdb.db.session.commit()

        '''Return response'''
        Query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qid).all()
        resp_fields = ['qid', 'qzid','ques_text', 'ans_text', 'anschoices'] 
        relnshp_flag = resp_fields.index('anschoices')
        question = utls.serialize_to_json(resp_fields, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'question\':%s\n}' %(question)
        response = jsonify(question=question)
        response.status_code = 200
        utls.display_tables()
        return response

    #DELETE  /api/quizzes/{qzid}/questions/{qid}
    def delete(self, qzid, qid):
        '''Delete question'''
        print "_________________________________________________"
        print "QuestionAPI del fn: %s" %(request.url)

        '''Updating no_ques col in quiz table'''
        L = qzdb.Quiz.query.filter_by(qzid = qzid).first()
        qzdb.Quiz.query.filter_by(qzid = qzid).update(dict(no_ques= (L.no_ques-1)))

        '''deleting Ans choices table entries for qid'''
        qzdb.Anschoice.query.filter(qzdb.Anschoice.qid == qid).delete()

        '''Finally deleting entries from Question table'''
        qzdb.Question.query.filter_by(qid = qid).delete()
        qzdb.db.session.commit()

        '''Return response'''
        response = jsonify(qid=qid)
        response.status_code = 204
        utls.display_tables()
        return response

api.add_resource(QuizzesAPI, '/api/quizzes')
api.add_resource(QuizAPI, '/api/quizzes/<int:qzid>')
api.add_resource(QuestionsAPI, '/api/quizzes/<int:qzid>/questions')
api.add_resource(QuestionAPI, '/api/quizzes/<int:qzid>/questions/<int:qid>')

if __name__ == '__main__':
    qzdb.db_init()
    app.debug = True
    app.run('192.168.33.10', 5001)


