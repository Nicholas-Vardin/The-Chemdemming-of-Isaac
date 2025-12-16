'''
numpy vector math

By Nicholas Vardin

This file contains functions used to manipulate vectors that are 2 lengthed iterables
'''


import numpy as np
import math

def scaleVector(v,scale):
    '''scales the inputted vector so that its absolute value is the scale'''
    absV = absValue(v)
    return np.array([float(scale*v[0]/absV),float(scale*v[1]/absV)])

def absValue(v):
    '''Returns absolute value of vector'''
    return (v[0]**2+v[1]**2)**(1/2)

def rotateVector(v,angle):
    '''rotates 2d vector by angle
    - Angle in radians'''
    return np.array([v[0]*math.cos(angle)-v[1]*math.sin(angle),v[0]*math.sin(angle)+v[1]*math.cos(angle)])