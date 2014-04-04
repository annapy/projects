#from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from rstflapi import app
import textwrap
import utls

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/vagrant/projects/quizngn/qz.db'
db = SQLAlchemy(app)

maxqz = 100
maxquestion = 10000
maxans = 50000
    
class Quiz(db.Model):
    """ Defines the columns and keys for Quiz table """
    qzid             = db.Column(db.Integer, primary_key=True)
    title            = db.Column(db.String(80), unique = True)
    difficulty_level = db.Column(db.String(80))
    text             = db.Column(db.String(80))
    no_ques          = db.Column(db.Integer)

    questions = db.relationship("Question", backref = "quiz")

    def generate_qzid():
        """Generator fn for unique quiz id"""
        for index in range(1, maxqz, 1):
            yield index

    gen_qzid = generate_qzid()

    def __init__ (self, title, difficulty_level, text, no_ques=0):
        self.qzid = self.gen_qzid.next()
        self.title = title
        self.difficulty_level = difficulty_level
        self.text = text
        self.no_ques = no_ques

    def __repr__(self):
        return '%i   %s     %s     %s     %i' % (self.qzid, self.title, self.difficulty_level, (self.text).ljust(20), self.no_ques)
                    

class Question(db.Model):
    """ Defines the columns and keys for Question table """
    qid       = db.Column(db.Integer, primary_key=True)
    ques_text = db.Column(db.String(80), unique = True)
    ans_text  = db.Column(db.String(80))
    qzid      = db.Column(db.Integer, db.ForeignKey('quiz.qzid'))

    anschoices = db.relationship("Anschoice", backref = "question")

    def generate_quesid():
        """Generator fn for unique ques id"""
        for index in range(1, maxquestion, 1):
            yield index

    gen_qid = generate_quesid()

    def __init__ (self, ques_text, ans_text, qzid):
        self.qid  = self.gen_qid.next()
        self.ques_text = ques_text
        self.ans_text  = ans_text
        self.qzid = qzid

    def __repr__(self):
        return '%i     %i          %s   %s' % (self.qid, self.qzid, self.ques_text, self.ans_text)

class Anschoice(db.Model):
    """ Defines the columns and keys for Answer Choices table """
    ansid      = db.Column(db.Integer, primary_key = True)
    qzid       = db.Column(db.Integer, db.ForeignKey('quiz.qzid'))
    qid        = db.Column(db.Integer, db.ForeignKey('question.qid'))
    ans_choice = db.Column(db.String(80))
    correct    = db.Column(db.Boolean)

    def generate_ansid():
        """Generator fn for unique ans id"""
        for index in range(1, maxans, 1):
            yield index

    gen_ansid = generate_ansid()

    def __init__ (self, qzid, qid, ans_choice, correct):
        self.ansid      = self.gen_ansid.next()
        self.qzid       = qzid
        self.qid        = qid
        self.ans_choice = ans_choice
        self.correct    = correct

    def __repr__(self):
        return '%i        %i     %i     %s      %r' % (self.ansid, self.qzid, self.qid, self.ans_choice, self.correct)


def db_init():
    """ Initial config/population of the database tables """

    #Using drop_all temporarily to prevent integrity error between
    #subsequent runs. If db_init is not called this can be removed.
    #this can also be called at the end of this fn
    db.drop_all()

    db.create_all()

    #populate Quiz table
    qz1 = Quiz( "Python Basics  ", "Simple  ", "Explanation", 2)
    qz2 = Quiz( "Python Advanced", "Moderate", "No text    ")
    db.session.add(qz1)
    db.session.add(qz2)
    db.session.commit()

    #populate Questions table
    ques1 = Question("What does 'def foo(): pass do", 
                      "A fn which does nothing",1)
    ques2 = Question("Is python an OOP l           ", 
                      "Yes python is an OOP l",1)
    db.session.add(ques1)
    db.session.add(ques2)
    db.session.commit()

    #populate Answer choices table
    ans1  = Anschoice(1, 1, "a. This function does nothing      ", True)
    ans2  = Anschoice(1, 1, "b. This function returns a fn pass ", False)
    ans3  = Anschoice(1, 1, "c. This function is not yet defined", False)
    ans4  = Anschoice(1, 2, "a. Yes Python is object oriented   ", True)
    ans5  = Anschoice(1, 2, "b. No Python is not object oriented", False)
    ans6  = Anschoice(1, 2, "c. Python may not be used as OOP l ", True)
    db.session.add(ans1)
    db.session.add(ans2)
    db.session.add(ans3)
    db.session.add(ans4)
    db.session.add(ans5)
    db.session.add(ans6)
    db.session.commit()

    utls.display_tables()

    return None


