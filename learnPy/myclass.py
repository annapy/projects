#Archana Bahuguna 31st Dec 2013 --------------

class MyClassSelfdata:
    print "This is printed from MyClassSelfdata class with attribute index and function fn and self"
    index = 0

    def fn(self):
         print "This is printed from inside the fn inside the class MyClassSelfdata"
         self.list = [1,2,5]
         print "This is printed after data is initzed to a list and before self data print cmd"
         print self.list

    def __init__(self):
         print "This is printed from inside init fn MyClassSelfData"
         self.data = [6,8]
         print "This is printed from inside init before self data print cmd"
         print self.data


