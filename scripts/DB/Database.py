from datetime import datetime
import os
import random
import re
import sqlite3
import scripts.DB.DatabaseUtils as Utils
from scripts.DB.Tables import USRADM as user
from scripts.DB.Tables import USRPST as post
from scripts.DB.Tables import USRLGNTKN as lgn
DATABASE = 'dbmain'

class Database:
    def __init__(self):
        self.delete_db()
        self.db = sqlite3.connect(DATABASE, check_same_thread=False)
        c = self.db.cursor()
        self.init_tables()

    def init_tables(self):
        user.USRADM_init(self.db)
        post.USRPST_init(self.db)
        lgn.USRLGNTKN_init(self.db)

    def delete_db(self):
        if os.path.exists(DATABASE):
            os.remove(DATABASE)

    def fetchHomePagePost(self):
        returnlist = []
        posts = post.fetchAllPost(self.db)
        for fullname, msg, posttime,imgurl in posts:
            posttime = datetime.strptime(posttime, '%Y%m%d %H:%M:%S').strftime("%d/%m/%Y %H:%M")
            msg = Utils.polluteContent(msg)
            current = {    "name" : fullname
                     ,  "content" : Utils.polluteContent(msg)
                     , "datetime" : posttime
                     ,   "imgurl" : imgurl}
            returnlist.append(current)
        return returnlist

    def login(self,userid,logintoken):
        lgn.USRLGNTKN_newRecord(self.db, userid,logintoken)

    def fetchUserProfileByUserID(self, userid):
        return user.USRADM_getUserProfile(self.db, userid)[0]

    def fetchUserIDByLoginToken(self,token):
        return lgn.USRLGNTKN_getUserIDByToken(self.db,token)

    def postcontent(self,userid,content):
        post.USRPST_newRecord(self.db,userid,Utils.cleanContent(content))

    #Adds new account to database
    def addNewAccount(self, username, fullname, password):
        userId = user.USRADM_generateid(self.db) #generates new id
        user.USRADM_newRecord(self.db,userId,username,fullname,password) #Inserts new account to database

    def loginValidation(self, username, password):
        userExists = user.USRADM_usernameexists(self.db, username)
        #user existent check
        if userExists:
            userid = user.USRADM_getUserIdByUsername(self.db, username)
            dbPassword = user.USRADM_getPasswordByUserId(self.db, userid)
            # Matching password check
            if str(dbPassword) == str(password):
                return 1
            else:
                return 0
        else:
            return 0

    def getUserIDByUsername(self, username):
        return user.USRADM_getUserIdByUsername(self.db, username)

    def getUserIDsBySearchTerm(self, searchTerm):
        return [i[0] for i in user.USRADM_fetchUserIDBySearchTerm(self.db,searchTerm)]

    def userExistsCheck(self, username):
        return user.USRADM_usernameexists(self.db, username)

    def fetchUserSpecificPostByUserId(self,userid):
        returnlist = []
        posts = post.fetchPostByUserId(self.db,userid)
        for fullname, msg, posttime,imgurl in posts:
            msg = Utils.polluteContent(msg)
            posttime = datetime.strptime(posttime, '%Y%m%d %H:%M:%S').strftime("%d/%m/%Y %H:%M")
            current = {    "name" : fullname
                     ,  "content" : msg
                     , "datetime" : posttime
                     ,   "imgurl" : imgurl}
            returnlist.append(current)
        return returnlist

    def fetchUsercardByIds(self,ids):
        returnlist = []
        for id in ids:
            susrid , fullname, usrimgurl = self.fetchUserProfileByUserID(id)
            component = {
                    "name" : fullname
                , "imgurl" : usrimgurl
            }
            returnlist.append(component)
        return returnlist
