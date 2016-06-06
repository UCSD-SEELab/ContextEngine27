import subprocess

fileName = arg1
decryptedKey = arg1+".dec"
args = ['openssl', 'rsautl', '-decrypt', '-inkey', 'private.pem',
'-in',  fileName, '-out', decryptedKey]
subprocess.Popen(args)
