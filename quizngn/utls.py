from collections import OrderedDict
from flask import request
import qzdb

def get_user_from_hdr():
    auth = request.headers.get('Authorization')
    username = ((auth.rsplit().pop()).rsplit(':')).pop(0)
    user_obj = qzdb.User.query.filter_by(username=username).first()
    userid = user_obj.userid
    return userid

def serialize_to_json(fields, query_result, a=0):
    """
    Serialize the query results into dict format so it can be
    converted to json format using jsonify fn
    """
    result = []
    for i in query_result:
        record = OrderedDict()
        for field in fields:
            if (field['relnshp']):
                x = getattr(i, field['name'])
                record[field['name']] = serialize_to_json(
                                              field['subfields'], 
                                              x)
            else:
                record[field['name']] = getattr(i, field['name'])
        result.append(record)

    return result

def display_tables():
    """ Displays db table entries after processing request """
    prompt = '__________________________________________\nTo view tables enter Yes/yes/y/No/no/n:'
    i = raw_input(prompt)
    if i.lower() in ('yes','y'):
        import os
        os.system('clear')
        qry = qzdb.User.query.all()
        print 'User Table\n=============:\nUserid Username \n'
        for i in qry:
            print i
        print '\n-----------------------------------------------------------'

        qry = qzdb.Quiz.query.all()
        print 'Quiz Table\n=============:\nQzid  Title         Difficulty Level   Text                Userid  No Ques\n'
        for i in qry:
            print i
        print '\n-----------------------------------------------------------'

        qry = qzdb.Question.query.all()
        print 'Questions Table\n================:\nQid Qzid               QText                    Ans Text   Userid\n'
        for i in qry:
            print i
        print '\n-----------------------------------------------------------'

        qry = qzdb.Anschoice.query.all()
        print 'Ans Choices Table\n================:\nAnsid  Qzid  Qid         Choices                               Correct\n'
        for i in qry:
            print i
        print '\n-----------------------------------------------------------'
    else:
        pass
    return None

