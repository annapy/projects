import os
from flask import Flask, request, json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api, Resource, reqparse
import qzdb 
import utls 
import basicauth 
import hashtbl 

app = Flask(__name__)
api = Api(app)

class InvalidUsageException(Exception):
    """ Handles exceptions not caught by framework and sends response
    """
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        super(InvalidUsageException,self).__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsageException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

class AdmnQuizzesAPI(Resource):
    """ Class that defines methods for processing get/post requests 
        for /api/quizzes endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type=str, required=True, 
                                   help="No title given for quiz", 
                                   location='json')
        self.reqparse.add_argument("difficulty_level", type=str, required=True,
                                   help="No difficulty level given for quiz", 
                                   location='json')
        self.reqparse.add_argument("text", type=str, required=True,
                                   help="Quiz text not provided", 
                                   location='json')
        super(QuizzesAPI, self).__init__()


    # GET /api/quizzes
    def get(self):
        """Get all quizzes"""
        print "_______________________________________________"
        print "QuizzesAPI get fn: %s" %(request)

        # Query from quiz table
        userid = utls.get_user_from_hdr()
        query_obj = qzdb.Quiz.query.filter_by(userid=userid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: No quizzes found', status_code=404))
            return response

        # Return response
        response_fields = [{'name':'qzid', 'relnshp':False,'subfields':None},
                           {'name':'title','relnshp':False,'subfields':None}, 
                           {'name':'difficulty_level','relnshp':False,
                            'subfields':None}, 
                           {'name':'text','relnshp':False,'subfields':None}, 
                           {'name':'no_ques','relnshp':False,'subfields':None}
                           ] 
        quizzes = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'quizzes\':%s}\n" %(quizzes)
        response = jsonify(quizzes=quizzes)
        response.status_code = 200
        utls.display_tables()
        return response

    # POST /api/quizzes
    @basicauth.login_required
    def post(self):
        """Add new quiz"""
        print "_________________________________________________"
        print "QuizzesAPI post fn: %s\nJson Request\n=============\n %s" %(request, request.json)

        # Get values from request
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value is not None:
                if (key == 'title'):
                    title = request.json['title']
                if (key == 'difficulty_level'):
                    difficulty_level = request.json['difficulty_level']
                if (key == 'text'):
                    text = request.json['text']

        userid = utls.get_user_from_hdr()

        # Update tables
        quiz_obj = qzdb.Quiz(title, difficulty_level, text, userid)
        qzdb.db.session.add(quiz_obj)
        qzdb.db.session.commit()
        
        # Return response
        location = "/api/quizzes/%s" % quiz_obj.qzid
        query_obj = qzdb.Quiz.query.filter_by(qzid=quiz_obj.qzid).all()
        response_fields = [{'name':'qzid', 'relnshp':False,'subfields':None},
                           {'name':'title','relnshp':False,'subfields':None}, 
                           {'name':'difficulty_level','relnshp':False,
                            'subfields':None}, 
                           {'name':'text','relnshp':False,'subfields':None}, 
                           {'name':'no_ques','relnshp':False,'subfields':None}
                           ] 
        quiz = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'quiz\':%s\n}" %(quiz)
        response = jsonify(quiz=quiz)
        response.status_code = 201
        response.location = location
        utls.display_tables()
        return response

class AdmnQuizAPI(Resource):
    """ Class that defines methods for processing get/patch/del requests 
        for /api/quizzes/<qzid> endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type=str, 
                             help="No title given", location='json')
        self.reqparse.add_argument("difficulty_level", type=str,
                             help="No difficulty level set", location='json')
        self.reqparse.add_argument("text", type=str, 
                             help="text", location='json')
        super(QuizAPI, self).__init__()


    # GET  /api/quizzes/{qzid}
    def get(self, qzid):
        """Get quiz details"""
        print "_________________________________________________"
        print "QuizAPI get fn: %s" %(request)

        # Check if user is auth to get details of this quiz
        userid = utls.get_user_from_hdr()
        query_obj = qzdb.Quiz.query.filter_by(qzid=qzid).first()
        if  (query_obj.userid != userid):
            response = handle_invalid_usage(InvalidUsageException('Error: Unauthorized Username for this quiz', \
                    status_code=401))
            return response

        # Query from quiz table
        query_obj = qzdb.Quiz.query.filter_by(qzid = qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: Quiz not found', status_code=404))
            return response

        # Return response
        response_fields = [{'name':'qzid', 'relnshp':False,'subfields':None},
                           {'name':'title','relnshp':False,'subfields':None}, 
                           {'name':'difficulty_level','relnshp':False,
                            'subfields':None}, 
                           {'name':'text','relnshp':False,'subfields':None}, 
                           {'name':'no_ques','relnshp':False,'subfields':None}] 
        quiz = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'quiz\':%s}\n" %(quiz)
        response = jsonify(quiz=quiz)
        utls.display_tables()
        response.status_code = 200
        return response

    # PATCH /api/quizzes/{qzid}
    @basicauth.login_required
    def patch(self, qzid):
        """Edit quiz details"""
        print "_________________________________________________"
        print "QuizAPI patch fn: %s \nJson Request\n=============\n %s" %(request, request.json) 

        # Get values from req
        args = self.reqparse.parse_args()
        cols = {}
        no_data = True
        for key, value in args.iteritems():
            if value is not None:
                no_data = False
                cols[key] = request.json[key]

        # Check if user is auth to update this quiz
        userid = utls.get_user_from_hdr()
        query_obj = qzdb.Quiz.query.filter_by(qzid=qzid).first()
        if  (query_obj.userid != userid):
            response = handle_invalid_usage(InvalidUsageException('Error: Unauthorized Username for this quiz', \
                    status_code=401))
            return response

        # If no input in patch request, return 400
        if no_data:
            response = handle_invalid_usage(InvalidUsageException('Error: No input data provided in Patch req', status_code=400))
            return response

        # Update tables
        qzdb.Quiz.query.filter_by(qzid=qzid).update(cols)
        qzdb.db.session.commit()

        # Return response
        query_obj = qzdb.Quiz.query.filter_by(qzid=qzid).all()
        response_fields = [{'name':'qzid', 'relnshp':False,'subfields':None},
                           {'name':'title','relnshp':False,'subfields':None}, 
                           {'name':'difficulty_level','relnshp':False,
                            'subfields':None}, 
                           {'name':'text','relnshp':False,'subfields':None}, 
                           {'name':'no_ques','relnshp':False,'subfields':None}
                           ] 
        quiz = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'quiz\':%s\n}" %(quiz)
        response = jsonify(quiz=quiz)
        response.status_code = 200
        utls.display_tables()
        return response

    # DELETE  /api/quizzes/{qzid}
    @basicauth.login_required
    def delete(self, qzid):
        """Delete quiz"""
        print "_________________________________________________"
        print "QuizAPI delete fn: %s" %(request)

        # Check if user is auth to delete this quiz
        userid = utls.get_user_from_hdr()
        query_obj = qzdb.Quiz.query.filter_by(qzid=qzid).first()
        if  (query_obj.userid != userid):
            response = handle_invalid_usage(InvalidUsageException
                             (
                              'Error: Unauthorized Username for this quiz', \
                              status_code=401
                              )
                             )
            return response

        # Delete all questions table entries for the quiz
        qzdb.Question.query.join(qzdb.Quiz).filter(qzdb.Question.qzid == qzid).delete()
        
        # Delete all Ans choices table entries for quiz
        qzdb.Anschoice.query.join(qzdb.Quiz).filter(qzdb.Anschoice.qzid == qzid).delete()

        # Delete quiz
        qzdb.Quiz.query.filter(qzdb.Quiz.qzid == qzid).delete()
        qzdb.db.session.commit()
        
        # Return response
        utls.display_tables()
        return 204

class AdmnQuestionsAPI(Resource):
    """ Class that defines methods for processing get/post requests 
        for /api/quizzes/<qzid>/questions endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("ques_text", type=str, required=True,
                             help="No ques text provided", location='json')
        self.reqparse.add_argument("ans_text", type=str, required=True,
                             help="No ans given", location='json')
        self.reqparse.add_argument("anschoices", type=list, required=True,
                             help="No choices given", location='json')
        super(QuestionsAPI, self).__init__()


    # GET /api/questions/{qzid}/questions
    def get(self, qzid):
        """Get all questions for quiz"""
        print "_________________________________________________"
        print "QuestionisAPI get fn: %s" %(request)

        # Check if user is auth to get details of this ques
        userid = utls.get_user_from_hdr()
        query_obj = qzdb.Quiz.query.filter_by(qzid=qzid).first()
        if  (query_obj.userid != userid):
            response = handle_invalid_usage(InvalidUsageException('Error: Unauthorized Username for this quiz', \
                    status_code=401))
            return response

        # Query from questions table
        query_obj = qzdb.Question.query.join(qzdb.Quiz).join(qzdb.Anschoice).filter(qzdb.Quiz.qzid == qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: No question for quiz found', status_code=404))
            return response

        # Return response
        response_fields = [{'name':'qid',  'relnshp':False, 'subfields':None}, 
                           {'name':'ques_text',  'relnshp':False, 'subfields':None}, 
                           {'name':'ans_text','relnshp':False, 'subfields':None},  
                           {'name':'qzid','relnshp':False, 'subfields':None},  
                           {'name':'anschoices','relnshp':True,'subfields':
                                        [{'name':'ans_choice',
                                          'relnshp':False,
                                          'subfields':None},
                                         {'name':'correct', 
                                          'relnshp':False, 
                                          'subfields':None}
                                         ]
                            } 
                          ] 
        questions = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'questions\':%s}\n" %(questions)
        response = jsonify(questions = questions)
        response.status_code = 200
        utls.display_tables()
        return response

    # POST /api/quizzes/{qzid}/questions
    @basicauth.login_required
    def post(self, qzid):
        """Add question to quiz"""
        print "_________________________________________________"
        print "QuestionsAPI post fn: %s \nJson Request\n=============\n %s" %(request, request.json)

        # Get data from req
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value is not None:
                if (key == 'ques_text'):
                    ques_text = request.json['ques_text']
                if (key == 'ans_text'):
                    ans_text = request.json['ans_text']
                if (key == 'anschoices'):
                    anschoices = request.json['anschoices']

        # Get userid from hdr
        userid = utls.get_user_from_hdr()

        # Post new data to table
        qn_obj = qzdb.Question(ques_text, ans_text, qzid, userid)
        qzdb.db.session.add(qn_obj)

        # Update correspnoding relationship tables 
        #Quiz table
        L = qzdb.Quiz.query.filter_by(qzid = qzid).first()
        qzdb.Quiz.query.filter_by(qzid = qzid).update(dict(no_ques= (L.no_ques+1)))

        # Ans choices table 
        ansidL = []
        for choice in range(len(anschoices)):
            ans_obj = qzdb.Anschoice(qzid,
                                     qn_obj.qid,
                                     anschoices[choice]["answer"], 
                                     anschoices[choice]["correct"]
                                    )
            qzdb.db.session.add(ans_obj)
        qzdb.db.session.commit()

        # Return response
        location = "/api/quizzes/%s/questions/%s" % (qzid, qn_obj.qid)
        query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qn_obj.qid).all()
        response_fields = [{'name':'ques_text',  'relnshp':False, 
                            'subfields':None}, 
                           {'name':'ans_text','relnshp':False, 
                            'subfields':None},  
                           {'name':'qzid','relnshp':False, 
                            'subfields':None},  
                           {'name':'anschoices','relnshp':True, 
                            'subfields':[{'name':'ans_choice','relnshp':False,
                                          'subfields':None},
                                         {'name':'correct', 'relnshp':False, 
                                          'subfields':None}]
                           } 
                          ] 
        question = utls.serialize_to_json(response_fields, query_obj, 0)

        print "Json response"
        print "=============\n"
        print "{\'question\':%s}\n" %(question)
        response = jsonify(question = question)
        response.location = location
        response.status_code = 201
        utls.display_tables()
        return response

class AdmnQuestionAPI(Resource):
    """ Class that defines methods for processing get/patch/del requests 
        for /api/quizzes/<qzid>/questions/<qid> endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ques_text', type=str, required=True,
                             help='No title given', location='json')
        self.reqparse.add_argument('ans_text', type=str, default="",
                             help='No ans provided', location='json')
        super(QuestionAPI, self).__init__()

    # GET  /api/quizzes/{qzid}/questions/{qid}
    def get(self, qzid, qid):
        """Get question qid for quiz"""
        print "_________________________________________________"
        print "QuestionAPI get fn: %s" %(request)

        # Check if user is auth to get details of this ques
        userid = utls.get_user_from_hdr()
        query_obj = qzdb.Question.query.filter_by(qid=qid).first()
        if (query_obj.userid != userid):
            response = handle_invalid_usage(InvalidUsageException('Error: Unauthorized Username for this quiz', \
                    status_code=401))
            return response

        # Query Question table
        query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: Question not found', status_code=404))
            return response

        # Return response
        response_fields = [{'name':'qid',  'relnshp':False, 'subfields':None}, 
                           {'name':'ques_text',  'relnshp':False, 'subfields':None}, 
                           {'name':'ans_text','relnshp':False, 'subfields':None},  
                           {'name':'qzid','relnshp':False, 'subfields':None},  
                           {'name':'anschoices','relnshp':True, 
                               'subfields':[{'name':'ans_choice',
                                'relnshp':False,'subfields':None},
                           {'name':'correct', 'relnshp':False, 
                            'subfields':None}]} 
                          ] 
        question = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'question\':%s}\n" %(question)
        response = jsonify(question = question)
        response.status_code = 200
        utls.display_tables()
        return response

    # PATCH /api/quizzes/{qzid}/questions/{qid}
    @basicauth.login_required
    def patch(self, qzid, qid):
        """Add question to quiz"""
        print "_________________________________________________"
        print "QuestionAPI patch fn: %s \nJson Request\n=============\n %s" %(request, request.json)

        # Check if question qid exists for qzid, raise error
        query_obj = qzdb.Question.query.filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: Question to edit not found for ques', status_code=400))
            return response

        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value is not None:
                if (key == 'ques_text'):
                    ques_text = request.json['ques_text']
                if (key == 'ans_text'):
                    ans_text = request.json['ans_text']
                if (key == 'anschoices'):
                    anschoices = request.json['anschoices']

        # Check if user is auth to update this ques
        userid = utls.get_user_from_hdr()
        query_obj = Question.query.filter_by(qid=qid).first()
        if  (query_obj.userid != userid):
            response = handle_invalid_usage(InvalidUsageException('Error: Unauthorized Username for this ques', \
                    status_code=401))
            return response

        # Update all table entries with input data
        qzdb.Question.query.filter_by(qid = qid).update(dict(ques_text=ques_text, ans_text=ans_text))

        # Updating correspnoding relationship tables
        # Ans choices table 
        query_obj = qzdb.Anschoice.query.filter_by(qid = qid)
        index = 0
        for choice in query_obj:
            ansid = query_obj[index].ansid
            ans_choice = anschoices[index]["answer"]
            correct    = anschoices[index]["correct"]
            qzdb.Anschoice.query.filter_by(ansid = ansid).update(dict(ans_choice = ans_choice, correct = correct))  
            index += 1
        qzdb.db.session.commit()

        # Return response
        query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qid).all()
        response_fields = [{'name':'qid',  'relnshp':False, 'subfields':None}, 
                           {'name':'ques_text',  'relnshp':False, 
                            'subfields':None}, 
                           {'name':'ans_text','relnshp':False, 
                            'subfields':None},  
                           {'name':'qzid','relnshp':False, 
                            'subfields':None},  
                           {'name':'anschoices','relnshp':True, 
                            'subfields':[{'name':'ans_choice','relnshp':False,
                            'subfields':None},
                           {'name':'correct', 'relnshp':False, 'subfields':None}]} 
                          ] 
        question = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'question\':%s\n}" %(question)
        response = jsonify(question=question)
        response.status_code = 200
        utls.display_tables()
        return response

    # DELETE  /api/quizzes/{qzid}/questions/{qid}
    @basicauth.login_required
    def delete(self, qzid, qid):
        """Delete question"""
        print "_________________________________________________"
        print "QuestionAPI del fn: %s" %(request.url)

        # Check if user is auth to del this ques
        userid = utls.get_user_from_hdr()
        query_obj = Question.query.filter_by(qid=qid).first()
        if  (query_obj.userid != userid):
            response = handle_invalid_usage(InvalidUsageException('Error: Unauthorized Username for this ques', \
                    status_code=401))
            return response

        # Updating no_ques col in quiz table
        L = qzdb.Quiz.query.filter_by(qzid = qzid).first()
        qzdb.Quiz.query.filter_by(qzid = qzid).update(dict(no_ques= (L.no_ques-1)))

        # Deleting Ans choices table entries for qid
        qzdb.Anschoice.query.filter(qzdb.Anschoice.qid == qid).delete()

        # Finally deleting entries from Question table
        qzdb.Question.query.filter_by(qid = qid).delete()
        qzdb.db.session.commit()

        # Return response
        response = jsonify(qid=qid)
        response.status_code = 204
        utls.display_tables()
        return response


