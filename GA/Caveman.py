import random as r
from scipy import interpolate
import numpy as np

MAXIMUM_WEIGHT_CAVEMAN = 1
HEIGHT = 5
BODY_WEIGHT_PROPORTION = 0.75
NUM_POINTS = 10

MINIMUM_LENGTH_FOREARM = 0.5
MAXIMUM_LENGTH_FOREARM = 1


MINIMUM_LENGTH_BICEP = 0.5
MAXIMUM_LENGTH_BICEP = 1

MINIMUM_LENGTH_STRING = 0.5
MAXIMUM_LENGTH_STRING = 1

MINIMUM_RADIUS_BOPPER = 0
MAXIMUM_RADIUS_BOPPER = 1

MINIMUM_HEIGHT_ARMS = 0
MAXIMUM_HEIGHT_ARMS = HEIGHT

class Appendage:
    def __init__(self, wFor, wBic, wBop):
        #weight meant to be set
        self.lForearm = r.uniform(MAXIMUM_LENGTH_FOREARM, MINIMUM_LENGTH_FOREARM)
        self.lBicep = r.uniform(MAXIMUM_LENGTH_BICEP, MINIMUM_LENGTH_BICEP)
        self.rBopper = r.uniform(MAXIMUM_RADIUS_BOPPER, MINIMUM_RADIUS_BOPPER)
        self.lString = r.uniform(MAXIMUM_LENGTH_STRING, MINIMUM_LENGTH_STRING)
        self.wForearm = wFor
        self.wBicep = wBic
        self.wBopper = wBop

class Caveman:    
    def __init__(self, numApp):
        self.nAppendages = numApp
        self.hBody = HEIGHT
        
        #sample the body weight between 0 and MAXIMUM_WEIGHT_CAVEMAN * BODY_WEIGHT_PROPORTION
        self.wBody = BODY_WEIGHT_PROPORTION * MAXIMUM_WEIGHT_CAVEMAN * r.random()

        #setting the weights, and then normalizing them.
        #remainingWeight holds the weight that is to be divided up into the arms and bopper.
        remainingWeight = (1 - BODY_WEIGHT_PROPORTION) * MAXIMUM_WEIGHT_CAVEMAN

        weg = [r.random() for _ in xrange(3 * numApp)]
        sumw = sum(weg)
        weg = [remainingWeight * (i / sumw) for i in weg]
        
        #setting the appendages
        self.appendages = []
        for j in xrange(numApp):
            self.appendages.append( Appendage(weg[int(j)], weg[int(j) + 1], weg[int(j) + 2]) )
        
        x = np.linspace(0, 1.0, num = NUM_POINTS)
        y = np.array([r.uniform(-1, 1) for _ in xrange(NUM_POINTS - 1)])
        y = np.append(y, y[0])
        self.impulse = interpolate.interp1d(x, y)

        #set elasticiy
        self.cElasticity = r.random()

