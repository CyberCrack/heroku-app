import sqlite3
conn = sqlite3.connect('usadmissions.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT * FROM admissions;")
rows = cursor.fetchall()
print("ID\tGRE\tGPA\tRank\tAdmit")
for row in rows:
	print(row)