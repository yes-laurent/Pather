import random
import time
from manim import *
from manim.utils.file_ops import open_file as open_media_file 
from Models.solution import *
from Models.point import *
from Models.car import *
from Models.move import *
import Models.generations as generations

#region constantes

# Chance de link avec un point existant (0-100)
LINKCHANCE = 25
POP = [1, 2]
WEIGHT = [LINKCHANCE/100, 1 - LINKCHANCE/100]

# Générer avec des diagonnales
DIAGONAL = False

# Nombre de points générés par nouveau point
NUMBEROFPOINTS = 3

# Size définit la grosseur du système généré.
SIZE = 50 

# Liste des points du système
POINTS = []
NEWPOINTS = []

# Liste des cars du système
CARS = []

# listes des solutions
SOLUTIONS = []

# Détermine le nombre de cars dans le système
NUMBEROFCARS = 5

# Détermine le nombre de solutions gardées comme modèles pour les générations futures
SELECTIONAMOUNT = 5

# Détermine le nombre de solution par population
POPULATIONSIZE = 5

# Détermine le nombre de générations tentées avant d'arriver à une solution
GENCOUNT = 5

# Densité du réseau généré (ToDo: À implémenter)
DENSITY = 5

#endregion

t = 0
def startTime():
    global t
    t = time.time()

def endTime():
    global t
    et = time.time()
    elapsed_time = et - t
    return elapsed_time

def createPoint(x, y, originPoint = None):
    p1 = GridPoint(x, y, availablePts = [])

    if x <= 15 and x > -15 and y <= 15 and y > -15:
        for p in POINTS:
            if p.x == x and p.y == y:
                c = random.choices(POP, WEIGHT)
                if(c[0] == 1) :
                    createDoubleLink(originPoint, p)
                break
        else:
            POINTS.append(p1)
            NEWPOINTS.append(p1)
            if (originPoint != None):
                createDoubleLink(originPoint, p1)
    del p1

def createDoubleLink(originPoint, destinationPoint):
    if not destinationPoint in originPoint.availablePts:
        originPoint.availablePts.append(destinationPoint)
    if not originPoint in destinationPoint.availablePts:
        destinationPoint.availablePts.append(originPoint)


def start():
    global SOLUTIONS
    startTime()

    print("gen #1: ")
    hasSelectionAmount = False
    for i in range(POPULATIONSIZE):
        for car in CARS:
            car.reset()
        generateSolution(i + 1, hasSelectionAmount=hasSelectionAmount)
        if (len(SOLUTIONS) > SELECTIONAMOUNT):
            hasSelectionAmount = True
            fitness()
            SOLUTIONS.pop()
    generations.incrementCompletedGens()
    
    print("TOP SOLUTION steps : " + str(len(SOLUTIONS[0].moves)))

    for gen in range(GENCOUNT):
        if (len(SOLUTIONS[0].steps) == 1):
            generations.endCompletedGens()
            break
        hasSelectionAmount = False
        solutionNumber = 0
        print("gen #" + str(gen + 2) + ": ")
        bestSolutions = fitness().copy()
        print("Best solution number of steps: " + str(len(bestSolutions[0].moves)))
        SOLUTIONS.clear()
        for solution in bestSolutions:
            SOLUTIONS.append(solution)
            for i in range(round(POPULATIONSIZE/SELECTIONAMOUNT)):
                solutionNumber += 1
                mutate(solution, solutionNumber, hasSelectionAmount)
                if (len(SOLUTIONS) > SELECTIONAMOUNT):
                    hasSelectionAmount = True
                    fitness()
                    SOLUTIONS.pop()
        generations.incrementCompletedGens()
    
    fitness()
    print('Best solution : ' + str(len(SOLUTIONS[0].moves)))
    print('Time to generate ' + str(GENCOUNT) + ' generations:', endTime(), 'seconds')
            
