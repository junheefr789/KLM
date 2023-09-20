# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import custom_widgets as cw
import portrait_explain_dialog
import ctypes
from tensorflow.keras.models import load_model
from skimage.io import imread
import cv2
import numpy as np

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,m_window):
        super().__init__()
        self.m_window = m_window
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.setupUi()
        try:
            self.model = load_model('generator.h5')
        except BaseException as b:
            print(str(b))
        self.open_explain()
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.setWindowIcon(QtGui.QIcon('./image/logo.png'))
        self.program_height = 700
        self.program_width = 1200
        self.border_px = int((2/1020)*screen_height)
        self.setStyleSheet('background-color: rgb(170, 170, 255);')
        self.setFixedSize(self.program_width, self.program_height)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setWindowTitle("  ")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(self.program_width*0.05,self.program_height*0.15,self.program_width*0.3,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/40))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("border-style:solid;\n"
                                 "color:white;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        rect = QtCore.QRect(self.program_width*0.05,self.program_height*0.3,self.program_width*0.3,self.program_width*0.3)
        self.drawing_widget = cw.DrawingWidget(self)
        self.drawing_widget.setGeometry(rect)
        self.drawing_widget.set_image_size(self.program_width*0.3,self.program_width*0.3)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.program_width*0.1,self.program_height*0.31+self.program_width*0.3,self.program_width*0.2,self.program_height*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_2.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("border-style:solid;\n"
                                 "color:black;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.02, self.program_width*0.08, self.program_width*0.04))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_pt = int(self.program_width/55)
        self.pushButton_3.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";"
"color:white;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(self.program_width*0.9, self.program_width*0.02, self.program_width*0.08, self.program_width*0.04))
        self.pushButton_4.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color:white;\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";")
        self.pushButton_4.setText("")
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(self.program_width*0.4, self.program_width*0.02, self.program_width*0.2, self.program_width*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/55))
        self.pushButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color:white;\n")
        
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(self.program_width*0.4, self.program_height*0.45, self.program_width*0.2, self.program_width*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/55))
        self.pushButton_5.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("border-style:solid;\n"
                                        "color:white;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(self.program_width*0.65,self.program_height*0.3,self.program_width*0.3,self.program_width*0.3))
        self.label_2.setStyleSheet("border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n")
        
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(self.program_width*0.7,self.program_height*0.31+self.program_width*0.3,self.program_width*0.2,self.program_height*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_6.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("border-style:solid;\n"
                                        "color:black;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(self.program_width*0.65,self.program_height*0.15,self.program_width*0.3,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/40))
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setStyleSheet("border-style:solid;\n"
                                 "color:white;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        
        self.pushButton_6.setText("그 림 저 장")
        self.pushButton.setText("도 움 말")
        self.pushButton_5.setText("초상화\n그리기")
        self.pushButton_2.setText("지  우  기")
        self.pushButton_3.setText("이전")
        self.pushButton_4.setText("종료")
        self.label.setText("얼굴 윤곽선 그림판")
        self.label_3.setText("초  상  화")
        
        self.pushButton.clicked.connect(self.open_explain)
        self.pushButton_2.clicked.connect(self.clear_widget)
        self.pushButton_3.clicked.connect(self.go_back)
        self.pushButton_4.clicked.connect(self.quit)
        self.pushButton_5.clicked.connect(self.draw_portrait)
        
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def clear_widget(self):
        try:
            self.drawing_widget.clear()
        except BaseException as b:
            print(str(b))
    
    def go_back(self):
        try:
            self.hide()
            self.m_window.show()
            self.m_window.init_cursor()
        except BaseException as b:
            print(str(b))
            
    def draw_portrait(self):
        try:
            self.drawing_widget.save_image()
            img = imread('asdfi.jpg',as_gray=True)
            img = cv2.resize(img,dsize=(256,256))
            img= np.array(img) / 127.5 - 1.
            img = img.reshape(1,256,256,1)
            gen = self.model.predict(img)
            gen = 0.5 * gen + 0.5
            gen = gen.squeeze()
            gen = cv2.resize(gen,dsize=(360,360))
            cv2.imshow('test',gen)
            cv2.waitKey(0)
        except BaseException as b:
            print(str(b))
            
        
    def quit(self):
        self.close()
    
    def open_explain(self):
        try:
            self.explain_dialog = portrait_explain_dialog.Ui_Dialog()
            aa = self.explain_dialog.showModal()
            if aa:
                return
        except BaseException as b:
            print(str(b))
    
