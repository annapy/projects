#file a.py

def func():
    print("func() is in a.py")

print ("from a.py")

if __name__ == "__main__":
    print ("a.py is being run directly")
else:
    print ("a.py is being imported by a different file")


