from flask import Flask, request
from flask import json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.restful.representations.json import output_json

app = Flask (__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/vagrant/projects/quizngn/arch.db'
db = SQLAlchemy(app)

#define MIN_NO_QUIZZES 0
#define MAX_NO_QUIZZES 100
#define MIN_NO_QUESTIONS 0
#define MAX_NO_QUESTIONS 1000

def gen_qzid():
    for index in range(1, 100, 1):
        yield index

g_qzid = gen_qzid()

def gen_quesid():
    for index in range(1, 1000, 1):
        yield index

g_qid = gen_quesid()

def gen_ansid():
    for index in range(1, 5000, 1):
        yield index

g_ansid = gen_ansid()

class Qz(db.Model):
    qzid             = db.Column(db.Integer, primary_key=True)
    title            = db.Column(db.String(80), unique = True)
    difficulty_level = db.Column(db.String(80))
    text             = db.Column(db.String(80))
    no_ques          = db.Column(db.Integer)

    questions = db.relationship("Qsn", backref = "qz")

    def __init__ (self, qzid, title, difficulty_level, text, no_ques):
        self.qzid = qzid
        self.title = title
        self.difficulty_level = difficulty_level
        self.text = text
        self.no_ques = no_ques

    def __repr__(self):
        return '\nQuiz: %i Title:%s Difficulty_level:%s Text:%s NumQ: %i' % (self.qzid, self.title, self.difficulty_level, self.text, self.no_ques)

class Qsn(db.Model):
    qid       = db.Column(db.Integer, primary_key=True)
    ques_text = db.Column(db.String(80), unique = True)
    ans_text  = db.Column(db.String(80))
    qzid      = db.Column(db.Integer, db.ForeignKey('qz.qzid'))

    anschoices = db.relationship("ACh", backref = "qsn")

    def __init__ (self, qid, ques_text, ans_text, qzid):
        self.qid  = qid
        self.ques_text = ques_text
        self.ans_text  = ans_text
        self.qzid = qzid

    def __repr__(self):
        return '\nQues %i. %s\nAns:%s\nqzid:%i' % (self.qid, self.ques_text, self.ans_text, self.qzid)

class ACh(db.Model):
    ansid      = db.Column(db.Integer, primary_key = True)
    quizid     = db.Column(db.Integer, db.ForeignKey('qz.qzid'))
    quesid     = db.Column(db.Integer, db.ForeignKey('qsn.qid'))
    ans_choice = db.Column(db.String(80))
    correct    = db.Column(db.Boolean)

    def __init__ (self, ansid, quizid, quesid, ans_choice, correct):
        self.ansid      = ansid
        self.quizid     = quizid
        self.quesid     = quesid
        self.ans_choice = ans_choice
        self.correct    = correct

    def __repr__(self):
        return '\nAns %i Quiz %i Ques %i:\n Choices %s Correct %r\n' % (self.ansid, self.quesid, self.quizid, self.ans_choice, self.correct)


def db_init():
    db.drop_all()
    db.create_all()

    qzid1 = g_qzid.next()
    qzid2 = g_qzid.next()
    qz1 = Qz(qzid1, "Python Basics", "Simple", "No text", 2)
    qz2 = Qz(qzid2, "Python Advanced", "Moderate", "No text", 0)
    db.session.add(qz1)
    db.session.add(qz2)
    db.session.commit()
    L = Qz.query.all()
    print "__________________ Quiz database _________________\n"
    for element in L:
        print element

    qid1 = g_qid.next()
    qid2 = g_qid.next()
    ques1 = Qsn(qid1, "What does the following code do? def foo(): pass", 
                      "You can define a function in python which does nothing",1)
    ques2 = Qsn(qid2, "Is python an Object oriented programming language?", 
                      "Yes python is an OOP language",1)
    db.session.add(ques1)
    db.session.add(ques2)
    db.session.commit()
    L = Qsn.query.all()
    print "__________________ Questions database _________________\n"
    for element in L:
        print element

    ansid1 = g_ansid.next()
    ansid2 = g_ansid.next()
    ansid3 = g_ansid.next()
    ans1  = ACh(ansid1, 1, 1, "a. This function does nothing", True)
    ans2  = ACh(ansid2, 1, 1, "b. This function returns a function called pass", False)
    ans3  = ACh(ansid3, 1, 1, "c. This function is not yet defined. It will give error", False)
    ansid4 = g_ansid.next()
    ansid5 = g_ansid.next()
    ansid6 = g_ansid.next()
    ans4  = ACh(ansid4, 1, 2, "a. Yes Python is object oriented", True)
    ans5  = ACh(ansid5, 1, 2, "b. No Python is not object oriented", False)
    ans6  = ACh(ansid6, 1, 2, "c. Python may or may not be used as an object oriented language", True)
    db.session.add(ans1)
    db.session.add(ans2)
    db.session.add(ans3)
    db.session.add(ans4)
    db.session.add(ans5)
    db.session.add(ans6)
    db.session.commit()
    L = ACh.query.all()
    print "___________________ Answers database __________________\n"
    for element in L:
        print element

    return None


'''
Trying this Archana ...
@api.representation('application/json')
def json(data, code, headers):
    resp = make_response(convert_data_to_xml(data), code)
    resp.headers.extend(headers)
    return resp
'''

def serialize_to_json(cols, query_result, frnkey_col):
    '''
    Serialize the query results into dict format so it can be
    converted to json format using jsonify fn
    '''
    import pdb; pdb.set_trace()
    result = []
    for i in query_result:
        record={}
        for col in cols:
            if (frnkey_col == 0): 
                record[col] = getattr(i, col)
            elif(col == cols[frnkey_col]):
                '''Serialzng data from other tables in query reslt
                   This is reqd when there is a 1 to many reltonship''' 
                x = getattr(i, col)
                frn_result = []
                index = 0
                for j in x:
                    frn_record = {}
                    for k in x[index].__table__.__dict__['columns'].keys():
                        frn_record[k] = getattr(x[index], k)
                    index += 1
                    frn_result.append(frn_record)
                record[col] = frn_result
        result.append(record)

    return result

'''
def serialize(model):
    SAMPLE CODE
     """Transforms a model into a dictionary which can be dumped to JSON."""
     # first we get the names of all the columns on your model
     columns = [c.key for c in class_mapper(model.__class__).columns]
     # then we return their values in a dict
     return dict((c, getattr(model, c)) for c in columns)

# we can then use this for your particular example
    serialized_labels = [
         serialize(label)
         for label in session.query(LabelsData).filter(LabelsData.deleted == False)
    ]
    your_json = dump(serialized_labels)
'''

class QuizzesAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type = str, required = True,
                             help = "*********No title given********", location = 'json')
        self.reqparse.add_argument("difficulty_level", type = str, required = True,
                             help = "No difficulty level set", location = 'json')
        self.reqparse.add_argument("text", type = str, required = True,
                             help = "text", location = 'json')
        self.reqparse.add_argument("no_ques", type = str,
                             help = "No questions given", location = 'json')
        super(QuizzesAPI, self).__init__()


    #GET /api/quizzes
    def get(self):
        '''Get all quizzes'''
        print "_______________________________________________"
        print "QuizzesAPI get fn: %s" %(request)
        cols = ['qzid','title', 'difficulty_level', 'text','no_ques']
        Query_obj = Qz.query.order_by(Qz.qzid).all()

        relnshp_flag = 0
        quizzes = serialize_to_json(cols, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'quizzes\':%s}\n' %(quizzes)
        response = jsonify(quizzes=quizzes)
        response.status_code = 200
        return response

    #POST /api/quizzes
    def post(self):
        '''Add new quiz'''
        print "_________________________________________________"
        print "QuizzesAPI post fn: %s" %(request)
        args = self.reqparse.parse_args()
        #print args.help
        for key, value in args.iteritems():
            if value != None:
                qzid  = g_qzid.next()
                title = request.json['title']
                difficulty_level = request.json['difficulty_level']
                text = request.json['text']
                '''Should no_ques be allowed here?'''
                no_ques = request.json['no_ques']
                Qz_obj = Qz(qzid, title, difficulty_level, text, no_ques)
                db.session.add(Qz_obj)
                db.session.commit()
                location = "/api/quizzes/"+str(qzid)
                Query_obj = Qz.query.filter_by(qzid=qzid).all()
                cols = ['qzid','title', 'difficulty_level', 'text','no_ques']
                relnshp_flag = 0
                quiz = serialize_to_json(cols, Query_obj, relnshp_flag)

                print "Json response"
                print "=============\n"
                print '{\'quiz\':%s\n}' %(quiz)
                response = jsonify(quiz=quiz)
                response.status_code = 201
                response.location = location
                print '{\'Response\':%s\n}' %(response)
                return response
                '''
                Archana - testing this
                import pdb; pdb.set_trace()
                response = output_json(quiz, 201, location)
                '''

class QuizAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type = str, required = True,
                             help = "*********No title given********", location = 'json')
        self.reqparse.add_argument("difficulty_level", type = str, required = True,
                             help = "No difficulty level set", location = 'json')
        self.reqparse.add_argument("text", type = str, required = True,
                             help = "text", location = 'json')
        self.reqparse.add_argument("no_ques", type = str,
                             help = "No questions given", location = 'json')
        super(QuizAPI, self).__init__()


    #GET  /api/quizzes/{qzid}
    def get(self, qzid):
        '''Get quiz details'''
        print "_________________________________________________"
        print "QuizAPI get fn: %s" %(request)
        cols = ['qzid','title', 'difficulty_level', 'text','no_ques']
        Query_obj = Qz.query.filter_by(qzid = qzid).all()
        relnshp_flag = 0
        quiz = serialize_to_json(cols, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'quiz\':%s}\n' %(quiz)
        response = jsonify(quiz=quiz)
        response.status_code = 200
        return response


    #PATCH /api/quizzes/{qzid}
    def patch(self, qzid):
        '''Edit quiz details'''
        print "_________________________________________________"
        print "QuizAPI patch fn: %s" %(request)
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value != None:
                qzid  = qzid
                title = request.json['title']
                difficulty_level = request.json['difficulty_level']
                text = request.json['text']
                no_ques = request.json['no_ques']
                Qz.query.filter_by(qzid = qzid).update(dict(title = title, difficulty_level= difficulty_level, text = text, no_ques=no_ques))
                db.session.commit()
                Query_obj = Qz.query.filter_by(qzid=qzid).all()
                cols = ['qzid','title', 'difficulty_level', 'text','no_ques']
                relnshp_flag = 0
                quiz = serialize_to_json(cols, Query_obj, relnshp_flag)

                print "Json response"
                print "=============\n"
                print '{\'quiz\':%s\n}' %(quiz)
                response = jsonify(quiz=quiz)
                response.status_code = 200
                return response

    #DELETE  /api/quizzes/{qzid}
    def delete(self, qzid):
        '''Delete quiz'''
        print "_________________________________________________"
        print "QuizAPI delete fn: %s" %(request)
        '''delete all questions for the quiz'''
        Qsn.query.join(Qz).filter(Qsn.qzid == qzid).delete()
        '''delete quiz'''
        Qz.query.filter(Qz.qzid == qzid).delete()
        db.session.commit()
        response = None
        response.status_code = 204
        return response

class QuestionsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("ques", type = str, required = True,
                             help = "No ques text provided", location = 'json')
        self.reqparse.add_argument("ans", type = str, required = True,
                             help = "No ans given", location = 'json')
        super(QuestionsAPI, self).__init__()

        relnshp_flag = 0

    #GET /api/questions/{qzid}/questions
    def get(self, qzid):
        '''Get all questions for quiz'''
        print "_________________________________________________"
        print "QuestionisAPI get fn: %s" %(request)
        import pdb; pdb.set_trace()
        Query_obj = Qsn.query.join(Qz).join(ACh).filter(Qz.qzid == qzid).all()
        cols = ['qid', 'qzid','ques_text', 'ans_text', 'anschoices'] 
        relnshp_flag = cols.index('anschoices')

        questions = serialize_to_json(cols, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'questions\':%s}\n' %(questions)
        response = jsonify(questions = questions)
        response.status_code = 200
        return response

    #POST /api/quizzes/{qzid}/questions
    def post(self, qzid):
        '''Add question to quiz'''
        print "_________________________________________________"
        print "QuestionsAPI post fn: %s" %(request)
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value != None:
                qid  = g_qid.next()
                ques = request.json['ques']
                ans = request.json['ans']
                qzid = request.json['qzid']
                qn_obj = Qsn(qid, ques, ans, qzid)
                db.session.add(qn_obj)
                '''Incrementing no of questions in respective quizdb'''
                L = Qz.query.filter_by(qzid = qzid).first()
                Qz.query.filter_by(qzid = qzid).update(dict(no_ques= (L.no_ques+1)))
                db.session.commit()
                location = "/api/quizzes/"+str(qzid)+"/questions/"+str(qid)

                Query_obj = Qsn.query.filter_by(qid = qid).all()
                cols = ['qid','ques', 'ans', 'qzid']
                relnshp_flag = 0
                questions = serialize_to_json(cols, Query_obj,relnshp_flag)
                print "Json response"
                print "=============\n"
                print '{\'questions\':%s}\n' %(questions)
                response = jsonify(questions = questions)
                response.location = location
                response.status_code = 201
                return response

class QuestionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ques', type = str, required = True,
                             help = 'No title given', location = 'json')
        self.reqparse.add_argument('ans', type = str, default = "",
                             help = 'No ans provided', location = 'json')
        '''
        self.reqparse.add_argument('qzid', type = str, default = "",
                             help = 'No quiz id given', location = 'json')
        '''
        super(QuestionAPI, self).__init__()

    #GET  /api/quizzes/{qzid}/questions/{qid}
    def get(self, qzid, qid):
        '''Get question qid for quiz'''
        print "_________________________________________________"
        print "QuestionAPI get fn: %s" %(request)
        Query_obj = Qsn.query.filter_by(qid = qid).all()
        cols = ['qid','ques', 'ans', 'qzid']
        relnshp_flag = 0
        question = serialize_to_json(cols, Query_obj, relnshp_flag)
        print "Json response"
        print "=============\n"
        print '{\'question\':%s}\n' %(question)
        response = jsonify(question = question)
        response.status_code = 200
        return response

    #PATCH /api/quizzes/{qzid}/questions/{qid}
    def patch(self, qzid, qid):
        '''Add question to quiz'''
        print "_________________________________________________"
        print "QuestionAPI patch fn: %s" %(request)
        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value != None:
                qid = qid
                ques = request.json['ques']
                ans = request.json['ans']
                qzid = request.json['qzid']
                L = Qsn.query.filter_by(qid = qid)
                Qsn.query.filter_by(qid = qid).update(dict(ques = ques, ans= ans, qzid=qzid))
                db.session.commit()
                Query_obj = Qsn.query.filter_by(qid = qid).all()
                cols = ['qid','ques', 'ans', 'qzid']

                relnshp_flag = 0
                quiz = serialize_to_json(cols, Query_obj, relnshp_flag)
                print "Json response"
                print "=============\n"
                print '{\'quiz\':%s\n}' %(quiz)
                response = jsonify(quiz=quiz)
                response.status_code = 200
                return response

    #DELETE  /api/quizzes/{qzid}/questions/{qid}
    def delete(self, qzid, qid):
        '''Delete quiz'''
        print "_________________________________________________"
        print "QuestionAPI del fn: %s" %(request.url)
        Qsn.query.filter_by(qid = qid).delete()
        '''decrementing no of questions in respective quizdb'''
        L = Qz.query.filter_by(qzid = qzid).first()
        Qz.query.filter_by(qzid = qzid).update(dict(no_ques= (L.no_ques-1)))
        db.session.commit()
        response = None
        response.status_code = 204
        return response

api.add_resource(QuizzesAPI, '/api/quizzes')
api.add_resource(QuizAPI, '/api/quizzes/<int:qzid>')
api.add_resource(QuestionsAPI, '/api/quizzes/<int:qzid>/questions')
api.add_resource(QuestionAPI, '/api/quizzes/<int:qzid>/questions/<int:qid>')

if __name__ == '__main__':
    db_init()
    app.debug = True
    app.run('192.168.33.10',5001)




