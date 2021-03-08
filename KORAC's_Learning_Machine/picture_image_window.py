# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import custom_widgets as cw
import cv2
import numpy as np
from PyQt5.Qt import QFileDialog
from custom_widgets import ImageViewer
import picture_train_dialog
global image
import ctypes
import os
import train_alam,alam
import ev3_connect_dialog
import matplotlib
matplotlib.use("Qt5AGG")
import matplotlib.pyplot as plt
import ev3_message_converter
import tensorflow as tf
class Ui_MainWindow(QtWidgets.QMainWindow):
    
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)
    MessageSignal = QtCore.pyqtSignal(int)

    def __init__(self,m_window):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.setWindowTitle("   ")
        self.menu_clicked = 0
        self.m_window = m_window
        self.capture_checked = 0
        self.while_count = 0
        self.table_row = 0
        self.table_column = 6
        self.t1 = None
        self.learning = 0
        self.class_count = 1
        self.current_class = 1
        self.class_image = []
        self.image_data = []
        self.class_name = []
        self.class_explain = []
        self.clicked_label_position = []
        self.preview = 0
        self.model = False
        self.quit_clicked = False
        self.path=None
        self.saved = 1
        self.ev3 = None
        self.connect  = 0
        self.connect_count = 0
        self.send_point = 95
        self.msg = 0
            
        self.setupUi()
    def set_cam(self):
        self.quit_clicked = False
        try:
            self.setCursor(QtCore.Qt.BusyCursor)
            self.label_4.setText('��ٷ��ּ���. �غ����Դϴ�.')
            self.cam = cv2.VideoCapture(0)
            if self.program_width*0.34 < 480:
                self.cam.set(3,640) 
                self.cam.set(4,480)
            else:
                self.cam.set(3,960)
                self.cam.set(4,540)
        except BaseException as b:
            print(str(b))
            self.label_4.setText("ķ�� ã�� ���߽��ϴ�.")
            
        try:
            _, image = self.cam.read()
            self.height, self.width = image.shape[:2]
        except BaseException as b:
            print(str(b))
            self.label_4.setText("ķ�� ������ �ֽ��ϴ�.")
        
        try:
            self.VideoSignal1.connect(self.cam_viewer1.setImage)
            self.VideoSignal2.connect(self.cam_viewer2.setImage)
            self.MessageSignal.connect(self.send_msg_ev3)
            self.label_4.setText('�غ� �Ϸ�Ǿ����ϴ�.')
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.show_video()
        except BaseException as b:
            print(str(b))
            self.label_4.setText("ķ�� �ñ׳��� ������ϴ�. ��������ּ���.")
            
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
        self.border_px = int((2/1020)*screen_height)
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
        self.pushButton_29 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_29.setGeometry(QtCore.QRect(0, self.program_height*0.2, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_29.setFont(font)
        self.pushButton_29.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_29.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(0, self.program_height*0.3, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(0, self.program_height*0.4, self.program_width*0.3, self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_13.setFont(font)
        self.pushButton_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_13.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(self.program_width*0.48, self.program_height*0.03, self.program_width*0.44, self.program_height*0.06))
        self.label_2.setStyleSheet("background-color: rgb(194, 194, 194);border-style:solid;border-color:white;border-width:"+str(self.border_px)+"px;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_width/60))
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color:black;\n"
                                   "color:white;")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label = QtWidgets.QLineEdit(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.36+self.program_height*0.17, self.program_width*0.36, self.program_width*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_width/60))
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color:black;\n"
                                   "color:white;")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.36+self.program_height*0.32, self.program_width*0.36, self.program_width*0.2))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
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
        
        self.line = QtWidgets.QLineEdit(self.frame_22)
        self.line.setGeometry(QtCore.QRect(self.program_width*0.3, self.program_height*0.89, self.program_width*0.05, self.program_height*0.03))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
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
        self.pushButton_15.setText("EV3 �����ϱ�")
        
        self.frame_4 = QtWidgets.QFrame(self.frame_22)
        self.frame_4.setGeometry(QtCore.QRect(0, self.program_height*0.57, self.program_width*0.36, self.program_height*0.32))
        self.frame_4.setStyleSheet("background-color: black;")
        self.la_1 = QtWidgets.QLabel(self.frame_4)
        self.la_1.setGeometry(QtCore.QRect(0,0,self.program_width*0.095, self.program_height*0.038))
        self.la_1.setAlignment(QtCore.Qt.AlignCenter)
        self.la_1.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_1.setText("1�� Ŭ����")
        self.la_1.setFont(font)
        self.la_2 = QtWidgets.QLabel(self.frame_4)
        self.la_2.setGeometry(QtCore.QRect(0,self.program_height*0.038,self.program_width*0.095, self.program_height*0.038))
        self.la_2.setAlignment(QtCore.Qt.AlignCenter)
        self.la_2.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_2.setText("2�� Ŭ����")
        self.la_2.setFont(font)
        self.la_3 = QtWidgets.QLabel(self.frame_4)
        self.la_3.setGeometry(QtCore.QRect(0,self.program_height*0.076,self.program_width*0.095, self.program_height*0.038))
        self.la_3.setAlignment(QtCore.Qt.AlignCenter)
        self.la_3.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_3.setText("3�� Ŭ����")
        self.la_3.setFont(font)
        self.la_4 = QtWidgets.QLabel(self.frame_4)
        self.la_4.setGeometry(QtCore.QRect(0,self.program_height*0.114,self.program_width*0.095, self.program_height*0.038))
        self.la_4.setAlignment(QtCore.Qt.AlignCenter)
        self.la_4.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_4.setText("4�� Ŭ����")
        self.la_4.setFont(font)
        self.la_5 = QtWidgets.QLabel(self.frame_4)
        self.la_5.setGeometry(QtCore.QRect(0,self.program_height*0.152,self.program_width*0.095, self.program_height*0.038))
        self.la_5.setAlignment(QtCore.Qt.AlignCenter)
        self.la_5.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_5.setText("5�� Ŭ����")
        self.la_5.setFont(font)
        self.la_6 = QtWidgets.QLabel(self.frame_4)
        self.la_6.setGeometry(QtCore.QRect(0,self.program_height*0.190,self.program_width*0.095, self.program_height*0.038))
        self.la_6.setAlignment(QtCore.Qt.AlignCenter)
        self.la_6.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_6.setText("6�� Ŭ����")
        self.la_6.setFont(font)
        self.la_7 = QtWidgets.QLabel(self.frame_4)
        self.la_7.setGeometry(QtCore.QRect(0,self.program_height*0.228,self.program_width*0.095, self.program_height*0.038))
        self.la_7.setAlignment(QtCore.Qt.AlignCenter)
        self.la_7.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_7.setText("7�� Ŭ����")
        self.la_7.setFont(font)
        self.la_8 = QtWidgets.QLabel(self.frame_4)
        self.la_8.setGeometry(QtCore.QRect(0,self.program_height*0.266,self.program_width*0.095, self.program_height*0.038))
        self.la_8.setAlignment(QtCore.Qt.AlignCenter)
        self.la_8.setStyleSheet("background-color:black;\n"
                           "color:white;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/75))
        self.la_8.setText("8�� Ŭ����")
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
        self.progress_label.setGeometry(QtCore.QRect(self.program_width*1.03,self.program_height*0.88,self.program_width*0.34,self.program_height*0.08))
        self.progress_label.setStyleSheet(
            "font-size:"+str(int(self.program_height/55))+"pt;"
            "background-color:black;\n"
            "color:white;"
            )
        self.progress_label.setText("�н� ���Դϴ�. ��ٷ��ּ���.")
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
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
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
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/55))
        self.pushButton_12.setFont(font)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.84, self.program_width*0.56, self.program_height*0.04))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/50))
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: black;\n"
"color:white;")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(self.program_width*0.42, self.program_height*0.88, self.program_width*0.56, self.program_height*0.11))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
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


        self.label_2.setText("CLASS_1")
        self.pushButton_2.setText("������Ʈ �ҷ�����")
        self.pushButton_3.setText("������Ʈ �����ϱ�")
        self.pushButton_4.setText("���θ޴��� �̵�")
        self.pushButton_8.setText("��  ��  ��  ��")
        self.pushButton_9.setText("�̹��� �ҷ�����")
        self.pushButton_10.setText("�̹��� �����ϱ�")
        self.pushButton_11.setText("Ŭ���� �����ϱ�")
        self.pushButton_12.setText("�н��Ϸ�����")
        self.pushButton_13.setText("�����ϱ�")
        self.label_6.setText("Ŭ���� �̸�")
        self.label_7.setText("Ŭ���� ����")
        self.label.setText("CLASS_1")
        self.label_5.setText("�� �� ��")
        self.textEdit.setText("")
        self.pushButton_29.setText("�� ������Ʈ")
        
        self.frame_2.hide()
        
        self.line.textChanged.connect(self.line_set_accuracy)
        self.slider.valueChanged.connect(self.slider_set_accuracy)
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
        self.pushButton_15.clicked.connect(self.connect_ev3)
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
                    self.ev3 = dda.ev3
                    self.pushButton_15.setText("EV3 �������")
                    self.connect = 1
            else:
                self.connect = 0
                self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                self.ev3.close()
                self.pushButton_15.setText("EV3 �����ϱ�")
                self.ev3 = None
        except BaseException as b:
            print(str(b))
    def move_class_1(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            try:
                if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>1:
                    self.image_data.append(self.class_image)
                    if self.label.text()=="":
                        self.class_name.append("CLASS_"+str(self.current_class))
                    else:
                        self.class_name.append(self.label.text())
                    self.class_explain.append(self.textEdit.toPlainText())
                elif self.current_class >1 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
                elif self.current_class != 1:
                    self.image_data[self.current_class-1]=self.class_image
                    if self.label.text()=="":
                        self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                    else:
                        self.class_name[self.current_class-1]=self.label.text()
                    self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
                else:
                    return
                self.current_class=1
                self.class_image=self.image_data[self.current_class-1]
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
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
            except BaseException as b:
                print(str(b))
        except BaseException as b:
            print(str(b))
    def move_class_2(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>2:
                self.image_data.append(self.class_image)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >2 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 2:
                self.image_data[self.current_class-1]=self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=2
            self.class_image=self.image_data[self.current_class-1]
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
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def move_class_3(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>3:
                self.image_data.append(self.class_image)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >3 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 3:
                self.image_data[self.current_class-1]=self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=3
            self.class_image=self.image_data[self.current_class-1]
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
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def move_class_4(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>4:
                self.image_data.append(self.class_image)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >4 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 4:
                self.image_data[self.current_class-1]=self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=4
            self.class_image=self.image_data[self.current_class-1]
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
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def move_class_5(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>5:
                self.image_data.append(self.class_image)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >5 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 5:
                self.image_data[self.current_class-1]=self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=5
            self.class_image=self.image_data[self.current_class-1]
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
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def move_class_6(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>6:
                self.image_data.append(self.class_image)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >6 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 6:
                self.image_data[self.current_class-1]=self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=6
            self.class_image=self.image_data[self.current_class-1]
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
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def move_class_7(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>7:
                self.image_data.append(self.class_image)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class >7 and len(self.class_image)==0:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
            elif self.current_class != 7:
                self.image_data[self.current_class-1]=self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=7
            self.class_image=self.image_data[self.current_class-1]
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
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def move_class_8(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==len(self.image_data)+1 and len(self.class_image)>0 and self.current_class>8:
                self.image_data.append(self.class_image)
                if self.label.text()=="":
                    self.class_name.append("CLASS_"+str(self.current_class))
                else:
                    self.class_name.append(self.label.text())
                self.class_explain.append(self.textEdit.toPlainText())
            elif self.current_class != 8:
                self.image_data[self.current_class-1]=self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1]="CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1]=self.label.text()
                self.class_explain[self.current_class-1]=self.textEdit.toPlainText()
            else:
                return
            self.current_class=8
            self.class_image=self.image_data[self.current_class-1]
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
            self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
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
                self.label_4.setText("Ŭ�����̸��� 16���̳��� �ۼ����ּ���")
                self.label.setText("")
                return
        except BaseException as b:
            print(str(b))
            
    @QtCore.pyqtSlot()        
    def error_learning(self):
        try:
            self.label_4.setText('�н����� ������ �߻��߽��ϴ�.\n �ٽ����ּ���.')
            self.progress_bar.hide()
            self.progress_label.hide()
            self.frame_23.show()
            self.learning -= 1
            self.pushButton_12.setText("�н��Ϸ�����")
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
            self.label_4.setText('�н��� �Ϸ�Ǿ����ϴ�.')
            self.pushButton_12.setText("���� ����")
        except BaseException as b:
            print(str(b)) 
    @QtCore.pyqtSlot(int)        
    def learning_process(self,num):        
        self.progress_bar.setValue(num)
    def go_image_learning(self):
        try:
            if self.check_capture():
                return
            if len(self.image_data) <= 1 and len(self.class_image)==0:
                self.label_4.setText('Ŭ������ 2�� �̻��̾�� �մϴ�.')
                return
            if self.learning==1:
                self.learning -=1
                self.t1.stop_learning()
                self.progress_bar.hide()
                self.progress_label.hide()
                self.pushButton_12.setText("�н��Ϸ� ����")
                self.frame_23.show()
                return
            if not self.preview:
                if self.current_class==len(self.image_data)+1 and len(self.class_image)>0:
                
                    self.image_data.append(self.class_image)
                    if self.label.text() == "":
                        self.class_name.append("CLASS_"+str(self.current_class))
                    else:
                        self.class_name.append(self.label.text())
                    self.class_explain.append(self.textEdit.toPlainText())
                for step in range(len(self.image_data)):
                    if len(self.image_data[step]) < 24:
                        self.label_4.setText("�̹����� 24�� �̻��̾�� �մϴ�.\n"
                                         "���� CLASS_"+str(step+1)+" -> "+str(len(self.image_data[step]))+"��")
                        return
                dialog = picture_train_dialog.Ui_Dialog(self.image_data)
                m = dialog.showModal()
                if m:
                    self.learning += 1
                    self.frame_23.hide()
                    self.progress_bar.setValue(0)
                    self.progress_label.show()
                    self.label_4.setText('�н��� �Դϴ�.')
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
                    self.pushButton_12.setText("�н� ��ҽ�Ű��")
                    self.saved = 0
                    self.t1 = ML_class(td,vd,tl,vl,le,ba,ep,ca)
                    self.t1.finish_signal.connect(self.finish_learning)
                    self.t1.process_signal.connect(self.learning_process)
                    self.t1.error_signal.connect(self.error_learning)
                    self.t1.predict_signal.connect(self.receive_function)
                    self.t1.start()
            else:
                tt = train_alam.Ui_Dialog('���� ������Ʈ��\n���� �Ͻðڽ��ϱ�?')
                aa = tt.showModal()
                if aa:
                    r= self.save_project()
                    if r=='e':
                        return
                else:
                    self.saved = 1
                self.preview = self.preview-1
                self.label.setReadOnly(False)
                self.textEdit.setReadOnly(False)
                self.t1.stop_learning()
                self.frame_22.hide()
                self.frame_23.show()
                if self.connect == 1:
                    self.connect = 0
                    self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                    self.ev3.close()
                    self.ev3 = None
                self.pushButton_12.setText("�н��Ϸ�����")
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
            if len(self.clicked_label_position)==0:
                self.label_4.setText("���õ� �̹����� �����ϴ�.\n"
                                    "������� �̹����� Ŭ�����ּ���")
                return
            else:
                self.clicked_label_position.sort()
                for step in range(len(self.clicked_label_position)):
                    self.class_image.pop(self.clicked_label_position[step][0]*6+self.clicked_label_position[step][1]-step)
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
                if len(self.class_image)==0:
                    self.delete_class()
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
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
                    
                    label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                    self.table.setCellWidget(row,col,label)
                else:        
                    label = self.table.cellWidget(row, col)
                    label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:red;\n")
                    self.table.setCellWidget(row,col,label)
                    self.clicked_label_position.append([row,col])
            else:
                if len(self.clicked_label_position) > 0:
                    for step in range(len(self.clicked_label_position)):
                        item = self.table.cellWidget(self.clicked_label_position[step][0], self.clicked_label_position[step][1])
                        item.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
    "border-style:solid;\n"
    "border-color:white;\n")
                        self.table.setCellWidget(self.clicked_label_position[step][0], self.clicked_label_position[step][1],item)
                    self.clicked_label_position = []
                else:
                    return
        except BaseException as b:
            print(str(b))    
    def open_image(self):
        try:
            if self.check_capture():
                return
            if self.check_previewed():
                return
            
            images = []
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
                    for step in range(len(paths)):
                        try:
                            stream = open( paths[step].encode("utf-8") , "rb")
                            bytes = bytearray(stream.read())
                            numpyArray = np.asarray(bytes, dtype=np.uint8)
                            img = cv2.imdecode(numpyArray , cv2.IMREAD_UNCHANGED)
                            if img.shape[-1]>3:
                                self.label_4.setText("�̹���ä�μ��� �����ϴ�.\n"
                                                     "jpg���Ϸ� ��ȯ���ּ���")
                                return
                            elif img.shape[-1]<3:
                                self.label_4.setText("�÷��̹����� �����մϴ�.")
                                return
                            img = cv2.resize(img,dsize=(224,224),interpolation=cv2.INTER_CUBIC)
                            images.append(img)
                        except BaseException as b:
                            print(str(b))
                            self.label_4.setText("�̹����� �ƴ� ������ �ֽ��ϴ�.")
                            return
                    for step in range(len(images)):
                        self.class_image.append(images[step])
                        height, width = images[step].shape[:2]
                        color_swapped_image = cv2.cvtColor(images[step], cv2.COLOR_BGR2RGB)
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
                        if (len(self.class_image)-1)%6!=0:
                            self.table.setCellWidget(self.table_row-1,(len(self.class_image)-1)%6,capture_label)
                        else:
                            self.table_row = self.table_row + 1
                            self.table.setRowCount(self.table_row)
                            self.table.setRowHeight(self.table_row-1,self.program_height*0.09)
                            self.table.setCellWidget(self.table_row-1,0,capture_label)
                        self.table.scrollToBottom()
                    self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def delete_class(self):
        try:
            if self.check_capture():
                return
            if self.check_previewed():
                return
            if self.current_class == len(self.image_data)+1:
                self.table.clearContents()
                self.table_row = 0
                self.class_image = []
                self.while_count = 0
                self.clicked_label_position = []
                self.label.setText("CLASS_"+str(self.current_class))
                self.textEdit.setText("")
                self.label_2.setText("CLASS_"+str(self.current_class))
            else:
                self.image_data.pop(self.current_class-1)
                self.class_name.pop(self.current_class-1)
                self.class_explain.pop(self.current_class-1)
                self.clicked_label_position = []
                if self.current_class == len(self.image_data)+1:
                    self.table.clearContents()
                    self.class_image = []
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
                    self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
        except BaseException as b:
            print(str(b))
    def go_next_class(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if len(self.image_data)>self.current_class:
                self.clicked_label_position = []
                self.image_data[self.current_class-1] = self.class_image
                if self.label.text()=="":
                    self.class_name[self.current_class-1] = "CLASS_"+str(self.current_class)
                else:
                    self.class_name[self.current_class-1] = self.label.text()
                self.class_explain[self.current_class-1] = self.textEdit.toPlainText()
                self.table_row=0
                self.table.clearContents()
                self.while_count=0
                self.class_image = []
                self.class_image = self.image_data[self.current_class]
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
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
            else:
                if self.current_class == 8:
                    self.label_4.setText("Ŭ������ 8������ �����Ҽ� �ֽ��ϴ�.")
                    return
                self.clicked_label_position = []
                if self.current_class==len(self.image_data)+1 and len(self.class_image)>0:
                    self.table.clearContents()
                    self.image_data.append(self.class_image)
                    self.class_image=[]
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
                    self.class_name[self.current_class-1] = self.label.text()
                    self.class_explain[self.current_class-1] = self.textEdit.toPlainText()
                    if self.label.text()=="":
                        self.label.setText("CLASS_"+str(self.current_class))
                    self.table.clearContents()
                    self.while_count=0
                    self.table_row = 0
                    self.class_image = []
                    self.current_class = self.current_class+1
                    self.label.setText("CLASS_"+str(self.current_class))
                    self.textEdit.setText("")
                    self.label_2.setText("CLASS_"+str(self.current_class))
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-1)*self.program_height*0.08)))
                else:
                    self.label_4.setText("���� Ŭ������ �̹����� �־���մϴ�.")
                    return
        except BaseException as b:
            print(str(b))
    def go_pre_class(self):
        try:
            if self.check_capture():
                return
            if self.label.text()=="":
                self.label_4.setText("Ŭ������ �̸��� �����ּž� �մϴ�.")
                return
            if self.current_class==1:
                self.label_4.setText("ù��° Ŭ�����Դϴ�.")
                return
            else:
                self.clicked_label_position = []
                if len(self.class_image)>0:
                    if self.current_class==len(self.image_data)+1:
                        self.image_data.append(self.class_image)
                        if self.label.text()=="":
                            self.class_name.append("CLASS_"+str(self.current_class))
                        else:
                            self.class_name.append(self.label.text())
                        self.class_explain.append(self.textEdit.toPlainText())
                    else:
                        self.image_data[self.current_class-1] = self.class_image
                        self.class_name[self.current_class-1] = self.label.text()
                        self.class_explain[self.current_class-1] = self.textEdit.toPlainText()
                else:
                    self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1+((self.current_class-2)*self.program_height*0.08)))
                self.current_class = self.current_class-1
                self.table.clearContents()
                self.table_row=0
                self.while_count=0
                self.class_image=[]
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
                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
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
        while True:
            try:
                if not self.quit_clicked:
                    ret, frame = self.cam.read()
                    if ret:
                        frame = cv2.flip(frame,1)
                        height,width = frame.shape[:2]
                        frame = cv2.resize(frame,dsize=(int(width*(self.program_width*0.34)/height),int(self.program_width*0.34)))
                        height,width = frame.shape[:2]
                        start_width = int((width-(self.program_width*0.34))/2)
                        frame = frame[:,start_width:int(start_width+(self.program_width*0.34)),:]
                        color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        qt_image1 = QtGui.QImage(color_swapped_image.data,
                                                self.program_width*0.34,
                                                self.program_width*0.34,
                                                color_swapped_image.strides[0],
                                                QtGui.QImage.Format_RGB888)
                        if not self.preview:
                            self.VideoSignal1.emit(qt_image1)
                        else:
                            self.VideoSignal1.emit(qt_image1)
                            qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.3,self.program_width*0.3))
                            self.VideoSignal2.emit(qt_image1)
                            frame = cv2.resize(frame,dsize=(224,224),interpolation=cv2.INTER_AREA)
                            frame = (np.asarray(frame, dtype=np.float32) / 127.0) - 1
                            frame = frame.reshape((1,224,224,3))
                            self.t1.receive_data(frame)
                        if self.capture_checked:
                            if self.while_count%2==0:
                                frame = cv2.resize(frame,dsize=(224,224),interpolation=cv2.INTER_AREA)
                                self.class_image.append(frame)
                                capture_label = QtWidgets.QLabel()
                                qt_image1 = qt_image1.scaled(QtCore.QSize(self.program_width*0.09,self.program_height*0.09))
                                pixmap = QtGui.QPixmap(qt_image1)
                                capture_label.setPixmap(pixmap)
                                capture_label.setStyleSheet("border-width:"+str(self.border_px*1.5)+"px;\n"
            "border-style:solid;\n"
            "border-color:white;\n")
                                self.append_table(capture_label)
                                self.while_count = self.while_count+1
                                self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
                            else:
                                self.while_count = self.while_count+1
                                
                        loop = QtCore.QEventLoop()
                        QtCore.QTimer.singleShot(10, loop.quit)
                        loop.exec_()
                else:
                    self.MessageSignal.disconnect(self.send_msg_ev3)
                    self.VideoSignal2.disconnect(self.cam_viewer2.setImage)
                    self.VideoSignal1.disconnect(self.cam_viewer1.setImage)
                    self.cam.release()
                    break
            except BaseException as b:
                continue
    def menu_show_event(self):
        try:
            if self.capture_checked:
                self.label_4.setText("���� �Կ� �߿��� �ٸ� ���� �� �� �����ϴ�!!")
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
            self.model = False
            self.pushButton.setStyleSheet("background-color:rgb(190, 190, 190);\n"
                                              "image:url('./image/menu_icon.png')")
            self.pushButton.move(self.program_width*0.02,self.program_width*0.02)
            self.menu_clicked = 1 - self.menu_clicked
            self.quit_clicked = True
            if self.connect == 1:
                self.connect = 0
                self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                self.ev3.close()
                self.ev3=None
            self.hide()
            self.m_window.show()
        except BaseException as b:
            print(str(b))
    def exit(self):
        try:
            if self.learning==1:
                self.label_4.setText('�н��߿��� �ȵ˴ϴ�.')
                return
            if self.saved ==0:
                tt = train_alam.Ui_Dialog('���� ������Ʈ��\n���� �Ͻðڽ��ϱ�?')
                aa = tt.showModal()
                if aa:
                    r= self.save_project()
                    if r=='e':
                        return
            self.model = False
            self.quit_clicked=True
            if self.connect == 1:
                self.connect = 0
                self.ev3.write(ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', '0'))
                self.ev3.close()
                self.ev3 = None
            self.close()
        except BaseException as b:
            print(str(b))
    def capture_image(self):
        try:
            if self.check_previewed():
                return
            self.capture_checked = 1 - self.capture_checked
            if self.capture_checked:
                self.pushButton_8.setText("��  ��  ��  ��  ��  ��")
            else:
                self.pushButton_8.setText("��  ��  ��  �� ")
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
                self.label_4.setText("���� �Կ� �߿��� �ٸ� ���� �� �� �����ϴ�!!")
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
                self.label_4.setText("���� �߿��� �Ҽ� �����ϴ�.")
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
            if self.check_capture():
                return
            if self.learning==1:
                self.label_4.setText("�н��߿��� �ȵ˴ϴ�.")
                return
            if self.model==False:
                self.label_4.setText("���� �н��� �ϼž��մϴ�.")
                return
            else:
                file_dialog = QFileDialog()
                file_dialog.setFileMode(QFileDialog.DirectoryOnly)
                file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
                count = 1
                if file_dialog.exec():
                    paths = file_dialog.selectedFiles()
                    path = paths[0]+"/image_project"
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
                                                                self.label_4.setText("�ش� ����� �ٸ� ������Ʈ�� �����ּ���!")
                                                                return 'e'
                    image_path = path+"/image"
                    image_file = np.asarray(self.image_data)
                    np.save(image_path,image_file)
                    self.model=False
                    name_path = path+"/name"
                    name_file = np.asarray(self.class_name)
                    np.save(name_path,name_file)
                    explain_path = path+"/explain"
                    explain_file = np.asarray(self.class_explain)
                    np.save(explain_path,explain_file)
                    self.saved = 1
                    al = alam.Ui_Dialog('����Ǿ����ϴ�.')
                    ala = al.showModal()
                    if ala:
                        return 'y'
        except BaseException as b:
            print(str(b))
    def make_dir(self,name):
        os.makedirs(name)
    def load_project(self):
        try:
            if self.learning==1:
                self.label_4.setText('�н��߿��� �ȵ˴ϴ�.')
                return
            if self.check_capture():
                self.label_4.setText('���� �Կ��߿��� �ҷ��� �� �����ϴ�.')
                return
            if self.connect == 1:
                self.label_4.setText('EV3 �����߿��� �ȵ˴ϴ�.')
                return
            if self.saved ==0:
                tt = train_alam.Ui_Dialog('���� ������Ʈ��\n���� �Ͻðڽ��ϱ�?')
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
                if self.preview==1:
                    self.t1.stop_learning()
                try:
                    image_data = np.load(paths[0]+"/image.npy",allow_pickle=True).tolist()
                    class_name = np.load(paths[0]+"/name.npy",allow_pickle=True).tolist()
                    class_explain = np.load(paths[0]+"/explain.npy",allow_pickle=True).tolist()
                except:
                    self.label_4.setText("������ ������Ʈ�� ������ ���ų�\n������Ʈ�� �ƴմϴ�.")
                    return
                self.image_data = image_data
                self.class_name = class_name
                self.model = False
                self.class_explain = class_explain
                
                try:
                    self.class_image = self.image_data[0]
                    self.menu_show_event()
                    self.capture_checked = 0
                    self.while_count = 0
                    self.table_row = 0
                    self.table_column = 6
                    self.class_count = len(self.image_data)
                    self.current_class = 1
                    self.clicked_label_position = []
                    self.preview = 0
                    self.saved=1
                    self.label.setText(self.class_name[0])
                    self.textEdit.setText(self.class_explain[0])
                    self.label_2.setText("CLASS_"+str(self.current_class)+" -> "+str(len(self.class_image))+"��")
                    self.pushButton_12.setText("�н��Ϸ� ����")
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
            if self.learning==1:
                self.label_4.setText('�н��߿��� �ȵ˴ϴ�.')
                return
            if self.capture_checked:
                return
            if self.saved ==0:
                tt = train_alam.Ui_Dialog('���� ������Ʈ��\n���� �Ͻðڽ��ϱ�?')
                aa = tt.showModal()
                if aa:
                    r= self.save_project()
                    if r=='e':
                        return
            self.model = False
            if self.preview:
                self.preview = 0
                self.frame_22.hide()
                self.frame_23.show()
                self.t1.stop_learning()
            
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
            self.saved = 1
            self.ev3 = None
            self.connect = 0
            self.connect_count = 0
            self.class_image = []
            self.image_data = []
            self.class_name = []
            self.class_explain = []
            self.clicked_label_position = []
            self.preview = 0
            self.model = None
            self.quit_clicked = False
            self.path=None
            self.table.clearContents()
            self.pushButton_31.setText('CLASS_1')
            self.pushButton_32.setText('CLASS_2')
            self.pushButton_33.setText('CLASS_3')
            self.pushButton_34.setText('CLASS_4')
            self.pushButton_35.setText('CLASS_5')
            self.pushButton_36.setText('CLASS_6')
            self.pushButton_37.setText('CLASS_7')
            self.pushButton_38.setText('CLASS_8')
            self.label_2.setText("CLASS_1")
            self.pushButton_2.setText("������Ʈ �ҷ�����")
            self.pushButton_3.setText("������Ʈ �����ϱ�")
            self.pushButton_4.setText("���θ޴��� �̵�")
            self.pushButton_8.setText("��  ��  ��  ��")
            self.pushButton_9.setText("�̹��� �ҷ�����")
            self.pushButton_10.setText("�̹��� �����ϱ�")
            self.pushButton_11.setText("Ŭ���� �����ϱ�")
            self.pushButton_12.setText("�н��Ϸ�����")
            self.pushButton_13.setText("�����ϱ�")
            self.label_6.setText("Ŭ���� �̸�")
            self.label_7.setText("Ŭ���� ����")
            self.label.setText("CLASS_1")
            self.label_5.setText("�� �� ��")
            self.textEdit.setText("")
            self.frame_22.hide()
            self.frame_23.resize(QtCore.QSize(self.program_width*0.36,self.program_height*0.1))
            self.frame_23.show()
            self.label_4.setText('���ο� ������Ʈ�Դϴ�.')
        except BaseException as b:
            print(str(b))
            
class ML_class(QtCore.QThread):#학습 및 예측을 위한 서브 스레드-> QThread 상속을 받아 구현
    
    #pyqt5의 경우 스레드간의 통신을 할때 시그널과 슬롯을 이용하여 진행한다.(기본적으로 이벤트에도 사용)
    #시그널(메세지)을 보내는 스레드에서는 시그널의 종류와 데이터 타입을 정의 
    #로직을 수행하는 중 신호를 보내야할때 emit() 메서드를 사용하여 수신측에 메세지 전달
    #신호를 받는 쪽에서는 해당 시그널을 받을 함수(메서드)를 정의. 송신측의 시그널이 정의가 되면 해당 시그널과 수신메서드를 connect() 메서드를 사용하여 연결한다. ->  기본적인 이벤트와 동작방식과 비슷하다.

    finish_signal = QtCore.pyqtSignal(list) #학습 완료 시그널. 메인 스레드에서 해당 시그널을 받는 메서드는 finish_learning() -> 해당 시그널이 수신되면 예측을 위한 Preview 화면을 띄운다.
    error_signal = QtCore.pyqtSignal() #에러 시그널. 학습도중 에러가 발생하면 해당 시그널을 내보낸다. 메인스레드에서 해당 시그널을 받는 메서드는 error_learning() -> 해당 시그널이 수신되면 학습이 취소되며, 서브스레드는 종료.        
    process_signal = QtCore.pyqtSignal(int) #(새롭게 수정한 코드에서는 사용하지 않음)진행 시그널. 학습진행률을 내보내는 시그널. 메인스레드에서 해당 시그널을 받는 메서드는 learning_process() -> 해당 시그널이 수신되면 progress_bar의 값이 바뀜.
    predict_signal = QtCore.pyqtSignal(list) #예측 시그널. preivew화면이 띄어지고난 후 메인스레드에서 보내는 image data를 학습한 모델을 거쳐 예측값을 산출하고, 메인스레드로 반환 ->
                                             #메인스레드에서 해당 시그널을 받는 메서드는 receive_function() -> 해당 시그널이 도착하면 preiview layout내의 progress_bar의 값을 변환.
    
    def __init__(self,train_data,val_data,train_label,val_label,learning_rate,batch_size,epoch,class_count):#constructor
        super().__init__()
        self.model = None #모델을 담는 변수
        self.train_data = train_data # 훈련데이터를 담는 변수
        self.val_data = val_data # 평가데이터를 담는 변수
        self.train_label = train_label # 훈련 라벨을 담는 변수 
        self.val_label = val_label # 평가 라벨을 담는 변수
        self.learning_rate = learning_rate # 학습률
        self.batch_size = batch_size # 작업수량
        self.epoch_size = epoch # 학습횟수
        self.class_count = class_count # 클래스 수량
        self.receive=1 # preview 화면이 띄어졌을시 메인스레드에서 보낸 이미지가 존재하는지를 확인하기 위한 변수
        self.learning_history = None # 학습이 진행되는 동안의 history를 담는 변수
        self.br = 0  #서브스레드를 종료시키기위한 변수
        self.data = None #메인스레드로부터 받은 image data를 담기위한 변수
        
    def stop_learning(self):#해당 메서드가 호출되면 서브스레드 종료
        self.br = 1 
        
    def get_model(self):#모델을 저장하기위한 메서드
        return self.model
    
    def receive_data(self,data):#메인스레드에서 이미지 전송시 해당 메서드로 전송
        if self.receive==0:
            self.receive+=1
            self.data = data
    
        
    def run(self):#핵심 메서드. start() 메서드호출시 해당 메서드가 불러와진다.
        try:
            #데이터를 ndarray로 바꾸는 과정. data shape은 샘플 하나당 (224,224,3)
            self.train_data = np.asarray(self.train_data, dtype= np.float32)
            self.train_label = np.asarray(self.train_label, dtype = np.float32)
            self.val_data = np.asarray(self.val_data, dtype = np.float32)
            self.val_label = np.asarray(self.val_label, dtype = np.float32)
            
            otmz = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)#optimizer선언 -> Adam optimizer사용. 현재까지는 가장 발전된 optimizer가 Adam으로 알고 있음. 이 전단계가 RMSprop
            IMG_SHAPE = (224, 224, 3)
            base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE, #mobilenetV2
                                               include_top=False, #해당 파라미터는 위에 fully-connected-layer를 포함시킬지의 여부를 선택, False시 제일 위의 layer가 Input layer가 됨.
                                               weights='imagenet')
            base_model.trainable = True #mobilenetV2를 추가 학습이 가능하게끔 함.
            
            global_average_layer = tf.keras.layers.GlobalAveragePooling2D() #pooling layer선언
            prediction_layer = tf.keras.layers.Dense(self.class_count,activation='softmax') # fully-connected-layer선언
            
            self.model = tf.keras.Sequential([ #모델 생성
                      base_model,
                      global_average_layer,
                      prediction_layer
                    ])
            
            self.model.compile(optimizer=otmz, #모델 컴파일 -> optimizer, 손실함수, trace를 위한 metrics값 설정.
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
            # 그래프를 그리기위하여 self.history에 담긴 변수를 분류하기 위한 변수들
            acc = []
            val_acc = []
            loss = []
            val_loss = []
            # 이미지데이터를 시각적으로 변화시키기위한 ImageDataGenerator 객체선언
            datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                featurewise_center=True,
                featurewise_std_normalization=True,
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                horizontal_flip=True)
          
            datagen.fit(self.train_data)#훈련데이터를 위에서 선언한 ImageDataGenerator를 사용하여 시각적으로 변화시킴.
            
            earlystop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=1, mode='min',baseline=0.001)#조기종료를 위한 earlystop객체 선언(추적할 변수,조건을 만족한 후 학습을 더 수행할 횟수, 추적할 값이 커지는지 작아지는지에 대한 설정값, 학습을 멈출 추적대상의 값) 
                                                                                                                   #-> val_loss값을 추적하여 해당 값이 0.001이하일시 한번 더 학습을 수행하고 종료
            #모델 학습
            self.learning_history = self.model.fit_generator(datagen.flow(self.train_data, self.train_label, batch_size=self.batch_size), validation_data=(self.val_data,self.val_label),callbacks=[earlystop],steps_per_epoch=len(self.train_data) / self.batch_size, epochs=self.epoch_size)
            #학습한 history를 변수별로 분류하여 담음(그래프를 그리기위한 조치)
            acc.append(self.learning_history.history['accuracy'])
            val_acc.append(self.learning_history.history['val_accuracy'])
            loss.append(self.learning_history.history['loss'])
            val_loss.append(self.learning_history.history['val_loss'])
            
            '''
            for e in range(self.epoch_size):
                batches = 0
                for x_batch, y_batch in datagen.flow(self.train_data, self.train_label, batch_size=self.batch_size,shuffle=True):
                    self.learning_history = self.model.fit(x = x_batch, y = y_batch, validation_data=(self.val_data,self.val_label))
                    acc.append(self.learning_history.history['acc'][0])
                    val_acc.append(self.learning_history.history['val_acc'][0])
                    loss.append(self.learning_history.history['loss'][0])
                    val_loss.append(self.learning_history.history['val_loss'][0])
                    process = int(100*((e*len(self.train_data)/self.batch_size)+(batches+1))/(self.epoch_size*len(self.train_data)/self.batch_size))
                    self.process_signal.emit(process)
                    batches += 1
                    if batches >= len(self.train_data) / self.batch_size or len(x_batch)<self.batch_size:
                   
                        break
          
            bt = len(self.train_data)//self.batch_size
            for step in range(self.epoch_size):
                for step2 in range(bt):
                    if self.br==1:
                        return
                    else:
                        td = self.train_data[(step2*self.batch_size):((step2+1)*self.batch_size)]
                        tl = self.train_label[(step2*self.batch_size):((step2+1)*self.batch_size)]
                    
                    
                        self.learning_history = self.model.fit(x = td, y = tl, validation_data=(self.val_data,self.val_label))
                        acc.append(self.learning_history.history['acc'][0])
                        val_acc.append(self.learning_history.history['val_acc'][0])
                        loss.append(self.learning_history.history['loss'][0])
                        val_loss.append(self.learning_history.history['val_loss'][0])
                        process = int(100*((step*bt)+(step2+1))/(self.epoch_size*bt))
                        self.process_signal.emit(process)'''
            his = []
            his.append(acc)
            his.append(val_acc)
            his.append(loss)
            his.append(val_loss)
            
            self.finish_signal.emit(his)#학습완료 학습완료 시그널 송신
        except BaseException as b:
            print(str(b))
            self.error_signal.emit()#에러발생시 에러 시그널 송신
            return
        self.receive = 0 #메인스레드로부터 예측을 위한 이미지데이터 수신준비
        while True:
            if self.br == 1:#해당스레드 종료
                break
            else:
                if self.receive==1:
                    predict = self.model.predict(self.data)#학습한 모델을 사용하여 클래스 예측
                    predict = predict.tolist()
                    self.predict_signal.emit(predict)#예측 시그널 송신
                    self.receive = 0 #메인스레드로부터 예측을 위한 이미지데이터 수신준비
        
        
        
