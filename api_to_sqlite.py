from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
import sqlite3


######### CREATE DATABASE ###########
engine = create_engine('sqlite:///scf.db')

Base = declarative_base()

######### CREATE TABLE ###########
class Issues(Base):
    __tablename__ = "Issues"
    issueid = Column(Integer, primary_key=True)
    created_at = Column(String)
    summary = Column(String)
    address = Column(String)
Issues.__table__.create(bind=engine, checkfirst=True)

######### EXTRACT DATA FROM API ###########
import requests

url = "https://seeclickfix.com/api/v2/issues?"

issues_json = requests.get(url).json()

######### TRANSFORM ###########

issues = list()

for i, entry in enumerate(issues_json['issues']):
    row = {}
    row['issueid'] = i
    row['created_at'] = entry['created_at']
    row['summary'] = entry['summary']
    row['address'] = entry['address']
    issues.append(row)

######### LOAD ###########
Session = sessionmaker(bind=engine)
session = Session()

for issue in issues:
    row = Issues(**issue)
    session.add(row)
    
session.commit()

    



