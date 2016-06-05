#!/usr/bin/env python

import io
import numpy as np
import math

class Coordinates(object):

    def __init__(self, c):
        coord  = []
        for i in c:
            coord.append(i)
            i+=1
        self.coords = coord

    def __hash__(self):
        return hash(str(self.coords))
        
    def __eq__(self, other):
        other_list = (other).coords
        if len(other_list) != len(self.coords):
            return False
        i = 0
        while i < len(self.coords):
            if int(self.coords[i]) != int(other_list[i]):
                return False
            i += 1
        return True

    def getCoords(self):
        coord = []
        for c in self.coords:
            coord.append(c)
        return coord

    def getDimension(self, d):
        if self.coords != None and len(self.coords) > d:
            return self.coords[d]
        else:
            return None

    def setDimension(self, d, val):
        if self.coords != None and len(self.coords) > d:
            self.coords[d] = val
        else:
            print ("Cannot set selected value")

    def getSize(self):
        return len(self.coords)

    def equals(self, other):
        other_list = (other).coords
        if len(other_list) != len(self.coords):
            return False
        i = 0
        while i < len(self.coords):
            if int(self.coords[i]) != int(other_list[i]):
                return False
            i += 1
        return True

    def __str__(self):
        return self.coords.__str__()
# ============================================================================================================================================================================

class ATTRIBUTE:
    DENSE = u'DENSE'
    TRANSITIONAL = u'TRANSITIONAL'
    SPARSE = u'SPARSE'

