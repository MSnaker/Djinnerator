import os
from password import Password
from appJar import gui
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

print(os.getcwd())
with open('./text/salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]
print(os.getcwd())
arr_lines = Password.import_encrypted()
enc_proof = b'gAAAAABhSd17y7PzMpGyLmQD7TZlPbXkURzrEmuO2SADY1Lc-HkQgNkoPPl6iqANnriaZNOWanv5B2rSj0M-iFiqwsxyuntKw_rdd1xb8ErZLp09QlvRAgY='

def press(button):
    pwd = bytes(app.getEntry('PwdEnt'),'utf-8')
    try:
        #code here to create key from a password
        f = Password.start_Fernet(salt,pwd)
        proof=str(f.decrypt(enc_proof),'utf-8')
    except (cryptography.fernet.InvalidToken, TypeError):
        proof = "wow, much try"
    if button == 'Acquire':
        app.setLabel('proofLab', proof)
    if button == 'Cancel':
        app.stop()
    
    if button == 'Generate':
        try:
            '''This method gets the y line of the x page, and decrypts it'''
            x = int(app.getEntry('firstEnt').lower(), 'utf-8') - 96
            y = int(app.getEntry('secondEnt').lower(), 'utf-8') - 96
            print('Decrypting', x, 'page,', y, 'line...')
            line = arr_lines[x][y]
            decr_line = f.decrypt(line)
            output = str(Password.pswgen(decr_line,y,3,'.,-'))
        except (cryptography.fernet.InvalidToken, TypeError):
            output = "wow, much try"
        app.setLabel('outLab',output)

with gui('Password Djinnerator') as app:
    # GUI elements that prove to the user that they have input the correct password
    int_row = 0
    app.addLabel('pwdLab', 'Enter Password', row=int_row,column=0)
    app.addEntry('PwdEnt',row = int_row, column = 1)
    int_row+=1
    app.addLabel('proofLab','',row = int_row, colspan=2)  
    int_row+=1
    app.addButton('Acquire', press, row = int_row, colspan=2)

    # GUI elements to input the parameters that will determine the password output
    # Page and line
    int_row+=1
    app.addLabel('EntriesLab','Entries:',row=int_row,colspan = 2)
    int_row+=1
    app.addEntry('firstEnt',row=int_row, column = 0)
    app.addEntry('secondEnt',row=int_row, column = 1)
    app.setEntryMaxLength('firstEnt',1)
    app.setEntryMaxLength('secondEnt',1)
    # Password length limits, non-allowed characters
    int_row+=1
    app.addLabel('MinLenLab', 'Minimum length: ',row = int_row, column = 0)
    app.addEntry('MinLenEnt', row = int_row, column = 1)
    int_row+=1
    app.addLabel('MaxLenLab', 'Maximum length: ',row = int_row, column = 0)
    app.addEntry('MaxLenEnt', row = int_row, column = 1)
    

    # GUI output
    int_row+=1
    app.addLabel('msgLab','Your password is: ', row= int_row, column=0)
    app.addLabel('outLab','',row = int_row, column = 1)
    int_row+=1
    app.addButtons(['Cancel', 'Generate'], press ,row = int_row)

app.go()
