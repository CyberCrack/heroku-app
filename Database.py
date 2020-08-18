import os
import sqlite3

import DeployableModel

databaseExits = True
if not os.path.exists("usadmissions.db"):
	databaseExits = False
conn = sqlite3.connect('usadmissions.db', check_same_thread=False)
cursor = conn.cursor()


def createDatabase():
	sql = '''CREATE TABLE admissions(
	   id INTEGER PRIMARY KEY AUTOINCREMENT,
	   gre INTEGER NOT NULL,
	   gpa REAL NOT NULL,
	   student_rank INTEGER NOT NULL,
	   admit INTEGER
	)'''
	cursor.execute(sql)


def insertData(gre, gpa, student_rank, admit):
	cursor.execute("INSERT INTO admissions (gre,gpa,student_rank,admit) VALUES ( ?, ?, ?, ?	)", (gre, gpa, student_rank, admit))
	conn.commit()


def deleteData(id):
	cursor.execute("DELETE FROM admissions WHERE id=?", (id,))
	conn.commit()


def getRecentID():
	cursor.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name='admissions';")
	return cursor.fetchall()[0][0]


if not databaseExits:
	createDatabase()


def updateGPA(gpa, id):
	cursor.execute("UPDATE admissions SET gpa = ? WHERE id = ?", (gpa, id))

	conn.commit()
	return cursor.rowcount


def updategre(gre, id):
	cursor.execute("UPDATE admissions SET gre = ? WHERE id = ?", (gre, id))

	conn.commit()
	return cursor.rowcount


def updaterank(rank, id):
	cursor.execute("UPDATE admissions SET student_rank = ? WHERE id = ?", (rank, id))

	conn.commit()
	return cursor.rowcount


def updateadmit(id):
	cursor.execute("SELECT gre,gpa,student_rank FROM admissions WHERE id=?", (id,))
	gre, gpa, rank = cursor.fetchone()
	admit = DeployableModel.getPredictions(gre=gre, gpa=gpa, rank=rank)
	cursor.execute("UPDATE admissions SET admit = ? WHERE id = ?", (admit, id))
	conn.commit()


def deleteRecord(id):
	cursor.execute("UPDATE admissions SET student_rank = ? WHERE id = ?", (id,))

	conn.commit()
	return cursor.rowcount
