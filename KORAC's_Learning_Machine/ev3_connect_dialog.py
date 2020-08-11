# -*- coding: euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
import serial
import train_alam
import ev3_message_converter

class Ui_Dialog(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.connect = 0
        self.ev3 = None
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi()
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.height = screen_height*0.3
        self.width = self.height*2
        self.setObjectName("Dialog")
        self.resize(self.width, self.height)
        border_px = int(2*1050/screen_height)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(self.width*0.02, self.height*0.02, self.width*0.96, self.height*0.1))
        self.label.setStyleSheet('border:none;')
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/35))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label_5")
        self.label.setText("��������� EV3 1���ϰ� �������ּ���.")
        self.line = QtWidgets.QLineEdit(self)
        self.line.setGeometry(QtCore.QRect(self.width*0.05, self.height*0.2, self.width*0.3, self.height*0.2))
        self.line.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/25))
        self.line.setFont(font)
        self.line.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(self.width*0.4, self.height*0.2, self.width*0.28, self.height*0.2))
        self.pushButton_4.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;\n")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/35))
        self.pushButton_4.setFont(font)
        self.pushButton_4.setText("�˻��ϱ�")
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(self.width*0.7, self.height*0.2, self.width*0.28, self.height*0.2))
        self.pushButton_5.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;\n")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/35))
        self.pushButton_5.setFont(font)
        self.pushButton_5.setText("�����ϱ�")
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(self.width*0.05, self.height*0.43, self.width*0.9, self.height*0.25))
        self.label_2.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;\n")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/55))
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.width*0.02, self.height*0.75, self.width*0.46, self.height*0.2))
        self.pushButton_2.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/50))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('Ȯ��')
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(self.width*0.52, self.height*0.75, self.width*0.46, self.height*0.2))
        self.pushButton_3.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/50))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setText('���')
        
        self.pushButton_4.clicked.connect(self.search_ev3)
        self.pushButton_5.clicked.connect(self.connect_ev3)
        self.pushButton_2.clicked.connect(self.check)
        self.pushButton_3.clicked.connect(self.rejected)
    def connect_ev3(self):
        if self.connect==1:
            self.label_2.setText("�̹� ����Ǿ����ϴ�.")
            return
        try:
            num = int(self.line.text())
            if num <= 0:
                self.label_2.setText("0���� ū ���ڸ� �־���մϴ�.")
                return
        except:
            self.label_2.setText("���ڸ� �Է��ؾ��մϴ�.")
            return
        try:
            self.ev3 = serial.Serial('COM'+str(num),timeout=3,write_timeout=3)
            s = ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', 'connect')
            self.ev3.write(s)
            self.connect = 1
            self.label_2.setText("����Ǿ����ϴ�.")
        except:
            self.label_2.setText('�߸��� ��Ʈ��ȣ�Դϴ�.')
            return
        
    def search_ev3(self):
        if self.connect==1:
            self.label_2.setText("�̹� ����Ǿ����ϴ�.")
            return
        self.label_2.setText("��ġ�� ã�� ���Դϴ�.")
        at = train_alam.Ui_Dialog('������� ����� ��ġ�� ã�µ�\n10�ʿ��� 1�������� �ð��� �ҿ�˴ϴ�.\n�����Ͻðڽ��ϱ�?\n(EV3�� �������ּž��մϴ�.)')
        ata = at.showModal()
        if ata:
            available = []
            for i in range(256):
                try:
                    self.ev3 = serial.Serial('COM'+str(i),timeout = 3, write_timeout = 3)
                    s = ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', 'connect')
                    self.ev3.write(s)
                    available.append(self.ev3.portstr)
                    self.ev3.close()   
                except serial.SerialException:
                    pass
            if len(available)==1:
                try:
                    self.label_2.setText("����� ��ġ�� ã�ҽ��ϴ�.")
                    self.ev3 = serial.Serial(available[0])
                    self.connect = 1
                    self.line.setReadOnly(True)
                    self.line.setText(available[0])
                except:
                    pass
            elif len(available)>1:    
                self.label_2.setText('2�� �̻��� ��ġ�� ����Ǿ��ֽ��ϴ�.\n1���� EV3�� ������ �ּ���.')
                return
            else:
                self.label_2.setText('�޼����� ������ �� �ִ� ��ġ�� �����ϴ�.\n������� ���� �����ϰ� �ٽ� �������ּ���.\n�ݵ�� PC���� ������� ��û�� �������մϴ�.')
                return
        else:
            self.label_2.setText("")
            
    def check(self):
        try:
            if self.connect == 1:
                self.accept()
            else:
                self.label_2.setText("���� ��ġ�� �����ؾ��մϴ�.")
                return
        except BaseException as b:
            print(b)
    def rejected(self):
        self.reject()
        
    def showModal(self):
        return super().exec_()

        
