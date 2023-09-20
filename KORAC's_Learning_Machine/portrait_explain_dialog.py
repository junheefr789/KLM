# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes

class Ui_Dialog(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi()
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.height = screen_height*0.8
        self.width = self.height*1.5
        self.setObjectName("Dialog")
        self.resize(self.width, self.height)
        border_px = int(2*1050/screen_height)
        self.setStyleSheet("background-color: rgb(255, 170, 255);\n"
                           "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(self.width*0.04, self.height*0.04, self.width*0.92, self.height*0.35))
        self.label.setStyleSheet('border:none;')
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/55))
        self.label.setFont(font)
        self.label.setObjectName("label_5")
        self.label.setText("1. 아래 그림과 같이 얼굴의 윤곽선을 그려주세요.\n    (눈썹, 눈, 코, 입, 윤곽선은 꼭 그려주세요!)\n\n2. '초상화그리기'버튼을 클릭해주세요.\n\n3. AI가 여러분이 그려준 그림을 바탕으로 \n    멋있는 초상화를 그려줍니다.")
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(self.width*0.1, self.height*0.47, self.height*0.3, self.height*0.3))
        aimage = QtGui.QImage('./image/portrait_sample_A.jpg')
        aimage = aimage.scaled(QtCore.QSize(self.height*0.3, self.height*0.3))
        self.label_2.setPixmap(QtGui.QPixmap(aimage))
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(self.width*0.27+self.height*0.3, self.height*0.57, self.height*0.1, self.height*0.1))
        self.label_3.setStyleSheet('background-color:white;')
        aimage = QtGui.QImage('./image/next.png')
        aimage = aimage.scaled(QtCore.QSize(self.height*0.1, self.height*0.1))
        self.label_3.setPixmap(QtGui.QPixmap(aimage))
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(self.width*0.44+self.height*0.4, self.height*0.47, self.height*0.3, self.height*0.3))
        self.label_4.setStyleSheet('background-color:white;')
        aimage = QtGui.QImage('./image/portrait_sample_B.jpg')
        aimage = aimage.scaled(QtCore.QSize(self.height*0.3, self.height*0.3))
        self.label_4.setPixmap(QtGui.QPixmap(aimage))
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(self.width*0.45, self.height*0.9, self.width*0.53, self.height*0.08))
        self.label_5.setStyleSheet("background-color: rgb(255, 170, 255);\n"
                                   "border:none;\n"
                                    "color:black;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/80))
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setText("출처 : https://github.com/kairess/edges2portrait_gan")
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.width*0.27, self.height*0.8, self.width*0.46, self.height*0.1))
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
        self.pushButton_2.setText('확 인')
        
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/35))
        
        self.pushButton_2.clicked.connect(self.check)
        
    def check(self):
        self.accept()
        
    def showModal(self):
        return super().exec_()
    
        