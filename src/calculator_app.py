import os
import sys

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from BlurWindow.blurWindow import blur
from calculator import StandardCalculator, ScientificCalculator

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

class WindowCalculator(QtWidgets.QMainWindow):

    def __init__(self):

        super(WindowCalculator, self).__init__()

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
        
        #******************************
        
        #*** Menu Variable ***
        self.openingMenu = False
        #*********************
        
        self.btnMenu.clicked.connect(self.animatedMenu)
        self.btnStdCalc.clicked.connect(self.onBtnFromMenuClicked)
        self.btnSciCalc.clicked.connect(self.onBtnFromMenuClicked)
        
        self.btnClose.clicked.connect(self.onBtnCloseClicked)
        self.btnMinimize.clicked.connect(self.onBtnMinimizeClicked)
        self.windowBar.mousePressEvent = self.dragWindow

        self.timerOnResize = QtCore.QTimer()
        self.timerOnResize.timeout.connect(self.setResizeFlag)  #To check if window is not resizing

        self.animation = QtCore.QPropertyAnimation(self.leftMenuBar, b"minimumWidth")

        self.calculator = StandardCalculator(widgets=self.stdCalc, display=self.lineEditResult)

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

    def onBtnCloseClicked(self):
        self.close()
    
    def onBtnMinimizeClicked(self):
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

    def onBtnFromMenuClicked(self):

        btn = self.sender()
        currentIdx = self.stackedWidget.currentIndex()

        if "Std" in btn.objectName():
            if currentIdx != 0:
                self.stackedWidget.setCurrentIndex(0)
                self.calculator = StandardCalculator(widgets=self.stdCalc, display=self.lineEditResult)
        
        elif "Sci" in btn.objectName():
            if currentIdx != 1:
                self.stackedWidget.setCurrentIndex(1)
                self.calculator = ScientificCalculator(widgets=self.sciCalc, display=self.lineEditResult)
        
def main():
    
    app = QtWidgets.QApplication(sys.argv)

    windowCalculator = WindowCalculator()
    windowCalculator.show()

    app.exec()


if __name__ == "__main__":
    main()
