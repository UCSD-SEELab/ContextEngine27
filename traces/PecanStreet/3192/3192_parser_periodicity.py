import csv
import datetime
import math
import numpy as np
import os.path
import pickle
import time


def createOutputRowByDOW(applianceName,
                    date,
                    time,
                    dayOfWeek,
                    applianceValue,
                    waterUsed,
                    isCooking,
                    isUsingWater,
                    isPluggingInCar,
                    history=0):
    if (applianceName not in inputDataActual):
        inputDataActual[applianceName] = [];

    inputDataActual[applianceName].append([date,
                                           time,
                                           dayOfWeek,
                                           applianceValue,
                                           waterUsed,
                                           isCooking,
                                           isUsingWater,
                                           isPluggingInCar]);

def generateOutputCSVsByDOW(inputDict, outputDict):
    for key in inputDict:
        inputRows = inputDict[key];
        outputRows = outputDict[key];
        dayByDayInput = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]};
        dayByDayOutput = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]};

        i = 0;
        for inputRow in inputRows:
            dayByDayInput[int(inputRow[2])].append(inputRow);
            if (i < len(outputRows)):
                dayByDayOutput[int(inputRow[2])].append(outputRows[i]);
            i += 1;

        for day in dayByDayInput:
            with open("3192_"
                      + key
                      + "_"
                      + str(day)
                      + "_input.csv", 'w', newline='') as csvFile:
                writer = csv.writer(csvFile);
                for inputRow in dayByDayInput[day]:
                    writer.writerow(inputRow);
            with open("3192_"
                      + key
                      + "_"
                      + str(day)
                      + "_output.csv", 'w', newline='') as csvFile:
                writer = csv.writer(csvFile);
                for outputRow in dayByDayOutput[day]:
                    writer.writerow(outputRow);

def generateOutputCSVs(inputDict, outputDict, history=0):
    for key in inputDict:
        inputRows = inputDict[key];
        outputRows = outputDict[key];

        history = [];

        i = 0;
        for inputRow in inputRows:
            generateOutputCSVsByDOW[int(inputRow[2])].append(inputRow);
            if (i < len(outputRows)):
                dayByDayOutput[int(inputRow[2])].append(outputRows[i]);
            i += 1;

        for day in generateOutputCSVsByDOW:
            with open("3192_"
                      + key
                      + "_"
                      + str(day)
                      + "_input.csv", 'w', newline='') as csvFile:
                writer = csv.writer(csvFile);
                for inputRow in generateOutputCSVsByDOW[day]:
                    writer.writerow(inputRow);
            with open("3192_"
                      + key
                      + "_"
                      + str(day)
                      + "_output.csv", 'w', newline='') as csvFile:
                writer = csv.writer(csvFile);
                for outputRow in dayByDayOutput[day]:
                    writer.writerow(outputRow);

# CSV input and output files
elecFilePath = "3192_elec.csv";
waterFilePath = "3192_water.csv";
outputFilePathBath = "periodicity/3192_bathroom.csv";
outputFilePathCar = "periodicity/3192_car.csv";
outputFilePathClWash = "periodicity/3192_clothWasher.csv";
outputFilePathDsWash = "periodicity/3192_dishWasher.csv";
outputFilePathDisp = "periodicity/3192_disposal.csv";
outputFilePathGen = "periodicity/3192_generation.csv";
outputFilePathKitchApp1 = "periodicity/3192_kitchenApp1.csv";
outputFilePathKitchApp2 = "periodicity/3192_kitchenApp2.csv";
outputFilePathLvgRm1 = "periodicity/3192_livingRoom1.csv";
outputFilePathMwave = "periodicity/3192_microwave.csv";
outputFilePathVent = "periodicity/3192_Vent.csv";
outputFilePathWaterUsed = "periodicity/3192_waterUsed.csv";
outputFilePathIsCooking = "periodicity/3192_isCooking.csv";
outputFilePathIsUsingWater = "periodicity/3192_isUsingWater.csv";
outputFilePathIsPluggingInCar = "periodicity/3192_isPluggingInCar.csv";

