def foo2(index):
    index += 1
    print index
    return None 

def foo():
    print "From inside fn foo"
    var = 12
    import pdb; pdb.set_trace()
    foo2(var)
    print var
    return None

foo()
