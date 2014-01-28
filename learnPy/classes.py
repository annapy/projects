#-----------Archana Bahuguna 1st Jan 2014 ----------------------------------
# http://docs.python.org/2/tutorial/classes.html - 9.4 Random remarks ------


###--- Function defined outside a class, assigned inside a class begin ---###
class MyClass(object):
    def __init__(self,x):
        self.x = x
'''
[60]: id(MyClass.__init__)
Out[60]: 44383920

In [62]: obj = MyClass(1)

In [63]: id(obj.__init__)
Out[63]: 44383920

In [64]: id(MyClass.x)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-64-15a5baea3ba9> in <module>()
----> 1 id(MyClass.x)

AttributeError: class MyClass has no attribute 'x'

In [65]: id(obj.x)
Out[65]: 34535352

Comments --- 
             i. The address of MyClass function __init__ and its object instance
                obj point to the same address in MyClass object
            
            ii. MyClass object does not have an attribute x while its object
                instance obj has an attribute x that was created when its instance
                was created and __init__ was called.
'''

###--- Function defined outside a class, assigned inside a class begin ---###
def foo(self,x):
    self.x = x
    return None

class MyClass1(object):
    f = foo


###--- Function __init__ defined outside a class, assigned inside a class begin ---###
def __init__(self,x):
    self.x = x
    return None

class MyClass2(object):
    f = __init__

'''
In [24]: id(__init__)
Out[24]: 41278232

In [25]: id(MyClass2.f)
Out[25]: 39480208

In [26]: obj = MyClass2

In [27]: id(obj.f)
Out[27]: 39480208

In [28]: id(obj.x)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-28-cbc8019b4147> in <module>()
----> 1 id(obj.x)

AttributeError: class MyClass2 has no attribute 'x'

In [29]: obj.x
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-29-5ed0bfca07ee> in <module>()
----> 1 obj.x

AttributeError: class MyClass2 has no attribute 'x'

Comments:     1. The address diff between f and __init__ is understandable
                 because a new instance of __init__ is being created by the
                 assignment statement f = __init__
              2. It is not understood why obj.x is not defined once the object
                 instance obj of Class MyClass2 is created. Because if the
                 function __init__ were defined directly 'inside the class instead
                 of separately outside and assigned inside to f',obj.x would be 
                 immediately defined.
'''

###--- Function defined inside a class, assigned again inside a class ---###
class MyClass3(object):
    def foo(self,x):
        self.x = x
        return None
    f = foo

'''
In [46]: id(MyClass3.foo)
Out[46]: 39479808

In [47]: id(MyClass3.f)
Out[47]: 39479808

In [48]: obj = MyClass3()

In [49]: id(obj.foo)
Out[49]: 39479808

In [50]: id(obj.f)
Out[50]: 39479808

In [51]: obj.foo(1)

In [52]: id(obj.foo)
Out[52]: 39479808

In [53]: id(obj.f)
Out[53]: 39479808

In [54]: obj.x
Out[54]: 1

In [55]: id(obj.x)
Out[55]: 29886392

Comments:    So the function foo inside the class MyClass3 and f have the same address.
             That is not surprising. But when we create a new object instance of the
             class obj = MyClass3(), it also has 2 functions which point to the same
             location; and when obj.foo(1) is called it creates the instance attribute
             x in object obj. Interestingly, there is only one instance attribute x
             while there are actually 2 functions which actually point to the same
             address. So this kind of definition would have significance where?
            
             Why will we ever define a function inside a class and then assign that
             function to another attribute? (f = foo). Why would we ever do this?

Also another interesting observation:
Previously I had called obj.foo(1) to create an attribute x for object obj such that
obj.x = 1

In [51]: obj.foo(1)

In [59]: obj.x
Out[59]: 1

In [55]: id(obj.x)
Out[55]: 29886392


Now if I again call obj with the other function that is assigned to foo, f, with arg =11,
a new attribute x is created for object instance obj with value = 11 instead of the 
previously assigned 1 value.

In [60]: obj.f(11)

In [61]: obj.x
Out[61]: 11

In [62]: id(obj.x)
Out[62]: 29886152

Also note as is obvious in reassignment, that the address of obj.x has changed from 29886392 
to 29886152
'''


###--- Function defined inside a class, assigned again inside a class ---###
class MyClass4(object):
    def foo(self):
        return 'hello world'
    goo = foo

'''
In [64]: id (MyClass4.foo)
Out[64]: 39479808

In [65]: id (MyClass4.goo)
Out[65]: 39479808

In [66]: obj = MyClass4()

In [68]: obj.foo()
Out[68]: 'hello world'

In [69]: obj.goo()
Out[69]: 'hello world'

In [70]: id(obj.foo)
Out[70]: 39480048

In [71]: id(obj.goo)
Out[71]: 39480048

'''
