#Archana Bahuguna 10th Jan 2014 --------------------

# Understanding the difference between __init__ and __call__

# __call__ function is called when the object instance is called
# so if you create an instance of object test like this->
# obj = test(100)
# __init__ will be called and obj.val will be defined
# but only when obj(1,2,x='A',y='B') is called will the
# __call__ method be called and the values args and kwargs
# be added as attributes to the instance obj

class test(object):
  "Class test: This is a doc string for this class"

  x = 10

  def __init__(self, val):
     self.val = 100
     print "inside __init__ method"

  def __call__(self,*args, **kwargs):
     print "inside __call__ method:"
     print "This fn is called when the class object instance is called"
     self.args = args
     self.kwargs = kwargs