#  Characteristic vector of a grid
class Grid(object):

    visited = False
    last_time_updated = 0
    last_time_element_added = 0
    grid_density = 0.0
    grid_attribute = ATTRIBUTE.SPARSE
    attraction_list = list()
    cluster = -1
    attributeChanged = False
    DIMENSION =0
    DIMENSION_UPPER_RANGE =0 
    DIMENSION_LOWER_RANGE =0 
    DIMENSION_PARTITION = 0
    TOTAL_GRIDS =0
    decay_factor =0 
    dense_threshold =0 
    sparse_threshold =0
    correlation_threshold =0
    

    def __init__(self, v, c, tg, D, attr, dim, dim_upper, dim_lower, dim_par, total_grids, decay, d_thres, s_thres,c_thres):
        self.visited = v
        self.cluster = c
        self.last_time_updated = tg
        self.grid_density = D
        self.grid_attribute = attr
        self.DIMENSION = dim
        self.DIMENSION_UPPER_RANGE = dim_upper 
        self.DIMENSION_LOWER_RANGE =dim_lower 
        self.DIMENSION_PARTITION = dim_par
        self.TOTAL_GRIDS = total_grids
        self.decay_factor = decay
        self.dense_threshold = d_thres
        self.sparse_threshold = s_thres
        self.correlation_threshold = c_thres
        self.attraction_list = list()


    def __hash__(self):
        return hash(str(self.name))
    
    def __eq__(self, other):
        return str(self.name) == str(other.name)


    def setVisited(self, v):
        self.visited = v

    def isVisited(self):
        return self.visited

    def setCluster(self, c):
        self.cluster = c

    def getCluster(self):
        return self.cluster

    def setLastTimeUpdated(self, tg):
        self.last_time_updated = tg

    def getLastTimeUpdated(self):
        return self.last_time_updated

    def setLastTimeElementAdded(self, tg):
        self.last_time_element_added = tg

    def getLastTimeElementAdded(self):
        return self.last_time_element_added

    def getGridDensity(self):
        return self.grid_density

    def updateGridDensity(self, time):
        self.grid_density = self.grid_density * (math.pow(self.decay_factor, time - self.last_time_updated)) + 1

    def updateDecayedGridDensity(self, time):
        self.grid_density = self.grid_density * (math.pow(self.decay_factor, time - self.last_time_updated))

    def isAttributeChangedFromLastAdjust(self):
        return self.attributeChanged

    def setAttributeChanged(self, val):
        self.attributeChanged = val

    def isDense(self):
        return self.grid_attribute == ATTRIBUTE.DENSE

    def isTransitional(self):
        return self.grid_attribute == ATTRIBUTE.TRANSITIONAL

    def isSparse(self):
        return self.grid_attribute == ATTRIBUTE.SPARSE

    def getGridAttribute(self):
        str_ = ""
        if self.isDense():
            str_ = "DENSE"
        if self.isTransitional():
            str_ = "TRANSITIONAL"
        if self.isSparse():
            str_ = "SPARSE"
        return str_

    def updateGridAttribute(self):
        avg_density = 1.0 / (self.TOTAL_GRIDS * (1 - self.decay_factor))
        if self.grid_attribute != ATTRIBUTE.DENSE and self.grid_density >= self.dense_threshold * avg_density:
            self.attributeChanged = True
            self.grid_attribute = ATTRIBUTE.DENSE
        elif self.grid_attribute != ATTRIBUTE.SPARSE and self.grid_density <= self.sparse_threshold * avg_density:
            self.attributeChanged = True
            self.grid_attribute = ATTRIBUTE.SPARSE
        elif self.grid_attribute != ATTRIBUTE.TRANSITIONAL and self.grid_density > self.sparse_threshold * avg_density and self.grid_density < self.dense_threshold * avg_density:
            self.attributeChanged = True
            self.grid_attribute = ATTRIBUTE.TRANSITIONAL

    def setInitialAttraction(self, attrL):
        for i in attrL:
            self.attraction_list.append(i)


    def normalizeAttraction(self, attr_list):

        total_attr = 0.0
        i = 0
        while i < 2 * self.DIMENSION + 1:
            total_attr += attr_list[i]
            i += 1
        if total_attr <= 0:
            return
        attr = float()
        #  normalize
        i = 0
        while i < 2 * self.DIMENSION + 1:
            attr = attr_list[i]
            attr_list[i]= attr / total_attr
            i += 1


    def getAttraction(self, data_coords, grid_coords):
        attr_list = list()
        i = 0

        while i < 2 * self.DIMENSION + 1:
            attr_list.append(1.0)
            i += 1
        last_element = 2 * self.DIMENSION
        i = 0
        closeToBigNeighbour = False
        while i < len(grid_coords):
            upper_range = self.DIMENSION_UPPER_RANGE[i]
            lower_range = self.DIMENSION_LOWER_RANGE[i]
            num_of_partitions = self.DIMENSION_PARTITION[i]
            partition_width = (upper_range - lower_range) / (num_of_partitions);
            center = grid_coords[i]*partition_width + partition_width/2.0;
            radius = partition_width / 2.0
            epsilon = 0.6*radius
            if data_coords[i] > center:
                closeToBigNeighbour = True
            if (radius - epsilon) > abs(data_coords[i] - center):
                attr_list[2 * i] = 0.0
                attr_list[2 * i + 1] = 0.0
                attr_list[last_element] = 1.0
            else:
                if closeToBigNeighbour:
                    weight1 = ((epsilon - radius) + (data_coords[i] - center))
                    weight2 = ((epsilon + radius) - (data_coords[i] - center))
                    prev_attr = attr_list[2 * i]
                    attr_list[2 * i] = prev_attr * weight1
                    attr_list[2 * i + 1] = 0.0
                    k =0
                    while k < 2 * self.DIMENSION + 1:
                        if k != 2 * i and k != 2 * i + 1:
                            prev_attr = attr_list[k]
                            attr_list[k] = prev_attr * weight2
                        k = k + 1
                else:
                    weight1 = ((epsilon - radius) - (data_coords[i] - center))
                    weight2 = ((epsilon + radius) + (data_coords[i] - center))
                    prev_attr = attr_list[2 * i + 1]
                    attr_list[2 * i + 1] = prev_attr * weight1
                    attr_list[2 * i] =  0.0
                    k =0
                    while k < 2 * self.DIMENSION + 1:
                        if k != 2 * i and k != 2 * i + 1:
                            prev_attr = attr_list[k]
                            attr_list[k] = prev_attr * weight2
                        k = k + 1
            i += 1
        self.normalizeAttraction(attr_list)
        return attr_list

    def updateGridAttraction(self, attr_list, time):
        last = 2 * self.DIMENSION
        i = 0
        while i < 2 * self.DIMENSION + 1:
            attraction_decay1 = self.attraction_list[i]*(math.pow(self.decay_factor,(time -self.last_time_updated) ))
            attr_new = attr_list[i] + attraction_decay1
            if attraction_decay1 <= self.correlation_threshold and attr_new > self.correlation_threshold and i != last and not self.attributeChanged:
                self.setAttributeChanged(True)
            self.attraction_list[i] = attr_new
            i += 1

    def updateDecayedGridAttraction(self, time):
        i = 0
        while i < 2 * self.DIMENSION + 1:
            attraction_decay = self.attraction_list[i]*(math.pow(self.decay_factor,(time -self.last_time_updated) ))
            self.attraction_list[i] = attraction_decay
            i += 1

            
    def getAttractionAtIndex(self, i):
        return self.attraction_list[i]


