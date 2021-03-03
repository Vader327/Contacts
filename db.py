import sqlite3
con = sqlite3.connect("database.db")
cur = con.cursor()
con.row_factory = sqlite3.Row

#cur.execute("INSERT INTO contacts (name,contact) VALUES (?,?)", ('Juan', 654321))
#on.commit()
rows = cur.execute("select * from contacts").fetchall()

for row in rows:
  print(row)

con.close()