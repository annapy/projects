import sqlite3
conn = sqlite3.connect('grocery.db')

c = conn.cursor()

#c.execute('SELECT * FROM grocery WHERE Price=2')
c.execute('SELECT * FROM grocery')

#Archana - Important note:
#To delete from grocery.db you need to commit and close conn
# Otherwise it will show the change temporarily but in the
#next run of py file, when you select * from grocery, it shows
#all data again......

#c.execute('DELETE FROM grocery WHERE VegetableId="Mangoes"')
#conn.commit()
#conn.close()

#c.execute('SELECT * FROM grocery')
L = c.fetchall()
print L
#c.execute("DELETE FROM grocery WHERE Price=2")
