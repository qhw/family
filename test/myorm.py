#!/usr/bin/python
import MySQLdb
from CONFIG import CONFIG
class ORM:
	def __init__(self):
		self.conn = MySQLdb.connect(host=CONFIG.HOST,user=CONFIG.USER,passwd=CONFIG.PASSWD,db=CONFIG.DB)
		self.cursor = self.conn.cursor()
		self.m_select = ""
		self.m_from = ""
		self.m_where = ""
		self.m_orderby = ""
		self.m_limit = ""

	def orm_query_1(self):
		self.sql = self.m_select + self.m_from + self.m_where + self.m_orderby + self.m_limit
		print self.sql
		return self.orm_query(self.sql)

	def orm_query(self, sql):
		return	(self.cursor.execute(sql), self.cursor.fetchall())

	def orm_select(self, m_select):
		self.m_select ="select " + m_select 
		return self
	
	def orm_from(self, m_from):
		self.m_from = " from " + m_from 
		return self

	def orm_where(self, m_where):
		self.m_where = " where"
		for key in m_where.keys():
			self.m_where +=" " + key + "='" + str(m_where[key]) +"' and"
		self.m_where = self.m_where[0:len(self.m_where)-4]
		return self

	def orm_limit(self, m_limit, offset=0):
		self.m_limit=" limit " + str(offset) +"," + str(m_limit)
		return self

	def orm_orderby(self, m_orderby, sort="asc"):
		self.m_orderby = " order by " + m_orderby +" " + sort
		return self

if __name__ == "__main__":
	orm = ORM()
	orm.orm_select("*")
	orm.orm_from("test")
	di = {'username':'dd'}
	orm.orm_where(di)
#	orm.orm_limit(2, 0)
	orm.orm_orderby("id", "desc")
	(num, results) =  orm.orm_query_1()
	for result in results:
		print result[1]
