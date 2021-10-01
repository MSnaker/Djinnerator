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

    