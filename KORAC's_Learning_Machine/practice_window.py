from PyQt5 import QtCore, QtGui, QtWidgets
import picture_image_window
import sound_learning_window
import motion_learning_window
import ctypes

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,m_window):
        super().__init__()
        self.m_window = m_window
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.image_motion_window = None
        self.picture_image_window = None
        self.mic_sound_window = None
        self.setupUi()
        self.image_menu()
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.setWindowIcon(QtGui.QIcon('./image/logo.png'))
        self.program_height = screen_height*0.8
        self.program_width = self.program_height*1.5
        self.setObjectName("MainWindow")
        self.setFixedSize(self.program_width, self.program_height)
        self.setWindowTitle("  ")
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, self.program_width, self.program_height))
        oImage = QtGui.QImage('./image/main_image.png')
        oImage = oImage.scaled(QtCore.QSize(self.program_width, self.program_height))
        self.label.setPixmap(QtGui.QPixmap(oImage))
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.02, self.program_width*0.08, self.program_width*0.04))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_pt = int(self.program_width/55)
        self.pushButton_3.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";"
"color:white;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(self.program_width*0.9, self.program_width*0.02, self.program_width*0.08, self.program_width*0.04))
        self.pushButton_4.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color:white;\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";")
        self.pushButton_4.setText("")
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(self.program_width*0.4, self.program_height*0.1, self.program_width*0.1, self.program_height*0.06))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_pt = int(self.program_width/85)
        self.pushButton.setStyleSheet("border:none;\n"
"border-top-left-radius:20px;\n"
"border-top-right-radius:20px;\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";"
"background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(self.program_width*0.5, self.program_height*0.1, self.program_width*0.1, self.program_height*0.06))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("border:none;\n"
"border-top-left-radius:20px;\n"
"border-top-right-radius:20px;\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";"
"background-color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(self.program_width*0.2, self.program_height*0.158, self.program_width*0.6, self.program_height*0.7))
        self.border_px = int((5/1050)*screen_height)
        self.listView.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-width:"+str(self.border_px)+"px;\n"
"border-radius:50px;")
        self.listView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listView.setObjectName("listView")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(self.program_width*0.225, self.program_height*0.17, self.program_width*0.55, self.program_height*0.15))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setCentralWidget(self.centralwidget)

        self.pushButton_3.setText("이전")
        self.pushButton_4.setText("종료")
        self.pushButton.setText("이미지")
        self.pushButton_2.setText("사운드")
        
        self.pushButton_3.clicked.connect(self.go_back)
        self.pushButton_4.clicked.connect(self.quit)
        self.pushButton.clicked.connect(self.image_menu)
        self.pushButton_2.clicked.connect(self.sound_menu)

        QtCore.QMetaObject.connectSlotsByName(self)
    
    def go_back(self):
        self.hide()
        self.m_window.show()
        
    def quit(self):
        self.close()
        
    def sound_menu(self):
        try:
            font_pt=int(self.program_width/85)
            self.listView.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
    "border-style:solid;\n"
    "border-color:rgb(170, 170, 255);\n"
    "border-width:"+str(self.border_px)+"px;\n"
    "border-radius:50px;")
            self.pushButton.setStyleSheet("border:none;\n"
    "font: "+str(font_pt)+"pt \"휴먼엑스포\";"
    "border-top-left-radius:20px;\n"
    "border-top-right-radius:20px;\n"
    "background-color: rgb(255, 255, 255);")
            self.pushButton_2.setStyleSheet("border:none;\n"
    "font: "+str(font_pt)+"pt \"휴먼엑스포\";"
    "border-top-left-radius:20px;\n"
    "border-top-right-radius:20px;\n"
    "background-color: rgb(170, 170, 255);")
            self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.pushButton.setCheckable(True)
            self.pushButton_2.setCheckable(False)
            while self.verticalLayout.count()>0:
                item = self.verticalLayout.takeAt(0)
                if not item:
                    continue
                it = item.widget()
                if it:
                    it.deleteLater()
            self.pushButton_7 = QtWidgets.QPushButton(self.verticalLayoutWidget)
            self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            font_pt = int(self.program_width/50)
            self.pushButton_7.setStyleSheet(
                '''
                QPushButton{border:none;background-color: rgba(0, 0, 0, 0);text-align:left;font: '''+str(font_pt)+'''pt \"휴먼엑스포\";color:white;}
                QPushButton:hover{color:rgb(170, 170, 255);}
                '''
                )
            self.pushButton_7.setText("1. 마이크를 활용한 소리학습")
            self.verticalLayout.addWidget(self.pushButton_7)
            self.pushButton_7.clicked.connect(self.connect_mic_sound_window)
        except BaseException as b:
            print(str(b))
    def image_menu(self):
        try:
            font_pt=int(self.program_width/85)
            self.listView.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
    "border-style:solid;\n"
    "border-color:rgb(255, 170, 255);\n"
    "border-width:"+str(self.border_px)+"px;\n"
    "border-radius:50px;")
            self.pushButton.setStyleSheet("border:none;\n"
    "font: "+str(font_pt)+"pt \"휴먼엑스포\";"
    "border-top-left-radius:20px;\n"
    "border-top-right-radius:20px;\n"
    "background-color: rgb(255, 170, 255);")
            self.pushButton_2.setStyleSheet("border:none;\n"
    "font: "+str(font_pt)+"pt \"휴먼엑스포\";"
    "border-top-left-radius:20px;\n"
    "border-top-right-radius:20px;\n"
    "background-color: rgb(255, 255, 255);")
            self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.pushButton.setCheckable(False)
            self.pushButton_2.setCheckable(True)
            while self.verticalLayout.count()>0:
                item = self.verticalLayout.takeAt(0)
                if not item:
                    continue
                it = item.widget()
                if it:
                    it.deleteLater()
            self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget)
            self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            font_pt = int(self.program_width/50)
            self.pushButton_5.setStyleSheet(
                '''
                QPushButton{border:none;background-color: rgba(0, 0, 0, 0);text-align:left;font: '''+str(font_pt)+'''pt \"휴먼엑스포\";color:white;}
                QPushButton:hover{color:rgb(255, 170, 255);}
                '''
                )
            self.pushButton_5.setObjectName("pushButton_5")
            self.pushButton_5.setText("1. 사진을 활용한 이미지 학습")
            self.verticalLayout.addWidget(self.pushButton_5)
            self.pushButton_6 = QtWidgets.QPushButton(self.verticalLayoutWidget)
            self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.pushButton_6.setStyleSheet(
                '''
                QPushButton{border:none;background-color: rgba(0, 0, 0, 0);text-align:left;font: '''+str(font_pt)+'''pt \"휴먼엑스포\";color:white;}
                QPushButton:hover{color:rgb(255, 170, 255);}
                '''
                )
            self.pushButton_6.setObjectName("pushButton_6")
            self.pushButton_6.setText("2. 사진을 활용한 포즈 학습")
            self.verticalLayout.addWidget(self.pushButton_6)
            self.pushButton_5.clicked.connect(self.connect_picture_image_window)
            self.pushButton_6.clicked.connect(self.connect_picture_motion_window)
        except BaseException as b:
            print(str(b))
    def connect_picture_image_window(self):
        try:
            self.pushButton_5.setCursor(QtCore.Qt.BusyCursor)
            self.hide()
            if self.picture_image_window == None:
                self.picture_image_window = picture_image_window.Ui_MainWindow(self.m_window)
            self.picture_image_window.show()
            self.picture_image_window.set_cam()
        except BaseException as b:
            print(str(b))
        
    def connect_picture_motion_window(self):
        try:
            self.pushButton_6.setCursor(QtCore.Qt.BusyCursor)
            self.hide()
            if self.image_motion_window == None:
                self.image_motion_window = motion_learning_window.Ui_MainWindow(self.m_window)
            self.image_motion_window.show()
            self.image_motion_window.set_cam()
        except BaseException as b:
            print(str(b))
    
    def connect_mic_sound_window(self):
        try:
            self.pushButton_7.setCursor(QtCore.Qt.BusyCursor)
            self.hide()
            if self.mic_sound_window == None:
                self.mic_sound_window = sound_learning_window.Ui_MainWindow(self.m_window)
            self.mic_sound_window.show()
            self.mic_sound_window.set_mic()
        except BaseException as b:
            print(str(b))