from PyQt5 import QtCore, QtGui, QtWidgets
import photo_synthesis_window
import ctypes
import pingpong_game_window

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,m_window):
        super().__init__()
        self.m_window = m_window
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.drawing_protrait_window = None
        self.age_gender_window = None
        self.pingpong_game_window = None
        self.photo_synthesis_window = None
        self.setupUi()
    
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
        
        font_pt=int(self.program_width/85)
        self.listView.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border-style:solid;\n"
"border-color:rgb(255, 170, 255);\n"
"border-width:"+str(self.border_px)+"px;\n"
"border-radius:50px;")
        self.pushButton_7 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_pt = int(self.program_width/50)
        self.pushButton_7.setStyleSheet(
            '''
            QPushButton{border:none;background-color: rgba(0, 0, 0, 0);text-align:left;font: '''+str(font_pt)+'''pt \"휴먼엑스포\";color:white;}
            QPushButton:hover{color:rgb(255, 170, 255);}
            '''
            )
        self.pushButton_7.setText("1. 핑퐁게임을 학습하는 AI")
        self.pushButton_8 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_pt = int(self.program_width/50)
        self.pushButton_8.setStyleSheet(
            '''
            QPushButton{border:none;background-color: rgba(0, 0, 0, 0);text-align:left;font: '''+str(font_pt)+'''pt \"휴먼엑스포\";color:white;}
            QPushButton:hover{color:rgb(255, 170, 255);}
            '''
            )
        self.pushButton_8.setText("2. 사진을 합성해주는 AI")
        self.verticalLayout.addWidget(self.pushButton_7)
        self.verticalLayout.addWidget(self.pushButton_8)

        self.pushButton_3.setText("이전")
        self.pushButton_4.setText("종료")
        
        self.pushButton_3.clicked.connect(self.go_back)
        self.pushButton_4.clicked.connect(self.quit)
        self.pushButton_7.clicked.connect(self.connect_pingpong)
        self.pushButton_8.clicked.connect(self.connect_photo)

        QtCore.QMetaObject.connectSlotsByName(self)
    
    def go_back(self):
        self.hide()
        self.m_window.show()
    def quit(self):
        self.close()
        
    def init_cursor(self):
        self.pushButton_7.setCursor(QtCore.Qt.ArrowCursor)
        self.pushButton_8.setCursor(QtCore.Qt.ArrowCursor)
    def connect_pingpong(self):
        try:
            self.pushButton_7.setCursor(QtCore.Qt.BusyCursor)
            self.hide()
            if self.pingpong_game_window == None:
                self.pingpong_game_window = pingpong_game_window.Ui_MainWindow(self)
            self.pingpong_game_window.show()
            self.pingpong_game_window.restart()
        except BaseException as b:
            print(str(b))
    def connect_photo(self):
        try:
            self.pushButton_8.setCursor(QtCore.Qt.BusyCursor)
            self.hide()
            if self.photo_synthesis_window == None:
                self.photo_synthesis_window  = photo_synthesis_window.Ui_MainWindow(self)
            self.photo_synthesis_window.show()
        except BaseException as b:
            print(str(b))