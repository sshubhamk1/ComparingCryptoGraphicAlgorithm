import sqlite3

def insert_into_database(firstName,lastName,email,password):
	return_value=True
	try:
		conn= sqlite3.connect('students.db')
		c = conn.cursor()
		#c.execute("CREATE TABLE students ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'Firstname' TEXT,'lastName' TEXT,'email' TEXT UNIQUE, 'password' TEXT,'cookie' TEXT)")
		c.execute("INSERT INTO students ('firstName', 'lastName','email','password') VALUES ('%s','%s','%s','%s')"%(firstName,lastName,email,password))
		#c.execute("DROP TABLE students")
	except Exception:
		return_value =False
	conn.commit()
	conn.close()
	return return_value

def compare_credentials(email,password):
	conn = sqlite3.connect('students.db')
	c = conn.cursor()
	try:
		c.execute("SELECT email,password FROM students WHERE email=='%s' AND password=='%s'"%(email,password))
		results = c.fetchall()
		conn.commit()
		conn.close()
	except Exception:
		return False
	if(len(results)==1):
		print results
		if((results[0][0]==email) and (results[0][1]==password)):
			return True
	return False


def update_credentials(data,email):
	conn = sqlite3.connect('students.db')
	c=conn.cursor()
	try:
		c.execute("UPDATE students set cookie='%s' where email='%s'"%(data,email))
		conn.commit()
		conn.close()
		return True
	except Exception:
		return False
