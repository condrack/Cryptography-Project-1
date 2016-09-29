#Taylor Condrack
from Crypto.Hash import HMAC
import socket
import sys
import random
import time

#creates socket and port 
created=socket.socket()
port = 8764
#this is the predetermined mac key that server and client share
mackey=b'qazwsxedcrfvt'
#creates initial tag
tag=HMAC.new(mackey)
#i create a separate tag to verify incoming packets
verify=HMAC.new(mackey)
hostname=socket.gethostname()
created.connect((hostname,port))
print created.recv(1024)

#prompts for password that will be used for key
password=raw_input("8 byte password > ")
#prompts for plaintext to be encrypted
data=raw_input("plaintext > ")
#computes mac on plaintext
tag.update(data)
#sends packets separtely
#the sleeps is to sync the sends and receives on server side
created.send(password)
#haptic feedback for user
print("working...")
time.sleep(1)
created.send(data)
time.sleep(1)
tags=tag.hexdigest()
created.send(tags)

#receives feedback either cipher text or error message
feedback=created.recv(1024)

feedback2=created.recv(1024)

#computes mac on feedback to verify mac
verify.update(feedback2)

if verify.hexdigest()==feedback:
	print("Encrypted: "+feedback2)
else:
#vague error incase mac fails for a second time
	sys.exit("error")

#close connection
created.close