class AdmnUserAPI(Resource):
    """ Class that defines methods for processing post requests 
        for /api/users endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, required=True,
                             help="No username provided", location='json')
        self.reqparse.add_argument("password", type=str, required=True,
                             help="No password given", location='json')
        super(AdmnUserAPI, self).__init__()

    # POST /api/admnusers
    def post(self):
        """Add new user"""
        print "_________________________________________________"
        print "UserAPI post fn: %s\nJson Request\n=============\n %s" %(request, request.json)

        # Get values from request
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value is not None:
                if (key == 'username'):
                    username = request.json['username']
                if (key == 'password'):
                    password = request.json['password']

        # Update tables
        user_obj = qzdb.User(username)
        qzdb.db.session.add(user_obj)
        qzdb.db.session.commit()

        # Insert user and hashed pwd in hash table
        hashtbl.ht.insert_user(username, password)
        
        # Return response
        location = "/api/users/%s" % user_obj.userid
        query_obj = qzdb.User.query.filter_by(userid=user_obj.userid).all()
        response_fields = [{'name':'userid',  'relnshp':False, 'subfields':None}] 
        user = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'user\':%s\n}" %(user)
        response = jsonify(user=user)
        response.status_code = 201
        response.location = location
        utls.display_tables()
        return response

# Quiz test taker APIs - user - will move to a different file later

class UsrQuizzesAPI(Resource):
    """ Class that defines methods for processing get/post requests 
        for /api/quizzes endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """
    # GET /quizzes
    def get(self):
        """Get all quizzes"""
        print "_______________________________________________"
        print "QuizzesAPI get fn: %s" %(request)

        # Query from quiz table
        query_obj = qzdb.Quiz.query.order_by(qzdb.Quiz.qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: No quizzes found', status_code=404))
            return response

        # Return response
        response_fields = [{'name':'qzid', 'relnshp':False,'subfields':None},
                           {'name':'title','relnshp':False,'subfields':None}] 
        quizzes = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'quizzes\':%s}\n" %(quizzes)
        response = jsonify(quizzes=quizzes)
        response.status_code = 200
        utls.display_tables()
        return response

class UsrQuizAPI(Resource):
    """ Class that defines methods for processing get/patch/del requests 
        for /api/quizzes/<qzid> endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """

    # GET  /quizzes/{qzid}
    def get(self, qzid):
        """Get quiz details"""
        print "_________________________________________________"
        print "QuizAPI get fn: %s" %(request)

        # Query from quiz table
        query_obj = qzdb.Quiz.query.filter_by(qzid=qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: Quiz not found', status_code=404))
            return response

        # Return response
        response_fields = [{'name':'qzid', 'relnshp':False,'subfields':None},
                           {'name':'title','relnshp':False,'subfields':None}, 
                           {'name':'difficulty_level','relnshp':False,'subfields':None}, 
                           {'name':'text','relnshp':False,'subfields':None}, 
                           {'name':'no_ques','relnshp':False,'subfields':None}] 
        quiz = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'quiz\':%s}\n" %(quiz)
        response = jsonify(quiz=quiz)
        utls.display_tables()
        response.status_code = 200
        return response

class Session_(dict):
    pass

class UsrQuizRtAPI(Resource):

    # GET /quizzes/{qzid}/result
    def get(self, qzid, qid):
        """Get result for taker of this  quiz"""
        print "_________________________________________________"
        print "UsrQuizRtAPI get fn: %s" %(request)

        # Find quiz result for session
        cookie = request.headers['Cookie']
        if cookie:
            if cookie not in user_session:
                response = handle_invalid_usage(InvalidUsageException('Error: Unauthorized, Cookie not found', status_code=405))
            result = user_session[cookie]['no_correct_ans']

        # Return response
        print "Json response"
        print "=============\n"
        print "{\'result\':%s}\n" %(result)
        response = jsonify (result = result)
        response.status_code = 200
        return result

class UsrQuestionAPI(Resource):
    """ Class that defines methods for processing get/patch/del requests 
        for /api/quizzes/<qzid>/questions/<qid> endpoint 
    """

    def __init__(self):
        """ Uses RequestParser class of Flask restful to parse/validate
            flask.request 
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('anschoices', type=str, required=True,
                             help='No ans choice provided', location='json')
        super(UsrQuestionAPI, self).__init__()

    # GET  /quizzes/{qzid}/questions/{qid}
    def get(self, qzid, qid):
        """Get question qid for quiz"""
        print "_________________________________________________"
        print "QuestionAPI get fn: %s" %(request)

        # Create new user session for quiz on req for first ques 
        cookie = None
        query_obj = qzdb.Question.query.filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).first()
        if (query_obj.qid == qid):       # First question
            cookie = os.urandom(24)
            no_correct = 0
            user_session[cookie] = {'no_correct_ans':no_correct}

        # Query Question table
        query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: Question not found', status_code=404))
            return response

        # Return response
        response_fields = [{'name':'qid',  'relnshp':False, 'subfields':None}, 
                           {'name':'ques_text',  'relnshp':False, 'subfields':None}, 
                           {'name':'anschoices','relnshp':True, 
                            'subfields':[{'name':'ans_choice','relnshp':False,'subfields':None},
                           {'name':'correct', 'relnshp':False, 'subfields':None}]} 
                                  ] 
        question = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'question\':%s}\n" %(question)
        response = jsonify(question = question)
        response.status_code = 200
        if cookie:
            response.set_cookie(cookie)
        utls.display_tables()
        return response

    def post(self, qzid, qid):
        """Answer question of quiz"""
        print "_________________________________________________"
        print "QuestionAPI patch fn: %s \nJson Request\n=============\n %s" %(request, request.json)

        # Check if cookie user_session exists
        cookie = request.headers['Cookie']
        if cookie not in user_session:
            response = handle_invalid_usage(InvalidUsageException('Error: No cookie found ', status_code=401))
            return response

        # Check if question qid exists for qzid, raise error
        query_obj = qzdb.Question.query.filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).all()
        if not query_obj:
            response = handle_invalid_usage(InvalidUsageException('Error: Question to edit not found for ques', status_code=400))
            return response

        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value is not None:
                if (key == 'anschoices'):
                    anschoices = request.json['anschoices']

        # Comparing quiz taker answers with actual ans choices in db
        no_correct = 0
        correct = True
        query_obj = qzdb.Anschoice.query.filter_by(qid=qid)

        index = 0
        for choice in query_obj:
            if (query_obj[index].correct != anschoices[index]["correct"]):
                correct = False
            index += 1
        if correct:
            no_correct += 1
        user_session[cookie]={'no_correct_ans':no_correct}

        query_obj = qzdb.Question.query.join(qzdb.Anschoice).filter(qzdb.Question.qid == qid).all()
        location = "/quizzes/<int:qzid>/result %s" % qzid

        # Return response
        response_fields = [{'name':'qid',  'relnshp':False, 'subfields':None}, 
                           {'name':'ques_text',  'relnshp':False, 'subfields':None}, 
                           {'name':'ans_text','relnshp':False, 'subfields':None},  
                           {'name':'qzid','relnshp':False, 'subfields':None},  
                           {'name':'anschoices','relnshp':True, 
                               'subfields':[{'name':'ans_choice','relnshp':False,'subfields':None},
                                            {'name':'correct', 'relnshp':False, 'subfields':None}]} 
                          ] 
        question = utls.serialize_to_json(response_fields, query_obj)
        print "Json response"
        print "=============\n"
        print "{\'question\':%s\n}" %(question)
        response = jsonify(question=question)
        response.status_code = 200
        query_obj = qzdb.Question.query.filter(qzdb.Question.qid == qid,qzdb.Question.qzid == qzid).order_by(qid).all()
        last = query_obj.pop()
        if (last.qid == qid):
            response.location = location
            user_session.pop(cookie)
        utls.display_tables()
        return response

api.add_resource(AdmnQuizzesAPI, '/admin/quizzes')
api.add_resource(AdmnQuizAPI, '/admin/quizzes/<int:qzid>')
api.add_resource(AdmnQuestionsAPI, '/admin/quizzes/<int:qzid>/questions')
api.add_resource(AdmnQuestionAPI, '/admin/quizzes/<int:qzid>/questions/<int:qid>')

api.add_resource(UsrQuizzesAPI, '/quizzes')
api.add_resource(UsrQuizAPI, '/quizzes/<int:qzid>')
api.add_resource(UsrQuizRtAPI, '/quizzes/<int:qzid>/result')
api.add_resource(UsrQuestionAPI, '/quizzes/<int:qzid>/questions/<int:qid>')

api.add_resource(AdmnUserAPI, '/admnusers')

if __name__ == '__main__':

    #Initial config for db, this can be disabled
    qzdb.db_init()
    user_session = Session_()
    app.debug = True
    app.run('192.168.33.10', 5001)

