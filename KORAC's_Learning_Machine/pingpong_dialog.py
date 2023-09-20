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
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/70))
        self.label.setFont(font)
        self.label.setText("1. AI�� ���带 �ŵ��ϸ� �������ӿ� ���Ͽ� ���ϴ�.\n    AI�� ���� ���±����� ���ӿ� ���Ͽ� �н��� �ϰ� ���� ���尡 ���۵˴ϴ�.\n   (1����� �����ϰ� �����Դϴ�.)\n\n"
                           "2. 'w'Ű�� ������ �г��� ���� �ö󰡰�, 's'Ű�� ������ �г��� �Ʒ��� �������ϴ�.\n\n"
                           "3. �÷��̾ �г��� �����̴� ���¿��� ���� �ĳ���\n   ���� ������ �ĳ��������� �� �������� �����Դϴ�.\n\n"
                           "4. ���� ������ 'x+'���� �������� �ð�������� �þ�ϴ�.\n\n"
                           "5. ��ǥ�� ���� ���� 0, ���� �Ʒ��� 683�Դϴ�.\n\n"
                           "6. ���� �ӵ��� �ð��� �������� �������� ���尡 ���� �����ϸ� �ʱ�ȭ�˴ϴ�.\n\n"
                           "7. �� AI���� �������� �̱�� �ִ��� �����غ�����!!")
        
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.width*0.27, self.height*0.85, self.width*0.46, self.height*0.1))
        self.pushButton_2.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/35))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('Ȯ ��')
        
        font = QtGui.QFont()
        font.setFamily("�޸տ�����")
        font.setPointSize(int(self.width/35))
        
        self.pushButton_2.clicked.connect(self.check)
        
    def check(self):
        self.accept()
        
    def showModal(self):
        return super().exec_()

