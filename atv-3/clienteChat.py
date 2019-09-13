# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
from rc4 import RC4

rc4 = RC4()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 4: 
	print "Correct usage: script, IP address, port number, nickname"
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
nickname = sys.argv[3]

while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 

	""" There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

	for socks in read_sockets: 
		if socks == server: 
                    message = socks.recv(2048)
                    rc4.setMensagem(message)
                    print(rc4.enc_dec("default"))
                    
		else: 
                    message = sys.stdin.readline()
                    aux = ""
                    for i in range(len(message)-1):
                        aux += message[i]
                    sys.stdout.write("<You>")
                    sys.stdout.write(aux)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    message = "<" + nickname + ">" + aux
                    rc4.setMensagem(message)
                    server.send(rc4.enc_dec("default"))
                    
server.close() 

