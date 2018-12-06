# -*- coding: utf-8 -*-   
import MySQLdb 

class Sql_Opt():
	def __init__(self):
		self.cursor = None

	def connect(self):
		self.db = MySQLdb.connect("localhost", "root", "12345678", "test", charset='utf8')
		self.cursor = self.db.cursor()

	def select(self,model,version):
		sql = 'SELECT version_number FROM edition where model="%s" AND version="%s";'%(model,version)
		#print sql
		self.cursor.execute(sql)
		data = self.cursor.fetchone()
		if data != None:
			return data[0]
		else: 	
			return None

	def insert(self,model,version,version_number):
		sql = 'INSERT INTO edition (version_number,model,version) VALUES ("%s","%s","%s");'
		param = (version_number,model,version)
		#print sql%param
		try:
			self.cursor.execute(sql%param)
			self.db.commit() 
			return True
		except BaseException:
			return False






