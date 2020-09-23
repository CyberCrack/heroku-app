import psycopg2
import os
import DeployableModel

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()


def checkDatabaseExists():
	sql = "SELECT to_regclass('admissions');"
	cursor.execute(sql)
	if cursor.fetchone()[0] == 'admissions':
		return True
	else:
		return False


def createDatabase():
	sql = '''CREATE TABLE admissions(
	   id SERIAL PRIMARY KEY ,
	   gre INTEGER NOT NULL,
	   gpa REAL NOT NULL,
	   student_rank INTEGER NOT NULL,
	   admit INTEGER
	)'''
	cursor.execute(sql)
	conn.commit()


def insertData(gre, gpa, student_rank, admit):
	cursor.execute("INSERT INTO admissions (gre,gpa,student_rank,admit) VALUES ( %s, %s, %s, %s	)", (gre, gpa, student_rank, admit))
	recent_id = str(getRecentID())
	cursor.execute("INSERT INTO student_login (username,student_password) VALUES ( %s, %s )", ("student" + recent_id, "student" + recent_id))
	conn.commit()


def deleteData(id):
	cursor.execute("DELETE FROM admissions WHERE id=%s", (id,))
	cursor.execute("DELETE FROM student_login WHERE id=%s", (id,))
	conn.commit()


def getRecentID():
	cursor.execute("SELECT last_value FROM admissions_id_seq;")
	return cursor.fetchone()[0]


def updateGPA(gpa, id):
	cursor.execute("UPDATE admissions SET gpa = %s WHERE id = %s", (gpa, id))

	conn.commit()
	return cursor.rowcount


def updategre(gre, id):
	cursor.execute("UPDATE admissions SET gre = %s WHERE id = %s", (gre, id))

	conn.commit()
	return cursor.rowcount


def updaterank(rank, id):
	cursor.execute("UPDATE admissions SET student_rank = %s WHERE id = %s", (rank, id))

	conn.commit()
	return cursor.rowcount


def updateadmit(id):
	cursor.execute("SELECT gre,gpa,student_rank FROM admissions WHERE id=%s", (id,))
	gre, gpa, rank = cursor.fetchone()
	admit = DeployableModel.getPredictions(gre=gre, gpa=gpa, rank=rank)
	cursor.execute("UPDATE admissions SET admit = %s WHERE id = %s", (admit, id))
	conn.commit()


def getRecord(id):
	cursor.execute("SELECT id,gre,gpa,student_rank FROM admissions WHERE id=%s", (id,))
	if cursor.rowcount == 1:
		stud_id, gre, gpa, rank = cursor.fetchone()
		return {"id": stud_id, "gre": gre, "gpa": gpa, "rank": rank}
	else:
		return "ID does not exist"


def verifyCredentials(data):
	cursor.execute("SELECT id FROM student_login WHERE username=%s and student_password=%s and id=%s",
				   (data['username'], data['password'], data['id']))

	return cursor.rowcount == 1


exists = checkDatabaseExists()
if not exists:
	createDatabase()
