import sqlite3
import os
import csv

# USRLGNTKN table details :
#   UTKUTKID   : login token id - PM
#   UTKUSRID   : userid - FM
#   UTKLGNTKN  : Login token

SCRIPT_CREATE ='CREATE TABLE USRLGNTKN (UTKUTKID integer PRIMARY KEY'
SCRIPT_CREATE+=', UTKUSRID integer'
SCRIPT_CREATE+=', UTKLGNTKN VARCHAR(32)'
SCRIPT_CREATE+=', FOREIGN KEY(UTKUSRID) REFERENCES USRADM(USRUSRID)'
SCRIPT_CREATE+=')'

def USRLGNTKN_init(db):
    #Create table
    USRLGNTKN_create(db)

def USRLGNTKN_create(db):
    c = db.cursor()
    c.execute(SCRIPT_CREATE)
    db.commit()

def USRLGNTKN_insert(db,id,userid,token):
    c = db.cursor()
    c.execute('INSERT INTO USRLGNTKN (UTKUTKID, UTKUSRID, UTKLGNTKN) VALUES (?,?,?)',(id,userid,token))
    db.commit()

def USRLGNTKN_update(db,userid,token):
    c = db.cursor()
    c.execute('UPDATE USRLGNTKN SET UTKLGNTKN = ?  WHERE UTKUSRID = ?',(token,userid))
    db.commit()

def USRLGNTKN_newRecord(db,userid,logintoken):
    #If user exist, update user's login token
    if USRLGNTKN_entryExist(db,userid):
        USRLGNTKN_update(db,userid,logintoken)
    else:
        id = USRLGNTKN_generateid(db)
        USRLGNTKN_insert(db,id,userid,logintoken)

def USRLGNTKN_getUserIDByToken(db,token):
    c = db.cursor()
    c.execute('SELECT UTKUSRID FROM USRLGNTKN WHERE UTKLGNTKN = ' + "'"+token + "'" )
    result = c.fetchall()
    return result[0][0]

def USRLGNTKN_generateid(db):
    c = db.cursor()
    c.execute('SELECT MAX(UTKUTKID)+1 FROM USRLGNTKN')
    return c.fetchall()[0][0]

def USRLGNTKN_entryExist(db,userid):
    c = db.cursor()
    c.execute('SELECT 1 FROM USRLGNTKN WHERE UTKUSRID = ' + str(userid) + '')
    return len(c.fetchall()) > 0
