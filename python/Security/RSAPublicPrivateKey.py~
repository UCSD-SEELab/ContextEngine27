import subprocess

subprocess.call(['openssl genrsa -aes128 -out private.pem 2048'], shell=True)
subprocess.call(['openssl rsa -in private.pem -outform PEM -pubout -out public.pem'], shell=True)
