from aesDecrypt import *
import sys

def decrypt(arg1, arg2):
    encryptedFile = open(arg2, "rb")
    returnFile = arg2+"DecryptOut"
    sys.argv = ['RSADecrypt.py', arg1]
    execfile("RSAEncrypt.py")
    keyFile = open(arg1+".dec", "rb")
    decryptedFile = open( returnFile, "wb")
    

    try:

	encryptedText = encryptedFile.read(16)
	key = keyFile.read(16)
	while encryptedText != '':
		
		if key == '':
			print "Key Read Error"
			
		else:
			decryptedText = aesDecrypt(encryptedText, key)
			decryptedFile.write(decryptedText)
			encryptedText = encryptedFile.read(16)
	
    finally:

	keyFile.close()
	encryptedFile.close()
	decryptedFile.close()
    return returnFile;
