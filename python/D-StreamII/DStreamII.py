# Defines a class D-StreamII which performs the D-StreamII clustering algorithm. 
# The data points are mapped to a multi dimensional grid. Contians two maps.
# First map "cluaters" contains a cluster id as key and list of Grid coordinates 
# which has same cluster id as value. The second map "gridList" stores all the 
# populates grids information by storing the values with coordinates as key and 
# Grid object as value. 

import io
import numpy as np
import math
import sys, os
from Grid import Grid
from ATTRIBUTE import ATTRIBUTE
from Coordinates import Coordinates

#sys.path.append("../python/Security/Encrypt/")
#from encrypt import encrypt
#from encrypt import rsaEncrypt
#sys.path.remove("../python/Security/Encrypt/")
#sys.path.append("../python/Security/Decrypt/")
#from decrypt import rsaDecrypt
#from decrypt import decrypt
sys.path.insert(1, os.path.join(sys.path[0], '..'));
                
from ContextEngineBase import *

class DStreamII(ContextEngineBase):
    
    gridList = {} 
    clusters = {}
    DIMENSION = 0
    DIMENSION_LOWER_RANGE = list()
    DIMENSION_UPPER_RANGE = list()
    DIMENSION_PARTITION = list()
    DIMENSION_GRIDSIZE = list()
    TOTAL_GRIDS = 1

    # tunable parameters
    dense_threshold = 3.0
    sparse_threshold = 0.8
    decay_factor = 0.998

    time_gap = 0
    correlation_threshold = 0.0
    latestCluster = 0
    complexity = 0;
    numInputs = 0;
    discreteOutput = 0;
    discreteInputs = [];
    key = {};

    #  Number of observations - a running count of the unique numbe of
    #  observations
    numObservations = 0;

    # Matrix model - each row represents a new input vector
    input_Obs = np.empty([0, 0]);

    # Output observation array
    output_Obs = np.empty([0]);    

    time = 0;                                                         

    def __init__(self, complexity, numInputs, discreteOutputs, discreteInputs, appFieldsDict):
        self.complexity = complexity;
        self.numInputs = numInputs;
        self.discreteOutputs = discreteOutputs;
        self.discreteInputs = discreteInputs;
        self.input_Obs = np.empty([0,numInputs]);
        self.DIMENSION = numInputs;
        self.TOTAL_GRIDS = 1;
        self.dense_threshold = 3.0;
        self.sparse_threshold = 0.8;
        self.time_gap = 0;
        self.decay_factor = 0.998;
        self.correlation_threshold = 0.0;
        self.latestCluster = 0;

        if 'gridSize' in appFieldsDict:
            gridSize = appFieldsDict.get("gridSize")
            if len(gridSize) == numInputs:
                self.DIMENSION_GRIDSIZE = gridSize

        if 'gridUpperRange' in appFieldsDict:
            gridUpperRange = appFieldsDict.get("gridUpperRange")
            if len(gridUpperRange) == numInputs:
                self.DIMENSION_UPPER_RANGE = gridUpperRange

        if 'gridLowerRange' in appFieldsDict:
            gridLowerRange = appFieldsDict.get("gridLowerRange")
            if len(gridLowerRange) == numInputs:
                self.DIMENSION_LOWER_RANGE = gridLowerRange

        if 'key' in appFieldsDict:

            key = appFieldsDict.get("key")
            if len(key) != 0:
                self.key = key


    #  Add a new training observation. Requirements: newInputObs must be a
    #  row array of size numInputs. newOutputObs must be a single value.
    def addSingleObservation(self, newInputObs, newOutputObs):
        if (len(newInputObs) == self.numInputs):
            self.input_Obs = np.vstack((self.input_Obs,newInputObs));
            self.output_Obs = np.append(self.output_Obs, newOutputObs);
            self.numObservations += 1;
        else:
            print("Wrong dimensions!");


    #  Add a set of training observations, with the newInputObsMatrix being a
    #  matrix of doubles, where the row magnitude must match the number of inputs,
    #  and the column magnitude must match the number of observations.
    #  and newOutputVector being a column vector of doubles
    def addBatchObservations(self, newInputObsMatrix, newOutputVector):
        i =0 
        for newInputVector in newInputObsMatrix:
            outputValue = newOutputVector[i]
            self.addSingleObservation(newInputVector, outputValue);
            i+=1

   #  Returns the name of the file that contains the encrypted data, takes in 
   #  name of the file containing key and name of the file to be encrypted

