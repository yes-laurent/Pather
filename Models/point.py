import math

class GridPoint:
    def __init__(self, x, y, nextMoveEmpty = True, availablePts = [], carNextMove = None):
        self.x = x
        self.y = y
        self.availablePts = availablePts
        self.nextMoveEmpty = nextMoveEmpty
        self.carNextMove = carNextMove
        self.weigth = 1

    def __repr__(self):
        return str("(" + str(self.x) + ", " + str(self.y) + ")")

    def resetAvailability(self):
        self.nextMoveEmpty = True
        self.carNextMove = None

    def evaluateDist(self, endPt):
        return math.sqrt( (self.x - endPt.x)**2
                + (self.y - endPt.y)**2 )
