# -*- coding: euc-kr -*-
import start_window
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui, QtWidgets
import alam

app = QtWidgets.QApplication(sys.argv)
start_w = start_window.Ui_Dialog()
start_w.show()


from PyQt5.QtWidgets import QMainWindow
import practice_window,play_window
import ctypes
import webbrowser
import os
import train_alam

class Ui_MainWindow(QMainWindow):
    global start_w
    
    def __init__(self):
        super().__init__()
        self.practice_window = None
        self.play_window = None
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.setWindowTitle("  ")
        self.setupUi()
        start_w.closed()
    
    def setupUi(self):
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.setWindowIcon(QtGui.QIcon('./image/logo.png'))
        if screen_width < 1200 and screen_height <600:
            self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
            self.setObjectName("MainWindow")
            self.resize(screen_width*0.4, screen_height*0.4)
            label = QtWidgets.QLabel(self)
            label.setGeometry(QtCore.QRect(0,0,screen_width*0.4,screen_height*0.4))
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("font-size:"+str(int(screen_width/80))+"pt;")
            label.setText("해상도가 낮습니다.\n가로는 '1200픽셀'이상\n세로는 '600픽셀'이상으로\n설정해주세요!!")
        else:
            self.program_height = screen_height*0.8
            self.program_width = self.program_height*1.5
            self.setObjectName("MainWindow")
            self.setFixedSize(self.program_width, self.program_height)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
            self.setSizePolicy(sizePolicy)
            self.centralwidget = QtWidgets.QWidget(self)
            self.centralwidget.setObjectName("centralwidget")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(0, 0, self.program_width, self.program_height))
            oImage = QtGui.QImage('./image/main_image.png')
            oImage = oImage.scaled(QtCore.QSize(self.program_width, self.program_height))
            self.label.setPixmap(QtGui.QPixmap(oImage))
            self.label.setText("")
            self.label.setObjectName("label")
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            font_pt = int(self.program_width/28)
            self.label_2.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_height*0.08, self.program_width*0.99, self.program_height*0.17))
            self.label_2.setStyleSheet("font: "+str(font_pt)+"pt \"Imprint MT Shadow\";\n"
    "color: rgb(255, 255, 255);\n"
    "background-color: rgba(0, 0, 0, 0);")
            self.label_2.setObjectName("label_2")
            self.label_3 = QtWidgets.QPushButton(self.centralwidget)
            self.label_3.setGeometry(QtCore.QRect(self.program_width*0.75, self.program_height*0.65, self.program_width*0.24, self.program_height*0.05))
            self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            font_pt = int(self.program_width/55)
            self.label_3.setStyleSheet(
                '''
                QPushButton{font: '''+str(font_pt)+'''pt \"휴먼엑스포\"; color: white; background-color: rgba(0, 0, 0, 0);text-align:left;}
                QPushButton:hover{font: '''+str(font_pt)+'''pt; color: yellow;}
                '''
                )
            self.label_4 = QtWidgets.QPushButton(self.centralwidget)
            self.label_4.setGeometry(QtCore.QRect(self.program_width*0.75, self.program_height*0.74, self.program_width*0.24, self.program_height*0.05))
            self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.label_4.setStyleSheet(
                '''
                QPushButton{font: '''+str(font_pt)+'''pt \"휴먼엑스포\"; color: white; background-color: rgba(0, 0, 0, 0);text-align:left;}
                QPushButton:hover{font: '''+str(font_pt)+'''pt; color: yellow;}
                '''
                )
            self.label_5 = QtWidgets.QPushButton(self.centralwidget)
            self.label_5.setGeometry(QtCore.QRect(self.program_width*0.75, self.program_height*0.83, self.program_width*0.24, self.program_height*0.05))
            self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.label_5.setStyleSheet(
                '''
                QPushButton{font: '''+str(font_pt)+'''pt \"휴먼엑스포\"; color: white; background-color: rgba(0, 0, 0, 0);text-align:left;}
                QPushButton:hover{font: '''+str(font_pt)+'''pt; color: yellow;}
                '''
                )
            self.label_6 = QtWidgets.QPushButton(self.centralwidget)
            self.label_6.setGeometry(QtCore.QRect(self.program_width*0.75, self.program_height*0.92, self.program_width*0.24, self.program_height*0.05))
            self.label_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.label_6.setStyleSheet(
                '''
                QPushButton{font: '''+str(font_pt)+'''pt \"휴먼엑스포\"; color: white; background-color: rgba(0, 0, 0, 0);text-align:left;}
                QPushButton:hover{font: '''+str(font_pt)+'''pt; color: yellow;}
                '''
                )
            self.label_2.setText("KORAC's Learning Machine")
            self.label_3.setText("프로그램 설명")
            self.label_4.setText("학습시켜보기")
            self.label_5.setText("AI와 놀기")
            self.label_6.setText("EXIT")
            self.label_3.clicked.connect(self.go_explain)
            self.label_4.clicked.connect(self.go_practice)
            self.label_6.clicked.connect(self.quit_window)
            self.label_5.clicked.connect(self.go_play)
            self.setCentralWidget(self.centralwidget)
    
            QtCore.QMetaObject.connectSlotsByName(self)
    
    def go_practice(self):
        try:
            self.hide()
            if self.practice_window==None:
                self.practice_window = practice_window.Ui_MainWindow(self)
            self.practice_window.show()
            self.practice_window.image_menu()
        except BaseException as b:
            print(str(b))
    
    def go_play(self):
        try:
            self.hide()
            if self.play_window==None:
                self.play_window = play_window.Ui_MainWindow(self)
            self.play_window.show()
        except BaseException as b:
            print(str(b))
    def quit_window(self):
        try:
            self.close()
        except BaseException as b:
            print(str(b))
    
    def go_explain(self):
        try:
            path = os.path.dirname(os.path.realpath(__file__))+"\html\index.html"
            ie = webbrowser.get('c:\\program files\\internet explorer\\iexplore.exe')
            ie.open(path)
        except Exception as b:
            try:
                tt = train_alam.Ui_Dialog("기본경로에 explorer가 없습니다.\nexplorer폴더를 기본경로로 이동해주세요. 기본경로는\n'C:/program files/internet explorer'\n입니다.")
                aa = tt.showModal()
                if aa:
                    path = os.path.dirname(os.path.realpath(__file__))+"\html\index.html"
                    ie = webbrowser.get('c:\\program files\\internet explorer\\iexplore.exe')
                    ie.open(path)
                else:
                    return
            except Exception as e:
                print(str(e))
                return

MainWindow = Ui_MainWindow()
MainWindow.show()

sys.exit(app.exec_())
