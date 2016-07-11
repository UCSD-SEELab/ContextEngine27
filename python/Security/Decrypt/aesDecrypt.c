/*******************************************************************************
 * Added by: Neha Ahlawat
 * This file accepts 16 bytes of encrypted data from Python wrapper
 * as a bytearray and calls the decrypt fucntion in aesRPi.c file in 
 * order to decrypt it. It then returns this decrypted data as a bytearray
 *******************************************************************************
 */

#include <python2.7/Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/time.h>

#define BUFSIZE 16

#include "aesRPi.h"

uint8_t iv[16] = {};

int main(int argc, char **argv)
{

	return 0;
}

/**************************************************************************************************
* The C function returns 16 bytes of decrypted data, which is written to a file/buffer as required
***************************************************************************************************
*/

static PyObject* aesDecrypt ( PyObject* self, PyObject* args) {
	static int run = 0;
	
	Py_ssize_t count;

	uint8_t *fileRead = (uint8_t*) malloc(BUFSIZE);
	memset(fileRead,0,BUFSIZE);
	uint8_t *decryptOut = (uint8_t*) malloc(BUFSIZE);
	uint8x16_t *in = (uint8x16_t*) malloc(16);
	uint8x16_t *out = (uint8x16_t*) malloc(16);
	uint8x16_t *key_v = (uint8x16_t*) malloc(16);
	uint8x16_t *iv_v = (uint8x16_t*) malloc(16);
	
	uint8_t RoundKey[176];
	static uint8x16_t RoundKey_v[11];
	uint8_t *key = (uint8_t*) malloc(KEYLEN);

	PyArg_ParseTuple(args, "s#|s#", &fileRead, &count, &key, &count);

	if(key == NULL)
	{	
		return Py_BuildValue("s#", "Key Read Error", count);
	}
	

	*iv_v = vld1q_u8(iv);

	Key = key;
	KeyExpansion(RoundKey);

	int i;
	for(i=0; i<11; i++) {
		RoundKey_v[i] = vld1q_u8(RoundKey+(i*16));
	}

	if(fileRead != 0){

		if (run == 0) {
			uint8_t initial = 0x00;
			iv[0] = initial;
			int i =1;
			for (i = 1; i<15; i++) {
				iv[i] = iv[i-1]+1;
			}
			*in = vld1q_u8(fileRead);
			AES128_CFB_decrypt(out, *in, run, RoundKey_v, *iv_v);
			vst1q_u8(decryptOut, *out);
			run++;
		}
		
		else {
			*in = vld1q_u8(fileRead);
			AES128_CFB_decrypt(out, *in, run, RoundKey_v, *iv_v);
			vst1q_u8(decryptOut, *out);
			run++;
		}
		
	}


	return Py_BuildValue("s#", decryptOut, count);
}
 
static PyMethodDef aesDecrypt_methods[] = {
      {"aesDecrypt", aesDecrypt, METH_VARARGS}
};

/************************************************************
*   Python calls this fucntion to initialize decrypt module
************************************************************
*/

void initaesDecrypt()
{
      (void) Py_InitModule("aesDecrypt", aesDecrypt_methods);
}


