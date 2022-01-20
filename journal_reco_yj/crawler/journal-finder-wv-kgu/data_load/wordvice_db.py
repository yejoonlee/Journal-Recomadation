import pymysql.cursors

class DB:
	db_host = 'wordvice-db.cimcf1c6lvo2.ap-northeast-1.rds.amazonaws.com'
	db_user = 'essayreview_beta'
	db_pass = 'beta'
	db_database = 'essayreview_beta'

	def __init__(self):
		self.conn = pymysql.connect(
			host=self.db_host,
			user=self.db_user,
			passwd=self.db_pass,
			charset='utf8',
			cursorclass=pymysql.cursors.DictCursor,
			db=self.db_database
		)

		self.cur = self.conn.cursor()

	def fetchall(self, query):
		self.cur.execute(query)
		return list(self.cur.fetchall())

	def listall(self, query):
		return list(self.fetchall(query))

DB = DB()