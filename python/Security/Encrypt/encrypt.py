from aesEncrypt import *
import sys

def encrypt(arg1, arg2):
    plainFile = open(arg2, "rb")
    returnFile = arg2+"EncryptOut"
    sys.argv = ['RSAEncrypt.py', arg1]
    execfile("RSAEncrypt.py")
    keyFile = open(arg1, "rb")
    encryptedFile = open( returnFile, "wb")

    try:
    		
        plainText = plainFile.read(16)
	keyVal = keyFile.read(16)
	while plainText != '':
		
	    if  keyVal == '':
		print "Key Read Error"
		
	    else:
		encryptedText = aesEncrypt(plainText, keyVal)
		encryptedFile.write(encryptedText)
		plainText = plainFile.read(16)
	
    finally:

	keyFile.close()
	plainFile.close()
	encryptedFile.close()

    return returnFile;
