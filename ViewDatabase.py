import os

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT * FROM admissions;")
rows = cursor.fetchall()
print("ID\tGRE\tGPA\tRank\tAdmit")
for row in rows:
	print(row)
