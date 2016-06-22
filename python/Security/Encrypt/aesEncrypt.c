/******************************************************************************
 * Added by: Neha Ahlawat
 * This file accepts 16 bytes of plaintext data from Python wrapper
 * as a bytearray and calls the encrypt fucntion in aesRPi.c file in 
 * order to encrypt it. It then returns this encrypted data as a bytearray
 *******************************************************************************
 */

#include <stdint.h>
#include <arm_neon.h>
#include <python3.4m/Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
* The C function returns 16 bytes of encrypted data, which is written to a file/buffer as required
***************************************************************************************************
*/

static PyObject* aesEncrypt ( PyObject* self, PyObject* args) {
	static int run = 0;
	
	Py_ssize_t count;

	uint8_t *fileRead = (uint8_t*) malloc(BUFSIZE);
	memset(fileRead,0,BUFSIZE);
	uint8_t *encryptOut = (uint8_t*) malloc(BUFSIZE);
	memset(encryptOut,0,BUFSIZE);
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
			AES128_CFB_encrypt(out, *in, run, RoundKey_v, *iv_v);
			vst1q_u8(encryptOut, *out);
			run++;
		}
		
		else {
			*in = vld1q_u8(fileRead);
			AES128_CFB_encrypt(out, *in, run, RoundKey_v, *iv_v);
			vst1q_u8(encryptOut, *out);
			run++;
		}
		
	}


	return Py_BuildValue("s#", encryptOut, count);
}
 
static PyMethodDef aesEncrypt_methods[] = {
      {"aesEncrypt", aesEncrypt, METH_VARARGS}, {NULL, NULL, 0}
};

static struct PyModuleDef aesEncryptFunc =
{
	
    PyModuleDef_HEAD_INIT,
    "aesEncrypt", /* name of module */
    "aes Module", /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    aesEncrypt_methods
};

/************************************************************
*   Python calls this fucntion to initialize encrypt module
************************************************************
*/

PyMODINIT_FUNC PyInit_aesEncrypt(void)
{
      return PyModule_Create(&aesEncryptFunc);
}



