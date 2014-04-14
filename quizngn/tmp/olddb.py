from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/vagrant/projects/quizngn/test.db'
db = SQLAlchemy(app)

class Quiz(db.Model):
    quizid           = db.Column(db.Integer,primary_key=True)
    title            = db.Column(db.String(80),unique = True)
    difficulty_level = db.Column(db.String(80))
    text             = db.Column(db.String(80),unique = True)
    no_questions     = db.Column(db.Integer)

    questions        = db.relationship("Question",  backref="quiz")
    anschoices       = db.relationship("AnsChoice", backref="quiz")

    def __init__(self, quizid, title, difficulty_level, text, no_questions):
        self.quizid = quizid
        self.title = title
        self.difficulty_level = difficulty_level
        self.text = text
        self.no_questions = no_questions

    def __repr__(self):
        return '                            \nQuiz %i: %s\nDifficulty level: %s\nDesc: %s\nNo of ques:%i\n_________________________________' % (self.quizid, self.title, self.difficulty_level, self.text, self.no_questions)

class Question(db.Model):
    quesid    = db.Column(db.Integer,primary_key=True)
    quizid    = db.Column(db.Integer,db.ForeignKey('quiz.quizid'))
    ques_text = db.Column(db.String(80))
    ans_text  = db.Column(db.String(80))

    anschoices       = db.relationship("AnsChoice", backref="question")

    def __init__(self, quesid, quizid, ques_text, ans_text):
        self.quesid = quesid
        self.quizid = quizid
        self.ques_text = ques_text
        self.ans_text = ans_text

    def __repr__(self):
        return '                            \nQuiz: %i\nQues: %i %s?\nAns :%s\n_________________________________' % (self.quizid, self.quesid, self.ques_text, self.ans_text)

class AnsChoice(db.Model):
    ansid     = db.Column(db.Integer, primary_key = True)
    quizid    = db.Column(db.Integer, db.ForeignKey('quiz.quizid'))
    quesid    = db.Column(db.Integer, db.ForeignKey('question.quesid'))
    ans_choice= db.Column(db.String(80))
    correct   = db.Column(db.Boolean)

    def __init__(self, ansid, quizid, quesid, ans_choice, correct):
        self.ansid = ansid 
        self.quizid = quizid
        self.quesid = quesid
        self.ans_choice = ans_choice
        self.correct = correct

    def __repr__(self):
        return '                            \nAns %i Quiz %i Ques %i:\n Ans choice:--\n%s %r\n_________________________________' % (self.ansid, self.quizid, self.quesid, self.ans_choice, self.correct)


if __name__ == '__main__':
    db.create_all()
    #import pdb; pdb.set_trace()
    qz_pythonb = Quiz(1, "Python Basics", "Moderate", "This quiz tests you on everything", 15)
    qz_pythona = Quiz(2, "Python Advanced", "Simple", "This quiz tests you on basics", 15)
    db.session.add(qz_pythonb)
    db.session.add(qz_pythona)
    db.session.commit()
    L = Quiz.query.all()
    for element in L:
        print element

    qs1_pythonb = Question(1, 1, "Is python object oriented?", "Yes, python is oo")
    qs2_pythonb = Question(2, 1, "Are C and python similar?", "There is a lot of diff")
    qs3_pythonb = Question(3, 2, "How do you reference a var?", "We do reference counting")
#    import pdb; pdb.set_trace()
    db.session.add(qs1_pythonb)
    db.session.add(qs2_pythonb)
    db.session.add(qs3_pythonb)
    db.session.commit()
    L = Question.query.all()
    for element in L:
        print element

    ans1        = AnsChoice(1, 1,1, "a. Yes Python is object oriented", True)
    ans2        = AnsChoice(2, 1,1, "b. No. Python is not object oriented", False)
    ans3        = AnsChoice(3, 1,1, "c. Python is both object oriented and modular", True)
#    import pdb; pdb.set_trace()
    db.session.add(ans1)
    db.session.add(ans2)
    db.session.add(ans3)
    db.session.commit()
    L = AnsChoice.query.all()
    for element in L:
        print element
    print "\n* * ===============  Queried rows  ================= * *"
#    Ques_lst1 = Question.query.filter_by(quizid=1)
#    for element in Ques_lst1:
#        print element
    print "\n* * ============= Query for QuizEngine DB  ========== * *"
    print "\n* * ************************************************* * *"
    #Get all Quizzes
    #Quizzes = Quiz.query.all()
    #Get Quiz 2
    #Quiz2 = Quiz.query.filter_by(quizid=2)
    #Get Question 1 from Quiz 1
    #Ques1ofQz1 = AnsChoice.query.join(Question).filter(Question.quesid==1).all()
    #for element in Ques1ofQz1:
    #    print element
    #Add Question to Quiz 1....................................
    qtxt = "How is garbage collection done in python?"
    anstxt = "A ref count is kept for ..."
    quesid = 4
    ansid = 4
    ansch1="a. No garbage collection is done in Python"
    correct1= False
    ansch2="b. We keep a count of number of times a var is used"
    correct2= True

    new_q = Question(quesid, 1, qtxt, anstxt)
    new_ansch1 = AnsChoice(ansid, 1, quesid, ansch1, correct1)
    ansid+=1
    new_ansch2 = AnsChoice(ansid, 1, quesid, ansch2, correct2)

    db.session.add(new_q)
    db.session.add(new_ansch1)
    db.session.add(new_ansch2)
    db.session.commit()

    L = Question.query.all()
    for element in L:
        print element
    L = AnsChoice.query.all()
    for element in L:
        print element


    db.drop_all()# doing this now so it doesnt give primary key error



