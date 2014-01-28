#----------Archana Bahuguna 12th jan 2014 ---------------

#Defining the factorial function non recursively

def nfact_nonrec(n):
   if n < 0:
      print "Factorial for negative noes is not defined"
      return 0
   elif n == 0:
      print "Factorial of zero (0!) is equal to:"
      return 1
   else:
      nfactorial = n
      for i in range(1,n):
         nfactorial=nfactorial*(n-i)
      print "Factorial is equal to:"
      return nfactorial

