# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
import numpy as np
import machine_learning

class Ui_Dialog(QtWidgets.QDialog):
    
    def __init__(self,data,label_data,epoch):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.data = np.asarray(data)
        self.label_data = np.asarray(label_data)
        self.epoch = epoch
        self.model = None
        self.setupUi()
        self.learning_data()
    
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
        self.label.setText("다음 라운드를 시작합니다.")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('확인')
        self.pushButton_2.clicked.connect(self.check)
        self.pushButton_2.hide()
        
    def learning_data(self):
        try:
            self.data = self.data/500
            self.label_data = self.label_data/500
            tt = machine_learning.pingpong_linear(self.data,self.label_data,self.epoch)
            self.model = tt.start_learning()
            if self.model != None:
                self.pushButton_2.show()
        except BaseException as b:
            print(str(b))
        
    def check(self):
        self.accept()
        
        
    def showModal(self):
        return super().exec_()

class m1(QtCore.QThread):
    
    def __init__(self,data,label):
        super().__init__()
        self.data = data
        self.label = label
        self.model = None
    
    def run(self):
        try:
            if len(self.data)==0:
                tt = machine_learning.pingpong_linear(self.data,self.label_data)
                self.model = tt.start_learning()
        except BaseException as b:
            print(str(b))
        
        