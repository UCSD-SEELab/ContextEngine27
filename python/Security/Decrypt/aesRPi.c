/****************************
 * Added by: Neha Ahlawat
 ****************************
 */

#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include "aesRPi.h"
#include "arm_neon.h"

#define rounds 10

static uint8x16_t Iv;

typedef uint8x16_t state_t;
static state_t* state;

static uint8_t temp;
static void AddRoundKey(uint8x16_t RoundKey)
{
      *state = veorq_u8(RoundKey,*state);
}

static uint8_t lut[16];
static void SubBytes(void)
{
	vst1q_u8(lut,*state);
	lut[0] = sbox[lut[0]];
	lut[1] = sbox[lut[1]];
	lut[2] = sbox[lut[2]];
	lut[3] = sbox[lut[3]];
	lut[4] = sbox[lut[4]];
	lut[5] = sbox[lut[5]];
	lut[6] = sbox[lut[6]];
	lut[7] = sbox[lut[7]];
	lut[8] = sbox[lut[8]];
	lut[9] = sbox[lut[9]];
	lut[10] = sbox[lut[10]];
	lut[11] = sbox[lut[11]];
	lut[12] = sbox[lut[12]];
	lut[13] = sbox[lut[13]];
	lut[14] = sbox[lut[14]];
	lut[15] = sbox[lut[15]];
	*state = vld1q_u8(lut);
}

unsigned int CycleCount,CycleCount2;
static void ShiftRows(void)
{
	uint8x16_t state_dup;
	state_dup = *state;
	temp = vgetq_lane_u8(state_dup, 1); 
	vst1q_lane_u8(&temp, *state, 13);
	temp = vgetq_lane_u8(state_dup, 2); 
	vst1q_lane_u8(&temp, *state, 10);
	temp = vgetq_lane_u8(state_dup, 3); 
	vst1q_lane_u8(&temp, *state, 7);
	temp = vgetq_lane_u8(state_dup, 5); 
	vst1q_lane_u8(&temp, *state, 1);
	temp = vgetq_lane_u8(state_dup, 6); 
	vst1q_lane_u8(&temp, *state, 14);
	temp = vgetq_lane_u8(state_dup, 7); 
	vst1q_lane_u8(&temp, *state, 11);
	temp = vgetq_lane_u8(state_dup, 9); 
	vst1q_lane_u8(&temp, *state, 5);
	temp = vgetq_lane_u8(state_dup, 10); 
	vst1q_lane_u8(&temp, *state, 2);
	temp = vgetq_lane_u8(state_dup, 11); 
	vst1q_lane_u8(&temp, *state, 15);
	temp = vgetq_lane_u8(state_dup, 13); 
	vst1q_lane_u8(&temp, *state, 9);
	temp = vgetq_lane_u8(state_dup, 14); 
	vst1q_lane_u8(&temp, *state, 6);
	temp = vgetq_lane_u8(state_dup, 15); 
	vst1q_lane_u8(&temp, *state, 3);
}

static uint8x16_t xtime(uint8x16_t x)
{
	uint8x16_t y = vshlq_n_u8(x,1);
	x = vshrq_n_u8(x,7);
	uint8x16_t n27 = vmovq_n_u8(0x1b);
	x = vmulq_u8(x,n27);
	x = veorq_u8(x,y);
	return x;
}

static void MixColumns(void)
{
	uint32x4_t a = vreinterpretq_u32_u8(*state);
	uint32x4_t b = vreinterpretq_u32_u8(xtime(*state));
	
	uint32x4_t a3 = veorq_u32(a,b);
	uint32x4_t a3r = vshlq_n_u32(a3,8);
	a3r = vsraq_n_u32(a3r,a3,24);
	
	uint32x4_t a2 = vshlq_n_u32(a,16);
	a2 = vsraq_n_u32(a2,a,16);
	
	uint32x4_t a1 = vshlq_n_u32(a,24);
	a1 = vsraq_n_u32(a1,a,8);
	
	uint32x4_t out = veorq_u32(b,a1);
	out = veorq_u32(out,a2);
	out = veorq_u32(out,a3r);
	*state = vreinterpretq_u8_u32(out);
}

static void Cipher(uint8x16_t RoundKey_v[])
{
	uint8_t round = 0;

	AddRoundKey(RoundKey_v[0]); 

	for(round = 1; round < rounds; ++round)
	{
		SubBytes();
		ShiftRows();
		MixColumns();
		AddRoundKey(RoundKey_v[round]);
	}

	SubBytes();
	ShiftRows();
	AddRoundKey(RoundKey_v[rounds]);
}

static void XorWithIn(uint8x16_t* buf, uint8x16_t input)
{
	*buf = veorq_u8(*buf,input);
}

void AES128_CFB_encrypt(uint8x16_t* output, uint8x16_t input, uint32_t length, uint8x16_t RoundKey_v[], uint8x16_t iv_v)
{
	if(length == 0)
	{
		Iv = iv_v;
	}
	*output = Iv;
	state = (state_t*)output;
	Cipher(RoundKey_v);
	XorWithIn(output,input);
	Iv = *output;
}

void AES128_CFB_decrypt(uint8x16_t* output, uint8x16_t input, uint32_t length, uint8x16_t RoundKey_v[], uint8x16_t iv_v)
{
	if(length == 0)
	{
		Iv = iv_v;
	}
	*output = Iv;
	state = (state_t*)output;
	Cipher(RoundKey_v);
	XorWithIn(output,input);
	Iv = input;
}
