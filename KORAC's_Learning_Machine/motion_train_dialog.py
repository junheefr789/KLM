# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import train_alam

class Ui_Dialog(QtWidgets.QDialog):
    
    def __init__(self,train_coords,learning_count):
        super().__init__()
        self.train_coords = train_coords
        self.train_data = []
        self.val_data = []
        self.train_label = []
        self.val_label = []
        self.learning = 0
        self.image_count = 0
        self.mm = None
        self.train_count = 0
        self.label_arr = []
        self.learn_count = 0
        self.acc = []
        self.loss = []
        self.val_acc = []
        self.val_loss = []
        self.batch_size = 0
        self.people_counts = []
        self.maxpeople = 1
        self.error = ''
        self.current_class = 1
        self.learning_count = learning_count
        for step in range(len(self.train_coords)):
            self.image_count = self.image_count + len(self.train_coords[step])
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi()
        self.people_count()
    
    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(900, 390)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(170, 70, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.lineEdit_5 = QtWidgets.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(170, 270, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(14)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(170, 170, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(14)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(170, 220, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(14)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_4.setObjectName("휴먼엑스포")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 300, 171, 51))
        self.pushButton_2.setStyleSheet("background-color:rgb(98, 86, 236);\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:2px;\n"
                                         "border-radius:20px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(700, 300, 171, 51))
        self.pushButton_3.setStyleSheet("background-color:rgb(255, 94, 79);\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:2px;\n"
                                         "border-radius:20px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_22 = QtWidgets.QLabel(self)
        self.label_22.setGeometry(QtCore.QRect(330, 20, 541, 191))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(10)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("border-style:solid;\n"
"border-color:black;\n"
"border-width:2px;")
        self.label_22.setText("")
        self.label_22.setObjectName("label_22")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(170, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_31 = QtWidgets.QLabel(self)
        self.label_31.setGeometry(QtCore.QRect(220, 70, 66, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.label_31.setFont(font)
        self.label_31.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_31.setObjectName("label_3")
        
        self.label_35 = QtWidgets.QLabel(self)
        self.label_35.setGeometry(QtCore.QRect(330, 231, 541, 51))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(14)
        self.label_35.setFont(font)
        self.label_35.setStyleSheet("color:red;\n"
                                    "border-style:solid;\n"
                                    "border-width:2px;\n"
                                    "border-color:black;")
        self.label_35.setText("")
        self.label_35.setAlignment(QtCore.Qt.AlignCenter)
        self.label_35.setObjectName("label_35")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(11)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(30, 70, 180, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(130, 120, 81, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton_6.setStyleSheet("border:none;\n"
"text-align:center;")
        self.pushButton_61 = QtWidgets.QPushButton(self)
        self.pushButton_61.setGeometry(QtCore.QRect(30, 120, 31, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_61.setFont(font)
        self.pushButton_61.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_61.setStyleSheet("border:none;\n"
"image:url('./image/left_arrow.png');")
        self.pushButton_62 = QtWidgets.QPushButton(self)
        self.pushButton_62.setGeometry(QtCore.QRect(270, 120, 31, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_62.setFont(font)
        self.pushButton_62.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_62.setStyleSheet("border:none;\n"
"image:url('./image/right_arrow.png');")
        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.setGeometry(QtCore.QRect(30, 170, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self)
        self.pushButton_8.setGeometry(QtCore.QRect(30, 220, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self)
        self.pushButton_9.setGeometry(QtCore.QRect(30, 270, 121, 31))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(12)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_9.setObjectName("pushButton_9")

        self.lineEdit_3.setText("0.0005")
        self.lineEdit_4.setText("16")
        self.lineEdit_5.setText("150")
        self.pushButton_2.setText("학습시키기")
        self.pushButton_3.setText("닫기")
        self.label_3.setText(str(len(self.train_coords)))
        self.label_31.setText("1번")
        self.pushButton_4.setText("클래스 수")
        self.pushButton_5.setText("클래스별 인원수")
        self.pushButton_6.setText("1명")
        self.pushButton_7.setText("학습률")
        self.pushButton_8.setText("작업 수량")
        self.pushButton_9.setText("학습 횟수")
        self.label_22.setText("단어를 클릭하시면 설명을 볼 수 있습니다.")
        
        self.pushButton_4.clicked.connect(self.set_explain3)
        self.pushButton_5.clicked.connect(self.set_explain2)
        self.pushButton_7.clicked.connect(self.set_explain4)
        self.pushButton_8.clicked.connect(self.set_explain5)
        self.pushButton_9.clicked.connect(self.set_explain6)
        self.pushButton_2.clicked.connect(self.start_learning)
        self.pushButton_3.clicked.connect(self.quit)
        self.pushButton_61.clicked.connect(self.pre_people)
        self.pushButton_62.clicked.connect(self.next_people)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def people_count(self):
        try:
            value_count = 0
            for step in range(len(self.train_coords)):
                for step2 in range(len(self.train_coords[step])):
                    for step3 in range(len(self.train_coords[step][step2])):
                        if self.train_coords[step][step2][step3][2] != 0 and self.train_coords[step][step2][step3][3] != 0:
                            value_count +=1
                if value_count<(len(self.train_coords[step]))/2:
                    self.people_counts.append(1)
                else:
                    self.people_counts.append(2)
                    self.maxpeople = 2
                value_count = 0
        except BaseException as b:
            print(str(b))   
    def next_people(self):
        try:
            if self.current_class==len(self.people_counts):
                return
            else:
                self.current_class +=1
                self.pushButton_6.setText(str(self.people_counts[self.current_class-1])+"명")
                self.label_31.setText(str(self.current_class)+"번")
        except BaseException as b:
            print(str(b))
    def pre_people(self):
        try:
            if self.current_class==1:
                return
            else:
                self.current_class -=1
                self.pushButton_6.setText(str(self.people_counts[self.current_class-1])+"명")
                self.label_31.setText(str(self.current_class)+"번")
        except BaseException as b:
            print(str(b))    
    def start_learning(self):
        self.train_data = []
        self.train_label = []
        self.val_data = []
        self.val_label = []
        self.model = None
        self.history = None
        self.ms = None
        try:
            self.learning_rate = float(self.lineEdit_3.text())
            if self.learning_rate <=0:
                self.label_35.setText("학습률은 0보다 커야합니다.")
                return
        except:
            self.label_35.setText("학습률엔 숫자만 넣을 수 있습니다.\n"
                                  "소수점은 8자리까지 넣어주세요")
            return        
        try:
            self.batch_size = int(self.lineEdit_4.text())
            if self.batch_size <= 0:
                self.label_35.setText("작업 수량이 1보다 작으면 안됩니다.")
                return
        except:
            self.label_35.setText("작업 수량엔 숫자만 넣을 수 있습니다.")
            return        
        try:
            self.epoch_size = int(self.lineEdit_5.text())
            if self.epoch_size <= 0:
                self.label_35.setText("학습 횟수가 1보다 작으면 안됩니다.")
                return
        except:
            self.label_35.setText("학습 횟수엔 숫자만 넣을 수 있습니다.")
            return
        if self.image_count<self.batch_size:
                self.label_35.setText("작업 수량이 이미지 수보다 많습니다.")
                return
        
        try:
            for step in range(len(self.train_coords)):
                for step2 in range(len(self.train_coords[step])):
                    if step2 <= len(self.train_coords[step])*0.8:
                        temp = np.zeros(len(self.train_coords))
                        temp[step] = 1
                        self.train_label.append(temp)
                        self.train_data.append(np.asarray(self.train_coords[step][step2]).reshape(6,17,1))
                    else:
                        temp = np.zeros(len(self.train_coords))
                        temp[step] = 1
                        self.val_label.append(temp)
                        self.val_data.append(np.asarray(self.train_coords[step][step2]).reshape(6,17,1))
            self.train_label = np.asarray(self.train_label)
            self.train_data = np.asarray(self.train_data)
            self.val_data = np.asarray(self.val_data)
            self.val_label = np.asarray(self.val_label)
            self.label_35.setText('학습중 입니다. 기다려주세요.')
            self.learning_count +=1
            self.accept()
        except BaseException as b:
            print(str(b))
    def set_explain2(self):
        text=" 클래스별 프로그램이 인식한 사람수 이다."
        self.label_22.setText(text)
    def set_explain3(self):
        text=" 사진을 저장한 클래스의 갯수이다."
        self.label_22.setText(text)
    def set_explain4(self):
        text=" 학습을 진행하는 속도이다.\n 높으면 빠르게 진행하지만 불안해지고\n 낮으면 천천히진행하지만 안정되게 학습한다."
        self.label_22.setText(text)
    def set_explain5(self):
        text=" 한번의 학습을 진행할때 여러번의 작업으로 나누어서 진행한다.\n 이 때 한번의 작업당 수행할 데이터량이다."
        self.label_22.setText(text)
    def set_explain6(self):
        text=" 몇번의 학습을 할 것인지에 대한 횟수이다."
        self.label_22.setText(text)

    def quit(self):
        if self.learning:
            return
        if self.learn_count >0 :
            self.accept()
        else:
            self.reject()
            
    def showModal(self):
        return super().exec_()

