import numpy as np
import os.path
import pickle
from Tesla import Tesla

def isMicrowaveActive(obs):
    if (obs > 1000):
        return True;
    else:
        return False;

def isKitchOut02Active(obs):
    if (obs > 25):
        return True;
    else:
        return False;

def isKitchOut0304Active(obs):
    if (obs > 1000):
        return True;
    else:
        return False;

def isOvenActive(obs):
    if (obs > 1500):
        return True;
    else:
        return False;

def isRefrigeratorActive(obs):
    if (obs > 500):
        return True;
    else:
        return False;

def isStoveActive(obs):
    if (obs > 1000):
        return True;
    else:
        return False;

# plot((1:150000), KitchOut02(1:150000), (1:150000), KitchOut04(1:150000), (1:150000), KitchOut03(1:150000), (1:150000), Microwave(1:150000), (1:150000), Oven01(1:150000), (1:150000), Oven02(1:150000))

# Get the raw appliance traces
kitchOut02Trace =   open('traces/kitch_out2.dat', mode='r');
kitchOut03Trace =   open('traces/kitch_out3.dat', mode='r');
kitchOut04Trace =   open('traces/kitch_out4.dat', mode='r');
micTrace =          open('traces/microwave.dat', mode='r');
oven01Trace =       open('traces/oven01.dat', mode='r');
oven02Trace =       open('traces/oven02.dat', mode='r');
refrigeratorTrace = open('traces/refrigerator.dat', mode='r');
stoveTrace =        open('traces/stove.dat', mode='r');

# Open files to write appliance output observation traces
kitchOut02OutputTrace =   open('traces/kitch_out2_obs.dat', mode='w');
kitchOut03OutputTrace =   open('traces/kitch_out3_obs.dat', mode='w');
kitchOut04OutputTrace =   open('traces/kitch_out4_obs.dat', mode='w');
micOutputTrace =          open('traces/microwave_obs.dat', mode='w');
oven01OutputTrace =       open('traces/oven01_obs.dat', mode='w');
oven02OutputTrace =       open('traces/oven02_obs.dat', mode='w');
refrigeratorOutputTrace = open('traces/refrigerator_obs.dat', mode='w');
stoveOutputTrace =        open('traces/stove_obs.dat', mode='w');

outputTrace =       open('traces/activity.dat', mode='w');


# Parse each to generate appliance activity observations
for i in range(0, 86400):
    # Parse each to generate appliance activity observations
    (timestamp, kitchOut02Output) = kitchOut02Trace.readline().split();
    kitchOut02Output =   isKitchOut02Active(float(kitchOut02Output));
    kitchOut03Output =   isKitchOut0304Active(float(kitchOut03Trace.readline().split()[1]));
    kitchOut04Output =   isKitchOut0304Active(float(kitchOut04Trace.readline().split()[1]));
    micOutput =          isMicrowaveActive(float(micTrace.readline().split()[1]));
    oven01Output =       isOvenActive(float(oven01Trace.readline().split()[1]));
    oven02Output =       isOvenActive(float(oven02Trace.readline().split()[1]));
    refrigeratorOutput = isRefrigeratorActive(float(refrigeratorTrace.readline().split()[1]));
    stoveOutput = isStoveActive(float(stoveTrace.readline().split()[1]));

    # Write individual appliance output observations to file
    kitchOut02OutputTrace.write(timestamp + "\t" + str(int(kitchOut02Output)) + "\n");
    kitchOut03OutputTrace.write(timestamp + "\t" + str(int(kitchOut03Output)) + "\n");
    kitchOut04OutputTrace.write(timestamp + "\t" + str(int(kitchOut04Output)) + "\n");
    micOutputTrace.write(timestamp + "\t" + str(int(micOutput)) + "\n");
    oven01OutputTrace.write(timestamp + "\t" + str(int(oven01Output)) + "\n");
    oven02OutputTrace.write(timestamp + "\t" + str(int(oven02Output)) + "\n");
    refrigeratorOutputTrace.write(timestamp + "\t" + str(int(refrigeratorOutput)) + "\n");
    stoveOutputTrace.write(timestamp + "\t" + str(int(stoveOutput)) + "\n");

    # Write the perceived user output observations to file
    outputTrace.write(timestamp + "\t" + str(int(kitchOut02Output\
                      or kitchOut03Output\
                      or kitchOut04Output\
                      or micOutput\
                      or oven01Output\
                      or oven02Output\
                      or refrigeratorOutput\
                      or stoveOutput)) + "\n");


# Close raw data file pointers
kitchOut02Trace.close();
kitchOut03Trace.close();
kitchOut04Trace.close();
micTrace.close();
oven01Trace.close();
oven02Trace.close();
refrigeratorTrace.close();
stoveTrace.close();
outputTrace.close();

# Close output observation file pointers
kitchOut02OutputTrace.close();
kitchOut03OutputTrace.close();
kitchOut04OutputTrace.close();
micOutputTrace.close();
oven01OutputTrace.close();
oven02OutputTrace.close();
refrigeratorOutputTrace.close();
stoveOutputTrace.close();
