'''This is a script that takes the previously encoded file, '''

import os
import numpy as np
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from numpy.core.arrayprint import printoptions
from numpy.core.records import array

# Function to import all pages of the origin file as a list (of lists) [list_pages(list_lines)].
def import_encrypted():
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
    return arr_lines

arr_lines = import_encrypted()

# This section is to use the same password and salt used before
print('Acquiring password...')
password = b'banananas'
print('Obtaining salt...')
with open('salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]

# This function is to set up the function Fernet to decode the lines.
def start_Fernet(salt,password):
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
    return f

f = start_Fernet(salt,password)
    
# Writing the decoded text to another file, to prove that we are on the right path (we can encrypt and then decrypt strings)
# We don't run this any more, as the script already gave a valid output once.
def export_decrypted():
    i = 1
    print('Writing to text file...')
    with open('./decoded.txt', 'w', encoding='utf-8') as fwrite:
        for array_page in arr_lines:
            fwrite.write(''.join(['Page',str(i)]))
            fwrite.write('\n')
            i +=1
            for bytes_line in array_page:
                decr_line = f.decrypt(bytes_line)
                fwrite.write(str(decr_line))
                fwrite.write('\n')

# This function extracts the first n words from the y line of the x page, and transforms the result into a password, accepting a string separators, that will rotate based on the line number in the page.

def pswgen(arr_lines, fernet, x, y, n, seps): 
    tr_from = 'AEIOUY'
    tr_to = '4310*<'

    print('Decrypting and generating password')
    line = arr_lines[x][y]
    fernet.decrypt(line)
    line_split = str(line, 'utf-8').split(' ')
    sep = seps[y%len(seps)]
    first = line_split[0].upper()
    trtable = first.maketrans(tr_from,tr_to)
    first_trans = first.translate(trtable)
    last = line_split[-1].upper()
    trtable = last.maketrans(tr_from,tr_to)
    last_trans = last.translate(trtable)
    mid = ''.join(line_split[1:-2])
    pswout = sep.join([first_trans,mid,last_trans])

    return pswout



     