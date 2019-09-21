# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
from rc4 import *
from sdes import *
from diffiehellman import *
from random import randint

if len(sys.argv) != 5:
        print "Correct usage: script, IP address, nickname, 'q', 'alpha'"
        exit()

sdese = SDESE()
sdesd = SDESD()
rc4 = RC4()
chavePrivada = randint(0, int(sys.argv[4]))
obj = DiffieHellman(int(sys.argv[3]), int(sys.argv[4]), chavePrivada)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
IP_address = str(sys.argv[1]) 
Port = 5354 
server.connect((IP_address, Port)) 
nickname = sys.argv[2]
x = 2
chavePublica = obj.getPublicKey()
chave = "1010101010"
enviarChave = 0
receberChave = 0
abriu = 1
end = 0
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
                    if message == "\crypt sdes":
                        x = 0
                        receberChave = 1
                        server.send(str(chavePublica))
                        print "A criptografia foi mudada para o modelo SDES"
                    elif message == "\crypt rc4":
                        x = 1
                        receberChave = 1
                        server.send(str(chavePublica))
                        print "A criptografia foi mudada para o modelo RC4"
                    elif message == "\crypt none":
                        x = 2
                        print "A Criptografia foi desabilitada"
                    elif receberChave == 1:
                        chave = obj.getChave(int(message))
                        receberChave = 0
                        server.send(str(chavePublica))
                    elif x == 0:
                    	if len(message) > 1:
                        	print(sdesd.complet(message, chave))
                        else:
                        	pass
                    elif x == 1:
                        if len(message) > 1:
                        	rc4.setMensagem(message)
                        	print(rc4.enc_dec(chave))
                        else: 
                        	pass
                    else:
                  		if len(message) > 1:
                  			print(message)
		else:
                    if enviarChave == 1:
                        server.send(str(chavePublica))
                        enviarChave = 0
                        continue
                    message = sys.stdin.readline()
                    if abriu == 1:
                        message == "\crypt sdes"
                        abriu = 0
                    if(message[:len(message)-1] == "\crypt sdes"):
                        server.send(message[:len(message)-1])
                        receberChave = 1
                        x = 0
                        print "A criptografia foi mudada para o modelo SDES"
                    elif message[:len(message)-1] ==  "\crypt rc4":
                        x = 1
                        server.send(message[:len(message)-1])
                        receberChave = 1
                        print "A criptografia foi mudada para o modelo RC4"
                    elif message[:len(message)-1] == "\end":
                        print "Saindo do chat..."
                        end = 1
                        break
                    elif message == "\crypt none":
                        print "Criptografia desabilitada"
                        server.send(message[:len(message)-1])
                        x = 2
                    elif message[:len(message)-1] == "\getPublicKey":
                        print "Chave publica: " + chavePublica
                    elif message[:len(message)-1] == "getSessionKey":
                        print "Chave de sessao: " + chave
                    elif message[:len(message)-1] == "\commands":
                        print "---------------------------------------------------------------------------------------------------------------------------"
                        print "Lista de comandos: "
                        print "\crypt sdes --> muda a criptografia atual para sdes com uma chave gerada por Diffie Hellman com os parametros escolhidos"
                        print "\crypt rc4 --> muda a criptografia atual para rc4 com uma chave gerada por Diffie Hellman com os parametros escolhidos"
                        print "\crypt none --> desabilita a criptografia"
                        print "\getPublicKey --> imprime a chave publica gerada pelo Diffie Hellman"
                        print "\getSessionKey --> imprime a chave de sessao(IMPORTANTE: essa chave deve ser mantida em sigilo!!!)"
                        print "\end --> finaliza a conexao e fecha o programa"
                        print "---------------------------------------------------------------------------------------------------------------------------"
                    else:
                        sys.stdout.write("<You> ")
                        sys.stdout.write(message)
                        sys.stdout.flush()
                        message = "<" + nickname + "> " + message[:len(message)-1]
                        if x == 0:
                            server.send(sdese.complet(message, chave))
                        elif x == 1:
                            rc4.setMensagem(message)
                            server.send(rc4.enc_dec(chave))
                        else:
                            server.send(message)
	if end == 1:
		break
server.close()