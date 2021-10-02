import os
from password import Password
from appJar import gui
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# print(os.getcwd())
with open('./text/salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]
# print(os.getcwd())

'''Section to import all pages of the origin file as a list (of lists) [list_pages(list_lines)].'''
        
print('Importing all lines from the encoded file...')
with open('./text/encoded.txt','rb') as fr:
    list_lines = fr.readlines()

print('Structuring the data...')
h = 30
arr_lines = [[] for y in range(h)]
page = 0
for line in list_lines:
    if line.startswith(b'Page'):
        print('Accessing page', page,'...')
        page+=1
        continue
    arr_lines[page-1].append([line])


enc_proof = b'gAAAAABhSd17y7PzMpGyLmQD7TZlPbXkURzrEmuO2SADY1Lc-HkQgNkoPPl6iqANnriaZNOWanv5B2rSj0M-iFiqwsxyuntKw_rdd1xb8ErZLp09QlvRAgY='

def press(button):
    pwd = bytes(app.getEntry('PwdEnt'),'utf-8')
    try:
        passwd = Password(salt, pwd)
        #code here to create key from a password
        proof = str(passwd.f.decrypt(enc_proof),'utf-8')
    except (cryptography.fernet.InvalidToken, TypeError):
        proof = "wow, much try"
    if button == 'Acquire':
        app.setLabel('proofLab', proof)
    if button == 'Cancel':
        app.stop()
    
    if button == 'Generate':
        x = ord(app.getEntry('firstEnt').lower()) - 96
        y = ord(app.getEntry('secondEnt').lower()) - 96
        line = arr_lines[x][y][0].strip()
        print(line)
        try:
            '''This method gets the y line of the x page, and decrypts it'''
            decr_line = str(passwd.f.decrypt(line).strip(), 'utf-8')
            print(decr_line, type(decr_line))
            output = str(passwd.pswgen(decr_line.split(None),y,3,'.,-'))
        except (cryptography.fernet.InvalidToken, TypeError):
            output = "wow, much try"
        print('Decrypting', x, 'page,', y, 'line...')
        app.setLabel('outLab',output)

app = gui('Password Djinnerator')
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