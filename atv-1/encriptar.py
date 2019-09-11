import sys

def transbd(v1,v2):
	if(v1 == 0 and v2 == 0):
		return 0
	if(v1 == 0 and v2 == 1):
		return 1
	if(v1 == 1 and v2 == 0):
		return 2
	if(v1 == 1 and v2 == 1):
		return 3
def transdb(v1):
	if v1 == 0:
		return '00'
	if v1 == 1:
		return '01'
	if v1 == 2:
		return '10'
	if v1 == 3:
		return '11'
def xor(n1,n2,lista):
	for x in range(0,len(lista)):
		if (n1[x] == n2[x]):
			lista[x] = 0
		else:
			lista[x] = 1
	return lista


def gerarChaves(n,chave):
	listaP10 = [3,5,2,7,4,10,1,9,8,6];
	listaP8 = [6,3,7,4,8,5,10,9];
	key = [0,0,0,0,0,0,0,0,0,0]
	final = [0,0,0,0,0,0,0,0]

	for i in range(0,10):
		key[i] = chave[listaP10[i]-1];

	for i in range(0,5):
		if (i == 0):
			aux = key[0];
		if (i == 4):
			key[4] = aux;
		else:
			key[i] = key[i+1];
		
	for i in range(5,10):
		if (i == 5):
			aux = key[5];
		if (i == 9):
			key[9] = aux;
		else:
			key[i] = key[i+1];
		
	if (n == 2):
		for i in range(0,2):
			for i in range(0,5):
				if (i == 0):
					aux = key[0];
				if (i == 4):
					key[4] = aux;
				else:
					key[i] = key[i+1];
		
			for i in range(5,10):
				if (i == 5):
					aux = key[5];
				if (i == 9):
					key[9] = aux;
				else:
					key[i] = key[i+1];

	for i in range(0,8):
		final[i] = int(key[listaP8[i]-1]);
	return final;


try:
    in_file = open(sys.argv[1], "r")
except:
    sys.exit("ERROR. Did you make a mistake in the spelling")
text = in_file.read()
in_file.close()
out_file = open('criptografado.txt', "w")
IP = [2,6,3,1,4,8,5,7]
IPi =[4,1,3,5,7,2,8,6]
EP = [3,0,1,2,1,2,3,0]
S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[1,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
P4 = [2,4,3,1]
perm1 = [0,0,0,0,0,0,0,0]
perm2 = [0,0,0,0,0,0,0,0]
aux = [0,0,0,0,0,0,0,0]
lista = [0,0,0,0,0,0,0,0]
ultima = [0,0,0,0,0,0,0,0]
mid = [0,0,0,0]
l = [0,0,0,0]
for i in range(0,len(text)):
	byte = bin(ord(text[i]));
	r = 0
	for j in range(9-len(byte),9):
		if r == 0 or r == 1:
			pass
		else:
			aux[j-1]=int(byte[r]);
		r = r+1	
	for j in range(0,8):
		perm1[j] = aux[IP[j]-1]
	for j in range(0,8):
		perm2[j] = perm1[EP[j]]
	key = gerarChaves(1,sys.argv[2])
	atual = xor(key,perm2,lista)
	linha1 = transbd(atual[0],atual[3])
	coluna1 = transbd(atual[1],atual[2])
	valor1 = transdb(S0[linha1][coluna1])
	linha2 = transbd(atual[4],atual[7])
	coluna2 = transbd(atual[5],atual[6])
	valor2 = transdb(S1[linha2][coluna2])
	valor = valor1+valor2
	for j in range(0,4):
		mid[j] = int(valor[P4[j]-1]) 
	valor = xor(mid,perm1[:4],l)
	for j in range(0,4):
		ultima[j] = perm1[j+4]
	for j in range(4,8):
		ultima[j] = valor[j-4]

	final = [0,0,0,0,0,0,0,0]
	aux = [0,0,0,0,0,0,0,0]
	lista = [0,0,0,0,0,0,0,0]
	mid = [0,0,0,0]
	l = [0,0,0,0]

	for j in range(0,8):
		perm2[j] = ultima[EP[j]] 
	key = gerarChaves(2,sys.argv[2])
	atual = xor(key,perm2,lista)
	linha1 = transbd(atual[0],atual[3])
	coluna1 = transbd(atual[1],atual[2])
	valor1 = transdb(S0[linha1][coluna1])
	linha2 = transbd(atual[4],atual[7])
	coluna2 = transbd(atual[5],atual[6])
	valor2 = transdb(S1[linha2][coluna2])
	valor = valor1+valor2
	for j in range(0,4):
		mid[j] = int(valor[P4[j]-1]) 
	valor = xor(mid,ultima[:4],l)
	for j in range(4,8):
		lista[j] = ultima[j]
	for j in range(0,4):
		lista[j] = valor[j]
	for j in range(0,8):
		final[j] = lista[IPi[j]-1]
	a = ''
	for j in range(0,8):
		a = a + str(final[j])	
	b = int(a,2)
	out_file.write(chr(b))
	
out_file.close()
	
