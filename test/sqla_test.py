#!/usr/bin/python

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqldb://root:192052@localhost:3306/plan')
Session = sessionmaker(bind=engine)
session = Session()
engine.echo = True
Base = declarative_base()

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key = True)
	username = Column(String(50))
	password = Column(String(50))
	createtime = Column(DateTime)


if __name__ == "__main__":
	print User.__table__
	print User.__mapper__
	our_user = session.query(User).filter("id = 2").one()
	print our_user.username
	for user in our_user:
	  print user.username
