/*Author: Jahya Burke
 *Date: Spring 2016
 *Description: This program finds the period of time series given in th form 
 *of a text file. The text file is read into an array and the function J_Period
 *runs on the array that is inputed when it is called. The program takes a file
 *input from the command line.
 *Run: ./a.out <Data File>
 */

#include <stdio.h>
#include <math.h>

/*Main reads in  a data file from the command line. Currently it is set to read
 *a text file that is in the format given by the National Climatic Data Center.
 *It reads in the time series for sacramento and san diego for 1 year and then
 *creates a new array made of the array concatenated with itself +1 and +2.
 *These two arrays are used as inputs to J_Period and the outcome is put in an
 *output file called J_Period_Out.txt 
 *Main can be changed do take any desired input an read it into an array that 
 *can be inputed to J_Period
 */

int JPeriod(int Temp[],int n, FILE *output); 

int main (int argc, char *argv[]) {
  int i, j, n = 0, a =0, Temp[8759], Temp2[8759];
  char d[100];

  FILE *output;
  char myfile[] = "J_Period_Out.txt";
  output = fopen(myfile, "w");

  if (argc != 2) {
    printf("Invalid Input. Try Again!\n");
  }

  else {
    printf("You inputed a good file!\n");
    FILE *data = fopen( argv[1], "r");
    if (data == 0) {
      printf("Could not open file.\n");
    }
    else {
      printf("Your file was opened!\n");
      for (i = 0; i < 301; i++) {
        fscanf(data, "%c", &d[i]);
      }
      for (i = 0; i < 8759; i++) {
        fscanf(data, "%d", &Temp[n]);
        n++;
        for (j = 0; j < 105; j++) {
          fscanf(data, "%c", &d[j]);
        }
      }
      for (i = 0; i < 8759; i++) {
        fscanf(data, "%d", &Temp2[a]);
        a++;
        for (j = 0; j < 105; j++) {
          fscanf(data, "%c", &d[j]);
        }
      }
    }
    fclose( data );
  }
   int Year[26277];
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 8759; j++) {
      int ind = 8759*i + j;
      Year[ind] = Temp[j]+i;
    }
  }  
  int ind, Year2[26277];
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 8759; j++) {
      ind = 8759*i + j;
      Year2[ind] = Temp2[j]+i;
    }
  }
  int b = n*3;
  fprintf(output, "For a set of multiple Years in San Diego\n");
  JPeriod(Year, b, output);
  fprintf(output, "For a set of multiple Years in Sacramento\n");
  JPeriod(Year2, b, output);
  return 0;
}

int JPeriod(int Temp[],int n, FILE *output) {
  int i, j, a, h = n/2, P;
  int err, p[h], low;
  for (i = 0; i < h; i++) {
    err = 0;
    a = 0;
    for (j = i+1; j < i + 1 + h; j++) {
      err += (Temp[j] - Temp[a])*(Temp[j] - Temp[a]);
      a++;
    }
    p[i] = err;
  }
  h = h-1;
  low = p[1];
  P = 1;
  for (i = 0; i < h; i++) {
    if (p[i] < low) {
      low = p[i];
      P = i + 1;
    }
  }
  int T[P];
  for (i = 0; i < P; i++) {
    T[i] = Temp[i];
  }   
  if (P != 1) {
    fprintf(output, "Period = %d\n", P);
    JPeriod(T,P,output);
    } 
  return P;
}

