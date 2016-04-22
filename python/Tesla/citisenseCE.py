import csv
import datetime
import math
import numpy as np
import os.path
import pickle
from Tesla import Tesla

class CitisenseCE():

    def __init__(self):
        self.outData = []
        self.tuplesCovered = []
        self.aqiTrainingLUT = {}
        self.aqiTestLUT = {}
        self.dateTimeLUT = {}
        self.dateTimeCE = Tesla(order=2, numInputs=2);
        self.coarseLatCE = Tesla(order=3, numInputs=1);
        self.coarseLngCE = Tesla(order=3, numInputs=1);
        self.aqiCE = Tesla(order=3, numInputs=3);

    def enumerateAQI(self, rawValue):
        if (rawValue < 0.0):
            return -1;
        elif (rawValue <= 50.0):
            return 0;
        elif (rawValue <= 100.0):
            return 1;
        elif (rawValue <= 150.0):
            return 2;
        elif (rawValue <= 200.0):
            return 3;
        elif (rawValue <= 300.0):
            return 4;
        else:
            return 5;

    def truncate(self, f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        s = '%.12f' % f
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])

    def genLUTs(self):
        with open('../traces/aqiOnly.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            index = 0
            for row in reader:
                if (not index == 0) and (len(row) > 0):
                    reading = float(row[6])
                    date = datetime.datetime.strptime(row[7]+"00", "%Y-%m-%d %H:%M:%S%z")
                    coarseLat = float(self.truncate(float(row[8]), 6))
                    coarseLng = float(self.truncate(float(row[9]), 6))
                    dateInt = date.hour*60+date.minute

                    if (index <= 1400):
                        self.coarseLatCE.addSingleObservation([float(row[8])], coarseLat);
                        self.coarseLngCE.addSingleObservation([float(row[9])], coarseLng);
                        if (date.hour, date.minute) not in self.dateTimeLUT:
                            self.dateTimeLUT[(date.hour, date.minute)] = dateInt
                            self.dateTimeCE.addSingleObservation([date.hour, date.minute], dateInt);
                        if (coarseLat, coarseLng, dateInt) in self.aqiTrainingLUT:
                            print("Duplicate found! "
                                  + str(reading)
                                  + " vs. "
                                  + str(self.aqiTrainingLUT[(coarseLat, coarseLng, dateInt)]));
                            continue;
                        else:
                            self.aqiTrainingLUT[(coarseLat, coarseLng, dateInt)] = reading;
                            self.aqiCE.addSingleObservation([coarseLat, coarseLng, dateInt], reading);

                    elif (index <= 2000):
                        self.aqiTestLUT[(coarseLat, coarseLng, dateInt)] = reading;

                    else:
                        break;

                index += 1;

##            print(max(self.aqiTestLUT))

test = CitisenseCE();
test.genLUTs();

test.dateTimeCE.train();
test.coarseLatCE.train();
test.coarseLngCE.train();
test.aqiCE.train();

## print(test.dateTimeCE.test([5, 22.3]));
## print(round(test.coarseLatCE.test([32.8553660]), 6));

allErrors = []
count = 0

for key in test.aqiTestLUT:
    actual = test.enumerateAQI(test.aqiTestLUT[key]);
    theoretical = test.enumerateAQI(test.aqiCE.test([key[0], key[1], key[2]]));
#    print(str(actual) + ":" + str(test.aqiCE.test([key[0], key[1], key[2]])));
    print((actual-theoretical)/max(actual, theoretical)
          if (max(actual, theoretical) != 0.0)
          else (actual-theoretical));
    if not (max(actual, theoretical) == 0.0):
        allErrors.append(abs(actual-theoretical)/max(actual, theoretical));
    else:
        allErrors.append(abs(actual-theoretical));
    count += 1;
print("Done. Average error: " + str(sum(allErrors)/count));
