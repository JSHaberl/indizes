import sqlite3
from faker import Faker

faker = Faker()
genbase = 500000

con = sqlite3.connect("mydb.db")
cur = con.cursor()
if input("Delete database?: ")  == ("Y" or "y"):
    cur.execute("DROP TABLE IF EXISTS personen")
con.commit()
cur.execute("CREATE TABLE IF NOT EXISTS personen(id, vorname, nachname)")

def generatedata(genrange: int,genmult: int = 1, first_namelist: list = [], last_namelist: list = []):
    fillcheck = cur.execute("SELECT COUNT(*) FROM personen").fetchall()[0][0]
    if genrange - fillcheck > 0:
        genrange -= fillcheck
        genrange = genrange / genmult
        genrange = int(genrange)
        for y in range(genmult):
            for x in range(genrange):
                cur.execute("INSERT INTO personen(vorname,nachname) VALUES(?, ?)", (faker.first_name() if y >= len(first_namelist) else first_namelist[y],faker.last_name() if y >= len(last_namelist) else last_namelist[y]))
        con.commit()

generatedata(genbase, 2, ["Joe"])

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
