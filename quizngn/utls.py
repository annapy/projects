from collections import OrderedDict
import qzdb

#def serialize_to_json(cols, query_result, frnkey_col):
def serialize_to_json(fields, query_result, a=0):
    '''
    Serialize the query results into dict format so it can be
    converted to json format using jsonify fn
    '''
    '''
    fields = [ {'name':'qid', 'relnshp':False, 'subfields':None},
               {'name':'qzid','relnshp':False,'subfields':None}},
               {'name':'anschoices', 'relnshp':True',
                                     'subfields':[fields...]}
             ]

    '''
    result = []
    import pdb; pdb.set_trace()
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

    
    '''
    result = []
    for i in query_result:
        record = OrderedDict()
        for col in cols:
            if ((frnkey_col == 0) | (col != cols[frnkey_col])): 
                record[col] = getattr(i, col)
            elif(col == cols[frnkey_col]):
                #Serialzng data from other tables in query reslt
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
        import pdb; pdb.set_trace()
      '''
    return result

def display_tables():
    ''' Displays db table entries after processing request '''
    prompt = '__________________________________________\nTo view tables enter Yes/yes/y/No/no/n:'
    i = raw_input(prompt)
    if i.lower() in ('yes','y'):
        import os
        os.system('clear')
        qry = qzdb.Quiz.query.all()
        print 'Quiz Table\n=============:\nQzid  Title         Difficulty Level   Text               No Ques\n'
        for i in qry:
            print i
        print '\n-----------------------------------------------------------'

        qry = qzdb.Question.query.all()
        print 'Questions Table\n================:\nQid Qzid               QText                    Ans Text\n'
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

