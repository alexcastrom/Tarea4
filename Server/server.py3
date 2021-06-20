import socket, pickle
import subprocess
import os
import io
import bcrypt 
##from numpy import base_repr
from damgard_jurik import keygen
import time
cheack="s"
#########################################################################################Funcion encode / decode
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n"
def encode(num, alphabet):

    if num == 0:
        return alphabet[0]
    arr = []
    arr_append = arr.append  # Extract bound-method for faster access.
    _divmod = divmod  # Access to locals is faster.
    base = len(alphabet)
    while num:
        num, rem = _divmod(num, base)
        arr_append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def decode(string, alphabet=BASE62):

    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num
###########################################################


print ("Server is Listening.....")
HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

try:
	filename = 'private'
	infile = open(filename,'rb')
	private = pickle.load(infile)
	infile.close()
except:
	r="x"
while True:
	c= input("a Recepcion solicitud generador de llave \nb recibir archivo encriptado \nc decifrar \n")
	try:
		
		if c =="b":####################################
			print ("Esperando 'c' en el Cliente\n")
			with conn,open("try",'wb') as file:
				while True:
					recvfile = conn.recv(4096)
					if not recvfile: break
					file.write(recvfile)
			
			
			input ("Enter para continuar\n")
			
			
			
			
		elif c=="a":############################ Generador de Llaves, esperar respuesta de cliente
			print ("Esperando 'a' del cliente")
			data = conn.recv(4096)
			
			public_key, private_key_ring = keygen(
			    n_bits=64,
			    s=1,
			    threshold=3,
			    n_shares=3
			)


			filename1 = 'public'
			outfile = open(filename1,'wb')
			pickle.dump(public_key,outfile)
			outfile.close()

			filename2 = 'private'
			outfile = open(filename2,'wb')
			pickle.dump(private_key_ring,outfile)
			outfile.close()
			

			filename = 'public'
			infile = open(filename,'rb')
			public = pickle.load(infile)
			infile.close()
			
			data_string = pickle.dumps(public)
			input("ENTER para continuar\n")
			conn.sendall(data_string)
			print ('Data Sent to Server\n')
		
			
			
		elif c=="d":
			conn.close()
			break
		elif c =="c":
			filename = 'private'
			infile = open(filename,'rb')
			private = pickle.load(infile)
			infile.close()

			filename = 'try'
			infile = open(filename,'rb')
			new_dict = pickle.load(infile)
			infile.close()
			x=0
			for i in new_dict:
				#print ("\n")
				#print (i)
				#print ("\n")
				m_prime = private.decrypt(i)
				new_dict[x]= encode(m_prime,BASE62)
				x=x+1
			with open('AsyDecifrado.txt', 'w') as file:
				file.writelines( new_dict )
			print ("Archivos Decifrados!!!!!\nRevisa tus resultados")
			break
		
	except:
		continue
	

