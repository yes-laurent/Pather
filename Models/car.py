import random

class Car:
    def __init__(self, startPt, endPt, currentPt, nextMove = None, hasArrived = False, stepCount = 0, started = False, optimalPath = []):
        self.startPt = startPt
        self.endPt = endPt
        self.currentPt = currentPt
        self.nextPt = nextMove
        self.stepCount = stepCount
        self.hasArrived = hasArrived
        self.started = started
        self.optimalPath = optimalPath

    def reset(self):
        self.currentPt = self.startPt
        self.nextPt = None
        self.stepCount = 0
        self.hasArrived = False
        self.started = False
        self.optimalPath = []


    # return : true if moved, false if stayed still
    def try_next_move(self):
        if len(self.optimalPath) <= 0:
            self.aStar()
        availablePts = self.currentPt.availablePts.copy()
        run = True
        while (run):
            chosenPt = self.optimalPath[-1]
            availablePts.remove(chosenPt)
            if chosenPt.nextMoveEmpty:
                self.nextPt = chosenPt
                chosenPt.nextMoveEmpty = False
                chosenPt.carNextMove = self
                run = False
            else:
                if len(availablePts) != 0 :
                    chosenPt.weight = 10
                    self.aStar()
                if self.optimalPath[-1] == chosenPt:

                    if self.started:
                        self.currentPt.nextMoveEmpty = False
                        if self.currentPt.carNextMove != None:
                            self.currentPt.carNextMove.try_next_move()
                        self.currentPt.carNextMove = self
                    self.nextPt = self.currentPt
                    run = False
                    

    
    def move(self)-> bool:
        if self.nextPt == self.optimalPath[-1]:
            self.optimalPath.pop()
        self.stepCount += 1
        self.currentPt = self.nextPt
        self.nextPt = None
        if self.currentPt != self.startPt:
            self.started = True
        if self.currentPt == self.endPt:
            self.hasArrived = True
        return self.hasArrived

    def aStar(self):
        openList = []
        closedList = []
        solution = []
        result = []
        #tuple: (le point, value g, value h, value f, parentPoint)
        #g : weight entre 2 points
        #h : distance entre le point et le endPt
        #f : g + h
        openList.append( (self.currentPt, 0, 0, 0, None) )

        searching = True

        while (len(openList) > 0 and searching):
            openList.sort(key = lambda a: a[3], reverse=True)
            q = openList.pop()
            for pt in q[0].availablePts:
                if pt == self.endPt:
                    solution.append( (pt,0,0,0,q) )
                    searching = False
                    break
                else:
                    g = q[1] + pt.weigth
                    h = pt.evaluateDist(self.endPt)
                    f = g+h
                if (len([item for item in openList if item[3] <= f and item[0] == pt]) <= 0 
                    and len([item for item in closedList if item[3] <= f and item[0] == pt]) <= 0):
                    openList.append( (pt,g,h,f,q) )
            if searching:
                closedList.append(q)
        
        while (solution[-1][4] != None):
            solution.append(solution[-1][4])
        solution.pop()
        for pt in solution:
            result.append(pt[0])
        self.optimalPath = result