# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import train_alam
import ctypes

class Ui_Dialog(QtWidgets.QDialog):
    
    def __init__(self,sound_data):
        super().__init__()
        self.sound_data = sound_data
        self.count = 0
        self.train_data = []
        self.train_label = []
        self.val_data = []
        self.val_label = []
        self.learning = 0
        self.sound_count = 0
        self.model = None
        self.val_count = 0
        self.train_count = 0
        self.label_arr = []
        self.batch_size = 0
        self.history = None
        self.error = None
        for step in range(len(self.sound_data)):
            self.sound_count += len(self.sound_data[step])
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
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.31,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(self.program_height/45)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
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

        self.pushButton_2.setText("�н� �غ��ϱ�")
        self.label_9.setText(str(len(self.sound_data)))
        self.label_5.setText("1")
        self.lineEdit_3.setText("0.0001")
        self.lineEdit_4.setText("16")
        self.lineEdit_5.setText("100")
        self.pushButton_3.setText("�ݱ�")
        self.label_3.setText("16000hz")
        self.pushButton_4.setText("���ø� ���ļ�")
        self.pushButton_5.setText("ä�μ�")
        self.pushButton_6.setText("Ŭ���� ��")
        self.pushButton_7.setText("�н���")
        self.pushButton_8.setText("�۾� ����")
        self.pushButton_9.setText("�н� Ƚ��")
        self.label_22.setText("�ܾ Ŭ���Ͻø� ������ �� �� �ֽ��ϴ�.")
        
        self.pushButton_4.clicked.connect(self.set_explain1)
        self.pushButton_5.clicked.connect(self.set_explain2)
        self.pushButton_6.clicked.connect(self.set_explain3)
        self.pushButton_7.clicked.connect(self.set_explain4)
        self.pushButton_8.clicked.connect(self.set_explain5)
        self.pushButton_9.clicked.connect(self.set_explain6)
        self.pushButton_2.clicked.connect(self.start_learning)
        self.pushButton_3.clicked.connect(self.quit)
        
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    
    def start_learning(self):
        self.train_data = []
        self.train_label = []
        self.val_data = []
        self.val_label = []
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
        if self.sound_count<self.batch_size:
                self.label_35.setText("�۾� ������ �̹��� ������ �����ϴ�.")
                return
        self.accept()
        
    def set_explain1(self):
        text=" ���ø� ���ļ��� �����ð�(2��)�� ���ø� Ƚ���� �ǹ��Ѵ�."
        self.label_22.setText(text)
    def set_explain2(self):
        text=" ���������� ä�μ��̴�.\n 1�̹Ƿ� ����ä���̴�."
        self.label_22.setText(text)
    def set_explain3(self):
        text=" �Ҹ��� ������ Ŭ������ �����̴�."
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

    def quit(self):
        self.reject()
            
    def showModal(self):
        return super().exec_()
