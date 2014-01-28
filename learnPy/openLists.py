
def openlists(L, no_sublists):
    #no_sublists = len(returnedL)
    index = 0
    subindex = 0

    returnedL=[[],[]]

    while subindex < no_sublists:
        index = 0
        while index < len(L):
            if isinstance(L[index], list) is False:
                returnedL[subindex].append(L[index])
            else:
                returnedL[subindex].append(L[index][subindex])
            index += 1
        subindex += 1
   
    print "["
#    import pdb; pdb.set_trace()
    for i in range(len(returnedL)):
        for j in range(len(returnedL[i])):
            print returnedL[i][j],","
        print "]"
    print "]"

    return returnedL

openlists([1,6,[3,4]],2)
