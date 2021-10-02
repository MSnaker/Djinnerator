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
    seps = app.getEntry('separatorsEnt').split(None)
    minlen = int(app.getEntry('minEnt'))
    maxlen = int(app.getEntry('maxEnt'))
    try:
        passwd = Password(salt, pwd, seps, minlen, maxlen)
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
        try:
            '''This method gets the y line of the x page, and decrypts it'''
            decr_line = str(passwd.f.decrypt(line).strip(), 'utf-8')
            output = str(passwd.pswgen(decr_line.split(None),y))
        except (cryptography.fernet.InvalidToken, TypeError):
            output = "wow, much try"
        print('Decrypting', x, 'page,', y, 'line...')
        app.setEntry('outEnt',output)

def launch(win):
    app.showSubWindow(win)

app = gui('Password Djinnerator')
# GUI elements that prove to the user that they have input the correct password
int_row = 0
app.addLabel('pwdLab', 'Enter Password', row = int_row,column=0)
app.addSecretEntry('PwdEnt',row = int_row, column = 1)
int_row += 1
app.addLabel('proofLab','',row = int_row, colspan=2)    
int_row += 1
app.addButton('Acquire', press, row = int_row, colspan=2)
int_row += 1
app.addButtons(['Parameters','Output'], launch, row = int_row, colspan=2)

app.startSubWindow('Output')
int_row = 0
app.addLabel('firstLab','Entries:',row = int_row,colspan = 2)
int_row += 1
app.addEntry('firstEnt',row = int_row, column = 0)
app.addEntry('secondEnt',row = int_row, column = 1)
app.setEntryMaxLength('firstEnt',1)
app.setEntryMaxLength('secondEnt',1)
int_row += 1
app.addEntry('outEnt',row = int_row, colspan=2)
int_row += 1
app.addButtons(['Cancel', 'Generate'], press ,row = int_row, colspan=2)
app.stopSubWindow()

app.startSubWindow('Parameters')
int_row = 0
app.addLabel('separatorsLab','Separators (no forbidden characters)', row = int_row, column = 0)
app.addEntry('separatorsEnt',row=int_row,column=1)
app.setEntryDefault('separatorsEnt',') \ | / (')
int_row +=1
app.addLabel('lengthLab','Password length (max/min)',row=int_row,column=0)
app.addEntry('minEnt',row=int_row,column=1)
app.addEntry('maxEnt',row=int_row,column=2)
app.setEntryDefault('minEnt','8')
app.setEntryDefault('maxEnt','16')
app.stopSubWindow()

app.go() 