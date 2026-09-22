import sqlite3
from faker import Faker

faker = Faker()
genbase = 500000
genvalue = genbase

con = sqlite3.connect("mydb.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS personen(id, vorname, nachname)")
fillcheck = cur.execute("SELECT COUNT(*) FROM personen").fetchall()[0][0]

print(fillcheck)

if genvalue - fillcheck > 0:
    genvalue -= fillcheck
    for x in range(genvalue):
        cur.execute("INSERT INTO personen(vorname,nachname) VALUES(?, ?)", (faker.first_name(), faker.last_name()),)
    con.commit()

cur.execute("CREATE INDEX IF NOT EXISTS idx_fullname ON personen (vorname, nachname) ")
if input() == ("Y" or "y"):
    cur.execute("DROP INDEX idx_fullname")
con.commit()
    
uniquenames = cur.execute("SELECT DISTINCT(concat(vorname, ' ', nachname)) FROM personen").fetchall()
uniquenamestotal = len(uniquenames)
uniquenamescount = cur.execute("SELECT COUNT(*) FROM personen GROUP BY concat(vorname, ' ', nachname)").fetchall()
avg = genbase / uniquenamestotal
summe = 0
for x in range(uniquenamestotal):
   summe += (uniquenamescount[x][0] - avg)**2

print(f"Varianz: {summe/genbase}")
con.close()
