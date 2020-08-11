# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes

class Ui_Dialog(QtWidgets.QDialog):
    
    def __init__(self,text):
        super().__init__()
        self.text = text
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi()
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.height = screen_height*0.3
        self.width = self.height*2
        self.setObjectName("Dialog")
        self.resize(self.width, self.height)
        border_px = int(2*1050/screen_height)
        self.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                           "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(self.width*0.01, self.height*0.02, self.width*0.98, self.height*0.58))
        self.label.setStyleSheet('border:none;')
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/35))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label_5")
        self.label.setText(self.text)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.width*0.26, self.height*0.65, self.width*0.46, self.height*0.3))
        self.pushButton_2.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/35))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('확인')
        
        
        self.pushButton_2.clicked.connect(self.check)
        
    def check(self):
        self.accept()
        
        
    def showModal(self):
        return super().exec_()
        
        
        