# Output file data, as a list of lists for each row
outputDataBath = []
outputDataCar = []
outputDataClWash = []
outputDataDsWash = []
outputDataDisp = []
outputDataGen = []
outputDataKitchApp1 = []
outputDataKitchApp2 = []
outputDataLvgRm1 = []
outputDataMwave = []
outputDataVent = []
outputDataWaterUsed = []
outputDataIsCooking = []
outputDataIsUsingWater = []
outputDataIsPluggingInCar = []
inputDataActual = {};
energyPredictionActual = {};
energyFlexBinaryActual = {};
energyFlexKWHActual = {};

# Lists storing timestamps and meter readings water usage.
timestampList = [];
waterMeterList = [];

# Columns and nominal (appliance not actively used) values for electricity
dateColumn = 0;
timeColumn = 1;

bathroom1Column = 4;
bathroom1Nominal = 0;
bathroom1Label = "bathroom1";

car1Column = 5;
car1Nominal = 0;
car1Label = "car1";

clothesWasher1Column = 6;
clothesWasher1Nominal = 0;
clothesWasher1Label = "clothesWasher1";

dishwasher1Column = 7;
dishwasher1Nominal = 0;
dishwasher1Label = "dishwasher1";

disposal1Column = 8;
disposal1Nominal = 0;
disposal1Label = "disposal1";

gener1Column = 11;
gener1Nominal = 0;
gener1Label = "gen";

kitchenapp1Column = 13;
kitchenapp1Nominal = 0;
kitchenapp1Label = "kitchenapp1";

kitchenapp2Column = 14;
kitchenapp2Nominal = 0;
kitchenapp2Label = "kitchenapp2";

livingroom1Column = 15;
livingroom1Nominal = 0.037
livingroom1Label = "livingroom1";

microwave1Column = 16;
microwave1Nominal = 0.009;
microwave1Label = "microwave1";

venthood1Column = 19;
venthood1Nominal = 0;
venthood1Label = "venthood1";

waterColumn = 20;

# Additional activity values
waterColumnName = "water";
cookingColumnName = "isCooking";
usingWaterColumnName = "isUsingWater";
isPluggingInCarColumnName = "isPluggingInCar";


# Open the water meter data and get the timestamps and meter readings
# to use for interpolation.
with open(waterFilePath) as csvFile:
    reader = csv.reader(csvFile);
    i = 0;
    for row in reader:
        inputList = [];
        outputValue = 0.0;
        if (i == 0):
            None;
        else:
            dtTimestamp = datetime.datetime.strptime(row[0],
                                                     '%m/%d/%Y %H:%M');
            
            timestampList.append(dtTimestamp.timestamp());
            waterMeterList.append(float(row[1]));

        # increment the row counter
        i+=1;

