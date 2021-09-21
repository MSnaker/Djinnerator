import password
from appJar import gui

with open('salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]

arr_lines = password.import_encrypted()

def press(button):
    if button == 'Cancel':
        app.stop()
    if button == 'Acquire':
        password = app.getEntry('Password')
        f = password.start_Fernet(salt,password)
        





app = gui()

app.addLabel("title", "Welcome to appJar")

app.go(startWindow==None)
