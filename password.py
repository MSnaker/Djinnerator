'''This is a script that takes the previously encoded file, '''

import os
import numpy as np
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from numpy.core.arrayprint import printoptions
from numpy.core.records import array

# Import all lines of the origin file as a list.
print('Importing all lines from the encoded file...')
os.chdir('./text')
with open('encoded.txt','rb') as fr:
    list_lines = fr.readlines()

print('Structuring the data...')
w, h = 38,31
arr_lines = [['boba' for x in range(w)] for y in range(h)]
page, i = 0, 0
for line in list_lines:
    if line.startswith(b'Page'):
        i = 0
        if len(line)>7:
            page = 10*int(chr(line[5]))+int(chr(line[6])) 
        else:
            page = int(chr(line[5]))
        print('Accessing page', page,'...')
        continue
    arr_lines[page][i] = line
    i+=1

i = 0
del arr_lines[0]
for page in arr_lines:
    i += 1
    for j in range(len(page)):
        if page[-1] == 'boba':
            del page[-1]
    # print('Page', i, 'is long:',len(page))

# This section is to use the same password and salt used before
print('Acquiring password...')
password = b'banananas'
print('Obtaining salt...')
with open('salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]
    # raw = fsalt.read().split(b'\n')
    # salt = raw[0]
    # key_old = raw[1]
# print('Salt is:', salt)
# print('Old key is:', key_old)

# This section is to set up the function Fernet to decode the lines.
print('Initialising Fernet...')
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  
    salt=salt,
    iterations=420069,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
# print('Fernet key is:', key)
f = Fernet(key)
    
for page in arr_lines[0:3]:
    print('Page____________')
    for line in page:
        decr_line = f.decrypt(line)
        print(decr_line)
