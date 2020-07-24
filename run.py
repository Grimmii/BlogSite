from flask import Flask, render_template, request, session, make_response,redirect, url_for
from scripts.DB.Database import Database
from scripts.DB import DatabaseUtils as Utils
from scripts import SessionKeys as sesskeys
from flask import make_response
import string
import random
LEN_LOGINTKN = 20
app = Flask(__name__)
app.secret_key = "ADMINXX"

dbmain = Database()

@app.errorhandler(404)
def page_not_found(e):
    return error()

# Displays an error page when user enters an invalid/non-existent URL
@app.route('/error')
def error():
    return render_template('ERR404PGE.html')

@app.route('/')
def index():
    try:
        return home()
    except Exception as e:
        return logout()

@app.route('/login', methods = ['POST'])
def login():
    #Validation check
    try:
        if (str(request.cookies.get(sesskeys.LOGINTOKEN) or '?') != '?'):
            redirect(url_for('profile'))
        username = request.form.get('username')
        password = request.form.get('password')
        csrfToken=request.form.get('CSRFToken')

        #Get a hash of the password
        if Utils.CheckCSRFToken(csrfToken) == False:
            return logout()
        # Turns username string to lowercase
        username = username.lower()

        if dbmain.loginValidation(username, password) == 1 :
            userid = dbmain.getUserIDByUsername(username)

            key = Utils.generateLoginToken(LEN_LOGINTKN)
            dbmain.login(userid,key)

            userid = dbmain.fetchUserIDByLoginToken(key)
            userid, fname, imgurl = dbmain.fetchUserProfileByUserID(userid)
            posts = dbmain.fetchHomePagePost()
            res  = make_response(render_template('HMEPGE.html', posts=posts, imgurl=imgurl,CSRF=Utils.genCSRFToken()))
            res.set_cookie(sesskeys.LOGINTOKEN, key,2147483647)
            return res
        else:
            return render_template('LGNPGE.html',error_message = 'Username and/or Password is incorrect',CSRF=Utils.genCSRFToken())
    except Exception as e:
        return logout()

@app.route('/logout')
def logout():
    try:
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
        dbmain.login(userid,'')
    except Exception as e:
        loggingIndex = 1
    finally:
        res  = make_response(render_template('LGNPGE.html', CSRF=Utils.genCSRFToken()))
        res.set_cookie(sesskeys.LOGINTOKEN, '',2147483647 )
        return res

@app.route('/profile')
def profile():
    try:
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
        userid, fname, imgurl = dbmain.fetchUserProfileByUserID(userid)
        posts = dbmain.fetchUserSpecificPostByUserId(userid)
        res  = make_response(render_template('PRFLPGE.html',profilepic=imgurl ,fname=fname,posts=posts,CSRF=Utils.genCSRFToken() ))
        res.set_cookie(sesskeys.LOGINTOKEN, request.cookies.get(sesskeys.LOGINTOKEN),2147483647)
        return res
    except Exception as e:
        return logout()

@app.route('/profile/PostContent',methods=['GET','POST'])
def profilepostcontent():
    try:
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
        content = request.form.get('userpostcontent')
        csrfToken = request.form.get('CSRFToken')
        if Utils.CheckCSRFToken(csrfToken) == False:
            return logout()
        content = Utils.escapeCharacters(content)

        if (str(content or '?') != '?'):
            dbmain.postcontent(userid,content)
        return redirect(url_for('profile'))
    except Exception as e:
        return logout()

@app.route('/home')
def home():
    try:
        if (str(request.cookies.get(sesskeys.LOGINTOKEN) or '?') == '?'):
            raise Exception('Missing login token')
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
        userid, fname, imgurl = dbmain.fetchUserProfileByUserID(userid)
        posts = dbmain.fetchHomePagePost()
        res  = make_response(render_template('HMEPGE.html', posts=posts, imgurl=imgurl,CSRF=Utils.genCSRFToken()))
        res.set_cookie(sesskeys.LOGINTOKEN, request.cookies.get(sesskeys.LOGINTOKEN) ,2147483647)
        return res
    except Exception as e:
        return logout()

@app.route('/home/PostContent',methods=['POST'])
def homepostcontent():
    try:
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
        content = request.form.get('userpostcontent')
        csrfToken = request.form.get('CSRFToken')
        if Utils.CheckCSRFToken(csrfToken) == False:
            return logout()

        content = Utils.escapeCharacters(content)

        if (str(content or '?') != '?'):
            dbmain.postcontent(userid,content)
        return redirect(url_for('home'))
    except Exception as e:
        return logout()

@app.route('/usersearch')
def usersearchpage(cards=[]):
    try:
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
        res  = make_response(render_template('USRSRHPGE.html',usercard=cards,CSRF=Utils.genCSRFToken()))
        res.set_cookie(sesskeys.LOGINTOKEN, request.cookies.get(sesskeys.LOGINTOKEN) ,2147483647)
        return res
    except Exception as e:
        return logout()

@app.route('/usersearch/search',methods=['GET','POST'])
def usersearch():
    try:
        userid = dbmain.fetchUserIDByLoginToken(request.cookies.get(sesskeys.LOGINTOKEN))
        searchterm = request.form.get('searchTerm')
        csrfToken= request.form.get('CSRFToken')
        if Utils.CheckCSRFToken(csrfToken)==False:
            return logout()
        if (str(searchterm or '?') == '?'):
            return redirect(url_for('usersearchpage'))
        searchterm = searchterm.lower()
        userids = dbmain.getUserIDsBySearchTerm(searchterm)
        cards = dbmain.fetchUsercardByIds(userids)
        return usersearchpage(cards)
    except Exception as e:
        return logout()

@app.route('/signup')
def singuppage():
    return render_template('RGTPGE.html',errMsg="",CSRF=Utils.genCSRFToken());

@app.route('/signup/signup', methods=['GET', 'POST'])
def signup():
    #Collects input from form in RGTPGE.html
    try:
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        RetToken=request.form.get('CSRFToken')
        username = username.lower()
        #Input parameter validation check
        if not dbmain.userExistsCheck(username) and Utils.passwordMatchValidation(password, confirmPassword) and Utils.CheckCSRFToken(RetToken):
            dbmain.addNewAccount(username, fullname, password)
            return render_template('LGNPGE.html',CSRF=Utils.genCSRFToken())
        else:
            return render_template('RGTPGE.html',errMsg="There has been an error",CSRF=Utils.genCSRFToken())
    except Exception as e:
        return render_template('RGTPGE.html',errMsg="There has been an error",CSRF=Utils.genCSRFToken())

if __name__ == "__main__":
    app.run()
