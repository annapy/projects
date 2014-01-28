import sqlite3
dataBase = '/home/vagrant/projects/pgdb/cfg/testAB.db'

class dBase(object):

    def __init__(self, db, conn=None, cur=None, view=None):
        self.conn = sqlite3.connect(db)
        self.cur  = conn.cursor()
        if view == None:
            view = []

    def sqlfunc(sql_str):
        self.cur.execute(sql_str)
        self.viewL = self.cur.fetchall()
        print self.viewL
        self.conn.commit()
        return None

    def cfg():
        self.cur.execute('''CREATE TABLE grocery (VegId,price,Qty,Wt,OrderQty)''')
        self.cur.execute("INSERT INTO grocery VALUES ('Tomato',2,100,20,25)")
        self.cur.execute("INSERT INTO grocery VALUES ('Potato',2,100,20,25)")
        self.viewL = self.cur.fetchall()
        print self.viewL
        self.conn.commit()
        return None

    def close():
        self.conn.close()
        return None


grocerydb = dBase(dataBase)
grocerydb.cfg()

    

#Archana - It is important to commit at the end (also close?)

#Create Table
#c.execute ('''CREATE TABLE grocery 
#         ( VegetableId,Price,Quantity,Weight,OrderedQty)''')


# Insert row of data
#c.execute("INSERT INTO grocery VALUES ('Tomato',2,100,20,25)")

#c.execute("INSERT INTO grocery VALUES ('Potato',3,150,20,40)")

#c.execute("INSERT INTO grocery VALUES ('Onion',2,50,20,0)")

#c.execute("INSERT INTO grocery VALUES ('Garlic',1,100,20,25)")

#c.execute("INSERT INTO grocery VALUES ('Ginger',2,20,20,0)")

#moredata = [('Oranges',3,200,100,24),
#            ('Mangoes',4, 300, 120, 60)]

#c.executemany('INSERT INTO grocery VALUES (?,?,?,?,?)',moredata)


# Save changes
#conn.commit()

#conn.close()
