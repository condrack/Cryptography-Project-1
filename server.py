#Taylor Condrack
import socket
#module for DES3 encryption routines
from Crypto.Cipher import DES3
from Crypto.Hash import HMAC
from Crypto import Random
import random
import sys
import time

#creates socket and port number
created=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=8764
error=b'MAC VERIFICATION FAILED'
#this is the predetermined mac key that server and client share
mackey=b'qazwsxedcrfvt'
#computes initial tag
tag=HMAC.new(mackey)
#i create a second tag to verify incoming packets
verify=HMAC.new(mackey)
#gets server name and binds it with the port number
hostname=socket.gethostname()
created.bind((hostname,port))
#waits for client to connect
created.listen(2)
#creates the address tuple with the socket, ip, and port
(client,(ip, p))=created.accept()

#prints connection confirmation and address
print 'connection established form ',p
#responds to client with necessary parameters and cipher info
client.send('Send password, plaintext for DES encryption, and MD5 hash MAC for message authentication')

#recieves packet form client
key=client.recv(1024)

#error checking: the key made from the pasword needs to be 8 bytes
#this concatenates bytes to the key if it is too short
#it truncates bytes if the key is too long
if len(key) < 16:
	add=16-len(key)
	for i in range(add):
		key=key+' '
elif len(key) >16:
	key=key[:16]
#recieves plaintext packet from the client
data=client.recv(1024)

tagr=client.recv(1024)
#computes mac on received plaintext
tag.update(data)

#verifys mac sent with plaintext with servers verify tag and plaintext
if tag.hexdigest()!=tagr:
	verify.update(error)
	client.send(verify.hexdigest())
	time.sleep(1)
	client.send(error)
	sys.exit()


#this forces the plaintext to contain bytes that are a multiple of 8
if len(data)%8!=0:
	add=8-len(data)%8
	for i in range(add):
		data=data+' '



#creates initilized vector with the correct block size
iv=Random.new().read(DES3.block_size)
#creates des variable from key in CFB mode and the iv
des=DES3.new(key,DES3.MODE_CFB,iv)
#encrypts the plaintext using DES3 algorithm
ciphertext=des.encrypt(data)
#returns the cipher text to the client
ciphertext=ciphertext.encode('string_escape')

#computes mac on cipher text
verify.update(ciphertext)

client.send(verify.hexdigest())
time.sleep(1)
client.send(ciphertext)

#close connection
client.close()

