'''This .py file is created to split a book.txt file into different files, that are the book's pages. It will also encrypt them using a custom password, so that the files may be then used to obtain passwords, given two parameters (page and line) and the decryption password.'''
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# This section is to estabilish a password, a salt, and we save the salt, otherwise we will not be able to decode the files afterwards.
print('Acquiring password...')
password = b'banananas'
print('Obtaining salt...')
salt = os.urandom(16)
print('Saving salt...')
with open(''.join([os.getcwd(),'/text/salt.txt']),'w',encoding='utf-8') as fsalt:
    fsalt.truncate(0)
    fsalt.write('\n')
    fsalt.write(str(salt))
fsalt.close()

# This section is to set up the function Fernet to encode the files.
print('Initialising Fernet...')
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  
    salt=salt,
    iterations=420069,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

# Open the file that contains the book that has to be parsed and encoded.
print('Opening book file...')
os.chdir('./text')
path = os.getcwd()
list_filename_join = [path,'/book.txt']
filename = ''.join(list_filename_join)
# print(filename)
fr = open(filename,'r',encoding="utf-8")

# Read the book lines, create a file for each of the first 30 pages, and then write in the file all of the lines of that page, except those that contain less than 20 chars (supposing that the maximum password length will be 20 characters).
print('Reading file lines...')
list_line = fr.readlines()

print('Encoding and writing lines to single files...')
fw = open(''.join([path,'/encoded.txt']),'w',encoding='utf-8')
for element in list_line:
    if element.startswith("Page"):
        if element.startswith("Page | 31"):
            print('Reached page 31, terminating script.')
            break
        str_pagenum = ''.join([element[7],element[8]])
        pagenum = int(str_pagenum)
        print('Creating line for pagebreak', pagenum, '...')
        fw.write('\n')
        fw.write(''.join(['Page ', str(pagenum)]))
        fw.write('\n')
        # list_filename_join = [path,'/pages/',str(pagenum),'.txt']
        # filename = ''.join(list_filename_join)
        # fw = open(filename,'w',encoding="utf-8")
    else:
        if len(element) > 20:
            element_enc = f.encrypt(bytes(element, 'utf-8'))
            fw.write(str(element_enc))
            fw.write('\n')

fr.close()
fw.close()

