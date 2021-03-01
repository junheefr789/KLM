# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import matplotlib.pyplot as plt
import random
import ctypes

class Ui_Dialog(QtWidgets.QDialog):
    
    def __init__(self,image_data):
        super().__init__()
        self.image_data = image_data
        self.train_data = []
        self.train_label = []
        self.val_data = []
        self.val_label = []
        self.learning = 0
        self.image_count = 0
        self.model = None
        self.val_count = 0
        self.train_count = 0
        self.label_arr = []
        self.batch_size = 0
        self.history = None
        self.error = None
        for step in range(len(self.image_data)):
            self.image_count += len(self.image_data[step])
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi()
    
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.program_height = screen_height * 0.5
        self.program_width = self.program_height * 1.7
        border_px = int(2/1050*screen_height)
        self.setObjectName("Dialog")
        self.resize(self.program_width, self.program_height)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.13,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/45)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.22,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/45)
        self.label_9.setFont(font)
        self.label_9.setText("")
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.lineEdit_3 = QtWidgets.QLabel(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.31,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/45)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.4,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/45)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_4.setObjectName("�޸տ�����")
        self.lineEdit_5 = QtWidgets.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.49,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/45)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.program_width*0.59,self.program_height*0.76,self.program_width*0.18,self.program_height*0.15))
        self.pushButton_2.setStyleSheet("background-color:rgb(98, 86, 236);\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/40))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(self.program_width*0.79,self.program_height*0.76,self.program_width*0.18,self.program_height*0.15))
        self.pushButton_3.setStyleSheet("background-color:rgb(255, 94, 79);\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/40))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_22 = QtWidgets.QLabel(self)
        self.label_22.setGeometry(QtCore.QRect(self.program_width*0.39,self.program_height*0.04,self.program_width*0.57,self.program_height*0.4))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/40))
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("border-style:solid;\n"
"border-color:black;\n"
"border-width:"+str(border_px)+"px;")
        self.label_22.setText("")
        self.label_22.setObjectName("label_22")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.04,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.program_height/45))
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(self.program_width*0.07,self.program_height*0.67,self.program_width*0.21,self.program_height*0.2))
        self.frame_2.setStyleSheet("border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.radioButton = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton.setGeometry(QtCore.QRect(self.program_width*0.01,self.program_height*0.01,self.program_width*0.19,self.program_height*0.05))
        self.radioButton.setStyleSheet("border:none;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_2.setGeometry(QtCore.QRect(self.program_width*0.01,self.program_height*0.07,self.program_width*0.19,self.program_height*0.05))
        self.radioButton_2.setStyleSheet("border:none;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_3.setGeometry(QtCore.QRect(self.program_width*0.01,self.program_height*0.13,self.program_width*0.19,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setStyleSheet("border:none;")
        self.label_35 = QtWidgets.QLabel(self)
        self.label_35.setGeometry(QtCore.QRect(self.program_width*0.39,self.program_height*0.48,self.program_width*0.57,self.program_height*0.2))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/40)
        self.label_35.setFont(font)
        self.label_35.setStyleSheet("color:red;\n"
                                    "border-style:solid;\n"
                                    "border-width:"+str(border_px)+"px;\n"
                                    "border-color:black;")
        self.label_35.setText("")
        self.label_35.setAlignment(QtCore.Qt.AlignCenter)
        self.label_35.setObjectName("label_35")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.04,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.13,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.22,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/50)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.31,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/50)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self)
        self.pushButton_8.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.40,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/50)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self)
        self.pushButton_9.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.49,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/50)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self)
        self.pushButton_10.setGeometry(QtCore.QRect(self.program_width*0.1,self.program_height*0.6,self.program_width*0.15,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/50)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_10.setStyleSheet("border:none;\n"
"")
        self.pushButton_10.setObjectName("pushButton_10")

        self.label_9.setText(str(len(self.image_data)))
        self.label_5.setText("3")
        self.lineEdit_3.setText("0.001")
        self.lineEdit_4.setText("16")
        self.lineEdit_5.setText("50")
        self.pushButton_2.setText("�н���Ű��")
        self.pushButton_3.setText("�ݱ�")
        self.label_3.setText("224 * 224")
        self.radioButton.setText("�¿���� �̹��� �߰�")
        self.radioButton_2.setText("���Ϲ��� �̹��� �߰�")
        self.radioButton_3.setText("�߰� ����")
        self.pushButton_4.setText("�̹��� �ػ�")
        self.pushButton_5.setText("ä�μ�")
        self.pushButton_6.setText("Ŭ���� ��")
        self.pushButton_7.setText("�н���")
        self.pushButton_8.setText("�۾� ����")
        self.pushButton_9.setText("�н� Ƚ��")
        self.pushButton_10.setText("�̹��� �߰�")
        self.label_22.setText("�ܾ Ŭ���Ͻø� ������ �� �� �ֽ��ϴ�.")
        self.radioButton_3.setChecked(True)
        
        self.pushButton_4.clicked.connect(self.set_explain1)
        self.pushButton_5.clicked.connect(self.set_explain2)
        self.pushButton_6.clicked.connect(self.set_explain3)
        self.pushButton_7.clicked.connect(self.set_explain4)
        self.pushButton_8.clicked.connect(self.set_explain5)
        self.pushButton_9.clicked.connect(self.set_explain6)
        self.pushButton_10.clicked.connect(self.set_explain7)
        self.pushButton_2.clicked.connect(self.start_learning)
        self.pushButton_3.clicked.connect(self.quit)
        
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    
    def start_learning(self):
        self.train_data = []
        self.train_label = []
        self.val_data = []
        self.val_label = []
        self.label_arr=[]
        try:
            self.learning_rate = float(self.lineEdit_3.text())
            if self.learning_rate <=0:
                self.label_35.setText("�н����� 0���� Ŀ���մϴ�.")
                return
        except:
            self.label_35.setText("�н����� ���ڸ� ���� �� �ֽ��ϴ�.\n"
                                  "�Ҽ����� 8�ڸ����� �־��ּ���")
            return        
        try:
            self.batch_size = int(self.lineEdit_4.text())
            if self.batch_size <= 0:
                self.label_35.setText("�۾� ������ 1���� ������ �ȵ˴ϴ�.")
                return
        except:
            self.label_35.setText("�۾� ������ ���ڸ� ���� �� �ֽ��ϴ�.")
            return        
        try:
            self.epoch_size = int(self.lineEdit_5.text())
            if self.epoch_size <= 0:
                self.label_35.setText("�н� Ƚ���� 1���� ������ �ȵ˴ϴ�.")
                return
        except:
            self.label_35.setText("�н� Ƚ���� ���ڸ� ���� �� �ֽ��ϴ�.")
            return
        if self.image_count<self.batch_size:
                self.label_35.setText("�۾� ������ �̹��� ������ �����ϴ�.")
                return
        try:
            for step in range(len(self.image_data)):
                self.count = step + 1
                self.train_count = int(len(self.image_data[step])*0.8)+1
                self.val_count = len(self.image_data[step]) - self.train_count
                for t1 in range(self.train_count):
                    self.train_data.append((self.image_data[step][t1]/127.0) -1)
                for v1 in range(self.val_count):
                    self.val_data.append((self.image_data[step][v1+self.train_count]/127.0) -1)
                    self.val_label.append(step)
                self.label_arr.append(self.train_count)
                
            for st in range(len(self.label_arr)):
                for st2 in range(self.label_arr[st]):
                    self.train_label.append(st)
        
            
            for step in range(len(self.train_data)):
                num = random.randint(0,len(self.train_data)-1)
                a = self.train_data[step]
                b = self.train_label[step]
                self.train_data[step] = self.train_data[num]
                self.train_label[step] = self.train_label[num]
                self.train_data[num] = a
                self.train_label[num] = b
                
                    
            self.accept()
            
        except BaseException as b:
            print(str(b))
    def set_explain1(self):
        text=" �̹��� �ػ󵵴� ���� *���� �ȼ� ���̴�.\n ���⼭�� 224*224�� �����̴�."
        self.label_22.setText(text)
    def set_explain2(self):
        text=" �̹��� ä�μ��̴�.\n ���� R,G,B�� �ǹ��Ѵ�.\n ���⼭�� 3ä�η� �����̴�."
        self.label_22.setText(text)
    def set_explain3(self):
        text=" ������ ������ Ŭ������ �����̴�."
        self.label_22.setText(text)
    def set_explain4(self):
        text=" �н��� �����ϴ� �ӵ��̴�.\n ������ ������ ���������� �Ҿ�������\n������ õõ������������ �����ǰ� �н��Ѵ�."
        self.label_22.setText(text)
    def set_explain5(self):
        text=" �ѹ��� �н��� �����Ҷ�\n�������� �۾����� ����� �����Ѵ�.\n�� �� �ѹ��� �۾��� ������ �����ͷ��̴�."
        self.label_22.setText(text)
    def set_explain6(self):
        text=" ����� �н��� �� �������� ���� Ƚ���̴�."
        self.label_22.setText(text)
    def set_explain7(self):
        text=" �Ʒÿ� �̹��������� �߰��� �ǹ��Ѵ�."  
        self.label_22.setText(text)
    def set_explain8(self):
        text=" �̹��������͸� �𵨿� ������� �� \n �������� �̹����� ��ȯ�� ��Ų��."
        self.label_22.setText(text)

    def quit(self):
        self.reject()
            
    def showModal(self):
        return super().exec_()
