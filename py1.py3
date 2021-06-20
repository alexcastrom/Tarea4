import socket, pickle

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
import subprocess
import os
import io
import bcrypt 
from damgard_jurik import keygen
import time


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
while True:
	choice=input("Para crackear archivos, Escribe 'a' y luego Enter\nPara Avanzar a Cifrado Asimetrico Escribe 'b' y luego Enter\n")
	
	if choice == "a": ###########################################################  Seccion de Crackeado

		os.system("hashcat --force -m 0 -a 0 -o dh.txt archivo_1 diccionario_2.dict")
		print("")
		input("archivo_1 Crackeado!!!, presiona enter para continuar")###Crack archivo_1
		os.system("clear")

		os.system("hashcat --force -m 10 -a 0 -o dh.txt archivo_2 diccionario_2.dict")
		print(" ")
		input("archivo_2 Crackeado!!!, presiona enter para continuar")###Crack archivo_2
		os.system("clear")

		os.system("hashcat --force -m 10 -a 0 -o dh.txt archivo_3 diccionario_2.dict")
		print(" ")
		input("archivo_3 Crackeado!!!, presiona enter para continuar")###Crack archivo_3
		os.system("clear")

		os.system("hashcat --force -m 1000 -a 0 -o dh.txt archivo_4 diccionario_2.dict")
		print(" ")
		input("archivo_4 Crackeado!!!, presiona enter para continuar")###Crack archivo_4
		os.system("clear")


		os.system("hashcat --force -m 1800 -a 0 -o dh.txt archivo_5 diccionario_2.dict")
		print(" ")
		input("archivo_5 Crackeado!!!, presiona enter para continuar")###Crack archivo_5
		os.system("clear")

		############################################################### Seccion creacion texto plano txt
		# with is like your try .. finally block in this case
		with open('dh.txt', 'r') as file:
			# read a list of lines into data
			data = file.readlines()
			i = 0
			for line in data:
				remplace = ""
				it = len(line)
				for index in range(it):
					#print (line[it-index-1])
					if line[it-index-1] == ":":
						break
					remplace = line[it-index-1] + remplace
				#print (remplace)
				data[i]=remplace
				i=i+1


		with open('plaint.txt', 'w') as file:
		    file.writelines( data )

		############################################################### Seccion Hash de texto plano a Bcrypt
		tic = time.perf_counter()
		with open('plaint.txt', 'r') as file:
			data = file.readlines()
			i=0
			for line in data:
				remplace = bcrypt.hashpw(line.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')+"\n"

				data[i]=remplace
				###print (data2[i])
				i=i+1
				#if i==10:###RECORDAR comentar
				#	break###RECORDAR comentar

		toc = time.perf_counter()
		print(f"Tiempo de cifrado:{toc - tic:0.4f} Segundos. Presionar Enter para continuar")

		with open('passBcr.txt', 'w') as file:
			file.writelines( data )
		toc = time.perf_counter()

		###############################################################Cifrado Asimetrico
	if choice =="b":
		while True:
			try:
				c=input("a peticion(Primero seleccionar 'a' en el Servidor)\nb encriptar\nc enviar hash (Primero Seleccionar 'b' en el servidor)\n")
				print("\n")
				if c=="a":
					s.sendall(b"Te lo ordeno")
					print ("peticion enviada")
					data = s.recv(4096)
					filename1 = 'Llave_publica'
					outfile = open(filename1,'wb')
					pickle.dump(pickle.loads(data),outfile)
					outfile.close()
					print ("Llave publica recibida!!!!\n\n")
					
				elif c=="b":
					filename1 = "Llave_publica"
					infile = open(filename1,'rb')
					public = pickle.load(infile)
					infile.close()

					with open('plaint.txt', 'r') as file:
						data = file.readlines()
						c=[]
						for line in data:
							m=decode(line,BASE62)
							##print (m)
							c.append(public.encrypt(m))
					##print(c)
					filename1 = 'asyh'
					outfile = open(filename1,'wb')
					pickle.dump(c,outfile)
					outfile.close()
					print("Archivos Encriptados!!!!!\n\n")
				elif c=="c":
				
					filename = 'asyh'
					infile = open(filename,'rb')
					private = pickle.load(infile)
					infile.close()
					data_string = pickle.dumps(private)
					s.sendall(data_string)
					###print (private)

					print ('Datos Encriptados Enviados!!!\n\n')
					break
				elif c=="e":
					break
				
			except:
				continue
	
	break
		
