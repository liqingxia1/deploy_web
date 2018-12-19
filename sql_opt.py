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

#
# conn = Sql_Opt()
# conn.connect()
# print conn.insert("C10", "v2.1.3", "C10_NCA_v2.1.3_201812141421_user")
# print conn.insert("C10", "v2.1.4", "C10_KHM_v2.1.4_201812141235_user")
# print conn.insert("C8", "v2.1.11", "C8_NCA_MSM8976_v2.1.11_201812132237_user")
# print conn.insert("C8", "v2.1.12", "C8_KHM_MSM8976_v2.1.12_201812132047_user")
# print conn.insert("CPE02", "v1.1.35", "CPE02_C_KHM_V1.1.35_2018121215_TR_user")



