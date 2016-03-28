import numpy as np
import os.path
import pickle
from Tesla import Tesla



# Tesla training objects
refrigeratorTrainer1 = Tesla(order=2,numInputs=1);
refrigeratorTrainer2 = Tesla(order=2,numInputs=2);
refrigeratorTrainer3 = Tesla(order=2,numInputs=3);
refrigeratorTrainer4 = Tesla(order=2,numInputs=4);

# Pickle files for trained data
refrigeratorPickleFile1 = 'traces/refrigeratorTrained1.dat';
refrigeratorPickleFile2 = 'traces/refrigeratorTrained2.dat';
refrigeratorPickleFile3 = 'traces/refrigeratorTrained3.dat';
refrigeratorPickleFile4 = 'traces/refrigeratorTrained4.dat';

# Open the files needed: input trace and output observations
refrigeratorTrace = open('traces/refrigerator.dat', mode='r');
refrigeratorOutputTrace = open('traces/refrigerator_obs.dat', mode='r');

# First, parse the first 3 elements, needed as additional inputs
# Add observations to the appropriate tesla training objects# First observation
# First observation
(timestamp, refrigeratorEntry1) = refrigeratorTrace.readline().split();
refrigeratorEntry1 = float(refrigeratorEntry1);
(timestamp, refrigeratorOutput) = refrigeratorOutputTrace.readline().split();
refrigeratorOutput = int(refrigeratorOutput);
refrigeratorTrainer1.addSingleObservation([refrigeratorEntry1], refrigeratorOutput);
# Second observation
(timestamp, refrigeratorEntry2) = refrigeratorTrace.readline().split();
refrigeratorEntry2 = float(refrigeratorEntry2);
(timestamp, refrigeratorOutput) = refrigeratorOutputTrace.readline().split();
refrigeratorOutput = int(refrigeratorOutput);
refrigeratorTrainer1.addSingleObservation([refrigeratorEntry2],\
                                          refrigeratorOutput);
refrigeratorTrainer2.addSingleObservation([refrigeratorEntry1,\
                                           refrigeratorEntry2],\
                                          refrigeratorOutput);
# Third observation
(timestamp, refrigeratorEntry3) = refrigeratorTrace.readline().split();
refrigeratorEntry3 = float(refrigeratorEntry3);
(timestamp, refrigeratorOutput) = refrigeratorOutputTrace.readline().split();
refrigeratorOutput = int(refrigeratorOutput);
refrigeratorTrainer1.addSingleObservation([refrigeratorEntry3],\
                                          refrigeratorOutput);
refrigeratorTrainer2.addSingleObservation([refrigeratorEntry2,\
                                           refrigeratorEntry3],\
                                          refrigeratorOutput);
refrigeratorTrainer3.addSingleObservation([refrigeratorEntry1,\
                                           refrigeratorEntry2,\
                                           refrigeratorEntry3],\
                                          refrigeratorOutput);

for i in range(0, 86397):
#for i in range(0, 3997):
    # Current observation
    (timestamp, refrigeratorEntry4) = refrigeratorTrace.readline().split();
    refrigeratorEntry4 = float(refrigeratorEntry4);
    (timestamp, refrigeratorOutput) = refrigeratorOutputTrace.readline().split();
    refrigeratorOutput = int(refrigeratorOutput);

    refrigeratorOutput = int(refrigeratorOutput);
    refrigeratorTrainer1.addSingleObservation([refrigeratorEntry4],\
                                              refrigeratorOutput);
##    refrigeratorTrainer2.addSingleObservation([refrigeratorEntry3,\
##                                               refrigeratorEntry4],\
##                                              refrigeratorOutput);
##    refrigeratorTrainer3.addSingleObservation([refrigeratorEntry2,\
##                                               refrigeratorEntry3,\
##                                               refrigeratorEntry4],\
##                                              refrigeratorOutput);
##    refrigeratorTrainer4.addSingleObservation([refrigeratorEntry1,\
##                                               refrigeratorEntry2,\
##                                               refrigeratorEntry3,\
##                                               refrigeratorEntry4],\
##                                              refrigeratorOutput);

    # Update old observations to set up for the next iteration
    refrigeratorEntry1 = refrigeratorEntry2;
    refrigeratorEntry2 = refrigeratorEntry3;
    refrigeratorEntry3 = refrigeratorEntry4;

    if (refrigeratorOutput > 0):
        print("High Value found!\n");

refrigeratorTrainer1.train();
##refrigeratorTrainer2.train();
##refrigeratorTrainer3.train();
##refrigeratorTrainer4.train();

##pickleFileRef = open(refrigeratorPickleFile, 'wb');
##pickle.dump(refrigeratorTrainer, pickleFileRef);

##else:
##    pickleFileRef = open(fridgePickleFile, 'rb');
##    fridgeTrainer = pickle.load(pickleFileRef);


print(refrigeratorTrainer1.numObservations);
print(refrigeratorTrainer1.coefficientVector[0]);

##print(refrigeratorTrainer2.numObservations);
##print(refrigeratorTrainer2.coefficientVector[0]);

##print(refrigeratorTrainer3.numObservations);
##print(refrigeratorTrainer3.coefficientVector[0]);

##print(refrigeratorTrainer4.numObservations);
##print(refrigeratorTrainer4.coefficientVector[0]);

testObs1 = float(refrigeratorTrace.readline().split()[1]);
testObs2 = float(refrigeratorTrace.readline().split()[1]);
testObs3 = float(refrigeratorTrace.readline().split()[1]);

for i in range(0,10001):
    testObs4 = float(refrigeratorTrace.readline().split()[1]);

    if (testObs4 > 300):
        print((testObs4, refrigeratorTrainer1.test([testObs4])));
##        print((testObs4, refrigeratorTrainer2.test([testObs3, testObs4])));
##        print((testObs4, refrigeratorTrainer3.test([testObs2, testObs3, testObs4])));
##        print((testObs4, refrigeratorTrainer4.test([testObs1, testObs2, testObs3, testObs4])));

    testObs1 = testObs2;
    testObs2 = testObs3;
    testObs3 = testObs4;

refrigeratorTrace.close();
refrigeratorOutputTrace.close();


##if (not os.path.isfile(fridgeTraceFile)):
##    for i in range(0, 86401):
##        (timestamp, entry) = refridgeTrace.readline().split();
##        timestamp = int(timestamp);
##        entry = float(entry);
##        outputEntry = 0;
##
##        if (entry > 500):
##    ##        print("High output found!");
##            outputEntry = 1;
##            
##        fridgeTrainer.addSingleObservation([entry], outputEntry);
##
##    fridgeTrainer.train();
##
##    pickleFileRef = open(fridgePickleFile, 'wb');
##    pickle.dump(fridgeTrainer, pickleFileRef);
##
##else:
##    pickleFileRef = open(fridgePickleFile, 'rb');
##    fridgeTrainer = pickle.load(pickleFileRef);
##
##
##print(fridgeTrainer.numObservations);
##print(fridgeTrainer.coefficientVector[0]);
##
##for i in range(0,10001):
##    testObs = float(f.readline().split()[1]);
##
##    if (testObs > 300):
##        print((testObs, fridgeTrainer.test([testObs])));
##
##refrigeratorTrace.close();
##pickleFileRef.close();
##
