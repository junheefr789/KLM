# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
import custom_widgets as cw
import cv2
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
import numpy as np
from PyQt5.Qt import QFileDialog
from custom_widgets import ImageViewer
import motion_train_dialog
import argparse
import matplotlib
matplotlib.use("Qt5AGG")
import matplotlib.pyplot as plt
import posenet
global image
import os
import train_alam,alam
import ev3_connect_dialog
import ev3_message_converter

class Ui_MainWindow(QtWidgets.QMainWindow):
    
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)
    MessageSignal = QtCore.pyqtSignal(int)

    def __init__(self,m_window):
        super().__init__()
        r = QtWidgets.QDesktopWidget().screenGeometry()
        self.window_width = r.width()
        self.window_height = r.height()
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.setWindowTitle("   ")
        self.menu_clicked = 0
        self.m_window = m_window
        self.capture_checked = 0
        self.while_count = 0
        self.table_row = 0
        self.table_column = 6
        self.class_count = 1
        self.model = False
        self.current_class = 1
        self.send_point=95
        self.class_image = []
        self.dq = 0
        self.image_data = []
        self.class_name = []
        self.saved = 1
        self.nomal = 0
        self.mm = None
        self.learning = 0
        self.class_explain = []
        self.train_coords = []
        self.class_coords = []
        self.clicked_label_position = []
        self.preview = 0
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--model',type=int, default=101)
        self.parser.add_argument('--cam_id',type=int, default=0)
        self.parser.add_argument('--cam_width',type=int, default=352)
        self.parser.add_argument('--cam_height',type=int, default=288)
        self.parser.add_argument('--scale_factor',type=float, default=0.7125)
        self.parser.add_argument('--file',type=str, default=None, help="Optionally use a video file instead of a live camera")
        self.args = self.parser.parse_args()
        self.learning_count = 0
        self.connect = 0
        self.connect_count = 0
        self.msg = 0
        self.ev3 = None
        self.setupUi()
    def set_cam(self):
        try:
            self.label_4.setText('기다려주세요. 준비중입니다.')
            self.setCursor(QtCore.Qt.BusyCursor)
            self.dq=0
            if self.args.file is not None:
                self.cap = cv2.VideoCapture(self.args.file)
                if self.program_width*0.34 < 480:
                    self.cap.set(3,352)
                    self.cap.set(4,288)
                    self.nomal = 400
                else:
                    self.cap.set(3,680)
                    self.cap.set(4,480)
                    self.nomal = 600
            else:
                self.cap = cv2.VideoCapture(self.args.cam_id)
                if self.program_width*0.34 < 480:
                    self.cap.set(3,352)
                    self.cap.set(4,288)
                    self.nomal = 300
                elif self.program_width*0.34 < 540:
                    self.cap.set(3,680)
                    self.cap.set(4,480)
                    self.nomal = 600
                else:
                    self.cap.set(3,960)
                    self.cap.set(4,540)
                    self.nomal = 900
        except:
            self.label_4.setText("캠을 찾지 못했습니다.")
            
        try:
            ret, image = self.cap.read()
        except:
            self.label_4.setText("캠에 문제가 있습니다.")

        try:
            self.VideoSignal1.connect(self.cam_viewer1.setImage)
            self.VideoSignal2.connect(self.cam_viewer2.setImage)
            self.MessageSignal.connect(self.send_msg_ev3)
            self.label_4.setText('준비가 완료되었습니다.')
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.show_video()
        except:
            return
        
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.setWindowIcon(QtGui.QIcon('./image/logo.png'))
        self.program_height = screen_height*0.8
        self.program_width = self.program_height*1.2
        self.predict_program_width = self.program_width*1.4
        self.setObjectName("MainWindow")
        self.setFixedSize(self.predict_program_width, self.program_height)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_height*0.1, self.program_width*0.36, self.program_width*0.36))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.border_px = int(2/1020*screen_height)
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet("border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.cam_viewer1 = cw.ImageViewer(self.frame)
        self.cam_viewer1.setGeometry(QtCore.QRect(self.program_width*0.01,self.program_width*0.01,self.program_width*0.34,self.program_width*0.34))
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.02, self.program_width*0.05, self.program_width*0.05))
        self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                      "image:url('./image/menu_icon.png');")
        self.pushButton.setObjectName("pushButton")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, self.program_width*0.3, self.program_height))
        self.frame_2.setStyleSheet("background-color: rgb(190, 190, 190);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(0, self.program_height*0.3, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_29 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_29.setGeometry(QtCore.QRect(0, self.program_height*0.2, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_29.setFont(font)
        self.pushButton_29.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_29.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(0, self.program_height*0.4, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;\n"
"")
        self.pushButton_3.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setGeometry(QtCore.QRect(0, self.program_height*0.5, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.pushButton_4.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setLocale(QtCore.QLocale(QtCore.QLocale.Korean, QtCore.QLocale.SouthKorea))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_13 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_13.setGeometry(QtCore.QRect(0, self.program_height*0.6, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_13.setFont(font)
        self.pushButton_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_13.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(self.program_width*0.48, self.program_height*0.03, self.program_width*0.44, self.program_height*0.06))
        self.label_2.setStyleSheet("background-color: rgb(194, 194, 194);border-style:solid;border-color:white;border-width:"+str(self.border_px)+"px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.03, self.program_width*0.05, self.program_height*0.06))
        self.pushButton_6.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                        "image:url('./image/left_arrow.png');")
        self.pushButton_6.setObjectName("pushButton_6")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.36+self.program_height*0.11, self.program_width*0.36, self.program_width*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/60))
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color:black;\n"
                                   "color:white;")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label = QtWidgets.QLineEdit(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.36+self.program_height*0.17, self.program_width*0.36, self.program_width*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/60))
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.36+self.program_height*0.26, self.program_width*0.36, self.program_width*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/60))
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color:black;\n"
                                   "color:white;")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.36+self.program_height*0.32, self.program_width*0.36, self.program_width*0.2))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/70))
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;")
        self.textEdit.setObjectName("textEdit")
        self.frame_22 = QtWidgets.QFrame(self.centralwidget)
        self.frame_22.setGeometry(QtCore.QRect(self.program_width*1.02,self.program_height*0.02,self.program_width*0.36,self.program_height*0.97))
        self.frame_23 = QtWidgets.QFrame(self.centralwidget)
        self.frame_23.setGeometry(QtCore.QRect(self.program_width*1.02,self.program_height*0.1,self.program_width*0.36,self.program_height*0.1))
        self.frame_23.setStyleSheet("border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;")
        self.pushButton_31 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_31.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.02,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_31.setText('CLASS_1')
        self.pushButton_31.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_32 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_32.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.1,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_32.setText('CLASS_2')
        self.pushButton_32.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_33 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_33.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.18,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_33.setText('CLASS_3')
        self.pushButton_33.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_34 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_34.setText('CLASS_4')
        self.pushButton_34.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.26,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_34.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_35 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_35.setText('CLASS_5')
        self.pushButton_35.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.34,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_35.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_36 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_36.setText('CLASS_6')
        self.pushButton_36.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.42,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_36.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_37 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_37.setText('CLASS_7')
        self.pushButton_37.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.5,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_37.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_38 = QtWidgets.QPushButton(self.frame_23)
        self.pushButton_38.setText('CLASS_8')
        self.pushButton_38.setGeometry(QtCore.QRect(self.program_width*0.02,self.program_height*0.58,self.program_width*0.32,self.program_height*0.06))
        self.pushButton_38.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        
        self.line = QtWidgets.QLineEdit(self.frame_22)
        self.line.setGeometry(QtCore.QRect(self.program_width*0.3, self.program_height*0.89, self.program_width*0.05, self.program_height*0.03))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/80))
        self.line.setFont(font)
        self.line.setAlignment(QtCore.Qt.AlignCenter)
        self.line.setStyleSheet("background-color:white;")
        self.line.setText("95")
        
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal,self.frame_22)
        self.slider.setGeometry(QtCore.QRect(0, self.program_height*0.89, self.program_width*0.29, self.program_height*0.03))
        self.slider.setRange(50, 99)
        self.slider.setSingleStep(1)
        self.slider.setValue(95)
        
        self.pushButton_15 = QtWidgets.QPushButton(self.frame_22)
        self.pushButton_15.setGeometry(QtCore.QRect(0, self.program_height*0.93, self.program_width*0.36, self.program_height*0.04))
        self.pushButton_15.setStyleSheet(
            "font-size:"+str(int(self.program_height/50))+"pt;"
            "background-color:white;"
            "border-color:white;\n"
            "border-width:"+str(self.border_px)+"px;"
            "border-radius:"+str(self.border_px*7)+"px;"
            )
        self.pushButton_15.setText("EV3 연결하기")
        
        self.frame_3 = QtWidgets.QFrame(self.frame_22)
        self.frame_3.setGeometry(QtCore.QRect(self.program_width*0.02, 0, self.program_width*0.32, self.program_height*0.384))
        self.frame_3.setStyleSheet("border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;\n"
"")
        self.frame_3.setObjectName("frame_3")
        self.cam_viewer2 = ImageViewer(self.frame_3)
        self.cam_viewer2.setGeometry(QtCore.QRect(self.program_width*0.01,self.program_width*0.01,self.program_width*0.3,self.program_width*0.3))
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(self.program_width*0.93, self.program_height*0.03, self.program_width*0.05, self.program_height*0.06))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                        "image:url('./image/right_arrow.png');")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.1, self.program_width*0.56, self.program_height*0.45))
        self.table.setStyleSheet("background-color: black;\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;")
        self.table.setColumnCount(self.table_column)
        self.table.setFixedHeight(self.program_height*0.45)
        self.table.setFixedWidth(self.program_width*0.56)
        self.table.setAutoScroll(True)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        for step in range(self.table_column):
            self.table.setColumnWidth(step,self.program_width*0.09)
        
        self.label_3 = QtWidgets.QLabel(self.frame_22)
        self.label_3.setGeometry(QtCore.QRect(0, self.program_height*0.4, self.program_width*0.36, self.program_height*0.05))
        self.label_3.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame_22)
        self.textEdit_2.setGeometry(QtCore.QRect(0, self.program_height*0.47, self.program_width*0.36, self.program_height*0.08))
        self.textEdit_2.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;")
        self.textEdit_2.setObjectName("textEdit_2")
        
        self.frame_4 = QtWidgets.QFrame(self.frame_22)
        self.frame_4.setGeometry(QtCore.QRect(0, self.program_height*0.57, self.program_width*0.36, self.program_height*0.32))
        self.frame_4.setStyleSheet("background-color: black;")
        self.la_1 = QtWidgets.QLabel(self.frame_4)
        self.la_1.setGeometry(QtCore.QRect(0,0,self.program_width*0.095, self.program_height*0.038))
        self.la_1.setAlignment(QtCore.Qt.AlignCenter)
        self.la_1.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_1.setText("1번 클래스")
        self.la_1.setFont(font)
        self.la_2 = QtWidgets.QLabel(self.frame_4)
        self.la_2.setGeometry(QtCore.QRect(0,self.program_height*0.038,self.program_width*0.095, self.program_height*0.038))
        self.la_2.setAlignment(QtCore.Qt.AlignCenter)
        self.la_2.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_2.setText("2번 클래스")
        self.la_2.setFont(font)
        self.la_3 = QtWidgets.QLabel(self.frame_4)
        self.la_3.setGeometry(QtCore.QRect(0,self.program_height*0.076,self.program_width*0.095, self.program_height*0.038))
        self.la_3.setAlignment(QtCore.Qt.AlignCenter)
        self.la_3.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_3.setText("3번 클래스")
        self.la_3.setFont(font)
        self.la_4 = QtWidgets.QLabel(self.frame_4)
        self.la_4.setGeometry(QtCore.QRect(0,self.program_height*0.114,self.program_width*0.095, self.program_height*0.038))
        self.la_4.setAlignment(QtCore.Qt.AlignCenter)
        self.la_4.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_4.setText("4번 클래스")
        self.la_4.setFont(font)
        self.la_5 = QtWidgets.QLabel(self.frame_4)
        self.la_5.setGeometry(QtCore.QRect(0,self.program_height*0.152,self.program_width*0.095, self.program_height*0.038))
        self.la_5.setAlignment(QtCore.Qt.AlignCenter)
        self.la_5.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_5.setText("5번 클래스")
        self.la_5.setFont(font)
        self.la_6 = QtWidgets.QLabel(self.frame_4)
        self.la_6.setGeometry(QtCore.QRect(0,self.program_height*0.190,self.program_width*0.095, self.program_height*0.038))
        self.la_6.setAlignment(QtCore.Qt.AlignCenter)
        self.la_6.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_6.setText("6번 클래스")
        self.la_6.setFont(font)
        self.la_7 = QtWidgets.QLabel(self.frame_4)
        self.la_7.setGeometry(QtCore.QRect(0,self.program_height*0.228,self.program_width*0.095, self.program_height*0.038))
        self.la_7.setAlignment(QtCore.Qt.AlignCenter)
        self.la_7.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_7.setText("7번 클래스")
        self.la_7.setFont(font)
        self.la_8 = QtWidgets.QLabel(self.frame_4)
        self.la_8.setGeometry(QtCore.QRect(0,self.program_height*0.266,self.program_width*0.095, self.program_height*0.038))
        self.la_8.setAlignment(QtCore.Qt.AlignCenter)
        self.la_8.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/75))
        self.la_8.setText("8번 클래스")
        self.la_8.setFont(font)
        self.bar_1 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_1.setGeometry(QtCore.QRect(self.program_width*0.095,0,self.program_width*0.265,self.program_height*0.038))
        self.bar_1.setStyleSheet("color:white;")
        self.bar_2 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_2.setGeometry(QtCore.QRect(self.program_width*0.095,self.program_height*0.038,self.program_width*0.265,self.program_height*0.038))
        self.bar_2.setStyleSheet("color:white;")
        self.bar_3 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_3.setGeometry(QtCore.QRect(self.program_width*0.095,self.program_height*0.076,self.program_width*0.265,self.program_height*0.038))
        self.bar_3.setStyleSheet("color:white;")
        self.bar_4 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_4.setGeometry(QtCore.QRect(self.program_width*0.095,self.program_height*0.114,self.program_width*0.265,self.program_height*0.038))
        self.bar_4.setStyleSheet("color:white;")
        self.bar_5 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_5.setGeometry(QtCore.QRect(self.program_width*0.095,self.program_height*0.152,self.program_width*0.265,self.program_height*0.038))
        self.bar_5.setStyleSheet("color:white;")
        self.bar_6 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_6.setGeometry(QtCore.QRect(self.program_width*0.095,self.program_height*0.190,self.program_width*0.265,self.program_height*0.038))
        self.bar_6.setStyleSheet("color:white;")
        self.bar_7 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_7.setGeometry(QtCore.QRect(self.program_width*0.095,self.program_height*0.228,self.program_width*0.265,self.program_height*0.038))
        self.bar_7.setStyleSheet("color:white;")
        self.bar_8 = QtWidgets.QProgressBar(self.frame_4)
        self.bar_8.setGeometry(QtCore.QRect(self.program_width*0.095,self.program_height*0.266,self.program_width*0.265,self.program_height*0.038))
        self.bar_8.setStyleSheet("color:white;")
        
        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setGeometry(QtCore.QRect(self.program_width*1.03,self.program_height*0.82,self.program_width*0.34,self.program_height*0.08))
        self.progress_label.setStyleSheet(
            "font-size:"+str(int(self.program_height/45))+"pt;"
            "background-color:black;\n"
            "color:white;"
            )
        self.progress_label.setText("학습 진행 상황")
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(self.program_width*1.03,self.program_height*0.91,self.program_width*0.34,self.program_height*0.06))
        self.progress_bar.setStyleSheet("color:white;")
        
        self.progress_label.hide()
        self.progress_bar.hide()
        
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.58, self.program_width*0.56, self.program_height*0.07))
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("background-color: rgb(98, 86, 236);\n"
                                         "border-style:solid;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/45))
        self.pushButton_8.setFont(font)
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.68, self.program_width*0.26, self.program_height*0.05))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.setStyleSheet("background-color:rgb(17, 212, 183);\n"
                                         "border-style:solid;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*7)+"px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/55))
        self.pushButton_9.setFont(font)
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(self.program_width*0.72, self.program_height*0.68, self.program_width*0.26, self.program_height*0.05))
        self.pushButton_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setStyleSheet("background-color:rgb(17, 212, 183);\n"
                                         "border-style:solid;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*7)+"px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/55))
        self.pushButton_10.setFont(font)
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.76, self.program_width*0.26, self.program_height*0.05))
        self.pushButton_11.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_11.setStyleSheet("background-color:rgb(17, 212, 183);\n"
                                         "border-style:solid;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*7)+"px;")
        self.pushButton_11.setObjectName("pushButton_11")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/55))
        self.pushButton_11.setFont(font)
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(self.program_width*0.72, self.program_height*0.76, self.program_width*0.26, self.program_height*0.05))
        self.pushButton_12.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_12.setStyleSheet("background-color:rgb(17, 212, 183);\n"
                                         "border-style:solid;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*7)+"px;")
        self.pushButton_12.setObjectName("pushButton_12")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/55))
        self.pushButton_12.setFont(font)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.84, self.program_width*0.56, self.program_height*0.04))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: black;\n"
