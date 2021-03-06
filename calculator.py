import os
import sys
import math

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from BlurWindow.blurWindow import blur

from constants import UI_DIR, STYLE_SHEET

class Calculator(QtWidgets.QMainWindow):

    textChanged = QtCore.pyqtSignal()   #Custom signal to detect changes on label

    def __init__(self):

        super(Calculator, self).__init__()

        uic.loadUi(os.path.join(UI_DIR, "calculator.ui"), self)

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)  #PyQt5 QtCore.Qt.FramelessWindowHint
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)   #PyQt5 QtCore.Qt.WA_TranslucentBackground
        self.setStyleSheet(STYLE_SHEET)

        QtWidgets.QSizeGrip(self.sizeGrip)

        blur(self.winId())
        #*** Mouse event var ***
        self.clicked = False
        self.oldPos = QtCore.QPointF()

        #*** Resizing control var ***
        self.resizing = False

        #*** Calculator variables *****
        self.decimalPoint = False
        self.clearScreen = False
        
        self.prevOperation = ""
        self.result = 0
        #******************************
        
        #*** Menu Variable ***
        self.openingMenu = False
        #*********************
        
        self.btnMenu.clicked.connect(self.animatedMenu)

        self.btn_0.clicked.connect(self.btnClicked)
        self.btn_1.clicked.connect(self.btnClicked)
        self.btn_2.clicked.connect(self.btnClicked)
        self.btn_3.clicked.connect(self.btnClicked)
        self.btn_4.clicked.connect(self.btnClicked)
        self.btn_5.clicked.connect(self.btnClicked)
        self.btn_6.clicked.connect(self.btnClicked)
        self.btn_7.clicked.connect(self.btnClicked)
        self.btn_8.clicked.connect(self.btnClicked)
        self.btn_9.clicked.connect(self.btnClicked)
        
        self.btnPlusMinus.clicked.connect(self.btnClicked)
        self.btnPercent.clicked.connect(self.btnClicked)
        self.btnAdd.clicked.connect(self.btnClicked)
        self.btnSub.clicked.connect(self.btnClicked)
        self.btnMul.clicked.connect(self.btnClicked)
        self.btnDiv.clicked.connect(self.btnClicked)
        self.btnEq.clicked.connect(self.btnClicked)

        self.btnOneDivX.clicked.connect(self.btnClicked)
        self.btnPow.clicked.connect(self.btnClicked)
        self.btnSqrt.clicked.connect(self.btnClicked)
        
        self.btnDel.clicked.connect(self.btnClicked)
        self.btnDot.clicked.connect(self.btnClicked)
        self.btnC.clicked.connect(self.btnClicked)
        
        self.btnClose.clicked.connect(self.btnClosePressed)
        self.btnMinimize.clicked.connect(self.btnMinimizePressed)

        self.textChanged.connect(self.checkLabel)   #Custom signal connect
        
        self.timerOnResize = QtCore.QTimer()
        self.timerOnResize.timeout.connect(self.setResizeFlag)  #To check if window is not resizing

        self.animation = QtCore.QPropertyAnimation(self.leftMenuBar, b"minimumWidth")

        self.windowBar.mousePressEvent = self.dragWindow

    def dragWindow(self, event):
        
        self.clicked = True
        self.oldPos = event.globalPosition()      # PyQt5 event.screenPos()

    def mouseReleaseEvent(self, event):

        self.clicked = False

    def mouseMoveEvent(self, event):
        
        if self.clicked and not self.resizing:

            delta = QtCore.QPointF (event.globalPosition() - self.oldPos)    # PyQt5 event.screenPos()
            self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))
            self.oldPos = event.globalPosition()    # PyQt5 event.screenPos()

    def resizeEvent(self, event):

        self.timerOnResize.start(10)
        self.resizing = True

    def setResizeFlag(self):
        self.resizing = False

    def btnClosePressed(self):
        self.close()
    
    def btnMinimizePressed(self):
        self.showMinimized()

    def animatedMenu(self):

        width = self.leftMenuBar.width()

        if not self.openingMenu:

            self.openingMenu = True

            self.animation.stop() 
            self.animation.setDuration(500)
            self.animation.setStartValue(width)
            self.animation.setEndValue(256)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutElastic)

        else:

            self.openingMenu = False  

            self.animation.stop() 
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(0)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InCirc)
        
        self.animation.start()

    def btnClicked(self):
        
        btn = self.sender()

        numbers = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        unaryOp = ("+/-", "%", "1/x", "pow(x,2)", "sqrt(x)")
        binaryOp = ("+", "-", "X", "/")
        
        #*** Set Decimal Point ***
        if btn.text() == "." and self.decimalPoint == False:
            
            self.decimalPoint = True

            if self.clearScreen:
                
                self.clearScreen = False
                self.labelResult.setText("0" + btn.text())

            else:
                self.labelResult.setText(self.labelResult.text() + btn.text())
        
        #*** Set Numbers ***
        if btn.text() in numbers:

            if self.clearScreen:

                self.labelResult.setText("0")
                self.clearScreen = False
            
            if self.labelResult.text() == "0":
                self.labelResult.setText(btn.text())

            else:

                self.labelResult.setText(self.labelResult.text() + btn.text())

        #*** Operations ***
        elif btn.text() in unaryOp:
            self.unaryOperation(btn.text())
        
        elif btn.text() in binaryOp:
            self.binaryOperation(btn.text())
        
        elif btn.text() == "=":
            self.getResult()

        else:
            
            if self.clearScreen:

                self.labelResult.setText("0")
                self.clearScreen = False
                
            self.clearDelete(btn.text())

        self.textChanged.emit() #Check if label has a decimal point

    def unaryOperation(self, op):
        
        try:

            if op == "+/-":
                
                if self.labelResult.text() != "0":

                    value = float(self.labelResult.text())
                    value *= -1

                    self.labelResult.setText(format(value, ".15g"))

            elif op == "%":
                
                    if self.labelResult.text() != "0":

                        value = float(self.labelResult.text())
                        value *= 0.01

                        self.labelResult.setText(format(value, ".15g"))

                        if not self.clearScreen:
                            self.clearScreen = True

            elif op == "pow(x,2)":

                if self.labelResult.text() != "0":

                    value = float(self.labelResult.text())
                    value = math.pow(value, 2)

                    self.labelResult.setText(format(value, ".15g"))

            elif op == "sqrt(x)":

                if self.labelResult.text() != "0":

                    value = float(self.labelResult.text())
                    value = math.sqrt(value)

                    self.labelResult.setText(format(value, ".15g"))

            else:

                if self.labelResult.text() != "0":

                    value = float(self.labelResult.text())
                    value = 1/value

                    self.labelResult.setText(format(value, ".15g"))

                else:

                    self.labelResult.setText("Can't Divide by Zero!")
                    self.clearScreen = True
                    self.result = 0
        
        except ValueError:
            pass

    def binaryOperation(self, op):

        #*** Binary Operations ***

        try:

            if op == "+":
                
                self.prevOperation = "add"
                self.result += float(self.labelResult.text())
                self.labelResult.setText("0")
            
            elif op == "-":
                
                self.prevOperation = "sub"
                self.result += float(self.labelResult.text())
                self.labelResult.setText("0")
            
            elif op == "X" :

                self.prevOperation = "mul"
                self.result += float(self.labelResult.text())
                self.labelResult.setText("0")

            else:

                self.prevOperation = "div"
                self.result += float(self.labelResult.text())
                self.labelResult.setText("0")
        
        except ValueError:
            pass
    
    def getResult(self):
        
        try:

            if self.prevOperation != "":

                if self.prevOperation == "add":
                    self.result += float(self.labelResult.text())

                elif self.prevOperation == "sub":
                    self.result -= float(self.labelResult.text())
                
                elif self.prevOperation == "mul":
                    self.result *= float(self.labelResult.text())

                else:

                    if self.labelResult.text() != "0":
                        self.result /= float(self.labelResult.text())
                                            
                    else:
                        self.result = "Can't Divide by Zero!"

                if isinstance(self.result, str):   #Check if result has a number or a message

                    self.labelResult.setText(self.result)

                else:

                    self.labelResult.setText(format(self.result, ".15g"))
                
                self.clearScreen = True
                self.result = 0
                self.prevOperation = ""

        except ValueError:
            pass

    def clearDelete(self, op):

        if op != ".":

            if op == "DEL":

                if self.labelResult.text() != "Can't Divide by Zero!":

                    if self.labelResult.text() != "" and self.labelResult.text() != "0" and len(self.labelResult.text()) != 1:
                        
                        self.labelResult.setText(
                            self.labelResult.text()[:len(self.labelResult.text()) - 1])

                    else:
                        
                        self.result = 0
                        self.labelResult.setText("0")
                    
                else:

                    self.result = 0
                    self.labelResult.setText("0")

            elif op== "C":

                self.result = 0
                self.labelResult.setText("0")

            else:
                
                self.result = 0
                self.labelResult.setText("0")

    @QtCore.pyqtSlot()
    def checkLabel(self):

        if not "." in self.labelResult.text() and self.decimalPoint == True:

            self.decimalPoint = False
        
def main():
    
    app = QtWidgets.QApplication(sys.argv)

    calculator = Calculator()
    calculator.show()

    app.exec()


if __name__ == "__main__":
    main()
