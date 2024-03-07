from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random

from base64 import b64encode, b64decode
import base64
from cryptography.hazmat.primitives import hashes
import hmac
import hashlib
hash = "SHA-256"

# Reminder make sure to change all plaintext to bytes before inputting into functions


# For generating the keys using key legnth of 2048
def generate_keys():
   keysize = 2048
   random_generator = Random.new().read
   key = RSA.generate(keysize, random_generator)
   private, public = key, key.public_key()
   return public, private

# For encrypting the plaintext
# Returns the encrypted ciphertext in b64 format
def encrypt(plaintext, public_key):
   cipher = PKCS1_OAEP.new(public_key)
   return b64encode(cipher.encrypt(plaintext.encode('utf-8'))).decode

# For decrypting the message
# Returns plaintext or whatever value it was encrypted from
def decrypt(ciphertext, private_key):
   cipher = PKCS1_OAEP.new(private_key)
   return cipher.decrypt(b64decode(ciphertext))


# For signing the message
# Hashes the plaintext using SHA256
# Encrypts it with the public key obtained from outside
# Returns the B64encoded format of the hashed and encrypted value
def sign(message, public_key):
   a = hashlib.sha256(message.encode('utf-8'))
   hash_value = a.digest()
   signed_message = encrypt(hash_value, public_key)
   return b64encode(signed_message).decode()


# For verifying the message
# The [message] parameter should be obtained from decrypting the encrypted plaintext 
# Then we hash the decrypted plaintext using SHA256
# Convert it to B64 format
# Decrypt the signed message to get the hashed value
# Convert this hashed value also into B64 format
# Compare the two hash values 
# If its equal return True
# If its unequal return False
def verify(message, signed_message, private_key):
   a = hashlib.sha256(message.encode('utf-8'))
   hash_value = b64encode(a.digest()).decode()

   decrypted_hash = decrypt(b64decode(signed_message), private_key)
   decrypted_hash = b64encode(decrypted_hash).decode()

   if hash_value == decrypted_hash:
      return True
   else:
      return False





# # THIS IS FOR DEBUG PURPOSES
# def encrypt_then_mac(message):
#     ciphertext = encrypt(message, private_key)
    
#     # Convert to hex format then to a string. Its still in hex format but just turned that into a string
#     cipher_hex_string = str(ciphertext.hex())

#     # Find the mac of the cipher_string. Its still in hex format but just turned that into a string
#     mac_string = str(get_mac(cipher_hex_string))

#     # Concatenate the two strings with a comma
#     final_value = cipher_hex_string + "," + mac_string
    
#     # Value to be sent through the socket
#     return final_value

# message = 'hello'



# public_key, private_key = generate_keys()
# test = encrypt('hello', public_key)
# print(b64decode(b64encode(test).decode()))
# signed_msg = sign('hello', public_key)
# print(verify(message, signed_msg, private_key))





# a = hashlib.sha256('your string or password'.encode('utf-8'))
# b = b64encode(a.digest()).decode()
# print(b)


# signed_message = encrypt(b64decode(b), public_key)

# comparison = decrypt(signed_message, private_key)
# print(b64encode(comparison).decode())




global public_key
global private_key

key_size = 2048

#Generate Keys
random_generator = Random.new().read
key = RSA.generate(key_size, random_generator)
private_key, public_key = key, key.public_key()

def encrypt(data, public_key):
   pass 

def decrypt(data, private_key):
   pass