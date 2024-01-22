__genCount = None
__completedGens = None

def createSolutions(genCount):
    global __genCount
    global __completedGens

    __genCount = genCount
    __completedGens = 0


def getGenCount():
    return __genCount

def getCompletedGens():
    return __completedGens

def incrementCompletedGens():
    global __completedGens
    
    __completedGens += 1

def endCompletedGens():
    global __completedGens

    __completedGens = __genCount
