
import subprocess

fileName = arg1
encryptedKey = arg1+".enc"
args = ['openssl', 'rsautl', '-encrypt', '-inkey', 'public.pem',
'-pubin', '-in',  fileName, '-out', encryptedKey]
subprocess.Popen(args)
