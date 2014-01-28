#---------------Archana Bahuguna 6th Jan 2014 -------------

#LIsts as stacks - push pop using list builtin functions
class stack:

    def __init__(self,L,index=0):
        self.L = L
        self.index = index

    def push(self,element):
        self.L.insert(element)
        seslf.index += 1
        return L

    def pop(self):
        element = self.L.pop()
        self.index -= 1
        return element
    
#LIsts as queues - push pop using list builtin functions
class queue:

    def __init__(self,L,index=0):
        self.L = L
        self.index = index

    def add(self,element):
        self.L.append(element)
        self.index += 1
        return L

    def delete(self):
        element = self.L.pop()
        self.index -= 1
        return element
        

#push, pop list functions

def Lpop(L):
#incomplete - L is mutable, so L address should not change
#Also what should I return here, just the last element? or the modified List itself
#Is there a way in python that we can pass address of parameters as args and modify 
 #them inside the fn like in C
    last = L[len(L)-1]
    L2 = [x for x in L if x < len(L)]
    return last
    
#sort list

def sortL(L):#incomplete
    # if 2^n elements are to be sorted in this manner, it should take n iterns:tbd
    # I am guessing this is binary sort
    #n = log(len(L))/log(2)....
    #while j <= n .....
    for x in range(len(L)-1):
        if (L[x]>L[x+1]):
            buff = L[x]
            L[x] = L[x+1]
            L[x+1] = buff
    #j++
    return L

# List comprehensions, for loops, iterations etc

def fnListComp1(L):
    print 'for element in L print element'
    for element in L:
        print element
    print 'for index in range(len(L))'
    for index in range(len(L)):
        print L[index]
    return None 

def fnDict1(Dict):
    for key in Dict:
        print key, Dict[key]
    return None

def fnTuple1(T):
    print 'for element in T print element'
    for element in T:
        print element
    print 'for index in range(len(T))'
    for index in range(len(T)):
        print T[index]
    return None

'''
for loop in execution - calls iter() and next()....
In [6]: str = "abcd"

In [7]: i = iter(str)

In [8]: i.next()
Out[8]: 'a'

In [9]: i.next()
Out[9]: 'b'

In [10]: i.next()
Out[10]: 'c'

In [11]: i.next()
Out[11]: 'd'

In [12]: i.next()
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-12-e590fe0d22f8> in <module>()
----> 1 i.next()

StopIteration:
'''
#More list comprehensions----
#---------------------------------------------------------------
def SqList(L):
    S = []
    for element in L:
       S.append(element**2)
    return S

#The same can be achieved by the following piece of code

def Sqlist2(L):
    S = [element**2 for element in L]
    return S
#---------------------------------------------------------------

#Write a fn to compare if 2 lists are equal or not 

def CheckIfEq(L1, L2):
     pass
#---------------------------------------------------------------

#Combine elements of 2 lists if they are not equal

def CombListsIfNotEq(L1, L2):
    L = []
    for x in L1:
        for y in L2:
            if x!= y:
                 L.append((x,y))
    return L            

#The above code can also be written as ...

def CombListsIfNotEq2(L1, L2):
    L = [(x,y) for x in L1 for y in L2 if x!=y]
    return L
#---------------------------------------------------------------

# filter the list to exclude negative numbers

def ExclNegFromList(L):
    L1 = [x for x in L if x >= 0]
    return L1

#Reverse a list in place (without using another list)-----------------------

def reverseList(L):
    for i in range(len(L)):
        L.insert(i,L.pop())
                