# mutates the solution and create a new one.
# return the newly created solution
def mutate(solution, solutionNumber, hasSelectionAmount):
    newSolution = Solution(solution.moves.copy(), solution.steps.copy())


    stepsLength = len(newSolution.steps)
    randomStep = random.randint(1, stepsLength - 1)

    for _ in range(0, stepsLength - randomStep):
        newSolution.steps.pop()
        newSolution.moves.pop()

    CARS.clear()
    for m in newSolution.moves[len(newSolution.moves) - 1]:
        CARS.append(Car(m.endPt, m.finalPt, m.endPt, started=m.started,stepCount=m.stepCount))

    generateSolution(solutionNumber, newSolution.moves, newSolution.steps, hasSelectionAmount)


def fitness():

    SOLUTIONS.sort(key=lambda x: x.steps[len(x.steps) -1], reverse=False)

    return SOLUTIONS[:SELECTIONAMOUNT]

# tries to generate a solution.
# returns True if it found a solution
# return False if it didn't
def generateSolution(solutionNumber,  initialMoves = [], initialSteps = [], hasSelectionAmount = False) -> bool:
    moves = initialMoves.copy()
    stepMoves = []
    stepSteps = 0
    currentSolution = Solution()
    currentSolution.steps = initialSteps.copy()
    if len(currentSolution.steps) != 0: 
       stepSteps = currentSolution.steps[len(currentSolution.steps) -1]
    nbCarsArrived = 0


    while (len(CARS) != nbCarsArrived):
        random.shuffle(CARS)
        for car in CARS:
            if not car.hasArrived:
                car.try_next_move()
        for car in CARS:
            if not car.hasArrived:
                cMove = Move(car.currentPt, car.nextPt, car.endPt, False, 0)
                if car.move():
                    nbCarsArrived += 1
                cMove.started = car.started
                cMove.stepCount = car.stepCount
                stepMoves.append(cMove)
                stepSteps += 1
        for pt in POINTS:
            pt.resetAvailability()
        moves.append(stepMoves.copy())
        currentSolution.steps.append(stepSteps)
        stepMoves.clear()
        if (hasSelectionAmount):
            if (currentSolution.steps[-1] > SOLUTIONS[SELECTIONAMOUNT -1].steps[-1]):
                return False

    currentSolution.moves = moves
    SOLUTIONS.append(currentSolution)
    return True

def chooseRandomPoint(currentPoint) :
    
    if DIAGONAL:
        choice = random.randint(1, 8)

        match choice:
            case 1:
                return currentPoint.x - 1, currentPoint.y - 1
            case 2:
                return currentPoint.x, currentPoint.y - 1
            case 3:
                return currentPoint.x + 1, currentPoint.y - 1
            case 4:
                return currentPoint.x - 1, currentPoint.y
            case 5:
                return currentPoint.x + 1, currentPoint.y
            case 6:
                return currentPoint.x - 1, currentPoint.y + 1
            case 7:
                return currentPoint.x, currentPoint.y + 1
            case 8:
                return currentPoint.x + 1, currentPoint.y + 1
    else:
        choice = random.randint(1, 4)

        match choice:
            case 1:
                return currentPoint.x, currentPoint.y - 1
            case 2:
                return currentPoint.x - 1, currentPoint.y
            case 3:
                return currentPoint.x + 1, currentPoint.y
            case 4:
                return currentPoint.x, currentPoint.y + 1


def generate():
    print("generating a new model...")

    NEWPOINTS.clear()
    POINTS.clear()

    createPoint(0, 0)

    for n in range(0, SIZE) :
        if len(NEWPOINTS) > 0:
            currentPoint = random.choice(NEWPOINTS)
            NEWPOINTS.remove(currentPoint)
            for n in range(0, NUMBEROFPOINTS):
                x, y = chooseRandomPoint(currentPoint)
                createPoint(x, y, currentPoint)

    for c in range(0, NUMBEROFCARS) :
        startPt = random.choice(POINTS)
        availablePts = POINTS.copy()
        availablePts.remove(startPt)
        CARS.append(Car(startPt, random.choice(availablePts), startPt))

    print("Number of points in the model: " + str(len(POINTS)))

