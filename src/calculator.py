import math

from PyQt6 import QtCore, QtWidgets, QtGui
from constants import *

class StandardCalculator(QtCore.QObject):

    def __init__(self, widgets, display):
        super(StandardCalculator, self).__init__()

        self.display = display
        self.widgets = widgets

        self.numbers = []
        self.operators = []

        self.groupButtons()
        self.connectButtonSignals()

        self.decimalPointExist = False
        self.clearScreen = False
        self.equalsClicked = True
        self.prevOperation = None
        self.firstValue = 0
        self.secondValue = 0

        self.display.setText("0")

    def groupButtons(self):

        for btn in self.widgets.findChildren(QtWidgets.QPushButton):

            if btn.text() in NUMBERS:
                self.numbers.append(btn)
            
            else:
                self.operators.append(btn)

    def setOperatorsEnabled(self, enabled=True):

        for btn in self.operators:
            btn.setEnabled(enabled)

    def connectButtonSignals(self):

        for btn in self.numbers:
            btn.clicked.connect(self.on_btn_clicked)

        for btn in self.operators:
            btn.clicked.connect(self.on_btn_clicked)

    def on_btn_clicked(self):
        
        btn = self.sender()

        input = btn.text()
        print("Input: ", btn.text())
        #*** Set Decimal Point ***
        if input == "." and self.decimalPointExist == False:
            pass
        
        #*** Set Numbers ***
        if input in NUMBERS:
            self.setNumber(input)

        #*** Operations ***
        elif input in UNARY_OPERATIONS:
            self.unaryOperation(input)
        
        elif input in BINARY_OPERATIONS:
            self.binaryOperation(input)
        
        elif input == "=":
            if not self.equalsClicked:
                self.equalsClicked = True

            self.getResult()

    def setNumber(self, input):
        
        if self.clearScreen:
            self.display.setText("0")
            self.clearScreen = False

        if self.display.text() == "0":

            strValue = input
        
        else:
            strValue = self.display.text() + input
        
        self.display.setText(strValue)

    def unaryOperation(self, operation):
        
        if operation == "%":
            value = float(self.display.text()) / 100

        elif operation == "+/-":
            value = float(self.display.text()) * -1

        elif operation == "1/x":
            value = 1 / float(self.display.text())

        elif operation == "pow(x,2)":
            value = math.pow(float(self.display.text()), 2)

        elif operation == "sqrt(x)":
            value = math.sqrt(float(self.display.text()))

        strValue = str(format(value, ".15g"))

        self.display.setText(strValue)
        self.clearScreen = True

    def binaryOperation(self, operation):
        
        if self.prevOperation == "/" and self.display.text() == "0":
            self.setOperatorsEnabled(enabled=False)
            self.display.setText("Error")
            self.firstValue = 0
            self.secondValue = 0
            self.prevOperation = None
            return

        if self.equalsClicked:
            self.equalsClicked = False
            self.firstValue = float(self.display.text())
            self.secondValue = 0

        else:
            self.firstValue += float(self.display.text())
        
        self.prevOperation = operation
        self.display.setText(str(self.firstValue))
        self.clearScreen = True

    def getResult(self):
        
        if self.secondValue  == 0:
            self.secondValue = float(self.display.text())

        if self.prevOperation == "+":
            self.firstValue += self.secondValue

        elif self.prevOperation == "-":
            self.firstValue -= self.secondValue

        elif self.prevOperation == "/":

            try:
                self.firstValue /= self.secondValue
            except:
                self.setOperatorsEnabled(enabled=False)
                self.display.setText("Error")
                self.firstValue = 0
                self.secondValue = 0
                self.prevOperation = None
                return

        elif self.prevOperation == "X":
            self.firstValue *= self.secondValue

        strValue = str(format(self.firstValue, ".15g"))
        self.display.setText(strValue)

class ScientificCalculator(StandardCalculator):

    def __init__(self, widgets, display):
        super(ScientificCalculator, self).__init__(widgets, display)