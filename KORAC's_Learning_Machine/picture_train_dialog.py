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
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/45)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.22,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/45)
        self.label_9.setFont(font)
        self.label_9.setText("")
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.lineEdit_3 = QtWidgets.QLabel(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.31,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/45)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.4,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/45)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_4.setObjectName("휴먼엑스포")
        self.lineEdit_5 = QtWidgets.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(self.program_width*0.18,self.program_height*0.49,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
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
        font.setFamily("휴먼엑스포")
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
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/40))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_22 = QtWidgets.QLabel(self)
        self.label_22.setGeometry(QtCore.QRect(self.program_width*0.39,self.program_height*0.04,self.program_width*0.57,self.program_height*0.4))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
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
        font.setFamily("휴먼엑스포")
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
        font.setFamily("휴먼엑스포")
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_2.setGeometry(QtCore.QRect(self.program_width*0.01,self.program_height*0.07,self.program_width*0.19,self.program_height*0.05))
        self.radioButton_2.setStyleSheet("border:none;")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_3.setGeometry(QtCore.QRect(self.program_width*0.01,self.program_height*0.13,self.program_width*0.19,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setStyleSheet("border:none;")
        self.label_35 = QtWidgets.QLabel(self)
        self.label_35.setGeometry(QtCore.QRect(self.program_width*0.39,self.program_height*0.48,self.program_width*0.57,self.program_height*0.2))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
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
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.13,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.22,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/50)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.31,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/50)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self)
        self.pushButton_8.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.40,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/50)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self)
        self.pushButton_9.setGeometry(QtCore.QRect(self.program_width*0.04,self.program_height*0.49,self.program_width*0.13,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(self.program_height/50)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet("border:none;\n"
"text-align:left;")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self)
        self.pushButton_10.setGeometry(QtCore.QRect(self.program_width*0.1,self.program_height*0.6,self.program_width*0.15,self.program_height*0.05))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
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
        self.pushButton_2.setText("학습시키기")
        self.pushButton_3.setText("닫기")
        self.label_3.setText("224 * 224")
        self.radioButton.setText("좌우반전 이미지 추가")
        self.radioButton_2.setText("상하반전 이미지 추가")
        self.radioButton_3.setText("추가 없음")
        self.pushButton_4.setText("이미지 해상도")
        self.pushButton_5.setText("채널수")
        self.pushButton_6.setText("클래스 수")
        self.pushButton_7.setText("학습률")
        self.pushButton_8.setText("작업 수량")
        self.pushButton_9.setText("학습 횟수")
        self.pushButton_10.setText("이미지 추가")
        self.label_22.setText("단어를 클릭하시면 설명을 볼 수 있습니다.")
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
        text=" 이미지 해상도는 가로 *세로 픽셀 수이다.\n 여기서는 224*224로 고정이다."
        self.label_22.setText(text)
    def set_explain2(self):
        text=" 이미지 채널수이다.\n 각각 R,G,B를 의미한다.\n 여기서는 3채널로 고정이다."
        self.label_22.setText(text)
    def set_explain3(self):
        text=" 사진을 저장한 클래스의 갯수이다."
        self.label_22.setText(text)
    def set_explain4(self):
        text=" 학습을 진행하는 속도이다.\n 높으면 빠르게 진행하지만 불안해지고\n낮으면 천천히진행하지만 안정되게 학습한다."
        self.label_22.setText(text)
    def set_explain5(self):
        text=" 한번의 학습을 진행할때\n여러번의 작업으로 나누어서 진행한다.\n이 때 한번의 작업당 수행할 데이터량이다."
        self.label_22.setText(text)
    def set_explain6(self):
        text=" 몇번의 학습을 할 것인지에 대한 횟수이다."
        self.label_22.setText(text)
    def set_explain7(self):
        text=" 훈련용 이미지데이터 추가를 의미한다."  
        self.label_22.setText(text)
    def set_explain8(self):
        text=" 이미지데이터를 모델에 집어넣을 시 \n 랜덤으로 이미지를 변환을 시킨다."
        self.label_22.setText(text)

    def quit(self):
        self.reject()
            
    def showModal(self):
        return super().exec_()