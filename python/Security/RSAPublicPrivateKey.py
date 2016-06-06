# Added by Neha Ahlawat
# This script must be run when network session is established for the very first time. 
# Thereafter, public key needs to be exchanged with the receiver befre running any encryption/decryption algorithm
# This process needs to be done only once.

import subprocess

subprocess.call(['openssl genrsa -aes128 -out private.pem 2048'], shell=True)
subprocess.call(['openssl rsa -in private.pem -outform PEM -pubout -out public.pem'], shell=True)