# ============================================================================================================================================================================

class DStreamII:
    
    gridList = {} 
    clusters = {}
    DIMENSION = 0
    DIMENSION_LOWER_RANGE = list()
    DIMENSION_UPPER_RANGE = list()
    DIMENSION_PARTITION = list()
    DIMENSION_GRIDSIZE = list()
    TOTAL_GRIDS = 1
    dense_threshold = 3.0

    #  Cm = 3.0
    sparse_threshold = 0.8

    #  Cl = 0.8
    time_gap = 0
    decay_factor = 0.998
    correlation_threshold = 0.0
    latestCluster = 0

    complexity = 0;

    numInputs = 0;

    discreteOutput = 0;

    discreteInputs = [];

    #  Number of observations - a running count of the unique numbe of
    #  observations
    numObservations = 0;

    # Matrix model - each row represents a new input vector
    #eg. x_Obs = array([[ 1.,  2.,  3.],
    #   [ 2.,  1.,  5.]])
    input_Obs = np.empty([0, 0]);

    # Output observation array
    # eg. y = [0, 1]
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


    #  Add a new training observation. Requirements: newInputObs must be a
    #  row array of size numInputs. newOutputObs must be a single value.
    def addSingleObservation(self, newInputObs, newOutputObs):
        if (len(newInputObs) == self.numInputs):
            self.input_Obs = np.vstack((self.input_Obs,newInputObs));
            #self.output_Obs = np.append(self.output_Obs, newOutputObs);
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
            #outputValue = newOutputVector.pop();
            self.addSingleObservation(newInputVector, outputValue);
            i+=1
            
    def printClusters(self):
        clusterKeys = self.clusters
        
        for ckey in clusterKeys:
            gridCoords = self.clusters.get(ckey)
            print (" Cluster Index: " + ckey.__str__()) 
            for coord in gridCoords:
                print ("   Coordinates: ")
                print (coord)


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

    def getDimensionBigNeighbours(self, from_, dim):
        coord = Coordinates(from_)
        val = coord.getDimension(dim)
        bigger = Coordinates(from_)
        bigger.setDimension(dim, val + 1)

        if bigger in self.gridList:
            return bigger
        return coord

    def getDimensionSmallNeighbours(self, from_, dim):
        coord = Coordinates(from_)
        val = coord.getDimension(dim)
        smaller = Coordinates(from_)
        smaller.setDimension(dim, val - 1)

        if smaller in self.gridList:
            return smaller
        return coord

    def checkUnconnectedClusterAndSplit(self, clusterIndex):
        if not clusterIndex in self.clusters:
            return
        gridCoords = self.clusters[clusterIndex]
        grpCoords = {}
        if gridCoords.isEmpty():
            return
        dfsStack = Stack()
        dfsStack.push(gridCoords.iterator().next())
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
        newCluster = self.latestCluster + 1
        self.latestCluster += 1
        self.clusters[newCluster]= grpCoords
        for c in grpCoords:
            g = self.gridList.get(c)
            g.setCluster(newCluster)


    def findStronglyCorrelatedNeighbourWithMaxClusterSize(self, coord, onlyDense):
        resultCoord = Coordinates(coord)
        initCoord = Coordinates(coord)
        largestClusterSize = 0
        
        grid = self.gridList[initCoord]
        i = 0
        while i < self.DIMENSION:
            big_neighbour = self.getDimensionBigNeighbours(coord,i)
            
            small_neighbour = self.getDimensionSmallNeighbours(coord,i)

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


    def adjustClustering(self, gridList, time):
        gridListKeys = gridList.keys()
        for coordkey in gridListKeys:
            grid = gridList.get(coordkey)
            key = coordkey.getCoords()

            if not grid.isAttributeChangedFromLastAdjust():
                continue 
            
            gridCluster = grid.getCluster()
            if grid.isSparse():
                if gridCluster in self.clusters:
                    clusterCoords = self.clusters.get(gridCluster)
                    grid.setCluster(0)
                    del clusterCoords[key]
                    self.checkUnconnectedClusterAndSplit(gridCluster)
            elif grid.isDense():
                neighbourCoords = self.findStronglyCorrelatedNeighbourWithMaxClusterSize(key, False);

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
            

    def updateParameters(self):
        factor = 0.0
        pairs = 0.0
        total_pairs = 0
        #print (self.DIMENSION_UPPER_RANGE)
        #print (self.DIMENSION_LOWER_RANGE)
        #print (self.DIMENSION_PARTITION)

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

