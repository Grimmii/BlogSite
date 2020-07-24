import sqlite3
import os
import csv
from scripts.DB.Tables import CSVPARAM as csvparameter
# USRADM table details :
#   USRUSRID   : Userid - PM
#   USRUSRNM   : username
#   USRFULLNM  : full name
#   USRUSRPASS : User's password
#   USRIMGURL : Image url

CONTENT_PATH = './scripts/DB/Tables/Content/'
CSV_USR = 'USRADM.csv'
USRADM_FULLPATH = CONTENT_PATH+CSV_USR
DEFAULT_IMGURL = 'https://upload.wikimedia.org/wikipedia/en/e/e0/WPVG_icon_2016.svg'

SCRIPT_CREATE ='CREATE TABLE USRADM (USRUSRID integer PRIMARY KEY'
SCRIPT_CREATE+=', USRUSRNM VARCHAR(32)'
SCRIPT_CREATE+=', USRFULLNM TEXT'
SCRIPT_CREATE+=', USRUSRPASS VARCHAR(8) '
SCRIPT_CREATE+=', USRIMGURL TEXT'
SCRIPT_CREATE+=')'

def USRADM_init(db):
    #Create table
    USRADM_create(db)
    #insert table content
    with open(USRADM_FULLPATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=csvparameter.CSV_DELMITER, quotechar=csvparameter.CSV_QUOTE, quoting=csv.QUOTE_MINIMAL,skipinitialspace=True)
        id = 0
        for row in csv_reader:
            if len(row) == 4:
                id +=1
                USRADM_insert(db,id,row[0],row[1],row[2],row[3])

def USRADM_create(db):
    c = db.cursor()
    c.execute(SCRIPT_CREATE)
    db.commit()

def USRADM_insert(db,id,username,fullname,password,imgurl=DEFAULT_IMGURL):
    c = db.cursor()
    c.execute('INSERT INTO USRADM (USRUSRID, USRUSRNM, USRFULLNM, USRUSRPASS,USRIMGURL) VALUES (?,?,?,?,?)',(id,username,fullname,password,imgurl))
    db.commit()

def USRADM_newRecord(db,id,username,fullname,password,imgurl=DEFAULT_IMGURL):
    with open(USRADM_FULLPATH,'a') as csvfile:
        # csvfile.write(username+','+fullname+','+password+','+imgurl+"\n")
        writer = csv.writer(csvfile, delimiter=csvparameter.CSV_DELMITER, quotechar=csvparameter.CSV_QUOTE, quoting=csv.QUOTE_MINIMAL)
        writer.writerows([[username, fullname,password,imgurl]])
    id = USRADM_generateid(db)
    USRADM_insert(db,id,username,fullname,password,imgurl)

def USRADM_generateid(db):
    c = db.cursor()
    c.execute('SELECT MAX(USRUSRID)+1 FROM USRADM')
    return c.fetchall()[0][0]

def USRADM_getUserProfile(db,userid):
    c = db.cursor()
    EXE_SCRIPT= 'SELECT USRUSRID,USRFULLNM,USRIMGURL '
    EXE_SCRIPT+='  FROM USRADM '
    EXE_SCRIPT+=' WHERE USRUSRID = ' + str(userid)
    c.execute(EXE_SCRIPT)
    result = c.fetchall()
    return result

def USRADM_usernameexists(db, username):
    c = db.cursor()
    c.execute('SELECT 1 FROM USRADM WHERE USRUSRNM = (?)', (username,))
    return len(c.fetchall()) > 0

def USRADM_getUserIdByUsername(db, username):
    c = db.cursor()
    c.execute('SELECT USRUSRID FROM USRADM WHERE USRUSRNM = (?) ', (username,))
    userId = c.fetchall()[0][0]
    return userId

def USRADM_getPasswordByUserId(db, userid):
    c = db.cursor()
    c.execute('SELECT USRUSRPASS FROM USRADM WHERE USRUSRID = (?)', (userid,))
    password = c.fetchall()[0][0]
    return password

def USRADM_fetchUserIDBySearchTerm(db, searchTerm):
    searchTerm = searchTerm.split()
    c = db.cursor()
    EXE_SCRIPT= 'SELECT USRUSRID FROM USRADM '
    EXE_SCRIPT+=' WHERE '
    if len(searchTerm) == 0:
        EXE_SCRIPT += ' 1=1 '
    else:
        EXE_SCRIPT += ' USRFULLNM LIKE ' + "'%"+  searchTerm[0]  + "%' "
        if len(searchTerm) > 1:
            for i in range(1,len(searchTerm)):
                EXE_SCRIPT += ' OR  USRFULLNM LIKE ' + "'%"+  searchTerm[i]  + "%' "
    EXE_SCRIPT+='  ORDER BY USRFULLNM ASC  '
    EXE_SCRIPT+='  LIMIT 7  '
    c.execute(EXE_SCRIPT)
    result = c.fetchall()
    return result
