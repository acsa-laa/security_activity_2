from sdes import SDESE
from sdes import SDESD

sdes = SDESE()
palavra = 'maria'
key = '1010101010'
a = sdes.complet(palavra,key)
print(a)
des = SDESD()
b = des.complet(a,key)
print(b)