#    def encrypt(self, plainTextFile):
#        if len(self.key) != 0:
#            rsaEncrypt(self.key);
#            return encrypt(self.key, plainTextFile);
#
#        else:
#            return
            
    #  Returns the name of the file that contains the decrypted data, takes in 
    #  name of the file containing key and name of the file to be decrypted
#    def decrypt(self, encyptedFile):
#        if len(self.key) != 0:
#            rsaDecrypt(self.key);
#            return decrypt(self.key, encyptedFile);
#
#        else:
#            return

            
    def printClusters(self):
        clusterKeys = self.clusters
        
        for ckey in clusterKeys:
            gridCoords = self.clusters.get(ckey)
            print (" Cluster Index: " + ckey.__str__()) 
            for coord in gridCoords:
                print ("   Coordinates: ")
                print (coord)


    # Returns all the neighbours in each dimension of a grid 
    def getNeighbours(self, from_):
        neighbours = list()
        dim = 0

        while dim < from_.getSize():
            val = from_.getDimension(dim)
            bigger = Coordinates(from_)
            bigger.setDimension(dim, val + 1)
            if bigger in self.gridList:
                neighbours.append(bigger)
            smaller = Coordinates(from_)
            smaller.setDimension(dim, val - 1)
            if smaller in self.gridList:
                neighbours.append(smaller)
            dim += 1
        return neighbours


    # return the big neihbour of a grid in a given dimension
    def getDimensionBigNeighbours(self, from_, dim):
        coord = Coordinates(from_)
        val = coord.getDimension(dim)
        bigger = Coordinates(from_)
        bigger.setDimension(dim, val + 1)

        if bigger in self.gridList:
            return bigger
        return coord
    
    # return the small neighbor of a grid in a given dimension
    def getDimensionSmallNeighbours(self, from_, dim):
        coord = Coordinates(from_)
        val = coord.getDimension(dim)
        smaller = Coordinates(from_)
        smaller.setDimension(dim, val - 1)

        if smaller in self.gridList:
            return smaller
        return coord


    # Checks if after removing a grid the cluster to which it 
    # belonged to remains connected or not. If the cluster
    # becomes unconnected, then split the cluster into two.
    def checkUnconnectedClusterAndSplit(self, clusterIndex):
        if not clusterIndex in self.clusters:
            return
        gridCoords = self.clusters[clusterIndex]
        grpCoords = {}
        if gridCoords.isEmpty():
            return
        
        
        dfsStack = Stack()
        dfsStack.push(gridCoords.iterator().next())
        # To check if the cluster is connected or unconnected.
        # Start with one grid and traverse through all the grids
        # belonging to the cluster. If all the nodes are covered
        # then the cluster is still connected otherwise it is 
        # unconnected.
        while not dfsStack.empty():
            coords = dfsStack.pop()
            grid = self.gridList.get(coords)
            if grid.isVisited():
                continue 
            grid.setVisited(True)
            neighbours = getNeighbours(coords)
            for ngbr in neighbours:
                grpCoords.append(ngbr)
                dfsStack.push(ngbr)

        if len(grpCoords) == len(gridCoords):
            return

        # Unconected clulster. 
        newCluster = self.latestCluster + 1
        self.latestCluster += 1
        self.clusters[newCluster]= grpCoords
        for c in grpCoords:
            g = self.gridList.get(c)
            g.setCluster(newCluster)


    # For each grid find the biggest strongly correlated dense neighbouring cluster
    def findStronglyCorrelatedNeighbourWithMaxClusterSize(self, coord, onlyDense):
        resultCoord = Coordinates(coord)
        initCoord = Coordinates(coord)
        largestClusterSize = 0
        
        grid = self.gridList[initCoord]
        i = 0
        while i < self.DIMENSION:
            big_neighbour = self.getDimensionBigNeighbours(coord,i)
            small_neighbour = self.getDimensionSmallNeighbours(coord,i)

            # check for big neighbours.
            if not big_neighbour.equals(initCoord):
                bigNeighbourGrid = self.gridList[big_neighbour]
                if not onlyDense or  bigNeighbourGrid.isDense():
                    bigNeighbourClusterIndex = bigNeighbourGrid.getCluster()

                    if not bigNeighbourClusterIndex == 0 and not bigNeighbourClusterIndex == grid.getCluster():

                        if bigNeighbourGrid.getAttractionAtIndex(2 * i + 1) > self.correlation_threshold and grid.getAttractionAtIndex(2 * i) > self.correlation_threshold:
                            if bigNeighbourClusterIndex in self.clusters:
                                bigNeighbourClusterGrids = self.clusters.get(bigNeighbourClusterIndex)
                                if len(bigNeighbourClusterGrids) >= largestClusterSize:
                                    largestClusterSize = len(bigNeighbourClusterGrids)
                                    resultCoord = big_neighbour

            # check for small neighbours.
            if not small_neighbour.equals(initCoord):
                smallNeighbourGrid = self.gridList[small_neighbour]
                if not onlyDense or smallNeighbourGrid.isDense():
                    smallNeighbourClusterIndex = smallNeighbourGrid.getCluster()
                    if not smallNeighbourClusterIndex == 0 and not smallNeighbourClusterIndex == grid.getCluster():
                        if smallNeighbourGrid.getAttractionAtIndex(2 * i) > self.correlation_threshold and grid.getAttractionAtIndex(2 * i + 1) > self.correlation_threshold:
                            if smallNeighbourClusterIndex in self.clusters:
                                smallNeighbourClusterGrids = self.clusters.get(smallNeighbourClusterIndex)
                                if len(smallNeighbourClusterGrids) >= largestClusterSize:
                                    largestClusterSize = len(smallNeighbourClusterGrids)
                                    resultCoord = small_neighbour
            i += 1
        return resultCoord


    # removes the sporadic grids after every time interval gap.
    # if the grid's density is less than density threshold function
    # then it is a sporadic grid.
    def removeSporadicGrids(self, gridList, time):
        removeGrids = list()
        gridListKeys = gridList.keys()
        for glKey in gridListKeys:
            grid = gridList.get(glKey)
            key = glKey.getCoords()
            lastTimeElementAdded = grid.getLastTimeElementAdded()
            densityThresholdFunc = (self.sparse_threshold * (1 - math.pow(self.decay_factor, time - lastTimeElementAdded + 1))) / (self.TOTAL_GRIDS * (1 - self.decay_factor))
            grid.updateDecayedGridDensity(time)
            grid.updateGridAttribute()
            grid.updateDecayedGridAttraction(time)
            grid.setLastTimeUpdated(time)
            if grid.getGridDensity() < densityThresholdFunc:
                removeGrids.append(key)
        #for index in removeGrids:
            #gridList.remove(index)   


    # This methos is called every time interval. The grids whose attributes are changes
    # from the last time interval gap call the clustering is modified for the grid.
    def adjustClustering(self, gridList, time):
        gridListKeys = gridList.keys()
        for coordkey in gridListKeys:
            grid = gridList.get(coordkey)
            key = coordkey.getCoords()

            if not grid.isAttributeChangedFromLastAdjust():
                continue 
            
            gridCluster = grid.getCluster()
            

            if grid.isSparse():

                # if the grid becomes sparse and it belogned to a cluster
                # check if the clusters becomes unconected or not
                if gridCluster in self.clusters:
                    clusterCoords = self.clusters.get(gridCluster)
                    grid.setCluster(0)
                    del clusterCoords[key]
                    self.checkUnconnectedClusterAndSplit(gridCluster)

            elif grid.isDense():

                # if the grid is dense then check if it can be clustered with it's neighbours
                neighbourCoords = self.findStronglyCorrelatedNeighbourWithMaxClusterSize(key, False);

                # if the grids doesn't contain any neighbor then create a new isolated cluster.
                if not neighbourCoords in self.gridList or neighbourCoords.equals(coordkey):

                    if not gridCluster in  self.clusters:
                    
                        clusterIndex = self.latestCluster + 1
                        self.latestCluster += 1
                        coordset = []
                        coordset.append(key)
                        self.clusters[clusterIndex] = coordset
                        grid.setCluster(clusterIndex)
                    grid.setAttributeChanged(False)
                    continue


                neighbour = self.gridList.get(neighbourCoords)
                neighbourClusterIndex = neighbour.getCluster()
                
                # if the neighbor doesnt belong to any cluster then do anything
                # otherwise merge the cluster with the neighbouring cluster.
                if not neighbourClusterIndex in self.clusters:
                    continue 
                neighbourClusterGrids = self.clusters.get(neighbourClusterIndex)
                
                
                if neighbour.isDense():
                    if not gridCluster in self.clusters:
                        grid.setCluster(neighbourClusterIndex)
                        self.clusters[neighbourClusterIndex].append(key)
                    else:
                        currentClusterGrids = self.clusters.get(gridCluster)
                        size1 = 0                        
                        for val in currentClusterGrids:
                            size1 +=1
                        size2 = 0
                        
                        for val in neighbourClusterGrids:
                            size2 +=1

                        if size2 >= size1:
                            for c in currentClusterGrids:
                                coord = Coordinates(c)
                                g = self.gridList.get(coord)
                                g.setCluster(neighbourClusterIndex)
                                self.clusters[neighbourClusterIndex].append(c)
                            del self.clusters[gridCluster]
                        else:
                            for c in neighbourClusterGrids:
                                g = self.gridList.get(c)
                                g.setCluster(gridCluster)
                                self.clusters[gridCluster].append(c)
                            del self.clusters[neighbourClusterIndex]

                elif neighbour.isTransitional():
                    if not gridCluster in self.clusters:
                        grid.setCluster(neighbourClusterIndex)
                        self.clusters[neighbourClusterIndex].append(key)
                    else:
                        currentClusterGrids = self.clusters.get(gridCluster)
                        if len(currentClusterGrids) >= len(neighbourClusterGrids):
                            self.clusters[gridCluster].append(neighbourCoords)
                            clusterGrid = clusters[neighbourClusterIndex]
                            del clusterGrid[neighbourCoords]

            elif grid.isTransitional():
                # if the grid is transitional then merge with the neighbouring cluster..
                if gridCluster in self.clusters:
                    del self.clusters[gridCluster]
                neighbourCoords = self.findStronglyCorrelatedNeighbourWithMaxClusterSize(key, True);
                if not neighbourCoords in self.gridList or neighbourCoords.equals(coordkey):
                    grid.setAttributeChanged(False)
                    grid.setCluster(0)
                    continue 
                
                neighbour = self.gridList.get(neighbourCoords)
                neighbourClusterIndex = neighbour.getCluster()
                if neighbourClusterIndex in self.clusters:
                    self.clusters[neighbourClusterIndex].append(key)

            grid.setAttributeChanged(False)
    


    # Maps the data points to corresponding grids and update/create grid 
    # object which contains charateristic vector. 
    def mapDataToGrid(self, dataInfo):
        datalength = len(dataInfo)
        if datalength != self.DIMENSION:
            return
        grid_coords = list()
        data_coords = list()
        data = 0.0
        grid_Width = 0.0
        dim_index = 0
        i = 0
        while i < datalength:
            data = float(dataInfo[i])
            data_coords.append(data)
            if data >= self.DIMENSION_UPPER_RANGE[i] or data < self.DIMENSION_LOWER_RANGE[i]:
                return
            grid_Width = float(self.DIMENSION_UPPER_RANGE[i] - self.DIMENSION_LOWER_RANGE[i]) / float(self.DIMENSION_PARTITION[i])
            dim_index = int(math.floor((data - self.DIMENSION_LOWER_RANGE[i]) / grid_Width))
            grid_coords.append(dim_index)
            i += 1

        
        gridCoords = Coordinates(grid_coords)

       # check if the grid object is already created or not. 
        if not gridCoords in self.gridList:
            g = Grid(False,0,self.time,1,ATTRIBUTE.SPARSE, self.DIMENSION, self.DIMENSION_UPPER_RANGE, self.DIMENSION_LOWER_RANGE, self.DIMENSION_PARTITION, self.TOTAL_GRIDS, self.decay_factor, self.dense_threshold, self.sparse_threshold, self.correlation_threshold)
            attrL = g.getAttraction(data_coords, grid_coords)
            g.setInitialAttraction(attrL)
            self.gridList[gridCoords] = g
        else:
            g = self.gridList[gridCoords]
            gridCoords = None
            g.updateGridDensity(self.time)
            g.updateGridAttribute()
            attrL = g.getAttraction(data_coords, grid_coords)
            g.updateGridAttraction(attrL, self.time)
            g.setLastTimeUpdated(self.time)
            

    # update the parameters based on the key value pair provided by the user.
    def updateParameters(self):
        factor = 0.0
        pairs = 0.0
        total_pairs = 0
        i =0
        while i < self.DIMENSION:
            factor  = self.TOTAL_GRIDS / self.DIMENSION_PARTITION[i]
            pairs = self.DIMENSION_PARTITION[i] - 1
            total_pairs += (factor)*(pairs)
            i += 1

        self.correlation_threshold = self.dense_threshold / (total_pairs * ( 1 - self.decay_factor))
        dense_to_sparse_time = math.log(self.sparse_threshold/ self.dense_threshold)/math.log(self.decay_factor)
        sparse_to_dense_time = math.log((self.TOTAL_GRIDS - self.dense_threshold) / (self.TOTAL_GRIDS - self.sparse_threshold))/ math.log(self.decay_factor)
        self.time_gap = int (min(dense_to_sparse_time, sparse_to_dense_time))
        return None;
            
    #  Train the coefficients on the existing observation matrix if there are
    #  enough observations.
    def train(self):
        upperRangeGiven = len(self.DIMENSION_UPPER_RANGE)
        lowerRangeGiven = len(self.DIMENSION_LOWER_RANGE)
        gridSizeGiven = len(self.DIMENSION_GRIDSIZE)
        if ( upperRangeGiven > 0 and lowerRangeGiven > 0 and gridSizeGiven > 0 ):
            i =0
            while i < self.DIMENSION:
                upperRange = self.DIMENSION_UPPER_RANGE[i]
                lowerRange = self.DIMENSION_LOWER_RANGE[i]
                gridSize = self.DIMENSION_GRIDSIZE[i]
                partition = int((upperRange-lowerRange)/gridSize)
                self.DIMENSION_PARTITION.append(partition)
                self.TOTAL_GRIDS *= partition
                i += 1
            self.updateParameters()
            return True
        
        if (self.numObservations >= 0):
            print("Training started");
            i=0            
            temparray = []

            while i <self.DIMENSION:
                tempInputOneDim = self.input_Obs[:,i]            

                tempOutput = self.output_Obs
                minVal = float(tempInputOneDim[0])
                maxVal = float(tempInputOneDim[0])

                clusterMaxValue = {}
                clusterMinValue = {}
                size = len(tempInputOneDim)
                j =0
                while j < size:
                    currVal = float(tempInputOneDim[j])
                    if ( currVal < minVal):
                        minVal = currVal

                    if ( currVal > maxVal):
                        maxVal = currVal

                    if ( gridSizeGiven > 0):
                        j +=1 
                        continue
                    

                    clusterId = float(tempOutput[j])
                    if not clusterId in clusterMaxValue:
                        clusterMaxValue[clusterId] = currVal
                        clusterMinValue[clusterId] = currVal
                    else:
                        if (clusterMaxValue.get(clusterId)< currVal):
                            clusterMaxValue[clusterId] = currVal
                        if (clusterMinValue.get(clusterId) > currVal):
                            clusterMinValue[clusterId] = currVal
                    
                    j += 1
                

                minDiff = 9223372036854775807
                gridSize = 1
                
                if ( gridSizeGiven == 0 ) :
                    clusterIdKeys = clusterMaxValue.keys()
                    minClusId = 0
                    for clusId in clusterIdKeys:
                        maxClusVal = clusterMaxValue.get(clusId)
                        minClusVal = clusterMinValue.get(clusId)
                        if maxClusVal == minClusVal:
                            continue
                    
                        currDiff = maxClusVal - minClusVal
                        if ( currDiff < minDiff):
                            minDiff = currDiff
                            minClusId = clusId
                    gridSize = 4*minDiff
                else :
                    gridSize = self.DIMENSION_GRIDSIZE[i]


                upperRange =0
                lowerRange =0

                if ( upperRangeGiven == 0):
                    upperRange = int(maxVal + maxVal)
                    self.DIMENSION_UPPER_RANGE.append(upperRange)
                else:
                    upperRange = self.DIMENSION_UPPER_RANGE[i]

                if ( lowerRangeGiven == 0):                
                    lowerRange = int(minVal - minVal)
                    self.DIMENSION_LOWER_RANGE.append(lowerRange)
                else:
                    lowerRange = self.DIMENSION_LOWER_RANGE[i]

                partition = int((upperRange - lowerRange)/(gridSize))
                self.DIMENSION_PARTITION.append(partition)
                self.TOTAL_GRIDS *= partition
                i += 1

            self.updateParameters()
            return True;
        else:
            print("Not enough observations to train!");
            return False;

    #  Execute the trained matrix against the given input observation
    #inputObsVector is a row vector of doubles
    def execute(self, inputObsVector):
        
        if(len(inputObsVector) == self.numInputs):            
            self.mapDataToGrid(inputObsVector);
            
            if self.time > 0 :
                if self.time % self.time_gap == 0:
                     self.removeSporadicGrids(self.gridList, self.time)
                     self.adjustClustering(self.gridList, self.time)
                     
            self.time += 1;    
            return None;
        else:
            print("Wrong dimensions, fail to execute");
            return None;

