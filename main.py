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
    app.addLabel('proofLab','',row = 1, colspan=2)    
    app.addLabel('pwdLab', 'Enter Password', row=0,column=0)
    app.addEntry('PwdEnt',row = 0, column = 1)

    app.addButton('Acquire', press, row = 2, colspan=2)

    app.addLabel('firstLab','Entries:',row=3,colspan = 2)
    app.addEntry('firstEnt',row=4, column = 0)
    app.addEntry('secondEnt',row=4, column = 1)
    app.setEntryMaxLength('firstEnt',1)
    app.setEntryMaxLength('secondEnt',1)

    app.addLabel('outLab','',row = 5, colspan=2)
    app.addButtons(['Cancel', 'Generate'], press ,row = 6)

app.go()
