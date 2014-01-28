#--------Archana Bahuguna 27 Dec 2013 -----------

#returns list with each element as the cube of elements in the input list

def cube (L):
    Cubed = []
    for i in range(len(L)):
          val = L[i]*L[i]*L[i]
          Cubed.append(val)
    return Cubed

if __name__ == "__main__":
    import sys
    cube(list(sys.argv[1]))
