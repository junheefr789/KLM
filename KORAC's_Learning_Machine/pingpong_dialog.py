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
        self.label.setGeometry(QtCore.QRect(self.width*0.04, self.height*0.04, self.width*0.92, self.height*0.65))
        self.label.setStyleSheet('border:none;')
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/70))
        self.label.setFont(font)
        self.label.setText("1. AI가 라운드를 거듭하며 핑퐁게임에 대하여 배웁니다.\n    AI가 지면 여태까지의 게임에 대하여 학습을 하고 다음 라운드가 시작됩니다.\n   (1라운드는 랜덤하게 움직입니다.)\n\n"
                           "2. 'w'키를 누르면 패널이 위로 올라가고, 's'키를 누르면 패널이 아래로 내려갑니다.\n\n"
                           "3. 플레이어가 패널을 움직이는 상태에서 공을 쳐내면\n   공의 각도가 쳐낸방향으로 더 기울어져서 움직입니다.\n\n"
                           "4. 공의 각도는 'x+'축을 기준으로 시계방향으로 늘어납니다.\n\n"
                           "5. 좌표는 제일 위가 0, 제일 아래가 683입니다.\n\n"
                           "6. 공의 속도는 시간이 지날수록 빨라지고 라운드가 새로 시작하면 초기화됩니다.\n\n"
                           "7. 총 AI에게 몇라운드까지 이길수 있는지 도전해보세요!!")
        
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.width*0.27, self.height*0.85, self.width*0.46, self.height*0.1))
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

