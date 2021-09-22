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
    if button == 'Cancel':
        app.stop()
    pwd = bytes(app.getEntry('PwdEnt'),'utf-8')
    try:
        #code here to create key from a password
        f = Password.start_Fernet(salt,pwd)
        proof=str(f.decrypt(enc_proof),'utf-8')
    except (cryptography.fernet.InvalidToken, TypeError):
        proof = "wow, much try"
    if button == 'Acquire':
        app.setLabel('proofLab', proof)


with gui('Password Djinnerator') as app:
    app.addLabel('proofLab','',row = 1, colspan=2)    
    app.addLabel('pwdLab', 'Enter Password', row=0,column=0)
    app.addEntry('PwdEnt',row = 0, column = 1)

    app.addButtons(['Cancel', 'Acquire'], press, row = 2)

app.go()
