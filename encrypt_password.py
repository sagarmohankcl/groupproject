#!/usr/bin/env python

#password encryptor 
import getpass
from Crypto.Cipher import DES

def encrypt(pwd):
#password = getpass.getpass()
	password = pwd * 8
	des = DES.new('synomili', DES.MODE_ECB) #Keyname must be 8 bytes long
	key1 = des.encrypt(password)
	#print 'Your DES encoded password is:'
	return key1.__repr__()

if __name__ == "__main__":
	encrypt(raw_input())