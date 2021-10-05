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
    
    def __init__(self, salt, password, seps, minlen, maxlen):
        '''This function is to set up the function Fernet to decode the lines.'''

        print('Initialising Fernet...')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  
            salt=salt,
            iterations=420069,
        )
        self.f = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
        print('Initialising default parameters...')
        self.list_seps = seps
        self.int_minlen = minlen
        self.int_maxlen = maxlen
        self.int_nwords = 3
        self.npage, self.nline = 0, 0
        self.output = ''

    def getline(self, arr_lines):
        '''This method gets the y line of the x page, and decrypts it
        '''
        print('Decrypting', self.npage, 'page,', self.nline, 'line...')
        line = arr_lines[self.npage][self.nline]
        decr_line = self.f.decrypt(line)
        return decr_line

    def pswgen(self,list_line, dict_swap): 
        '''This method extracts the first n words from a string and transforms the result into a password, accepting a string separators, that will rotate based on the line number in the page.
        '''
        print('Generating password...')
        sep = self.list_seps[self.nline%len(self.list_seps)]
        # First word
        first = list_line[0].upper()
        first_trans = first.translate(dict_swap)
        # Last word
        last = list_line[self.int_nwords-1].upper()
        last_trans = last.translate(dict_swap)
        # Middle word (or agglomerate)
        mid = ''.join(list_line[1:self.int_nwords-1])
        self.str_output = sep.join([first_trans,mid,last_trans])

    def tune(self, list_line):
        '''Something's wrong, I can feel it.'''
        len_pwd = 0
        for word in list_line[0:self.int_nwords]:
            len_pwd += len(word) + 1
        len_pwd -= 1
        print(len_pwd)
        if len_pwd>self.int_maxlen:
            self.int_nwords -= 1
            self.tune(list_line)
        else: 
            if len_pwd>self.int_minlen:
                self.int_nwords += 1
                self.tune(list_line)

        