class MainScene(Scene):
    def construct(self):

        maxX = max(pt.x for pt in POINTS)
        minX = min(pt.x for pt in POINTS)
        maxY = max(pt.y for pt in POINTS)
        minY = min(pt.y for pt in POINTS)

        rangeX = abs(maxX) + abs(minX)
        rangeY = abs(maxY) + abs(minY)

        SIZEX=rangeX/7.5
        SIZEY=rangeY/7.5
        CENTERX = (maxX + minX)/2
        CENTERY = (maxY + minY)/2

        groupdots = VGroup()
        grouplines = VGroup()
        for p in POINTS:
            dot = Dot([(p.x - CENTERX)/SIZEX , (p.y - CENTERY) /SIZEY, 0])
            groupdots.add(dot)
            for ap in p.availablePts:
                line = Line(dot.get_center(),[(ap.x - CENTERX)/SIZEX, (ap.y - CENTERY)/SIZEY,0])
                grouplines.add(line)
        self.play(Create(groupdots))
        self.play(Create(grouplines))
        self.pause()
        for step in SOLUTIONS[0].moves:
            groupmoves = VGroup()
            groupAnim = []
            for move in step:
                if (move.startPt != move.finalPt):
                    if (move.endPt == move.finalPt):
                        dotStart = Dot([(move.startPt.x - CENTERX)/SIZEX,(move.startPt.y - CENTERY)/SIZEY,0],color=GREEN)
                    else:
                        dotStart = Dot([(move.startPt.x - CENTERX)/SIZEX,(move.startPt.y - CENTERY)/SIZEY,0],color=RED)
                    groupmoves.add(dotStart)
                    dotEnd = Dot([(move.endPt.x - CENTERX)/SIZEX,(move.endPt.y - CENTERY)/SIZEY,0])
                    line = Line(dotStart.get_center(),dotEnd.get_center())
                    groupAnim.append(MoveAlongPath(dotStart, line))
            self.add(groupmoves)
            self.play(AnimationGroup(*groupAnim,lag_ratio=0))
            self.remove(*[groupmoves[i] for i in range(0,len(groupmoves))])

def start_app(worldSize, density, carCount, generation, population, selectionAmount, diagonal):
    global SIZE
    global DENSITY
    global NUMBEROFCARS
    global SELECTIONAMOUNT
    global GENCOUNT
    global POPULATIONSIZE
    global SOLUTIONS
    global DIAGONAL
    global POINTS
    global NEWPOINTS
    global CARS
    
    generations.createSolutions(generation)
    SIZE = worldSize
    DENSITY = density
    DIAGONAL = diagonal

    manage_density()

    NUMBEROFCARS = carCount
    SELECTIONAMOUNT = selectionAmount
    GENCOUNT = generations.getGenCount()
    POPULATIONSIZE = population
    SOLUTIONS = []
    POINTS = []
    NEWPOINTS = []
    CARS = []   

    generate()
    start()

def render():
    scene = MainScene()
    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)

def manage_density():
    global LINKCHANCE
    global NUMBEROFPOINTS
    match DENSITY:
        case 1:
            LINKCHANCE = 0
            NUMBEROFPOINTS = 1
        case 2:
            LINKCHANCE = 25
            NUMBEROFPOINTS = 3
        case 3:
            LINKCHANCE = 50
            NUMBEROFPOINTS = 4
        case 4:
            LINKCHANCE = 75
            NUMBEROFPOINTS = 6
        case 5:
            LINKCHANCE = 100

            NUMBEROFPOINTS = 50

if __name__ == '__main__':
    start_app(5,5,5,5,5,5, True)
    render()