# Open the electricity meter data and generate the processed output
with open(elecFilePath) as csvFile:
    # Derived activities
    isCooking = 0;
    isUsingWater = 0;
    oldWaterMeterValue = 0;
    oldCarChargingValue = 0;
    
    reader = csv.reader(csvFile);
    i = 0;
    for row in reader:
        outputValue = 0.0;
        outputRow = []
        outputRowBath = []
        outputRowCar = []
        outputRowClWash = []
        outputRowDsWash = []
        outputRowDisp = []
        outputRowGen = []
        outputRowKitchApp1 = []
        outputRowKitchApp2 = []
        outputRowLvgRm1 = []
        outputRowMwave = []
        outputRowVent = []

        outputRowWaterUsed = []
        outputRowIsCooking = []
        outputRowIsUsingWater = []
        outputRowIsPluggingInCar = []
        if (i == 0):
            # Create a row with the column names. Comment out any elements you don't want.
            #outputRow.append(row[dateColumn]);
            #outputRow.append(row[timeColumn]);
            #outputRowBath.append(row[bathroom1Column]);
            #outputRowCar.append(row[car1Column]);
            #outputRowClWash.append(row[clothesWasher1Column]);
            #outputRowDsWash.append(row[dishwasher1Column]);
            #outputRowDisp.append(row[disposal1Column]);
            #outputRowGen.append(row[gener1Column]);
            #outputRowKitchApp1.append(row[kitchenapp1Column]);
            #outputRowKitchApp2.append(row[kitchenapp2Column]);
            #outputRowLvgRm1.append(row[livingroom1Column]);
            #outputRowMwave.append(row[microwave1Column]);
            #outputRowVent.append(row[venthood1Column]);
            print ("first row ignored")
            #outputRowWater.append(waterColumnName);
            #outputRow.append(cookingColumnName);
            #outputRow.append(usingWaterColumnName);
            #outputRow.append(isPluggingInCarColumnName);

        else:
            # Get the current timestamp and convert to datetime.
            timeString = row[dateColumn];
            dtTimestamp = datetime.datetime.strptime(timeString,
                                                     '%m/%d/%Y %H:%M');
            dtDOW = dtTimestamp.weekday();

            #Generate derived activity data

            # Water Usage
            waterUsed = 0;

            # Car Plugged in
            isPluggingInCar = 0;


            # Is Cooking
            isCooking = 0;
            if (float(row[disposal1Column]) > disposal1Nominal
                or float(row[kitchenapp1Column]) > kitchenapp1Nominal
                or float(row[kitchenapp2Column]) > kitchenapp2Nominal
                or float(row[microwave1Column]) > microwave1Nominal
                or float(row[venthood1Column]) > venthood1Nominal):
                isCooking = 1;
                
            if (i == 1):
                oldWaterMeterValue = np.interp(dtTimestamp.timestamp(),
                                                  timestampList,
                                                  waterMeterList);
                oldCarChargingValue = float(row[car1Column]);
                
            else:
                newWaterMeterValue = np.interp(dtTimestamp.timestamp(),
                                                  timestampList,
                                                  waterMeterList);
                newCarChargingValue = float(row[car1Column]);

                # Determine if the water meter changed at all
                if (newWaterMeterValue > oldWaterMeterValue):
                    waterUsed = newWaterMeterValue - oldWaterMeterValue;

                # Determine if car was unplugged
                if (oldCarChargingValue == 0 and newCarChargingValue > 0):
                    isPluggingInCar = 1;

                # Update the old values with new ones. DO NOT TRY TO USE OLD
                # VALUES AFTER THIS LINE!
                oldCarChargingValue = newCarChargingValue;
                oldWaterMeterValue = newWaterMeterValue;
                
            # Determine if water is being actively used by the user
            isUsingWater = 0;
            if (waterUsed > 0
                and (float(row[bathroom1Column]) > bathroom1Nominal
                or float(row[disposal1Column]) > disposal1Nominal
                or float(row[kitchenapp1Column]) > kitchenapp1Nominal
                or float(row[kitchenapp2Column]) > kitchenapp2Nominal)):
                isUsingWater = 1;

            # Create a row with the column names. Comment out any elements you don't want.
            #outputRow.append(row[dateColumn]);
            #outputRow.append(row[timeColumn]);
            outputRowBath.append(row[bathroom1Column]);
            outputRowCar.append(row[car1Column]);
            outputRowClWash.append(row[clothesWasher1Column]);
            outputRowDsWash.append(row[dishwasher1Column]);
            outputRowDisp.append(row[disposal1Column]);
            outputRowGen.append(row[gener1Column]);
            outputRowKitchApp1.append(row[kitchenapp1Column]);
            outputRowKitchApp2.append(row[kitchenapp2Column]);
            outputRowLvgRm1.append(row[livingroom1Column]);
            outputRowMwave.append(row[microwave1Column]);
            outputRowVent.append(row[venthood1Column]);

            outputRowWaterUsed.append(waterUsed);
            outputRowIsCooking.append(isCooking);
            outputRowIsUsingWater.append(isUsingWater);
            outputRowIsPluggingInCar.append(isPluggingInCar);

            # Create appropriate input and output rows for each appliance
            #createOutputRowByDOW(bathroom1Label, row[dateColumn], row[timeColumn],
            #                dtDOW, row[bathroom1Column], waterUsed, isCooking,
            #                isUsingWater, isPluggingInCar);
            #if (bathroom1Label not in energyPredictionActual):
            #    energyPredictionActual[bathroom1Label] = [];
            #else:
            #    energyPredictionActual[bathroom1Label].append([float(row[bathroom1Column])]);

            #createOutputRowByDOW(car1Label, row[dateColumn], row[timeColumn],
            #                dtDOW, row[car1Column], waterUsed, isCooking,
            #                isUsingWater, isPluggingInCar);
            #if (car1Label not in energyPredictionActual):
            #    energyPredictionActual[car1Label] = [];
            #else:
            #    energyPredictionActual[car1Label].append([float(row[car1Column])]);

            #createOutputRowByDOW(clothesWasher1Label, row[dateColumn], row[timeColumn],
            #                dtDOW, row[clothesWasher1Column], waterUsed, isCooking,
            #                isUsingWater, isPluggingInCar);
            #if (clothesWasher1Label not in energyPredictionActual):
            #    energyPredictionActual[clothesWasher1Label] = [];
            #else:
            #    energyPredictionActual[clothesWasher1Label].append([float(row[clothesWasher1Column])]);

            #createOutputRowByDOW(kitchenapp1Label, row[dateColumn], row[timeColumn],
            #                dtDOW, row[kitchenapp1Column], waterUsed, isCooking,
            #                isUsingWater, isPluggingInCar);
            #if (kitchenapp1Label not in energyPredictionActual):
            #    energyPredictionActual[kitchenapp1Label] = [];
            #else:
            #    energyPredictionActual[kitchenapp1Label].append([float(row[kitchenapp1Column])]);




        # Write the row to outputData
        outputDataBath.append(outputRowBath);
        outputDataCar.append(outputRowCar)
        outputDataClWash.append(outputRowClWash)
        outputDataDsWash.append(outputRowDsWash)
        outputDataDisp.append(outputRowDisp)
        outputDataGen.append(outputRowGen)
        outputDataKitchApp1.append(outputRowKitchApp1)
        outputDataKitchApp2.append(outputRowKitchApp2)
        outputDataLvgRm1.append(outputRowLvgRm1)
        outputDataMwave.append(outputRowMwave)
        outputDataVent.append(outputRowVent)
        outputDataWaterUsed.append(outputRowWaterUsed)
        outputDataIsCooking.append(outputRowIsCooking)
        outputDataIsUsingWater.append(outputRowIsUsingWater)
        outputDataIsPluggingInCar.append(outputRowIsPluggingInCar)


        # increment the row counter
        i+=1;

