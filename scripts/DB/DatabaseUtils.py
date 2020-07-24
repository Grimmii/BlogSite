import random
import string

detergent = {
    '\n' : '\\n'
}
pollution = {
    '\\n' : '<br/>'
}
restrictedChar = ['|']

characters = {
    '&' : '&amp;',
    '<' : '&lt;',
    '>' : '&gt;',
    '"' : '&quot;',
    '\'' : '&#x27;',
    '/' : '&#x2F'
}

def generateLoginToken(tokenLength=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tokenLength))

def inputValidation(fullname, username, password, confirmPassword):
    #If any of the fields are empty
    # unused empty password validation
    if (str(fullname or 'X') == 'X') or (str(username  or 'X') == 'X') or (str(password  or 'X') == 'X') or (str(confirmPassword  or 'X') == 'X'):
        return 0
    else: #Fields are all filled in
        return 1

def passwordMatchValidation(password, confirmPassword):
    if password == confirmPassword:
        return 1
    else:
        return 0

#for saving posts
def cleanContent(content):
    for character in restrictedChar:
        content = content.replace(character,'')

    for key in detergent.keys():
        content = content.replace(key,detergent[key])
    return content

# for displaying posts
def polluteContent(content):
    for key in pollution.keys():
        content = content.replace(key,pollution[key])
    return content

# Escapes characters in the content string
def escapeCharacters(content):
    for key in characters.keys():
        content = content.replace(key, characters[key])
    return content

tokens=[]
def genCSRFToken():
    key=''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    tokens.append(key)
    return key


def CheckCSRFToken(key):
    if key in tokens:
        #Remove from list
        tokens.remove(key)
        return True
    else:
        return False
