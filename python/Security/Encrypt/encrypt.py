# Added by Neha Ahlawat
# This python wrapper for encryption reads in the file/buffer, 16 bytes at a time, 
# and calls the C function that implements AES encryption.

from aesEncrypt import *
import sys
import os
import subprocess

# This function encrypts a plain-text file/buffer
# parameters for encrypt function are plaintext file/buffer name and the AES Key, 
# it returns the name of encrypted file. 

def encrypt(arg1, arg2):
    plainFile = open(arg2, "r")
    returnFile = arg2+"EncryptOut.csv"
    keyFile = open(arg1, "rb")
    encryptedFile = open( returnFile, "wb")
    sample = open("sample.csv", "wb")

    try:
        plainText = None
        plainText = plainFile.read()
        st = os.stat(arg2)
        fileSize = st.st_size
        fileSize = sys.getsizeof(plainText)
        iteration = fileSize/16 
        bytesLeft = fileSize%16
	keyVal = keyFile.read(16)
	for i in range(0, iteration-1):
		
	    if  keyVal == '':
		print ("Key Read Error")
		
	    else:
                start = i*16;
                encryptedText = bytearray(16)
                encryptedText = aesEncrypt(plainText[start:(start+16)], keyVal)
                encryptedFile.write(encryptedText)

        encryptedText = bytearray(16)
        lastByte = plainText[(start+16):(start+16 + bytesLeft)]
        lastByte = "{0:<16}".format(lastByte)
        encryptedText = lastByte
        encryptedText = aesEncrypt(encryptedText, keyVal)
        encryptedFile.write(encryptedText)
        
    finally:

	keyFile.close()
	plainFile.close()
	encryptedFile.close()

    return returnFile;

# Before encrypting the data, this fucntion encrypts the 
# AES key using the public key of the receiver and stores it in a file.

def rsaEncrypt(arg1):
    fileName = arg1
    encryptedKey = arg1+".enc"
    args = ['openssl', 'rsautl', '-encrypt', '-inkey', 'public.pem','-pubin', '-in',  fileName, '-out', encryptedKey]
    subprocess.Popen(args)
    return