# Write output data to file
with open(outputFilePathBath, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataBath:
        writer.writerow(outputValue);
with open(outputFilePathCar, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataCar:
        writer.writerow(outputValue);
with open(outputFilePathClWash, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataClWash:
        writer.writerow(outputValue);
with open(outputFilePathDsWash, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataDsWash:
        writer.writerow(outputValue);
with open(outputFilePathDisp, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataDisp:
        writer.writerow(outputValue);
with open(outputFilePathGen, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataGen:
        writer.writerow(outputValue);
with open(outputFilePathKitchApp1, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataKitchApp1:
        writer.writerow(outputValue);
with open(outputFilePathLvgRm1, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataLvgRm1:
        writer.writerow(outputValue);
with open(outputFilePathMwave, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataMwave:
        writer.writerow(outputValue);
with open(outputFilePathVent, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataVent:
        writer.writerow(outputValue);
with open(outputFilePathWaterUsed, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataWaterUsed:
        writer.writerow(outputValue);
with open(outputFilePathIsCooking, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataIsCooking:
        writer.writerow(outputValue);
with open(outputFilePathIsUsingWater, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputDataIsUsingWater:
        writer.writerow(outputValue);
with open(outputFilePathIsPluggingInCar, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile);
    for outputValue in outputRowIsPluggingInCar:
        writer.writerow(outputValue);


# Write input file
#generateOutputCSVsByDOW(inputDataActual, energyPredictionActual);
