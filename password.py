'''This file initialises the class Password, which contains all the methods necessary to run the main.py script.'''

import os
import numpy as np
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from numpy.core.arrayprint import printoptions
from numpy.core.records import array

class Password():
    def import_encrypted():
        '''Function to import all pages of the origin file as a list (of lists) [list_pages(list_lines)].'''
        
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
                if i>9:
                    page = 10*int(chr(line[5]))+int(chr(line[6])) 
                else:
                    page = int(chr(line[5]))
                print('Accessing page', page,'...')
                i+=1
                continue
            arr_lines[page][i] = line

        i = 0
        del arr_lines[0]
        for page in arr_lines:
            i += 1
            for j in range(len(page)):
                if page[-1] == 'boba':
                    del page[-1]
        return arr_lines

    def start_Fernet(salt,password):
        '''This function is to set up the function Fernet to decode the lines.'''

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

    # def export_decrypted():
        '''Writing the decoded text to another file, to prove that we are on the right path (we can encrypt and then decrypt strings)
        We don't run this any more, as the script already gave a valid output once.'''

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

    def getline(arr_lines, fernet, x, y):
        '''This method gets the y line of the x page, and decrypts it'''

        print('Decrypting', x, 'page,', y, 'line...')
        line = arr_lines[x][y]
        decr_line = fernet.decrypt(line)
        return decr_line

    def pswgen(line_split, int_nline, n, seps): 
        '''This method extracts the first n words from a string and transforms the result into a password, accepting a string separators, that will rotate based on the line number in the page.'''
        tr_from = 'AEIOUY'
        tr_to = '4310*<'
        print('Generating password...')
        sep = seps[int_nline%len(seps)]
        first = line_split[0].upper()
        trtable = first.maketrans(tr_from,tr_to)
        first_trans = first.translate(trtable)
        last = line_split[n-1].upper()
        trtable = last.maketrans(tr_from,tr_to)
        last_trans = last.translate(trtable)
        mid = ''.join(line_split[1:n-1])
        pswout = sep.join([first_trans,mid,last_trans])

        return pswout

    def tune(line_split, int_nwords, int_minlen, int_maxlen):
        '''Something's wrong, I can feel it. 
        How can I call a self call and make this recursive?'''
        len_pwd = 0
        for word in line_split[0:int_nwords]:
            len_pwd += len(word) + 1
        len_pwd -= 1
        if len_pwd>int_maxlen:
            int_nwords -= 1
            Password.tune(line_split, int_nwords, int_minlen, int_maxlen)
        else: 
            if len_pwd>int_minlen:
                int_nwords += 1
                Password.tune(line_split, int_nwords, int_minlen, int_maxlen)
        return

    def sep_tune(seps, forbidden):
        temporary = []
        for character in seps:
            if character not in forbidden:
                temporary.append(character)
        seps = ''.join(temporary)
        return
        