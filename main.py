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

# Default parameters
int_nwords, int_minlen, int_maxlen = 3, 8, 16
seps = '.,-'
forbidden = []

def press(button):

    if button == 'Acquire':
        pwd = bytes(app.getEntry('PwdEnt'),'utf-8')
        try:
            #code here to create key from a password
            f = Password.start_Fernet(salt,pwd)
            proof=str(f.decrypt(enc_proof),'utf-8')
        except (cryptography.fernet.InvalidToken, TypeError):
            proof = "wow, much try"
        app.setLabel('proofLab', proof)
    if button == 'Cancel':
        app.stop()
    
    if button == 'Generate':
        try:
            '''This method gets the y-th line of the x-th page, and decrypts it'''
            x = int(app.getEntry('firstEnt').lower(), 'utf-8') - 96
            y = int(app.getEntry('secondEnt').lower(), 'utf-8') - 96
            print('Decrypting', x, 'page,', y, 'line...')
            line = arr_lines[x][y]
            decr_line = f.decrypt(line)
            # Here it is determined if the password satisfies the parameters acquired, if parameters have been provided
            uno = app.getEntry('MinLenEnt')
            if uno != None:
                int_minlen = uno
            doss = app.getEntry('MaxLenEnt')
            if doss != None:
                int_maxlen = doss
            tress = app.getEntry('naEnt')
            if tress != None:
                forbidden = tress
            line_split = str(decr_line, 'utf-8').split(' ')
            Password.tune(line_split, int_nwords, int_minlen, int_maxlen)
            Password.sep_tune(seps,forbidden)
            # Here the password is actually generated
            output = str(Password.pswgen(line_split,y,int_nwords,seps))
        except (cryptography.fernet.InvalidToken, TypeError):
            output = "wow, much try"
        app.setLabel('outLab',output)


app = gui('Password Djinnerator')
# GUI elements that prove to the user that they have input the correct password
int_row = 0
app.addLabel('pwdLab', 'Enter Password', row=int_row,column=0)
app.addSecretEntry('PwdEnt',row = int_row, column = 1)
int_row+=1
app.addLabel('proofLab','',row = int_row, colspan=2)  
int_row+=1
app.addButton('Acquire', press, row = int_row, colspan=2)

def launch(win):
    app.showSubWindow(win)

# these go in the main window
int_row +=1
app.addButtons(["Parameters", "PwGen"], launch, row = int_row, colspan = 2)

# this is a pop-up
app.startSubWindow("Parameters", modal=True)
# Password length limits, non-allowed characters
int_row+=1
app.addLabel('MinLenLab', 'Minimum length: ',row = int_row, column = 0)
app.addEntry('MinLenEnt', row = int_row, column = 1)
int_row+=1
app.addLabel('MaxLenLab', 'Maximum length: ',row = int_row, column = 0)
app.addEntry('MaxLenEnt', row = int_row, column = 1)
int_row+=1
app.addLabel('naLab', 'Non-allowed characters (separate with space): ',row = int_row, column = 0)
app.addEntry('naEnt', row = int_row, column = 1)
app.stopSubWindow()

# this is another pop-up
app.startSubWindow("PwGen")
# GUI elements to input the parameters that will determine the password output
# Page and line
int_row+=1
app.addLabel('EntriesLab','Entries:',row=int_row,colspan = 2)
int_row+=1
app.addEntry('firstEnt',row=int_row, column = 0)
app.addEntry('secondEnt',row=int_row, column = 1)
app.setEntryMaxLength('firstEnt',1)
app.setEntryMaxLength('secondEnt',1)

# GUI output
int_row+=1
app.addLabel('msgLab','Your password is: ', row= int_row, column=0)
app.addLabel('outLab','',row = int_row, column = 1)
int_row+=1
app.addButtons(['Cancel', 'Generate'], press ,row = int_row)
app.stopSubWindow()

app.go()
