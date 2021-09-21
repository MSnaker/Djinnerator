import password
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

with open('salt.txt','rb') as fsalt:
    salt = fsalt.readlines()[0]
pwd = b'banananas'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  
    salt=salt,
    iterations=420069,
)
key = base64.urlsafe_b64encode(kdf.derive(password))

f = password.start_Fernet(salt, pwd)

proof = b'Bananarama was pretty good!'
enc_proof = f.encrypt(proof)

with open('./text/key.txt','wb') as fkey:
    fkey.write(key)
    fkey.write(b'\n')
    fkey.write(proof)
    fkey.write(b'\n')
    fkey.write(enc_proof)