"color:white;")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.88, self.program_width*0.56, self.program_height*0.11))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/60))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"border-width:"+str(self.border_px)+"px;\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-radius:"+str(self.border_px*10)+"px;\n"
"color:red;")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.textEdit.raise_()
        self.label.raise_()
        self.frame.raise_()
        self.pushButton.raise_()
        self.frame_2.raise_()
        self.label_2.raise_()
        self.pushButton_6.raise_()
        self.frame_3.raise_()
        self.pushButton_7.raise_()
        self.label_3.raise_()
        self.textEdit_2.raise_()
        self.pushButton_8.raise_()
        self.pushButton_9.raise_()
        self.pushButton_10.raise_()
        self.pushButton_11.raise_()
        self.pushButton_12.raise_()
        self.label_4.raise_()
        self.setCentralWidget(self.centralwidget)

        self.pushButton_29.setText("새 프로젝트")
        self.label_2.setText("CLASS_1")
        self.pushButton_2.setText("프로젝트 불러오기")
        self.pushButton_3.setText("프로젝트 저장하기")
        self.pushButton_4.setText("메인메뉴로 이동")
        self.pushButton_8.setText("사  진  촬  영")
        self.pushButton_9.setText("이미지 불러오기")
        self.pushButton_10.setText("이미지 삭제하기")
        self.pushButton_11.setText("클래스 삭제하기")
        self.pushButton_12.setText("학습하러가기")
        self.pushButton_13.setText("종료하기")
        self.label_6.setText("클래스 이름")
        self.label_7.setText("클래스 설명")
        self.label.setText("CLASS_1")
        self.label_5.setText("알 림 판")
        self.textEdit.setText("")
        
        self.frame_2.hide()
        
        self.line.textChanged.connect(self.line_set_accuracy)
        self.slider.valueChanged.connect(self.slider_set_accuracy)
        self.pushButton_15.clicked.connect(self.connect_ev3)
        self.pushButton_29.clicked.connect(self.new_project)
        self.pushButton_2.clicked.connect(self.load_project)
        self.label.textChanged.connect(self.change_button_name)
        self.pushButton_3.clicked.connect(self.save_project)
        self.pushButton_12.clicked.connect(self.go_image_learning)
        self.table.cellClicked.connect(self.clicked_image)
        self.pushButton_9.clicked.connect(self.open_image)
        self.pushButton_11.clicked.connect(self.delete_class)
        self.pushButton_6.clicked.connect(self.go_pre_class)
        self.pushButton_7.clicked.connect(self.go_next_class)
        self.pushButton.clicked.connect(self.menu_show_event)
        self.pushButton_4.clicked.connect(self.quit)
        self.pushButton_10.clicked.connect(self.delete_image)
        self.pushButton_8.clicked.connect(self.capture_image)
        self.pushButton_13.clicked.connect(self.exit)
        self.pushButton_31.clicked.connect(self.move_class_1)
        self.pushButton_32.clicked.connect(self.move_class_2)
        self.pushButton_33.clicked.connect(self.move_class_3)
        self.pushButton_34.clicked.connect(self.move_class_4)
        self.pushButton_35.clicked.connect(self.move_class_5)
        self.pushButton_36.clicked.connect(self.move_class_6)
        self.pushButton_37.clicked.connect(self.move_class_7)
        self.pushButton_38.clicked.connect(self.move_class_8)
        self.frame_22.hide()
        
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def slider_set_accuracy(self):
        try:
            self.line.setText(str(self.slider.value()))
            self.send_point = int(self.slider.value())
        except BaseException as b:
            print(str(b))
        
    def line_set_accuracy(self):
        try:
            num = int(self.line.text())
            if num>=10 and num<50:
                num = 50
            self.line.setText(str(num))
            self.slider.setValue(num)
            self.send_point = num
        except:
            return
    
    @QtCore.pyqtSlot(int)
    def send_msg_ev3(self):
        try:
            message = str(self.msg)
            s = ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', message)
            self.ev3.write(s)
        except BaseException as b:
            print(str(b))
        
    def connect_ev3(self):
        try:
            if self.connect == 0:
                dda = ev3_connect_dialog.Ui_Dialog()
                aaa = dda.showModal()
                if aaa:
                    try:
                        self.ev3 = dda.ev3
                        self.pushButton_15.setText("EV3 연결끊기")
                        self.connect = 1
                    except BaseException as b:
                        print(str(b))
            else:
                try:
                    self.connect = 0
                    self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                    self.ev3.close()
                except:
                    pass
                self.pushButton_15.setText("EV3 연결하기")
                self.ev3 = None    
        except BaseException as b:
            print(str(b))
    
    
    def move_class_1(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            try:
                if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>1:
                    self.image_data.append(self.class_image)
                    self.train_coords.append(self.class_coords)
                    if self.label.text()=="":
                        self.class_name.append("CLASS_"+str(self.current_class))
                    else:
                        self.class_name.append(self.label.text())
                    self.class_explain.append(self.textEdit.toPlainText())
                elif self.current_class >1 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
                elif self.current_class != 1:
                    self.image_data[self.current_class-1]=self.class_image
                    self.train_coords[self.current_class-1]= self.class_coords
                    if self.label.text()=="":
                        self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                    else:
                        self.class_name[self.current_class-1]=self.label.text()
                    self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
                else:
                    return
                self.current_class=1
                self.class_image=self.image_data[self.current_class-1]
                self.class_coords = self.train_coords[self.current_class-1]
                self.table_row=0
                self.table.clearContents()
                self.while_count=0
                for step in range(len(self.class_image)):
                    height, width = self.class_image[step].shape[:2]
                    color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                    qt_image1 = QtGui.QImage(color_swapped_image.data,
                                                 width,
                                                 height,
                                                 color_swapped_image.strides[0],
                                                 QtGui.QImage.Format_RGB888)
                    capture_label = QtWidgets.QLabel()
                    qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                    pixmap = QtGui.QPixmap(qt_image1)
                    capture_label.setPixmap(pixmap)
                    capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
        "border-style:solid;\n"
        "border-color:white;\n")
                    if step%6!=0:
                        self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                    else:
                        self.table_row = self.table_row + 1
                        self.table.setRowCount(self.table_row)
                        self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                        self.table.setCellWidget(self.table_row-1,0,capture_label)
                    self.table.scrollToBottom()
                self.label.setText(self.class_name[self.current_class-1])
                self.textEdit.setText(self.class_explain[self.current_class-1])
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
            except BaseException as b:
                print(str(b))
        except BaseException as b:
            print(str(b))
    def move_class_2(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>2:
                self.image_data.append(self.class_image)
                self.train_coords.append(self.class_coords)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >2 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 2:
                self.image_data[self.current_class-1]=self.class_image
                self.train_coords[self.current_class-1]= self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=2
            self.class_image=self.image_data[self.current_class-1]
            self.class_coords = self.train_coords[self.current_class-1]
            self.table_row=0
            self.table.clearContents()
            self.while_count=0
            for step in range(len(self.class_image)):
                height, width = self.class_image[step].shape[:2]
                color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                capture_label = QtWidgets.QLabel()
                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                pixmap = QtGui.QPixmap(qt_image1)
                capture_label.setPixmap(pixmap)
                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                if step%6!=0:
                    self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                else:
                    self.table_row = self.table_row + 1
                    self.table.setRowCount(self.table_row)
                    self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                    self.table.setCellWidget(self.table_row-1,0,capture_label)
                self.table.scrollToBottom()
            self.label.setText(self.class_name[self.current_class-1])
            self.textEdit.setText(self.class_explain[self.current_class-1])
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))
    def move_class_3(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>3:
                self.image_data.append(self.class_image)
                self.train_coords.append(self.class_coords)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >3 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 3:
                self.image_data[self.current_class-1]=self.class_image
                self.train_coords[self.current_class-1]= self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=3
            self.class_image=self.image_data[self.current_class-1]
            self.class_coords = self.train_coords[self.current_class-1]
            self.table_row=0
            self.table.clearContents()
            self.while_count=0
            for step in range(len(self.class_image)):
                height, width = self.class_image[step].shape[:2]
                color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                capture_label = QtWidgets.QLabel()
                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                pixmap = QtGui.QPixmap(qt_image1)
                capture_label.setPixmap(pixmap)
                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                if step%6!=0:
                    self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                else:
                    self.table_row = self.table_row + 1
                    self.table.setRowCount(self.table_row)
                    self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                    self.table.setCellWidget(self.table_row-1,0,capture_label)
                self.table.scrollToBottom()
            self.label.setText(self.class_name[self.current_class-1])
            self.textEdit.setText(self.class_explain[self.current_class-1])
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))
    def move_class_4(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>4:
                self.image_data.append(self.class_image)
                self.train_coords.append(self.class_coords)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >4 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 4:
                self.image_data[self.current_class-1]=self.class_image
                self.train_coords[self.current_class-1]= self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=4
            self.class_image=self.image_data[self.current_class-1]
            self.class_coords = self.train_coords[self.current_class-1]
            self.table_row=0
            self.table.clearContents()
            self.while_count=0
            for step in range(len(self.class_image)):
                height, width = self.class_image[step].shape[:2]
                color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                capture_label = QtWidgets.QLabel()
                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                pixmap = QtGui.QPixmap(qt_image1)
                capture_label.setPixmap(pixmap)
                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                if step%6!=0:
                    self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                else:
                    self.table_row = self.table_row + 1
                    self.table.setRowCount(self.table_row)
                    self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                    self.table.setCellWidget(self.table_row-1,0,capture_label)
                self.table.scrollToBottom()
            self.label.setText(self.class_name[self.current_class-1])
            self.textEdit.setText(self.class_explain[self.current_class-1])
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))
    def move_class_5(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>5:
                self.image_data.append(self.class_image)
                self.train_coords.append(self.class_coords)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >5 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 5:
                self.image_data[self.current_class-1]=self.class_image
                self.train_coords[self.current_class-1]= self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=5
            self.class_image=self.image_data[self.current_class-1]
            self.class_coords = self.train_coords[self.current_class-1]
            self.table_row=0
            self.table.clearContents()
            self.while_count=0
            for step in range(len(self.class_image)):
                height, width = self.class_image[step].shape[:2]
                color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                capture_label = QtWidgets.QLabel()
                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                pixmap = QtGui.QPixmap(qt_image1)
                capture_label.setPixmap(pixmap)
                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                if step%6!=0:
                    self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                else:
                    self.table_row = self.table_row + 1
                    self.table.setRowCount(self.table_row)
                    self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                    self.table.setCellWidget(self.table_row-1,0,capture_label)
                self.table.scrollToBottom()
            self.label.setText(self.class_name[self.current_class-1])
            self.textEdit.setText(self.class_explain[self.current_class-1])
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))
    def move_class_6(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>6:
                self.image_data.append(self.class_image)
                self.train_coords.append(self.class_coords)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >6 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 6:
                self.image_data[self.current_class-1]=self.class_image
                self.train_coords[self.current_class-1]= self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=6
            self.class_image=self.image_data[self.current_class-1]
            self.class_coords = self.train_coords[self.current_class-1]
            self.table_row=0
            self.table.clearContents()
            self.while_count=0
            for step in range(len(self.class_image)):
                height, width = self.class_image[step].shape[:2]
                color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                capture_label = QtWidgets.QLabel()
                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                pixmap = QtGui.QPixmap(qt_image1)
                capture_label.setPixmap(pixmap)
                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                if step%6!=0:
                    self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                else:
                    self.table_row = self.table_row + 1
                    self.table.setRowCount(self.table_row)
                    self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                    self.table.setCellWidget(self.table_row-1,0,capture_label)
                self.table.scrollToBottom()
            self.label.setText(self.class_name[self.current_class-1])
            self.textEdit.setText(self.class_explain[self.current_class-1])
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))
    def move_class_7(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>7:
                self.image_data.append(self.class_image)
                self.train_coords.append(self.class_coords)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >7 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 7:
                self.image_data[self.current_class-1]=self.class_image
                self.train_coords[self.current_class-1]= self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=7
            self.class_image=self.image_data[self.current_class-1]
            self.class_coords = self.train_coords[self.current_class-1]
            self.table_row=0
            self.table.clearContents()
            self.while_count=0
            for step in range(len(self.class_image)):
                height, width = self.class_image[step].shape[:2]
                color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                capture_label = QtWidgets.QLabel()
                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                pixmap = QtGui.QPixmap(qt_image1)
                capture_label.setPixmap(pixmap)
                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                if step%6!=0:
                    self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                else:
                    self.table_row = self.table_row + 1
                    self.table.setRowCount(self.table_row)
                    self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                    self.table.setCellWidget(self.table_row-1,0,capture_label)
                self.table.scrollToBottom()
            self.label.setText(self.class_name[self.current_class-1])
            self.textEdit.setText(self.class_explain[self.current_class-1])
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))
    def move_class_8(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>8:
                self.image_data.append(self.class_image)
                self.train_coords.append(self.class_coords)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class != 8:
                self.image_data[self.current_class-1]=self.class_image
                self.train_coords[self.current_class-1]= self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=8
            self.class_image=self.image_data[self.current_class-1]
            self.class_coords = self.train_coords[self.current_class-1]
            self.table_row=0
            self.table.clearContents()
            self.while_count=0
            for step in range(len(self.class_image)):
                height, width = self.class_image[step].shape[:2]
                color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                capture_label = QtWidgets.QLabel()
                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                pixmap = QtGui.QPixmap(qt_image1)
                capture_label.setPixmap(pixmap)
                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                if step%6!=0:
                    self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                else:
                    self.table_row = self.table_row + 1
                    self.table.setRowCount(self.table_row)
                    self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                    self.table.setCellWidget(self.table_row-1,0,capture_label)
                self.table.scrollToBottom()
            self.label.setText(self.class_name[self.current_class-1])
            self.textEdit.setText(self.class_explain[self.current_class-1])
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))   
    def change_button_name(self):
        try:
            if len(self.label.text())<=16:
                self.label_4.setText("")
                if self.current_class == 1:
                    self.pushButton_31.setText(self.label.text())
                elif self.current_class == 2:
                    self.pushButton_32.setText(self.label.text())
                elif self.current_class == 3:
                    self.pushButton_33.setText(self.label.text())
                elif self.current_class == 4:
                    self.pushButton_34.setText(self.label.text())
                elif self.current_class == 5:
                    self.pushButton_35.setText(self.label.text())
                elif self.current_class == 6:
                    self.pushButton_36.setText(self.label.text())
                elif self.current_class == 7:
                    self.pushButton_37.setText(self.label.text())
                elif self.current_class == 8:
                    self.pushButton_38.setText(self.label.text())
            else:
                self.label_4.setText("클래스이름은 16자이내로 작성해주세요")
                self.label.setText("")
                return
        except BaseException as b:
            print(str(b))
    @QtCore.pyqtSlot()        
    def error_learning(self):
        try:
            self.label_4.setText('학습도중 에러가 발생했습니다.\n 다시해주세요.')
            self.progress_bar.hide()
            self.progress_label.hide()
            self.frame_23.show()
            self.learning -= 1
            self.pushButton_12.setText("학습하러가기")
        except:
            pass
    @QtCore.pyqtSlot(list)        
    def finish_learning(self,history):
        try:
            if len(history[0])>0 and len(history[1])>0 and len(history[2])>0 and len(history[3])>0:
                acc = history[0]
                val_acc = history[1]
                loss = history[2]
                val_loss = history[3]
                plt.figure(figsize=(8, 8))
                plt.subplot(1, 2, 1)
                plt.plot(range(len(acc)), acc, label='train_accracy')
                plt.plot(range(len(val_acc)), val_acc, label='val_accracy')
                plt.legend(loc='lower right')
                plt.title('train and validation accracy')
            
                plt.subplot(1, 2, 2)
                plt.plot(range(len(loss)), loss, label='train_loss')
                plt.plot(range(len(val_loss)), val_loss, label='val_loss')
                plt.legend(loc='upper right')
                plt.title('train and validation loss')
                plt.show()
            self.progress_bar.hide()
            self.progress_label.hide()
            self.learning -= 1
            self.preview += 1
            self.model = True
            self.frame_22.show()
            self.label_4.setText('학습이 완료되었습니다.')
            self.pushButton_12.setText("예측 중지")
        except BaseException as b:
            print(str(b)) 
    @QtCore.pyqtSlot(int)        
    def learning_process(self,num):        
        self.progress_bar.setValue(num)
    def go_image_learning(self):
        try:
            if self.check_capture():
                return
            if self.learning==1:
                self.learning -=1
                self.t1.stop_learning()
                self.progress_bar.hide()
                self.progress_label.hide()
                self.pushButton_12.setText("학습하러 가기")
                self.frame_23.show()
                return
            if len(self.train_coords)<=1 and self.current_class==1:
                self.label_4.setText('클래스가 2개 이상이어야 합니다.')
                return
            if not self.preview:
                try:
                    if self.current_class==len(self.image_data)+1 and len(self.class_image)>0:
                        self.image_data.append(self.class_image)
                        self.train_coords.append(self.class_coords)
                        if self.label.text() == "":
                            self.class_name.append("CLASS_"+str(self.current_class))
                        else:
                            self.class_name.append(self.label.text())
                        self.class_explain.append(self.textEdit.toPlainText())
                    for step in range(len(self.image_data)):
                        if len(self.image_data[step]) < 1:
                            self.label_4.setText("이미지가 1장 이상이어야 합니다.\n"
                                             "현재 CLASS_"+str(step+1)+" -> "+str(len(self.image_data[step]))+"장")
                            return
                    for step in range(len(self.image_data)):
                        if len(self.image_data[step]) < 50:
                            self.label_4.setText("이미지가 50장 이상이어야 합니다.\n"
                                             "현재 CLASS_"+str(step+1)+" -> "+str(len(self.image_data[step]))+"장")
                            return
                    dialog = motion_train_dialog.Ui_Dialog(self.train_coords,self.learning_count)
                    m = dialog.showModal()
                    if m:
                        self.learning += 1
                        self.frame_23.hide()
                        self.progress_bar.setValue(0)
                        self.progress_bar.show()
                        self.progress_label.show()
                        self.label_4.setText('학습중 입니다.')
                        td = dialog.train_data
                        tl = dialog.train_label
                        vd = dialog.val_data
                        vl = dialog.val_label
                        le = dialog.learning_rate
                        ba = dialog.batch_size
                        ep = dialog.epoch_size
                        ca = len(self.image_data)
                        self.label.setReadOnly(True)
                        self.textEdit.setReadOnly(True)
                        self.pushButton_12.setText("학습 취소시키기")
                        self.learning_count = dialog.learning_count
                        self.saved = 0
                        self.t1 = ML_class(td,vd,tl,vl,le,ba,ep,ca,self.learning_count)
                        self.t1.finish_signal.connect(self.finish_learning)
                        self.t1.process_signal.connect(self.learning_process)
                        self.t1.error_signal.connect(self.error_learning)
                        self.t1.predict_signal.connect(self.receive_function)
                        self.t1.start()
                except BaseException as b:
                    print(str(b))
            else:
                tt = train_alam.Ui_Dialog('현재 프로젝트를\n저장 하시겠습니까?')
                aa = tt.showModal()
                if aa:
                    r= self.save_project()
                    if r=='e':
                        return
                self.t1.stop_learning()
                if self.connect == 1:
                    self.ev3.close()
                    self.connect = 0
                self.label.setReadOnly(False)
                self.textEdit.setReadOnly(False)
                self.frame_22.hide()
                self.frame_23.show()
                self.preview = self.preview-1
                self.pushButton_12.setText("학습하러가기")
        except BaseException as b:
            print(str(b))  
    @QtCore.pyqtSlot(list)
    def receive_function(self,predict):
        try:
            self.set_progressbars(predict)
            for step in range(len(predict[0])):
                if predict[0][step] >= (self.send_point/100):
                    self.msg = step+1
                    self.label_3.setText(self.class_name[step])
                    self.textEdit_2.setText(self.class_explain[step])
                elif predict[0][step] > 1-(self.send_point/100):
                    self.label_3.setText("")
                    self.textEdit_2.setText("")
                    self.msg = 0
            if self.connect == 1:
                try:
                    self.send_msg_ev3(self.msg)
                except BaseException as b:
                    print(str(b))
        except BaseException as b:
            print(str(b))  
    
    def delete_image(self):
        try:
            if self.check_previewed():
                return
            if self.check_capture():
                return
            try:
                if len(self.clicked_label_position)==0:
                    self.label_4.setText("선택된 이미지가 없습니다.\n"
                                        "지우려는 이미지를 클릭해주세요")
                    return
                else:
                    self.clicked_label_position.sort()
                    for step in range(len(self.clicked_label_position)):
                        self.class_image.pop(self.clicked_label_position[step][0]*6+self.clicked_label_position[step][1]-step)
                        self.class_coords.pop(self.clicked_label_position[step][0]*6+self.clicked_label_position[step][1]-step)
                    self.clicked_label_position=[]
                    self.table_row=0
                    self.table.clearContents()
                    self.while_count=0
                    for step in range(len(self.class_image)):
                        height, width = self.class_image[step].shape[:2]
                        color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                        qt_image1 = QtGui.QImage(color_swapped_image.data,
                                                 width,
                                                 height,
                                                 color_swapped_image.strides[0],
                                                 QtGui.QImage.Format_RGB888)
                        capture_label = QtWidgets.QLabel()
                        qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                        pixmap = QtGui.QPixmap(qt_image1)
                        capture_label.setPixmap(pixmap)
                        capture_label.setStyleSheet("border-width:3px;\n"
        "border-style:solid;\n"
        "border-color:white;\n")
                        if step%6!=0:
                            self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                        else:
                            self.table_row = self.table_row + 1
                            self.table.setRowCount(self.table_row)
                            self.table.setRowHeight(self.table_row-1,76)
                            self.table.setCellWidget(self.table_row-1,0,capture_label)
                        self.table.scrollToBottom()
                    if len(self.class_image)==0:
                        self.delete_class()
                    self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
            except BaseException as b:
                print(str(b))
        except BaseException as b:
            print(str(b))
    def clicked_image(self, row, col):
        try:
            if self.check_capture():
                return
            
            if self.check_previewed():
                return
            checked = False
            for step in range(len(self.clicked_label_position)):
                if self.clicked_label_position[step]==[row,col]:
                    checked = True
                    self.clicked_label_position.pop(step)
                    break
            if len(self.class_image)>= (row*6)+col+1:
                if checked:
                    label = self.table.cellWidget(row, col)
                    
                    label.setStyleSheet("border-width:3px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                    self.table.setCellWidget(row,col,label)
                else:        
                    label = self.table.cellWidget(row, col)
                    label.setStyleSheet("border-width:3px;\n"
    "border-style:solid;\n"
    "border-color:red;\n")
                    self.table.setCellWidget(row,col,label)
                    self.clicked_label_position.append([row,col])
            else:
                if len(self.clicked_label_position) > 0:
                    for step in range(len(self.clicked_label_position)):
                        item = self.table.cellWidget(self.clicked_label_position[step][0], self.clicked_label_position[step][1])
                        item.setStyleSheet("border-width:3px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                        self.table.setCellWidget(self.clicked_label_position[step][0], self.clicked_label_position[step][1],item)
                    self.clicked_label_position = []
                else:
                    return
        except BaseException as b:
            print(str(b))    
    @QtCore.pyqtSlot()
    def open_image(self):
        try:
            if self.check_capture():
                return
            if self.check_previewed():
                return
            
            file_dialog = QFileDialog()
            file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            file_view = file_dialog.findChild(QtWidgets.QListView, "listView")
    
            if file_view:
                file_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
                f_tree_view = file_dialog.findChild(QtWidgets.QTreeView)
                if f_tree_view:
                    f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    
                if file_dialog.exec():
                    paths = file_dialog.selectedFiles()
                    try:
                        parser = argparse.ArgumentParser()
                        parser.add_argument('--model',type=int, default=101)
                        parser.add_argument('--scale_factor',type=float, default=1.0)
                        args = parser.parse_args()
                        with tf.Session() as sess2:
                            model_cfg, model_outputs = posenet.load_model(args.model, sess2)
                            output_stride = model_cfg['output_stride']
    
                            for f in paths:
                                input_image, draw_image, output_scale = posenet.read_imgfile(
                                    f, scale_factor=args.scale_factor, output_stride=output_stride)
    
                                heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess2.run(
                                                model_outputs,
                                                feed_dict={'image:0': input_image}
                                                )
    
                                pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
                                    heatmaps_result.squeeze(axis=0),
                                    offsets_result.squeeze(axis=0),
                                    displacement_fwd_result.squeeze(axis=0),
                                    displacement_bwd_result.squeeze(axis=0),
                                    output_stride=output_stride,
                                    max_pose_detections=10,
                                    min_pose_score=0.25)
                                
                                if pose_scores[0]==0:
                                    self.label_4.setText('자세를 인식할 대상이 없는 사진이 있습니다.')
                                    continue
                                elif pose_scores[2]!=0:
                                    self.label_4.setText('2명 이상의 사진은 불러올수 없습니다.')
                                else:
                                    keypoint_coords *= output_scale
                                    keypoint_count = []
                                    score = []
                                    motion_count= []
                                    draw_image = posenet.draw_skel_and_kp(
                                    draw_image, pose_scores, keypoint_scores, keypoint_coords,
                                    min_pose_score=0.25, min_part_score=0.25)
                                    for step2 in range(17):
                                        keypoint_count.append(pose_scores[0])
                                        keypoint_count.append(keypoint_scores[0][step2]*2)
                                        keypoint_count.append(keypoint_coords[0][step2][0]/self.nomal)
                                        keypoint_count.append(keypoint_coords[0][step2][1]/self.nomal)
                                        keypoint_count.append(pose_scores[1])
                                        keypoint_count.append(keypoint_scores[1][step2]*2)
                                        keypoint_count.append(keypoint_coords[1][step2][0]/self.nomal)
                                        keypoint_count.append(keypoint_coords[1][step2][1]/self.nomal)
                                        score.append(keypoint_count)
                                        keypoint_count = []
                                    motion_count.append(score)
                                    motion_count = np.asarray(motion_count)
                                    self.class_coords.append(motion_count)
                                    
                                    self.class_image.append(draw_image)
                                    height, width = draw_image.shape[:2]
                                    color_swapped_image = cv2.cvtColor(draw_image, cv2.COLOR_BGR2RGB)
                                    qt_image1 = QtGui.QImage(color_swapped_image.data,
                                                             width,
                                                             height,
                                                             color_swapped_image.strides[0],
                                                             QtGui.QImage.Format_RGB888)
                                    capture_label = QtWidgets.QLabel()
                                    qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                                    pixmap = QtGui.QPixmap(qt_image1)
                                    capture_label.setPixmap(pixmap)
                                    capture_label.setStyleSheet("border-width:3px;\n"
            "border-style:solid;\n"
            "border-color:white;\n")
                                    if (len(self.class_image)-1)%6!=0:
                                        self.table.setCellWidget(self.table_row-1,(len(self.class_image)-1)%6,capture_label)
                                    else:
                                        self.table_row = self.table_row + 1
                                        self.table.setRowCount(self.table_row)
                                        self.table.setRowHeight(self.table_row-1,76)
                                        self.table.setCellWidget(self.table_row-1,0,capture_label)
                                    self.table.scrollToBottom()
                                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
                    except:
                        self.label_4.setText('이미지가 아닌 파일이 있습니다.')
                        return
        except BaseException as b:
            print(str(b))
    def delete_class(self):
        try:
            if self.check_capture():
                return
            if self.check_previewed():
                return
            try:
                if self.current_class == len(self.image_data)+1:
                    self.table.clearContents()
                    self.table_row = 0
                    self.class_image = []
                    self.class_coords = []
                    self.while_count = 0
                    self.clicked_label_position = []
                    self.label.setText("CLASS_"+str(self.current_class))
                    self.textEdit.setText("")
                    self.label_2.setText("CLASS_"+str(self.current_class))
                else:
                    self.image_data.pop(self.current_class-1)
                    self.class_name.pop(self.current_class-1)
                    self.class_explain.pop(self.current_class-1)
                    self.train_coords.pop(self.current_class-1)
                    self.clicked_label_position = []
                    if self.current_class == len(self.image_data)+1:
                        self.table.clearContents()
                        self.class_image = []
                        self.class_coords = []
                        self.table_row = 0
                        self.while_count = 0
                        self.label.setText("CLASS_"+str(self.current_class))
                        self.textEdit.setText("")
                        self.label_2.setText("CLASS_"+str(self.current_class))
                    else:
                        for step in range(len(self.class_name)):
                            if self.class_name[step] == "CLASS_"+str(step+2):
                                self.class_name[step] = "CLASS_"+str(step+1)
                        try:
                            self.pushButton_31.setText(self.class_name[0])
                            self.pushButton_32.setText(self.class_name[1])
                            self.pushButton_33.setText(self.class_name[2])
                            self.pushButton_34.setText(self.class_name[3])
                            self.pushButton_35.setText(self.class_name[4])
                            self.pushButton_36.setText(self.class_name[5])
                            self.pushButton_37.setText(self.class_name[6])
                            self.pushButton_38.setText(self.class_name[7])
                        except:
                            print('')
                        self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((len(self.image_data)-1)*self.program_height*0.08)))
                        self.table_row=0
                        self.table.clearContents()
                        self.while_count=0
                        self.class_image = []
                        self.class_coords = self.train_coords[self.current_class-1]
                        self.class_image = self.image_data[self.current_class-1]
                        for step in range(len(self.class_image)):
                            height, width = self.class_image[step].shape[:2]
                            color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                                     width,
                                                     height,
                                                     color_swapped_image.strides[0],
                                                     QtGui.QImage.Format_RGB888)
                            capture_label = QtWidgets.QLabel()
                            qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                            pixmap = QtGui.QPixmap(qt_image1)
                            capture_label.setPixmap(pixmap)
                            capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
        "border-style:solid;\n"
        "border-color:white;\n")
                            if step%6!=0:
                                self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                            else:
                                self.table_row = self.table_row + 1
                                self.table.setRowCount(self.table_row)
                                self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                                self.table.setCellWidget(self.table_row-1,0,capture_label)
                            self.table.scrollToBottom()
                        self.label.setText(self.class_name[self.current_class-1])
                        self.textEdit.setText(self.class_explain[self.current_class-1])
                        self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
            except BaseException as b:
                print(str(b))
        except BaseException as b:
            print(str(b))
    def go_next_class(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if len(self.image_data)>self.current_class:
                self.clicked_label_position = []
                self.image_data[self.current_class-1] = self.class_image
                self.train_coords[self.current_class-1] = self.class_coords
                if self.label.text()=="":
                    self.class_name[self.current_class-1] = "CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1] = self.label.text()
                self.class_explain[self.current_class-1] = self.textEdit.toPlainText()
                self.table_row=0
                self.table.clearContents()
                self.while_count=0
                self.class_image = []
                self.class_coords = []
                self.class_image = self.image_data[self.current_class]
                self.class_coords = self.train_coords[self.current_class]
                for step in range(len(self.class_image)):
                    height, width = self.class_image[step].shape[:2]
                    color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                    qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                    capture_label = QtWidgets.QLabel()
                    qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                    pixmap = QtGui.QPixmap(qt_image1)
                    capture_label.setPixmap(pixmap)
                    capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                    if step%6!=0:
                        self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                    else:
                        self.table_row = self.table_row + 1
                        self.table.setRowCount(self.table_row)
                        self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                        self.table.setCellWidget(self.table_row-1,0,capture_label)
                    self.table.scrollToBottom()
                self.current_class = self.current_class+1
                self.label.setText(self.class_name[self.current_class-1])
                self.textEdit.setText(self.class_explain[self.current_class-1])
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
            else:
                if self.current_class == 8:
                    self.label_4.setText("클래스는 8개까지 생성할수 있습니다.")
                    return
                self.clicked_label_position = []
                if self.current_class==len(self.image_data)+1 and len(self.class_image)>0:
                    self.table.clearContents()
                    self.image_data.append(self.class_image)
                    self.train_coords.append(self.class_coords)
                    self.class_image=[]
                    self.class_coords = []
                    self.while_count=0
                    self.table_row=0
                    if self.label.text()=="":
                        self.class_name.append("CLASS_"+str(self.current_class))
                        self.label.setText("CLASS_"+str(self.current_class))
                    else:
                        self.class_name.append(self.label.text())
                    self.class_explain.append(self.textEdit.toPlainText())
                    self.current_class = self.current_class+1
                    self.label.setText("CLASS_"+str(self.current_class))
                    self.textEdit.setText("")
                    self.label_2.setText("CLASS_"+str(self.current_class))
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-1)*self.program_height*0.08)))
                elif self.current_class==len(self.image_data):
                    self.image_data[self.current_class-1] = self.class_image
                    self.train_coords[self.current_class-1] = self.class_coords
                    self.class_name[self.current_class-1] = self.label.text()
                    self.class_explain[self.current_class-1] = self.textEdit.toPlainText()
                    if self.label.text()=="":
                        self.label.setText("CLASS_"+str(self.current_class))
                    self.table.clearContents()
                    self.while_count=0
                    self.table_row = 0
                    self.class_image = []
                    self.class_coords=[]
                    self.current_class = self.current_class+1
                    self.label.setText("CLASS_"+str(self.current_class))
                    self.textEdit.setText("")
                    self.label_2.setText("CLASS_"+str(self.current_class))
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-1)*self.program_height*0.08)))
                else:
                    self.label_4.setText("현재 클래스에 이미지가 있어야합니다.")
                    return
        except BaseException as b:
            print(str(b))
    @QtCore.pyqtSlot()
    def go_pre_class(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("클래스의 이름을 적어주셔야 합니다.")
                return
            if self.current_class==1:
                self.label_4.setText("첫번째 클래스입니다.")
                return
            else:
                self.clicked_label_position = []
                if len(self.class_image)>0:
                    if self.current_class==len(self.image_data)+1:
                        self.image_data.append(self.class_image)
                        self.train_coords.append(self.class_coords)
                        if self.label.text()=="":
                            self.class_name.append("CLASS_"+str(self.current_class))
                        else:
                            self.class_name.append(self.label.text())
                        self.class_explain.append(self.textEdit.toPlainText())
                    else:
                        self.image_data[self.current_class-1] = self.class_image
                        self.train_coords[self.current_class-1] = self.class_coords
                        self.class_name[self.current_class-1] = self.label.text()
                        self.class_explain[self.current_class-1] = self.textEdit.toPlainText()
                else:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
                self.current_class = self.current_class-1
                self.table.clearContents()
                self.table_row=0
                self.while_count=0
                self.class_image=[]
                self.class_coords = self.train_coords[self.current_class-1]
                self.class_image = self.image_data[self.current_class-1]
                for step in range(len(self.class_image)):
                    height, width = self.class_image[step].shape[:2]
                    color_swapped_image2 = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                    qt_image2 = QtGui.QImage(color_swapped_image2.data,
                                             width,
                                             height,
                                             color_swapped_image2.strides[0],
                                             QtGui.QImage.Format_RGB888)
                    capture_label2 = QtWidgets.QLabel()
                    qt_image2 = qt_image2.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                    pixmap = QtGui.QPixmap(qt_image2)
                    capture_label2.setPixmap(pixmap)
                    capture_label2.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                    if step%6!=0:
                        self.table.setCellWidget(self.table_row-1,step%6,capture_label2)
                    else:
                        self.table_row = self.table_row + 1
                        self.table.setRowCount(self.table_row)
                        self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                        self.table.setCellWidget(self.table_row-1,0,capture_label2)
                    self.table.scrollToBottom()
                self.label.setText(self.class_name[self.current_class-1])
                self.textEdit.setText(self.class_explain[self.current_class-1])
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
        except BaseException as b:
            print(str(b))
    def append_table(self,image_label):
        try:
            if (len(self.class_image)-1)%6!=0:
                self.table.setCellWidget(self.table_row-1,(len(self.class_image)-1)%6,image_label)
            else:
                self.table_row = self.table_row + 1
                self.table.setRowCount(self.table_row)
                self.table.setColumnCount(self.table_column)
                self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                self.table.setCellWidget(self.table_row-1,0,image_label)
            self.table.scrollToBottom()
        except BaseException as b:
            print(str(b))
    @QtCore.pyqtSlot()
    def show_video(self):
        with tf.Session() as sess:
            self.model_cfg, self.model_output= posenet.load_model(self.args.model,sess)
            self.output_stride = self.model_cfg['output_stride']
        
            while True:
                try:
                    if self.dq == 1:
                        break
                    input_image, display_image, output_scale = posenet.read_cap(self.cap, scale_factor=self.args.scale_factor, output_stride=self.output_stride)
                
                    heatmaps_result, offsets_result, displacements_fwd_result,displacements_bwd_result = sess.run(
                        self.model_output,
                        feed_dict = {'image:0':input_image}
                        )
                
                    pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                        heatmaps_result.squeeze(axis=0),
                        offsets_result.squeeze(axis=0),
                        displacements_fwd_result.squeeze(axis=0),
                        displacements_bwd_result.squeeze(axis=0),
                        output_stride=self.output_stride,
                        max_pose_detections=10,
                        min_pose_score=0.15)
                    print(pose_scores[0])
                    print(keypoint_scores[0])
                    print(keypoint_coords[0])
                    
                    keypoint_coords *= output_scale
                    overlay_image = posenet.draw_skel_and_kp(
                        display_image, pose_scores, keypoint_scores, keypoint_coords,
                        min_pose_score=0.15, min_part_score=0.1)
                    overlay_image = cv2.flip(overlay_image,1)
                    height,width = overlay_image.shape[:2]
                    overlay_image = cv2.resize(overlay_image,dsize=(int(width*(self.program_width*0.34)/height),int(self.program_width*0.34)))
                    height,width = overlay_image.shape[:2]
                    start_width = int((width-(self.program_width*0.34))/2)
                    overlay_image = overlay_image[:,start_width:int(start_width+(self.program_width*0.34)),:]
                    height, width = overlay_image.shape[:2]
                    color_swapped_image = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2RGB)
                    qt_image1 = QtGui.QImage(color_swapped_image.data,
                                             width,
                                             height,
                                             color_swapped_image.strides[0],
                                             QtGui.QImage.Format_RGB888)
                    if not self.preview:
                        self.VideoSignal1.emit(qt_image1)
                    else:
                        self.VideoSignal1.emit(qt_image1)
                        qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.3,self.program_width*0.3))
                        self.VideoSignal2.emit(qt_image1)
                        motion_count = []
                        keypoint_count = []
                        score=[]
                        data=[]
                        for step2 in range(17):
                            keypoint_count.append(keypoint_scores[0][step2]*pose_scores[0]*2)
                            keypoint_count.append((keypoint_coords[0][step2][0]/self.nomal)*keypoint_scores[0][step2])
                            keypoint_count.append((keypoint_coords[0][step2][1]/self.nomal)*keypoint_scores[0][step2])
                            keypoint_count.append(keypoint_scores[1][step2]*pose_scores[1]*2)
                            keypoint_count.append((keypoint_coords[1][step2][0]/self.nomal)*keypoint_scores[1][step2])
                            keypoint_count.append((keypoint_coords[1][step2][1]/self.nomal)*keypoint_scores[1][step2])
                            score.append(keypoint_count)
                            keypoint_count = []
                        motion_count.append(score)
                        score=[]
                        data.append(motion_count)
                        data = np.asarray(data)
                        data = data.reshape(1,6,17,1)
                        self.t1.receive_data(data)
                        
                    if self.capture_checked:
                        capture_label = QtWidgets.QLabel()
                        qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                        pixmap = QtGui.QPixmap(qt_image1)
                        capture_label.setPixmap(pixmap)
                        capture_label.setStyleSheet("border-width:3px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                        self.append_table(capture_label)
                        self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
                        score = []
                        keypoint_count = []
                        motion_count = []
                        if pose_scores[2]!=0:
                            self.capture_checked = 0
                            self.label_4.setText("모션은 최대 2사람만 캡쳐가 가능합니다.")
                            self.pushButton_8.setText("사 진 촬 영")
                            continue
                        
                        if pose_scores[0]==0:
                            self.capture_checked = 0
                            self.label_4.setText("모션을 인식할 대상이 화면에 없습니다.")
                            self.pushButton_8.setText("사 진 촬 영")
                            continue
                            
                        for step2 in range(17):
                            keypoint_count.append(keypoint_scores[0][step2]*pose_scores[0]*2)
                            keypoint_count.append(keypoint_coords[0][step2][0]/self.nomal)
                            keypoint_count.append(keypoint_coords[0][step2][1]/self.nomal)
                            keypoint_count.append(keypoint_scores[1][step2]*pose_scores[1]*2)
                            keypoint_count.append(keypoint_coords[1][step2][0]/self.nomal)
                            keypoint_count.append(keypoint_coords[1][step2][1]/self.nomal)
                            score.append(keypoint_count)
                            keypoint_count = []
                        motion_count.append(score)
                        score=[]
                        self.class_coords.append(motion_count)
                        self.class_image.append(overlay_image)
                        self.while_count = self.while_count+1
                    loop = QtCore.QEventLoop()
                    QtCore.QTimer.singleShot(25, loop.quit)
                    loop.exec_()
                except BaseException as b:
                    continue
    def menu_show_event(self):
        try:
            if self.capture_checked:
                self.label_4.setText("사진 촬영 중에는 다른 것을 할 수 없습니다!!")
                return
            else:
                if self.menu_clicked==1:
                    self.frame_2.hide()
                    self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                              "image:url('./image/menu_icon.png')")
                    self.pushButton.move(self.program_width*0.02,self.program_width*0.02)
                    self.menu_clicked = 0
                else:
                    self.frame_2.show()
                    self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                              "image:url('./image/menu_close_icon.png')")
                    self.pushButton.move(self.program_width*0.3,self.program_width*0.02)
                    self.menu_clicked = 1
        except BaseException as b:
            print(str(b))
    def quit(self):
        try:
            self.new_project()
            self.frame_2.hide()
            self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                              "image:url('./image/menu_icon.png')")
            self.pushButton.move(self.program_width*0.02,self.program_width*0.02)
            self.menu_clicked = 1 - self.menu_clicked
            self.dq = 1
            if self.connect == 1:
                self.connect = 0
                self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                self.ev3.close()
            self.VideoSignal1.disconnect(self.cam_viewer1.setImage)
            self.VideoSignal2.disconnect(self.cam_viewer2.setImage)
            self.MessageSignal.disconnect(self.send_msg_ev3)
            self.cap.release()
            self.hide()
            self.m_window.show()
        except BaseException as b:
            print(str(b))
    def exit(self):
        try:
            if self.learning==1:
                self.label_4.setText('학습중에는 안됩니다.')
                return
            if self.saved ==0:
                tt = train_alam.Ui_Dialog('현재 프로젝트를\n저장 하시겠습니까?')
                aa = tt.showModal()
                if aa:
                    r= self.save_project()
                    if r=='e':
                        return
            if self.preview==1:
                self.t1.stop_learning()
                self.preview -=1
                self.frame_22.hide()
                self.frame_23.show()
            if self.connect == 1:
                self.connect = 0
                self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                self.ev3.close()
            self.dq = 1
            self.VideoSignal1.disconnect(self.cam_viewer1.setImage)
            self.VideoSignal2.disconnect(self.cam_viewer2.setImage)
            self.cap.release()
            self.close()
        except BaseException as b:
            print(str(b))
    @QtCore.pyqtSlot()        
    def capture_image(self):
        try:
            if self.check_previewed():
                self.label_4.setText("예측 중에는 할 수 없습니다.")
                return
            self.capture_checked = 1 - self.capture_checked
            if self.capture_checked:
                self.pushButton_8.setText("사  진  촬  영  중  지")
            else:
                self.table_row = 0
                self.table.clearContents()
                for step in range(len(self.class_image)):
                    height, width = self.class_image[step].shape[:2]
                    color_swapped_image2 = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                    qt_image2 = QtGui.QImage(color_swapped_image2.data,
                                             width,
                                             height,
                                             color_swapped_image2.strides[0],
                                             QtGui.QImage.Format_RGB888)
                    capture_label2 = QtWidgets.QLabel()
                    qt_image2 = qt_image2.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                    pixmap = QtGui.QPixmap(qt_image2)
                    capture_label2.setPixmap(pixmap)
                    capture_label2.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                    if step%6!=0:
                        self.table.setCellWidget(self.table_row-1,step%6,capture_label2)
                    else:
                        self.table_row = self.table_row + 1
                        self.table.setRowCount(self.table_row)
                        self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                        self.table.setCellWidget(self.table_row-1,0,capture_label2)
                    self.table.scrollToBottom()
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
                self.pushButton_8.setText("사  진  촬  영 ")
        except BaseException as b:
            print(str(b))    
    def check_capture(self):
        try:
            if self.menu_clicked:
                self.frame_2.hide()
                self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                              "image:url('./image/menu_icon.png')")
                self.pushButton.move(self.program_width*0.02,self.program_width*0.02)
                self.menu_clicked = 1 - self.menu_clicked
            if self.capture_checked:
                self.label_4.setText("사진 촬영 중에는 다른 것을 할 수 없습니다!!")
                return True
            else:
                self.label_4.setText("")
                return False
        except BaseException as b:
            print(str(b))
    def check_previewed(self):
        try:
            if self.menu_clicked:
                self.frame_2.hide()
                self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                              "image:url('./image/menu_icon.png')")
                self.pushButton.move(self.program_width*0.02,self.program_width*0.02)
                self.menu_clicked = 1 - self.menu_clicked
            if self.preview:
                self.label_4.setText("예측 중에는 할수 없습니다.")
                return True
            else:
                self.label_4.setText("")
                return False
        except BaseException as b:
            print(str(b))
    def set_progressbars(self,predict):
        try:
            self.frame_4.resize(self.program_width*0.36,len(predict[0])*self.program_height*0.038)
            if len(predict[0])==2:
                self.bar_1.setValue(int(predict[0][0]*100))
                self.bar_2.setValue(int(predict[0][1]*100))
            if len(predict[0])==3:
                self.bar_1.setValue(int(predict[0][0]*100))
                self.bar_2.setValue(int(predict[0][1]*100))
                self.bar_3.setValue(int(predict[0][2]*100))
            if len(predict[0])==4:
                self.bar_1.setValue(int(predict[0][0]*100))
                self.bar_2.setValue(int(predict[0][1]*100))
                self.bar_3.setValue(int(predict[0][2]*100))
                self.bar_4.setValue(int(predict[0][3]*100))
            if len(predict[0])==5:
                self.bar_1.setValue(int(predict[0][0]*100))
                self.bar_2.setValue(int(predict[0][1]*100))
                self.bar_3.setValue(int(predict[0][2]*100))
                self.bar_4.setValue(int(predict[0][3]*100))
                self.bar_5.setValue(int(predict[0][4]*100))
            if len(predict[0])==6:
                self.bar_1.setValue(int(predict[0][0]*100))
                self.bar_2.setValue(int(predict[0][1]*100))
                self.bar_3.setValue(int(predict[0][2]*100))
                self.bar_4.setValue(int(predict[0][3]*100))
                self.bar_5.setValue(int(predict[0][4]*100))
                self.bar_6.setValue(int(predict[0][5]*100))
            if len(predict[0])==7:
                self.bar_1.setValue(int(predict[0][0]*100))
                self.bar_2.setValue(int(predict[0][1]*100))
                self.bar_3.setValue(int(predict[0][2]*100))
                self.bar_4.setValue(int(predict[0][3]*100))
                self.bar_5.setValue(int(predict[0][4]*100))
                self.bar_6.setValue(int(predict[0][5]*100))
                self.bar_7.setValue(int(predict[0][6]*100))
            if len(predict[0])==8:
                self.bar_1.setValue(int(predict[0][0]*100))
                self.bar_2.setValue(int(predict[0][1]*100))
                self.bar_3.setValue(int(predict[0][2]*100))
                self.bar_4.setValue(int(predict[0][3]*100))
                self.bar_5.setValue(int(predict[0][4]*100))
                self.bar_6.setValue(int(predict[0][5]*100))
                self.bar_7.setValue(int(predict[0][6]*100))
                self.bar_8.setValue(int(predict[0][7]*100))
        except BaseException as b:
            print(str(b))
    def save_project(self):
        try:
            if self.learning==1:
                self.label_4.setText('학습중에는 안됩니다.')
                return
            if self.check_capture():
                return
            if self.model==False:
                self.label_4.setText("먼저 학습을 하셔야합니다.")
                return
            else:
                file_dialog = QFileDialog()
                file_dialog.setFileMode(QFileDialog.DirectoryOnly)
                file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
                count = 1
                if file_dialog.exec():
                    paths = file_dialog.selectedFiles()
                    path = paths[0]+"/motion_project"
                    try:
                        self.make_dir(path)
                    except:
                        count += 1
                        path = path + str(count)
                        try:
                            self.make_dir(path)
                        except:
                            count += 1
                            path = path[0:len(path)-1] + str(count)
                            try:
                                self.make_dir(path)
                            except:
                                count += 1
                                path = path[0:len(path)-1] + str(count)
                                try:
                                    self.make_dir(path)
                                except:
                                    count += 1
                                    path = path[0:len(path)-1] + str(count)
                                    try:
                                        self.make_dir(path)
                                    except:
                                        count += 1
                                        path = path[0:len(path)-1] + str(count)
                                        try:
                                            self.make_dir(path)
                                        except:
                                            count += 1
                                            path = path[0:len(path)-1] + str(count)
                                            try:
                                                self.make_dir(path)
                                            except:
                                                count += 1
                                                path = path[0:len(path)-1] + str(count)
                                                try:
                                                    self.make_dir(path)
                                                except:
                                                    count += 1
                                                    path = path[0:len(path)-1] + str(count)
                                                    try:
                                                        self.make_dir(path)
                                                    except:
                                                        count += 1
                                                        path = path[0:len(path)-1] + str(count)
                                                        try:
                                                            self.make_dir(path)
                                                        except:
                                                            count += 1
                                                            path = path[0:len(path)-1] + str(count)
                                                            try:
                                                                self.make_dir(path)
                                                            except:
                                                                self.label_4.setText("해당 경로의 다른 프로젝트를 지워주세요!")
                                                                return 'e'
                    self.pushButton_12.setText("학습시키기")
                    image_path = path+"/image"
                    image_file = np.asarray(self.image_data)
                    np.save(image_path,image_file)
                    name_path = path+"/name"
                    name_file = np.asarray(self.class_name)
                    np.save(name_path,name_file)
                    explain_path = path+"/explain"
                    explain_file = np.asarray(self.class_explain)
                    np.save(explain_path,explain_file)
                    coord_path = path+"/coord"
                    coord_file = np.asarray(self.train_coords)
                    np.save(coord_path,coord_file)
                    self.model = False
                    self.saved = 1
                    al = alam.Ui_Dialog('저장되었습니다.')
                    ala = al.showModal()
                    if ala:
                        return 'y'
        except BaseException as b:
            print(str(b))
            pass
    def make_dir(self,name):
        os.makedirs(name)
    def load_project(self):
        try:
            if self.learning==1:
                self.label_4.setText('학습중에는 안됩니다.')
                return
            if self.check_capture():
                self.label_4.setText('캡처중에는 불러올수 없습니다.')
                return
            if self.connect == 1:
                self.label_4.setText('EV3 연결중에는 안됩니다.')
                return
            if self.saved ==0:
                tt = train_alam.Ui_Dialog('현재 프로젝트를\n저장 하시겠습니까?')
                aa = tt.showModal()
                if aa:
                    r= self.save_project()
                    if r=='e':
                        return
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.DirectoryOnly)
            file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
    
            if file_dialog.exec():
                paths = file_dialog.selectedFiles()
                try:
                    if self.preview==1:
                        self.t1.stop_learning()
                    image_data = np.load(paths[0]+"/image.npy",allow_pickle=True).tolist()
                    class_name = np.load(paths[0]+"/name.npy",allow_pickle=True).tolist()
                    class_explain = np.load(paths[0]+"/explain.npy",allow_pickle=True).tolist()
                    train_coords = np.load(paths[0]+"/coord.npy",allow_pickle=True).tolist()
                except BaseException as b:
                    print(str(b))    
                    self.label_4.setText("선택한 프로젝트에 파일이 없거나\n프로젝트가 아닙니다.")
                    return
                
                self.image_data = image_data
                self.class_name = class_name
                self.class_explain = class_explain
                self.train_coords = train_coords
                
                try:
                    self.class_image = self.image_data[0]
                    self.class_coords = self.train_coords[0]
                    self.menu_show_event()
                    self.capture_checked = 0
                    self.while_count = 0
                    self.table_row = 0
                    self.table_column = 6
                    self.saved = 1
                    self.class_count = len(self.image_data)
                    self.current_class = 1
                    self.clicked_label_position = []
                    self.preview = 0
                    self.label.setText(self.class_name[0])
                    self.textEdit.setText(self.class_explain[0])
                    self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"장")
                    self.pushButton_12.setText("학습하러 가기")
                    for step in range(len(self.class_image)):
                        color_swapped_image = cv2.cvtColor(self.class_image[step], cv2.COLOR_BGR2RGB)
                        qt_image1 = QtGui.QImage(color_swapped_image.data,
                                                     self.program_width*0.09,
                                                     self.program_height*0.09,
                                                     color_swapped_image.strides[0],
                                                     QtGui.QImage.Format_RGB888)
                        capture_label = QtWidgets.QLabel()
                        qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                        pixmap = QtGui.QPixmap(qt_image1)
                        capture_label.setPixmap(pixmap)
                        capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
            "border-style:solid;\n"
            "border-color:white;\n")
                        if step%6!=0:
                            self.table.setCellWidget(self.table_row-1,step%6,capture_label)
                        else:
                            self.table_row = self.table_row + 1
                            self.table.setRowCount(self.table_row)
                            self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                            self.table.setCellWidget(self.table_row-1,0,capture_label)
                    self.table.scrollToBottom()
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((len(self.class_name)-1)*self.program_height*0.08)))
                except BaseException as b:
                    print(str(b))
                self.label.setReadOnly(True)
                self.textEdit.setReadOnly(True)
                self.frame_22.hide()
                self.frame_23.show()
        except BaseException as b:
            print(str(b))
    def new_project(self):
        try:
            if self.capture_checked:
                return
            if self.saved ==0:
                tt = train_alam.Ui_Dialog('현재 프로젝트를\n저장 하시겠습니까?')
                aa = tt.showModal()
                if aa:
                    r= self.save_project()
                    if r=='e':
                        return
            if self.preview:
                self.t1.stop_learning()
                self.frame_22.hide()
                self.frame_23.show()
            
            if self.connect:
                self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                self.connect = 0
                self.ev3.close()
                self.ev3 = None
            self.frame_2.hide()
            self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                              "image:url('./image/menu_icon.png')")
            self.pushButton.move(self.program_width*0.02,self.program_width*0.02)
            self.menu_clicked = 0
            self.capture_checked = 0
            self.while_count = 0
            self.table_row = 0
            self.table_column = 6
            self.class_count = 1
            self.current_class = 1
            self.class_image = []
            self.image_data = []
            self.saved = 1
            self.ev3 = None
            self.connect = 0
            self.connect_count = 0
            self.class_name = []
            self.mm = None
            self.class_explain = []
            self.train_coords = []
            self.class_coords = []
            self.clicked_label_position = []
            self.preview = 0
            self.table.clearContents()
            self.label_2.setText("CLASS_1")
            self.pushButton_2.setText("프로젝트 불러오기")
            self.pushButton_3.setText("프로젝트 저장하기")
            self.pushButton_4.setText("메인메뉴로 이동")
            self.pushButton_8.setText("사  진  촬  영")
            self.pushButton_9.setText("이미지 불러오기")
            self.pushButton_10.setText("이미지 삭제하기")
            self.pushButton_11.setText("클래스 삭제하기")
            self.pushButton_12.setText("학습하러가기")
            self.pushButton_13.setText("종료하기")
            self.label_6.setText("클래스 이름")
            self.label_7.setText("클래스 설명")
            self.label.setText("CLASS_1")
            self.label_5.setText("알 림 판")
            self.textEdit.setText("")
            self.frame_22.hide()
            self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1))
            self.frame_23.show()
            self.label_4.setText('새로운 프로젝트입니다.')
        except BaseException as b:
            print(str(b))
            
