import sqlite3
import os
import csv
import time
from datetime import datetime
from scripts.DB.Tables import CSVPARAM as csvparameter
# USRPST table details :
#   UPTPSTID   : Post id - PM
#   UPTUSRID   : user id - FM --> USRADM's USRUSRID
#   UPTCONTENT : Content
#   UPTPSTTIME : Post date time

CONTENT_PATH = './scripts/DB/Tables/Content/'
CSV_POST = 'USRPST.csv'
USRPST_FULLPATH = CONTENT_PATH+CSV_POST
DATETIME_FORMAT = '%Y%m%d %H:%M:%S'

SCRIPT_CREATE ='CREATE TABLE USRPST (UPTPSTID integer PRIMARY KEY'
SCRIPT_CREATE+=', UPTUSRID integer '
SCRIPT_CREATE+=', UPTCONTENT TEXT'
SCRIPT_CREATE+=', UPTPSTTIME DATETIME'
SCRIPT_CREATE+=', FOREIGN KEY(UPTUSRID) REFERENCES USRADM(USRUSRID)'
SCRIPT_CREATE+=')'

def USRPST_init(db):
    #Create table
    USRPST_create(db)
    #insert table content
    with open(USRPST_FULLPATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=csvparameter.CSV_DELMITER, quotechar=csvparameter.CSV_QUOTE,)
        id = 0
        for row in csv_reader:
            if len(row) == 3:
                id +=1
                USRPST_insert(db,id,row[0],row[1],row[2])

def USRPST_create(db):
    c = db.cursor()
    c.execute(SCRIPT_CREATE)
    db.commit()

def USRPST_insert(db,id,usrid,content,timestr):
    c = db.cursor()
    c.execute('INSERT INTO USRPST (UPTPSTID, UPTUSRID, UPTCONTENT, UPTPSTTIME) VALUES (?,?,?,?)',(id,usrid,content,timestr))
    db.commit()

def USRPST_newRecord(db,usrid,content):
    datetimestr = datetime.now().strftime(DATETIME_FORMAT)
    with open(USRPST_FULLPATH,'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=csvparameter.CSV_DELMITER, quotechar=csvparameter.CSV_QUOTE, quoting=csv.QUOTE_MINIMAL)
        writer.writerows([[usrid, content,datetimestr]])
    id = USRPST_generateid(db)
    USRPST_insert(db,id,usrid,content,datetimestr)

def USRPST_generateid(db):
    c = db.cursor()
    c.execute('SELECT MAX(UPTPSTID)+1 FROM USRPST')
    return c.fetchall()[0][0]

#Query

def fetchAllPost(db):
    c = db.cursor()
    QUERY = 'SELECT USRFULLNM name , UPTCONTENT msg, UPTPSTTIME posttime, USRIMGURL img'
    QUERY+= '  FROM USRPST , USRADM '
    QUERY+= ' WHERE UPTUSRID = USRUSRID '
    QUERY+= ' ORDER BY UPTPSTTIME DESC '
    c.execute(QUERY)
    return c.fetchall()

def fetchPostByUserId(db,userid):
    c = db.cursor()
    QUERY = 'SELECT USRFULLNM name , UPTCONTENT msg, UPTPSTTIME posttime, USRIMGURL img'
    QUERY+= '  FROM USRPST , USRADM '
    QUERY+= ' WHERE UPTUSRID = ' + str(userid)
    QUERY+= '   AND UPTUSRID = USRUSRID '
    QUERY+= ' ORDER BY UPTPSTTIME DESC '
    c.execute(QUERY)
    return c.fetchall()
