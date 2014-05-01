# ****************************************************************#
#
#        Archana Bahuguna       Apr 12 2014     Hash table
#
# This hash table may not work correctly for boundary values like
# 0 or 100 index of the hashtable - hasnt been tested thoroughly
# Also may not always generate a unique key
#
# ****************************************************************#

class hshtbl(object):
    """This is a basic implementation of a hash table with a hash
    table dict allowing 100 entries and any collisions are accodmdtd
    in a 10 entry bucket which is an extn of the hash tbl itself

    When a user is to be inserted, a hash is created on the username
    which returns a key (40) for the dict 

    The username and a hash_password value of the password(37) are then entered
    as the value for the key

    Example: Archana, helix@b! --> hashtbl{40:{'Archana':37}}
    """
    def __init__(self, bkt_index=0, len_tbl=100, len_bkt=10, shiftval=4):
        self.hashtbl = {}
        self.bkt_index = bkt_index
        self.len_tbl   = len_tbl
        self.len_bkt   = len_bkt
        self.shiftval  = shiftval 

    def get_bkt_index(self):
        return self.bkt_index

    def set_bkt_index(self, index):
        self.bkt_index = index
        return None

    def hash_password(self, password):
        """Method to use a hash algo to encrypt the passowrd
        The original password is never stored in a database/table
        This algo is very random, not recommended
        """

        i = 0
        # Hash algo on password
        for char in password:
            i += ord(char)
        encrypted_pwd = ((i<< self.shiftval) + 53)%97
        return encrypted_pwd

    def search_key_in_bkt(self, username):
        exists = False
        key = 0
        begin = self.len_tbl
        end   = self.len_tbl+self.len_bkt
        for bktkey in range(begin, end):
            if self.hashtbl.get(bktkey) and (username in self.hashtbl.get(bktkey)):
                exists = True
                key = bktkey
        return key, exists

    def search_key_in_ht(self, username):
        """Hash table is implemented as a dict of len 100 with a
        bucket of 10.  The algo for now is a bit random- it may not produce a unique 
        key
        """
        exists = False
        # Hash algo on username
        i = 0
        for char in username:
            i += ord(char)
        key = ((i>> self.shiftval) % self.len_tbl) 

        if self.hashtbl.get(key) and (username in self.hashtbl.get(key)):
            # key found in hash table
            exists = True
            print "Key %d found in hash table" % key
        return key, exists


    def get_key(self, username, password):
        """Insert data in hash table
        Normally password is never stored in a hash table for security
        reasons - the key is a hash-algrthm run on the password.
        """
        key,exists = self.search_key_in_ht(username)
        if exists:
            return key, exists
        elif self.hashtbl.get(key) and (username not in self.hashtbl.get(key)):
            # collision, search key in bkt
            key, exists = self.search_key_in_bkt(username)
            if exists:
                return key, exists
            else:
                key = self.len_tbl+self.get_bkt_index()
        return key, exists

    def insert_user(self, username, password):
        key, exists = self.get_key(username, password)
        if exists:
            print "Error inserting: Key exists in hashtbl"
        else:
            self.hashtbl[key]={username:self.hash_password(password)}
            print "\nSuccessful insert in hashtbl: %d %s" % (key, self.hashtbl[key])

    def verify_password(self, username, password):
        key, exists = self.get_key(username, password)
        if exists:
            if self.hash_password(password) == self.hashtbl[key][username]:
                print "\nAuthentication Success: Username password match %s" % username
                return True
            else:
                print "\nError: User %s cannot be authenticated-Password mismatch" % username
        else:
            print "\nError: User %s cannot be authenticated-Username  not found"% username
        return False

ht = hshtbl()

"""
if __name__ == '__main__':
    a = hshtbl()
    print"\n----------------Insert user:Arch---------------------------\n"
    a.insert_user("Archana","secret")
    # Test for duplicate key
    print"\n----------------Insert duplicate user Arch-----------------\n"
    a.insert_user("Archana","secret")
    # Test for collision-insert in bucket
    print"\n----------------Insert user collision----------------------\n"
    a.insert_user("Rachana","ubiquitous")
    #test for authorized pwd in hstbl
    print"\n----------------Authorize user Archana correct pwd --------\n"
    a.verify_password("Archana","secret")
    #test for authorized pwd in bkt
    print"\n---------------Authorize user in bkt-----------------------\n"
    a.verify_password("Rachana","ubiquitous")
    #test for pwd not matching
    print"\n---------------Password mismatch Rachana-------------------\n"
    a.verify_password("Rachana","biquitous")
    #test for user not found
    print"\n---------------User not found------------------------------\n"
    a.verify_password("Beyonce","lotus")
    print a.hashtbl
"""
