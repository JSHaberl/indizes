import sqlite3


genrange = range(500000)

con = sqlite3.connect("mydb.db")
cur = con.cursor()
cur.execute("CREATE TABLE personen(id, vorname, nachname)")

for x in genrange:
    cur.execute("INSERT INTO personen(vorname,nachname) VALUES(?, ?)", faker.name().split()) 
    con.commit()
    
    
print("Test")
