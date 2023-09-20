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
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/35))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label_5")
        self.label.setText("블루투스는 EV3 1대하고만 연결해주세요.")
        self.line = QtWidgets.QLineEdit(self)
        self.line.setGeometry(QtCore.QRect(self.width*0.05, self.height*0.2, self.width*0.3, self.height*0.2))
        self.line.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
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
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/35))
        self.pushButton_4.setFont(font)
        self.pushButton_4.setText("검색하기")
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(self.width*0.7, self.height*0.2, self.width*0.28, self.height*0.2))
        self.pushButton_5.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;\n")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/35))
        self.pushButton_5.setFont(font)
        self.pushButton_5.setText("연결하기")
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(self.width*0.05, self.height*0.43, self.width*0.9, self.height*0.25))
        self.label_2.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;\n")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
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
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/50))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('확인')
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(self.width*0.52, self.height*0.75, self.width*0.46, self.height*0.2))
        self.pushButton_3.setStyleSheet("background-color:white;\n"
                                         "border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(border_px)+"px;\n"
                                         "border-radius:"+str(border_px*10)+"px;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.width/50))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setText('취소')
        
        self.pushButton_4.clicked.connect(self.search_ev3)
        self.pushButton_5.clicked.connect(self.connect_ev3)
        self.pushButton_2.clicked.connect(self.check)
        self.pushButton_3.clicked.connect(self.rejected)
    def connect_ev3(self):
        if self.connect==1:
            self.label_2.setText("이미 연결되었습니다.")
            return
        try:
            num = int(self.line.text())
            if num <= 0:
                self.label_2.setText("0보다 큰 숫자를 넣어야합니다.")
                return
        except:
            self.label_2.setText("숫자만 입력해야합니다.")
            return
        try:
            self.ev3 = serial.Serial('COM'+str(num),timeout=3,write_timeout=3)
            s = ev3_message_converter.encodeMessage(ev3_message_converter.MessageType.Text, 'abc', 'connect')
            self.ev3.write(s)
            self.connect = 1
            self.label_2.setText("연결되었습니다.")
        except:
            self.label_2.setText('잘못된 포트번호입니다.')
            return
        
    def search_ev3(self):
        if self.connect==1:
            self.label_2.setText("이미 연결되었습니다.")
            return
        self.label_2.setText("장치를 찾는 중입니다.")
        at = train_alam.Ui_Dialog('블루투스 연결된 장치를 찾는데\n10초에서 1분정도의 시간이 소요됩니다.\n진행하시겠습니까?\n(EV3만 연결해주셔야합니다.)')
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
                    self.label_2.setText("연결된 장치를 찾았습니다.")
                    self.ev3 = serial.Serial(available[0])
                    self.connect = 1
                    self.line.setReadOnly(True)
                    self.line.setText(available[0])
                except:
                    pass
            elif len(available)>1:    
                self.label_2.setText('2개 이상의 장치가 연결되어있습니다.\n1대의 EV3만 연결해 주세요.')
                return
            else:
                self.label_2.setText('메세지를 전송할 수 있는 장치가 없습니다.\n블루투스 페어링을 삭제하고 다시 연결해주세요.\n반드시 PC에서 블루투스 요청을 보내야합니다.')
                return
        else:
            self.label_2.setText("")
            
    def check(self):
        try:
            if self.connect == 1:
                self.accept()
            else:
                self.label_2.setText("먼저 장치를 연결해야합니다.")
                return
        except BaseException as b:
            print(b)
    def rejected(self):
        self.reject()
        
    def showModal(self):
        return super().exec_()