class ML_class(QtCore.QThread):
    
    finish_signal = QtCore.pyqtSignal(list)
    error_signal = QtCore.pyqtSignal()
    process_signal = QtCore.pyqtSignal(int)
    predict_signal = QtCore.pyqtSignal(list)
    
    def __init__(self,train_data,val_data,train_label,val_label,learning_rate,batch_size,epoch,class_count,learning_count):
        super().__init__()
        self.model = None
        self.train_data = train_data
        self.val_data = val_data
        self.train_label = train_label
        self.val_label = val_label
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epoch_size = epoch
        self.class_count = class_count
        self.receive=1
        self.learning_history = None
        self.br = 0
        self.learning_count = learning_count
        self.data = None
        
    def stop_learning(self):
        self.br = 1
        
    def receive_data(self,data):
        if self.receive==0:
            self.receive+=1
            self.data = data
        
    def run(self):
        self.X=None
        self.x=None
        self.Y=None
        self.W1=None
        self.W2=None
        self.W3=None
        self.L1=None
        self.L2=None
        self.b=None
        self.hypothesis=None
        self.cost=None
        self.optimizer=None
        self.sess=None
        self.keep_prob = tf.placeholder(tf.float32)
        try:
            self.X = tf.placeholder(tf.float32, [None,6,17,1])
            self.x = tf.reshape(self.X,[-1,6,17,1])
            self.Y = tf.placeholder(tf.float32, [None,self.class_count]) 
            self.W1 = tf.Variable(tf.random_normal([3,3,1,16], stddev=0.1))
            self.L1 = tf.nn.conv2d(self.x, self.W1, strides=[1,2,2,1], padding='SAME') 
            self.L1 = tf.nn.relu(self.L1)
            self.L1 = tf.nn.max_pool(self.L1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
            self.L1 = tf.nn.dropout(self.L1, keep_prob=self.keep_prob)
            self.W2 = tf.Variable(tf.random_normal([3,3,16,32], stddev = 0.1))
            self.L2 = tf.nn.conv2d(self.L1, self.W2, strides=[1,2,2,1], padding='SAME')
            self.L2 = tf.nn.relu(self.L2)
            self.L2 = tf.nn.max_pool(self.L2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
            self.W3 = tf.Variable(tf.random_normal([3,3,32,64], stddev = 0.1))
            self.L3 = tf.nn.conv2d(self.L2, self.W3, strides=[1,2,2,1], padding='SAME')
            self.L3 = tf.nn.relu(self.L3)
            self.L3 = tf.nn.max_pool(self.L3, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
            self.L3 = tf.nn.dropout(self.L3, keep_prob=self.keep_prob)
            self.L3 = tf.reshape(self.L3, [-1,1*1*64])
            self.W4 = tf.get_variable("w"+str(self.learning_count),[1*1*64,self.class_count])
            self.b = tf.Variable(tf.random_normal([self.class_count]))
            self.hypothesis = tf.matmul(self.L3, self.W4) + self.b
            self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.hypothesis, labels=self.Y))
            self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
            self.sess = tf.Session()
            self.sess.run(tf.global_variables_initializer())
            acc = []
            val_acc = []
            loss = []
            val_loss = []
            for step in range(self.epoch_size):
                total_batch = int(len(self.train_data) / self.batch_size)
                a_cost = 0
                for i in range(total_batch):
                    batch_xs = self.train_data[i:((i+1)*self.batch_size)]
                    batch_ys = self.train_label[i:((i+1)*self.batch_size)]
                    feed_dict = {self.X: batch_xs, self.Y: batch_ys, self.keep_prob:0.8}
                    c, _, = self.sess.run([self.cost,self.optimizer], feed_dict=feed_dict)
                    a_cost += c/total_batch
                    process = int(100*((step*total_batch)+(i+1))/(self.epoch_size*total_batch))
                    self.process_signal.emit(process)
                correct_prediction = tf.equal(tf.argmax(self.hypothesis, 1), tf.arg_max(self.Y, 1))
                accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
                temp = self.sess.run(accuracy,feed_dict={self.X: self.train_data, self.Y:self.train_label, self.keep_prob:1})
                acc.append(temp)
                loss.append(a_cost)
                temp2 = self.sess.run(accuracy,feed_dict={self.X: self.val_data, self.Y:self.val_label, self.keep_prob:1})
                b_cost = self.sess.run(self.cost,feed_dict={self.X: self.val_data, self.Y:self.val_label, self.keep_prob:1})
                val_acc.append(temp2)
                val_loss.append(b_cost)
                
            his = []
            his.append(acc)
            his.append(val_acc)
            his.append(loss)
            his.append(val_loss)
            self.finish_signal.emit(his)
        except BaseException as b:
            print(str(b))
            self.error_signal.emit()
            return
        self.receive = 0
        while True:
            if self.br == 1:
                break
            else:
                if self.receive==1:
                    predict = self.sess.run(tf.nn.softmax(logits=self.hypothesis),feed_dict={self.X:self.data, self.keep_prob:1})
                    predict = predict.tolist()
                    self.predict_signal.emit(predict)
                    self.receive = 0
        
