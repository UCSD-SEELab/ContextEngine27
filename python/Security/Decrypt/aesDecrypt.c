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

static PyObject* aesDecrypt ( PyObject* self, PyObject* args) {
	static int run = 0;
	//FILE *fp;
	//fp = fopen("metasense_stratfordcar_5april2016.dat", "rb");
	//FILE *kp;
	//kp = fopen("AESKEY", "rb");

	//setbuf(stdout,NULL);
	//if(kp == NULL) { printf("KEY read Error\n"); exit(1); }
	
	uint8_t *fileRead = (uint8_t*) malloc(BUFSIZE);
	memset(fileRead,0,BUFSIZE);
	Py_ssize_t count;
	Py_ssize_t count1;
	uint8_t *key = (uint8_t*) malloc(KEYLEN);
	memset(key,0,KEYLEN);

	PyArg_ParseTuple(args, "s#|s#", &fileRead, &count, &key, &count);
	uint8_t *decryptOut = (uint8_t*) malloc(BUFSIZE);
	memset(decryptOut,0,BUFSIZE);
		
	// The array that stores the round keys.
	
	//while(!feof(kp)){
	//	fread(key,1,KEYLEN,kp);
	//}

	if (run == 0) {
		uint8_t initial = 0x00;
		iv[0] = initial;
		int i =1;
		for (i = 1; i<15; i++) {
			iv[i] = iv[i-1]+1;
		}
		AES128_CBC_decrypt_buffer(decryptOut, fileRead, BUFSIZE, key, iv);
		
		run++;
		//printf ("\n run = %d", run);
	}
	
	else {
		AES128_CBC_decrypt_buffer(decryptOut, fileRead, BUFSIZE, key, 0);
	}

	//free(fileRead);	
	//fclose(fpout);
	//fclose(fp);
	//fclose(kp);
	
	return Py_BuildValue("s#", decryptOut, count);
}
 
 
static PyMethodDef aesDecrypt_methods[] = {
      {"aesDecrypt", aesDecrypt, METH_VARARGS}
};

/*
 *   Python calls this to let us initialize our module
 */
void initaesDecrypt()
{
      (void) Py_InitModule("aesDecrypt", aesDecrypt_methods);
}


