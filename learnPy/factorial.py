#--------Archana Bahuguna 12th Jan 2014 -------- 

#Writing a recursive function to call factorial

def nfactorial(n):
   if n < 0:
      print "Error: Factorial is not defined for negative noes"
      return 0
   if n > 0:
      nfact = n*nfactorial(n-1)
      return nfact
   else:
      print "The factorial value calculated is:"
      return 1

