import sqlite3

class DBLink():
	
	def __init__(self):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		try:
			self.cursor.execute("CREATE TABLE USERS (NAME VARCHAR(20) UNIQUE)")
		except:
			pass

		try:
			self.cursor.execute("CREATE TABLE TODOTHINGS (USER VARCHAR(20), THING VARCHAR(50) UNIQUE, COMMENT VARCHAR(200))")
		except:
			pass

		self.connection.close()

	#
	#--------------- USERS -------------------------
	#

	def set_user(self, name):
		self.connection = sqlite3.connect("sqlite3.db")
		self.cursor = self.connection.cursor()

		#try:
		self.cursor.execute("INSERT INTO USERS VALUES (?)", (name,))
		# except:
		# 	print("Nombre de usuario ya existente")

		self.connection.commit()
		self.connection.close()

	def get_users(self):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		self.cursor.execute("SELECT * FROM USERS")
		users = self.cursor.fetchall()

		self.connection.commit()
		self.connection.close()

		return users

	def update_user(self, oldname, newname):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		self.cursor.execute("UPDATE USERS SET NAME=? WHERE NAME=?", (newname, oldname))
		self.cursor.execute("UPDATE TODOTHINGS SET USER=? WHERE USER=?", (newname, oldname))


		self.connection.commit()
		self.connection.close()

	def delete_user(self, name):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		self.cursor.execute("DELETE FROM USERS WHERE NAME=?", (name,))
		self.cursor.execute("DELETE FROM TODOTHINGS WHERE USER=?", (name,))


		self.connection.commit()
		self.connection.close()

	#
	#--------------- TODOTHINGS ----------------------
	#

	def set_todothing(self, todothing):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		self.cursor.execute("INSERT INTO TODOTHINGS VALUES(?,?,?)", todothing)

		self.connection.commit()
		self.connection.close()

	def get_todothings(self, user):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		self.cursor.execute("SELECT * FROM TODOTHINGS WHERE USER=?", (user,))
		todothings = self.cursor.fetchall()

		self.connection.commit()
		self.connection.close()

		return todothings

	def update_todothing(self, old_thing, new_thing, new_comment):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		self.cursor.execute("UPDATE TODOTHINGS SET THING=?, COMMENT=? WHERE THING=?", (new_thing, new_comment, old_thing))

		self.connection.commit()
		self.connection.close()

	def delete_todothing(self, thing):
		self.connection = sqlite3.connect("DB")
		self.cursor = self.connection.cursor()

		self.cursor.execute("DELETE FROM TODOTHINGS WHERE THING=?", (thing,))

		self.connection.commit()
		self.connection.close()
