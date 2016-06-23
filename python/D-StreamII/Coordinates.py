# Defines a class Coordinates which contains the coordinate values of a element of a grid.
# Stores the coordinates value for each dimension in a list  
import io
import numpy as np
import math
import sys, os

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
