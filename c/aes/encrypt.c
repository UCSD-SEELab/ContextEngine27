#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <arm_neon.h>
#include <sys/time.h>

#define BUFSIZE 16

#include "aesRPi.h"

int main(int argc, char **argv)
{
	if(argc < 2) {
		fprintf(stderr,"Enter KEY file name\n");
		return -1;
	}
	
	FILE *fp;
	//fp = stdin;
	fp = fopen("../metasense_stratfordcar_5april2016.dat" , "rb");
    FILE *fpout;
	//fpout = stdout;
    fpout = fopen("eOut", "rb");
	FILE *kp;
	kp = fopen(argv[1], "rb");
	setbuf(stdout,NULL);
	if(kp == NULL) { printf("KEY read Error\n"); exit(1); }

	uint8_t *fileRead = (uint8_t*) malloc(BUFSIZE);
	memset(fileRead,0,BUFSIZE);
	uint8_t *encryptOut = (uint8_t*) malloc(BUFSIZE);
	uint8x16_t *in = (uint8x16_t*) malloc(16);
	uint8x16_t *out = (uint8x16_t*) malloc(16);
	uint8x16_t *key_v = (uint8x16_t*) malloc(16);
	uint8x16_t *iv_v = (uint8x16_t*) malloc(16);
	
	uint8_t RoundKey[176];
	static uint8x16_t RoundKey_v[11];
	uint8_t *key = (uint8_t*) malloc(KEYLEN);
	fread(key,1,KEYLEN,kp);
	uint8_t iv[]  = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };

	*iv_v = vld1q_u8(iv);

	Key = key;
	KeyExpansion(RoundKey);

	int i;
	for(i=0; i<11; i++) {
		RoundKey_v[i] = vld1q_u8(RoundKey+(i*16));
	}

	int j = 0;
	while(!feof(fp))
	{
		if(fread(fileRead,1,BUFSIZE,fp) != 0){
			*in = vld1q_u8(fileRead);
			AES128_CFB_encrypt(out, *in, j, RoundKey_v, *iv_v);
			vst1q_u8(encryptOut, *out);
			fwrite (encryptOut,1,BUFSIZE,fpout);
			memset(fileRead,0,BUFSIZE);
			j=1;
		}
		else break;
	}

	free(fileRead);
	free(encryptOut);
	free(in);
	free(out);
	free(key_v);
	free(iv_v);
	fclose(fpout);
	fclose(fp);
	fclose(kp);
    return 0;
}

