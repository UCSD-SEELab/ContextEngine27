# Defines a class Grid which contains the characteristic vector. Characteristic vector includes grid density, grid attribute, 
# last time the grid was updated and attraction of each grids with its neighbours. Each grid consists of 2 neighbbours in each 
# dimension. 2-D grid will have 4 neighbours. Similarly 3 dimensional grids contains 6 neighbours.

import io
import numpy as np
import math
from ATTRIBUTE import ATTRIBUTE

class Grid(object):

    # Characteristic Vector of a grid
    visited = False
    last_time_updated = 0
    last_time_element_added = 0
    grid_density = 0.0
    grid_attribute = ATTRIBUTE.SPARSE
    attraction_list = list()   # The last element of the list contains the attraction of the grid with itself.
    cluster = -1
    attributeChanged = False

    # Paramters which are required as a input from the user
    DIMENSION =0
    DIMENSION_UPPER_RANGE =0 
    DIMENSION_LOWER_RANGE =0 
    DIMENSION_PARTITION = 0

    # Parameters which are computed based on the user input
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


    # update the grid attributes of a grid based on the current density 
    # of the grid. This  method is called every time inteval gap. 
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

    # Normalises the attraction of each grid with its neighbour
    # such that total attraction of a grid is equal to 1.
    def normalizeAttraction(self, attr_list):

        total_attr = 0.0
        i = 0
        while i < 2 * self.DIMENSION + 1:
            total_attr += attr_list[i]
            i += 1
        if total_attr <= 0:
            return
        attr = float()
        
        i = 0
        while i < 2 * self.DIMENSION + 1:
            attr = attr_list[i]
            attr_list[i]= attr / total_attr
            i += 1

    # Calculates and return a list of attraction values of each grid in all dimensions
    def getAttraction(self, data_coords, grid_coords):
        attr_list = list()
        i = 0

        while i < 2 * self.DIMENSION + 1:
            attr_list.append(1.0)
            i += 1
        last_element = 2 * self.DIMENSION
        i = 0
        closeToBigNeighbour = False

        # Iterate over all the dimensions
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

            # if data point of a grid lies within the hypercube 
            # then set the attraction of the grid to its neighbor 
            # as 0 and to itself as 1
            if (radius - epsilon) > abs(data_coords[i] - center):
                attr_list[2 * i] = 0.0
                attr_list[2 * i + 1] = 0.0
                attr_list[last_element] = 1.0
            else:
                
                # Calculate the attraction of the data point with both the neighbours.
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

        # Normalizr attraction
        self.normalizeAttraction(attr_list)
        return attr_list

    # update the grid attraction every time interval gap
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

