CC           = gcc
CFLAGS       = -Wall -mfpu=neon -oFast -O3 -ftree-vectorize
OBJCOPY      = objcopy

all: encrypt.out decrypt.out 
encrypt.o : aesRPi.h encrypt.c
	# compiling encrypt.c
	$(CC) $(CFLAGS) -c encrypt.c -o encrypt.o
decrypt.o : aesRPi.h decrypt.c
	# compiling decrypt.c
	$(CC) $(CFLAGS) -c decrypt.c -o decrypt.o

aesRPi.o : aesRPi.h aesRPi.c
	# compiling aesRPi.c
	$(CC) $(CFLAGS) -c aesRPi.c -o aesRPi.o

encrypt.out : aesRPi.o encrypt.o
	# linking object code to binary
	$(CC) $(CFLAGS) aesRPi.o encrypt.o -o encrypt.out
decrypt.out : aesRPi.o decrypt.o
	# linking object code to binary
	$(CC) $(CFLAGS) aesRPi.o decrypt.o -o decrypt.out

clean:
	rm -f *.o *.out
