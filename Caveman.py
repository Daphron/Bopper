from __future__ import division
import random as r
from scipy import interpolate
import numpy as np

#from deap import base

MAXIMUM_WEIGHT_CAVEMAN = 5
HEIGHT = 10
BODY_WEIGHT_PROPORTION = 0.75
NUM_POINTS = 3

MINIMUM_LENGTH_FOREARM = 2
MAXIMUM_LENGTH_FOREARM = 5

MINIMUM_FORCE = -3
MAXIMUM_FORCE = 3

MINIMUM_LENGTH_BICEP = 2
MAXIMUM_LENGTH_BICEP = 4

MINIMUM_LENGTH_STRING = 0
MAXIMUM_LENGTH_STRING = 0

MINIMUM_RADIUS_BOPPER = 1
MAXIMUM_RADIUS_BOPPER = 1

MINIMUM_HEIGHT_ARMS = HEIGHT * (3.0/4)
MAXIMUM_HEIGHT_ARMS = HEIGHT * (3.0/4)

class Appendage:
    def __init__(self, wFor, wBic, wBop, params=None, index=0):
        #weight meant to be set
        self.lForearm = r.uniform(MAXIMUM_LENGTH_FOREARM, MINIMUM_LENGTH_FOREARM)
        self.lBicep = r.uniform(MAXIMUM_LENGTH_BICEP, MINIMUM_LENGTH_BICEP)
        self.rBopper = r.uniform(MAXIMUM_RADIUS_BOPPER, MINIMUM_RADIUS_BOPPER)
        self.lString = r.uniform(MAXIMUM_LENGTH_STRING, MINIMUM_LENGTH_STRING)
        self.wForearm = wFor
        self.wBicep = wBic
        self.wBopper = wBop

        x = np.linspace(0, 1.0, num = NUM_POINTS)
        y = np.array([r.uniform(MAXIMUM_FORCE, MINIMUM_FORCE) for _ in xrange(NUM_POINTS - 1)])
        y = np.append(y, y[0])
        self.iElbow = np.poly1d(np.polyfit(x, y, 10))
        x = np.linspace(0, 1.0, num = NUM_POINTS)
        y = np.array([r.uniform(MAXIMUM_FORCE, MINIMUM_FORCE) for _ in xrange(NUM_POINTS - 1)])
        y = np.append(y, y[0])
        self.iShoulder = np.poly1d(np.polyfit(x, y, 10))

        #set elasticiy
        self.elasticity = r.random()

        if params is not None:
            if index == 0:
                self.lForearm = params[1]
                self.lBicep = params[2]
                self.rBopper = params[3]
                self.lString = params[4]
                self.wForearm = params[5]
                self.wBicep = params[6]
                self.wBopper = params[7]
            elif index == 1:
                self.lForearm = params[8]
                self.lBicep = params[9]
                self.rBopper = params[10]
                self.lString = params[11]
                self.wForearm = params[12]
                self.wBicep = params[13]
                self.wBopper = params[14]


class Caveman():
    
    def __init__(self, numApp, params=None):

        self.weights = (1,)
        # self.nAppendages = numApp
        self.hBody = HEIGHT


        self.arm_height = r.uniform(MAXIMUM_HEIGHT_ARMS, MINIMUM_HEIGHT_ARMS)

        #sample the body weight between 0 and MAXIMUM_WEIGHT_CAVEMAN * BODY_WEIGHT_PROPORTION
        actProp = r.uniform(BODY_WEIGHT_PROPORTION, 0)
        self.wBody = MAXIMUM_WEIGHT_CAVEMAN * actProp

        #setting the weights, and then normalizing them.
        #remainingWeight holds the weight that is to be divided up into the arms and bopper.
        remainingWeight = (1 - actProp) * MAXIMUM_WEIGHT_CAVEMAN

        weg = [r.random() for _ in xrange(3 * numApp)]
        sumw = sum(weg)
        weg = [remainingWeight * (i / sumw) for i in weg]

        ################################################
        if params is not None:
            self.wBody = params[0]
        ###############################################
        
        #setting the appendages
        self.appendages = []
        for j in xrange(numApp):
            self.appendages.append( Appendage(weg[int(j)], weg[int(j) + 1], weg[int(j) + 2], params, j) )
        

