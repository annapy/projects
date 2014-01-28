#file b.py
import a

print ("from b.py")

a.func()

if __name__ == "__main__":
    print ("b.py is being run directly")
else:
    print ("b.py is being imported by a different file")


