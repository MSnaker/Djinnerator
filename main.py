import password
from appJar import gui

with open('salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]

arr_lines = password.import_encrypted()
enc_proof = b'gAAAAABhSd17y7PzMpGyLmQD7TZlPbXkURzrEmuO2SADY1Lc-HkQgNkoPPl6iqANnriaZNOWanv5B2rSj0M-iFiqwsxyuntKw_rdd1xb8ErZLp09QlvRAgY='

def press(button):
    if button == 'Cancel':
        app.stop()
    if button == 'Acquire':
        pwd = app.getEntry('PwdEnt')
        try:
            #code here to create key from a password
            f = password.start_Fernet(salt,pwd)
            proof=str(f.decrypt(enc_proof),'utf-8')
        except (cryptography.fernet.InvalidToken, TypeError):
            proof = "wow, much try"
        app.setLabel('proofLabel', proof)


app = gui()
app.addLabel('proofLabel',"Proof label")
app.addEntry('PwdEnt')


app.go()
