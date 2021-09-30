import unittest
from password import Password as psw
import os
import numpy as np
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from numpy.core.arrayprint import printoptions
from numpy.core.records import array

password = b'banananas'
with open('./text/salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]
enc_proof = b'gAAAAABhSd17y7PzMpGyLmQD7TZlPbXkURzrEmuO2SADY1Lc-HkQgNkoPPl6iqANnriaZNOWanv5B2rSj0M-iFiqwsxyuntKw_rdd1xb8ErZLp09QlvRAgY='

class TestStringMethods(unittest.TestCase):

    def test_init(self):
        psw_obj = psw(salt, password)
        proof = b'Bananarama was pretty good!'
        decr = psw_obj.f.decrypt(enc_proof)
        print(decr)
        self.assertEqual(decr, proof)

    def test_import(self):
        print('Importing all lines from the encoded file...')
        with open('./text/encoded.txt','rb') as fr:
            list_lines = fr.readlines()

        print('Structuring the data...')
        # w, h = 38,31
        # self.arr_lines = [['boba' for x in range(w)] for y in range(h)]
        arr_lines = []
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
            arr_lines[page-1].append([line])

        # del self.arr_lines[0] 
        # for page in self.arr_lines:
        #     while(page[-1] == 'boba'):
        #         del page[-1]
