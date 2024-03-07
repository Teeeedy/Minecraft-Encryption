from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_Cipher
from Crypto import Random
from base64 import b64decode, b64encode
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
hash = "SHA-256"


class CryptographySession:
    def __init__(self):
        print("Generating Cryptographic Key Pair")
                
        keysize = 2048
        random_generator = Random.new().read
        key = RSA.generate(keysize, random_generator)
        self.private_key, self.public_key = key, key.public_key()

    def setRecipientPublicKey(self, key):
        #key is b64 encoded
        key = b64decode(key)
        key = RSA.importKey(key)
        self.recipient_public_key = key
        pass

    def encrypt(self, data):
	    #encrypt with recipient public key
        cipher = PKCS1_v1_5_Cipher.new(self.recipient_public_key)
        data = cipher.encrypt(data)
        return b64encode(data)
    
    def decrypt(self, data):
        data = b64decode(data)
        cipher = PKCS1_v1_5_Cipher.new(self.private_key)
        return cipher.decrypt(data, None)
    
    def sign(self, message):
        signer = PKCS1_v1_5.new(self.private_key)
        digest = SHA256.new()
        digest.update(message)

        return b64encode(signer.sign(digest))
    
    def verify(self, message, signature):
        signer = PKCS1_v1_5.new(self.recipient_public_key)
        digest = SHA256.new()
        digest.update(message)
        return signer.verify(digest, b64decode(signature))