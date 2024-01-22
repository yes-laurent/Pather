import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import os
import main
import threading
import time
import Models.generations as generations

WORLDSIZE = 5
DENSITY = 1
CARCOUNT = 1
DIAGONAL = True
GENERATION = 2
POPULATION = 2
SELECTIONAMOUNT = 2

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Pather'
        self.left = 50
        self.top = 50
        self.width = 400
        self.height = 200
        self.initUI()
    
    def initUI(self):
        # Center app
        self.setWindowIcon(QtGui.QIcon(os.path.join('Assets', 'icon.png')))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        self.createWorldLayout()
        self.createSimulationLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.worldGroupBox)
        windowLayout.addWidget(self.simulationGroupBox)

        self.startBtn = QPushButton('Start', self)
        self.startBtn.clicked.connect(self.on_click)
        windowLayout.addWidget(self.startBtn)

        self.pbar = QProgressBar(self)
        windowLayout.addWidget(self.pbar)
        self.pbar.hide()

        self.setLayout(windowLayout)
        
        self.show()

    def createWorldLayout(self):
        self.worldGroupBox = QGroupBox("World generation options")
        layout = QHBoxLayout()
        
        WorldSize = QSpinBox()
        WorldSize.setMinimum(5)
        WorldSize.setMaximum(100)
        WorldSize.valueChanged.connect(self.world_value_changed)
        labelWorldSize = QLabel(self)
        labelWorldSize.setText("Size")

        layout.addWidget(labelWorldSize)
        layout.addWidget(WorldSize)
        
        Density = QSpinBox()
        Density.setMinimum(1)
        Density.setMaximum(5)
        Density.valueChanged.connect(self.density_value_changed)
        labelDensity = QLabel(self)
        labelDensity.setText("Density (1-5)")
        
        layout.addWidget(labelDensity)
        layout.addWidget(Density)

        CarCount = QSpinBox()
        CarCount.setMinimum(1)
        CarCount.setMaximum(100)
        CarCount.valueChanged.connect(self.carCount_value_changed)
        labelCarCount = QLabel(self)
        labelCarCount.setText("Car count")

        layout.addWidget(labelCarCount)
        layout.addWidget(CarCount)

        Diagonals = QCheckBox("Generate diagonals")
        Diagonals.setChecked(True)
        Diagonals.stateChanged.connect(self.diagonnal_value_changed)

        layout.addWidget(Diagonals)

        self.worldGroupBox.setLayout(layout)

    def world_value_changed(self, worldSize):
        global WORLDSIZE
        WORLDSIZE = worldSize

    def density_value_changed(self, density):
        global DENSITY
        DENSITY = density

    def carCount_value_changed(self, carCount):
        global CARCOUNT
        CARCOUNT = carCount

    def diagonnal_value_changed(self, diagonnal):
        global DIAGONAL
        if diagonnal == 0:
            DIAGONAL = False
        else:
            DIAGONAL = True

    def createSimulationLayout(self):
        self.simulationGroupBox = QGroupBox("Solutions options")
        layout = QHBoxLayout()
        
        Selection = QSpinBox()
        Selection.setMinimum(2)
        Selection.setMaximum(100)
        Selection.valueChanged.connect(self.selection_value_changed)
        labelWorldSize = QLabel(self)
        labelWorldSize.setText("Selection amount")

        layout.addWidget(labelWorldSize)
        layout.addWidget(Selection)
        
        Population = QSpinBox()
        Population.setMinimum(2)
        Population.setMaximum(100)
        Population.valueChanged.connect(self.population_value_changed)
        labelDensity = QLabel(self)
        labelDensity.setText("Population size")
        
        layout.addWidget(labelDensity)
        layout.addWidget(Population)

        Generation = QSpinBox()
        Generation.setMinimum(2)
        Generation.setMaximum(100)
        Generation.valueChanged.connect(self.generation_value_changed)
        labelCarCount = QLabel(self)
        labelCarCount.setText("Generation count")

        layout.addWidget(labelCarCount)
        layout.addWidget(Generation)

        self.simulationGroupBox.setLayout(layout)

    def selection_value_changed(self, selection):
        global SELECTIONAMOUNT
        SELECTIONAMOUNT = selection

    def population_value_changed(self, population):
        global POPULATION
        POPULATION = population

    def generation_value_changed(self, generation):
        global GENERATION
        GENERATION = generation

    @pyqtSlot()
    def on_click(self):
        self.pbar.show()
        self.startBtn.setEnabled(False)
        t = threading.Thread(target=main.start_app, args=(WORLDSIZE, DENSITY, CARCOUNT, GENERATION, POPULATION, SELECTIONAMOUNT,DIAGONAL,))
        t.start()
        run = True
        time.sleep(0.1)
        while (run):
            self.pbar.setValue(round(generations.getCompletedGens()/generations.getGenCount() * 100))
            if (generations.getCompletedGens() >= generations.getGenCount()):
                run = False
        t.join()
        t2 = threading.Thread(target=main.render())
        t2.start()
        t2.join()
        self.pbar.hide()
        self.startBtn.setEnabled(True)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()
    sys.exit(app.exec_())
