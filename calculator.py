import os
import sys
import math

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from BlurWindow.blurWindow import blur

from constants import(
    UI_DIR,
    STYLE_SHEET,    
    NUMBERS,
    EQ,
    DECIMAL_POINT,
    DEL_CLEAR,
    UNARY_OPERATIONS,
    BINARY_OPERATIONS,
)

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

        for idx in range(self.comboBox.count()):
            self.comboBox.model().item(idx).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        for idx in range(self.comboBox_2.count()):
            self.comboBox_2.model().item(idx).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

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
        self.btnStdCalc.clicked.connect(self.on_btnFromMenu_clicked)
        self.btnSciCalc.clicked.connect(self.on_btnFromMenu_clicked)

        self.grpBtnOperation = []
        self.grpBtnNumber = []
        self.grpBtnEq = []
        self.grpBtnDEL_C = []
        self.grpBtnDecimalPoint = []

        self.grpBtnOperationEnabled = True

        self.__groupButtons()
        self.__connectGroupButtonSignals()

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

    def __groupButtons(self):

        for btn in QtCore.QObject.findChildren(self, QtWidgets.QPushButton):
            if btn.text() in NUMBERS:
                self.grpBtnNumber.append(btn)
            
            elif(btn.text() in UNARY_OPERATIONS or btn.text() in BINARY_OPERATIONS and
                    not btn.objectName() in ("btnMinimize", "btnClose")):

                self.grpBtnOperation.append(btn)

            elif btn.text() in EQ:
                self.grpBtnEq.append(btn)

            elif btn.text() in DEL_CLEAR:
                self.grpBtnDEL_C.append(btn)
            
            elif btn.text() in DECIMAL_POINT:
                self.grpBtnDecimalPoint.append(btn)

            else:
                pass
                
    def __connectGroupButtonSignals(self):

        for btn in self.grpBtnNumber:
            btn.clicked.connect(self.on_btn_clicked)
        
        for btn in self.grpBtnOperation:
            btn.clicked.connect(self.on_btn_clicked)
        
        for btn in self.grpBtnEq:
            btn.clicked.connect(self.on_btn_clicked)

        for btn in self.grpBtnDEL_C:
            btn.clicked.connect(self.on_btn_clicked)
        
        for btn in self.grpBtnDecimalPoint:
            btn.clicked.connect(self.on_btn_clicked)

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

    def on_btnFromMenu_clicked(self):

        btn = self.sender()
        currentIdx = self.stackedWidget.currentIndex()

        if "Std" in btn.objectName():
            if currentIdx != 0:
                self.result = 0
                self.labelResult.setText("0")
                self.stackedWidget.setCurrentIndex(0)
        
        elif "Sci" in btn.objectName():
            if currentIdx != 1:
                self.result = 0
                self.labelResult.setText("0")
                self.stackedWidget.setCurrentIndex(1)

    def on_btn_clicked(self):
        
        btn = self.sender()

        numbers = NUMBERS
        unaryOp = UNARY_OPERATIONS
        binaryOp = BINARY_OPERATIONS
        
        #*** Set Decimal Point ***
        if btn.text() == "." and self.decimalPoint == False:
            
            self.decimalPoint = True

            if self.clearScreen:
                if not self.grpBtnOperationEnabled:
                    self.setOperationEnabled(state=True)

                self.clearScreen = False
                self.labelResult.setText("0" + btn.text())

            else:
                self.labelResult.setText(self.labelResult.text() + btn.text())
        
        #*** Set Numbers ***
        if btn.text() in numbers:

            if self.clearScreen:
                if not self.grpBtnOperationEnabled:
                    self.setOperationEnabled(state=True)

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

            if self.clearScreen:
                
                if not self.grpBtnOperationEnabled:
                    self.setOperationEnabled(state=True)

                self.labelResult.setText("0")
                self.clearScreen = False
            
            self.getResult()

        else:
            
            if self.clearScreen:
                
                if not self.grpBtnOperationEnabled:
                    self.setOperationEnabled(state=True)

                self.labelResult.setText("0")
                self.clearScreen = False
                
            self.clearDelete(btn.text())

        self.textChanged.emit() #Check if label has a decimal point

    def unaryOperation(self, op):

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

            try:
                value = float(self.labelResult.text())
                value = 1/value
                self.labelResult.setText(format(value, ".15g"))

            except ZeroDivisionError:
                self.labelResult.setText("Can't Divide by Zero!")
                self.setOperationEnabled(state=False)
                self.clearScreen = True
                self.result = 0
                return
        
        self.clearScreen = True
            
    def binaryOperation(self, op):

        #*** Binary Operations ***
        
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
    
    def getResult(self):
        
        if self.prevOperation != "":

            if self.prevOperation == "add":
                self.result += float(self.labelResult.text())

            elif self.prevOperation == "sub":
                self.result -= float(self.labelResult.text())
            
            elif self.prevOperation == "mul":
                self.result *= float(self.labelResult.text())

            else:
                
                try:
                    self.result /= float(self.labelResult.text())

                except ZeroDivisionError:
                    
                    self.labelResult.setText("Can't Divide by Zero!")
                    self.setOperationEnabled(state=False)
                    self.prevOperation = ""
                    self.clearScreen = True
                    self.result = 0
                    return
                    
            self.labelResult.setText(format(self.result, ".15g"))
            self.clearScreen = True
            self.result = 0

    def setOperationEnabled(self, state):
        
        if state is False and self.grpBtnOperationEnabled:
            self.grpBtnOperationEnabled = state
        
        elif state is True and not self.grpBtnOperationEnabled:
            self.grpBtnOperationEnabled = state
        
        else:
            pass

        for btn in self.grpBtnOperation:
            btn.setEnabled(state)

    def clearDelete(self, op):
        
        if not self.grpBtnOperationEnabled:
                    self.setOperationEnabled(state=True)
                    
        if op != ".":

            if op == "DEL":

                if self.labelResult.text() != "" and self.labelResult.text() != "0" and len(self.labelResult.text()) != 1:
                    
                    self.labelResult.setText(
                        self.labelResult.text()[:len(self.labelResult.text()) - 1])

                else:
                    
                    self.result = 0
                    self.labelResult.setText("0")

            elif op== "C":

                self.result = 0
                self.labelResult.setText("0")

            else:
                pass

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
