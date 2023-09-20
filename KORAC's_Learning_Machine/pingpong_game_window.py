from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
import custom_widgets as cw
import math
import random
import time
import pingpong_alert,train_alam, pingpong_dialog
import numpy as np

class Ui_MainWindow(QtWidgets.QMainWindow):
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self,m_window):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.width_min = 0
        self.width_max = 0
        self.angle = 0
        self.round = 0
        self.t1 = None
        self.m_window = m_window
        self.model = None
        self.training_data = []
        self.label_data = []
        self.low_screen = 0
        self.setupUi()
        self.open_dialog()
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.setWindowIcon(QtGui.QIcon('./image/logo.png'))
        self.program_height = 970
        self.program_width = 1750
        if screen_width<1500 and screen_height<900:
            self.low_screen = 1
        if self.low_screen == 1:
            self.program_height = 600
            self.program_width = 1100
        self.border_px = 2
        self.setStyleSheet('background-color: rgb(170, 170, 255);')
        self.setFixedSize(self.program_width, self.program_height)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setWindowTitle("  ")
        self.game_frame = QtWidgets.QFrame(self)
        self.game_frame_width = self.program_width*0.6+2*(self.border_px)
        self.game_frame_height = self.program_height*0.7+2*(self.border_px)
        self.game_frame.setGeometry(QtCore.QRect(self.program_width*0.05-self.border_px,self.program_height*0.15-self.border_px,self.program_width*0.6+2*(self.border_px),self.program_height*0.7+2*(self.border_px)))
        self.game_frame.setStyleSheet("border-width:"+str(self.border_px)+"px;\n"
"border-style:solid;\n"
"border-color:white;\n"
"background-color:black;")
        self.ball = cw.Ball(self.game_frame)
        self.ball.setGeometry(QtCore.QRect(0,0,50,50))
        if self.low_screen==1:
            self.ball.resize(35,35)
            self.ball.low_screen=1
        oImage = QtGui.QImage('./image/ball.png')
        oImage = oImage.scaled(QtCore.QSize(50, 50))
        if self.low_screen==1:
            oImage = oImage.scaled(QtCore.QSize(35,35))
        self.ball.setPixmap(QtGui.QPixmap(oImage))
        self.ball.setStyleSheet('border:none;')
        
        self.player_pannel = cw.MoveLabel(self.game_frame)
        self.player_pannel_width = 40
        self.player_pannel_height = 194
        if self.low_screen==1:
            self.player_pannel_width = 30
            self.player_pannel_height = 150
            self.player_pannel.low_screen=1
        self.player_pannel_y = 0
        self.player_pannel.setGeometry(QtCore.QRect(0,0,self.player_pannel_width,self.player_pannel_height))
        self.player_pannel.setStyleSheet('background-color: gray;')
        
        self.ai_pannel = cw.MoveLabel(self.game_frame)
        self.ai_pannel_width = 40
        self.ai_pannel_height = 194
        if self.low_screen==1:
            self.ai_pannel_width= 30
            self.ai_pannel_height = 150
            self.ai_pannel.low_screen=1
        self.ai_pannel_y = 0
        self.ai_pannel.setGeometry(QtCore.QRect(1013,0,self.ai_pannel_width,self.ai_pannel_height))
        self.ai_pannel.setStyleSheet('background-color: gray;')
        
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(self.program_width*0.67,self.program_height*0.15,self.program_width*0.25,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border-width:"+str(self.border_px)+"px;\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-radius:"+str(self.border_px*10)+"px;\n"
"color:black;")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(self.program_width*0.67,self.program_height*0.3,self.program_width*0.25,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border-width:"+str(self.border_px)+"px;\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-radius:"+str(self.border_px*10)+"px;\n"
"color:black;")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(self.program_width*0.67,self.program_height*0.45,self.program_width*0.25,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border-width:"+str(self.border_px)+"px;\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-radius:"+str(self.border_px*10)+"px;\n"
"color:black;")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(self.program_width*0.67,self.program_height*0.6,self.program_width*0.25,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border-width:"+str(self.border_px)+"px;\n"
"border-style:solid;\n"
"border-color:white;\n"
"border-radius:"+str(self.border_px*10)+"px;\n"
"color:black;")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.02, self.program_width*0.08, self.program_width*0.04))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_pt = int(self.program_width/60)
        self.pushButton_3.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";"
"color:white;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(self.program_width*0.9, self.program_width*0.02, self.program_width*0.08, self.program_width*0.04))
        self.pushButton_4.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color:white;\n"
"font: "+str(font_pt)+"pt \"휴먼엑스포\";")
        self.pushButton_4.setText("")
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.player_pannel.move(0,240)
        self.ball.move(502,316)
        
        if self.low_screen==1:
            self.player_pannel.move(0,137)
            self.ball.move(317,195)
        
        self.pushButton_3.setText("이전")
        self.pushButton_4.setText("종료")
        
        
        self.pushButton_3.clicked.connect(self.go_back)
        self.pushButton_4.clicked.connect(self.quit)
        
        self.move(int((screen_width-self.program_width)/2),int(screen_height*0.01))
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def keyPressEvent(self, event):
        super(Ui_MainWindow,self).keyPressEvent(event)
        try:
            if event.key() == QtCore.Qt.Key_W or event.key() == QtCore.Qt.Key_Up:
                self.player_pannel.move_up()
            elif event.key() == QtCore.Qt.Key_S or event.key() == QtCore.Qt.Key_Down:
                self.player_pannel.move_down()
            else:
                return
        except BaseException as b:
            print(str(b))
            
    def open_dialog(self):
        aaa = pingpong_dialog.Ui_Dialog()
        aa = aaa.showModal()
        if aa:
            return
        
    def go_back(self):
        try:
            if self.t1 != None:
                self.t1.break_game=1
            self.hide()
            self.m_window.show()
            self.m_window.init_cursor()
        except BaseException as b:
            print(str(b))
            
    def play_ball(self):
        try:
            self.round += 1
            self.label.setText("현재 라운드: "+str(self.round)+"라운드")
            self.label_2.setText("")
            self.label_3.setText("")
            self.label_4.setText("")
            self.player_pannel.move(0,250)
            self.player_pannel.y = 250
            self.ai_pannel.move(1013,0)
            self.ai_pannel.y = 0
            self.ball.move(502,316)
            if self.low_screen==1:
                self.player_pannel.move(0,137)
                self.player_pannel.y = 137
                self.ai_pannel.move(629,0)
                self.ai_pannel.y = 0
                self.ball.move(317,195)
            num = random.randint(0,1)
            if num == 0:
                num = random.randint(200,230)
                self.angle = num
            elif num == 1:
                num = random.randint(130,160)
                self.angle = num
            self.t1 = ball_coord(self.ball,self.angle,self.player_pannel,self.ai_pannel,self.low_screen)
            self.t1.BallCoordSignal.connect(self.move_ball)
            self.t1.aiSignal.connect(self.call_ai)
            self.t1.LearinigSignal.connect(self.learning_data)
            self.t1.overSignal.connect(self.game_over)
            self.t1.start()
        except BaseException as b:
            print(str(b))
    
    def restart(self):
        self.training_data = []
        self.label_data = []
        self.round = 0
        self.player_pannel.move(0,240)
        self.player_pannel.y = 250
        self.ai_pannel.move(1013,0)
        self.ai_pannel.y = 0
        self.ball.move(502,316)
        if self.low_screen==1:
            self.player_pannel.move(0,137)
            self.player_pannel.y = 137
            self.ai_pannel.move(629,0)
            self.ai_pannel.y = 0
            self.ball.move(317,195)
        ui = train_alam.Ui_Dialog('게임을 시작합니다.')
        aa = ui.showModal()
        if aa:
            self.play_ball()
        else:
            self.go_back()
            
    @QtCore.pyqtSlot()
    def game_over(self):
        try:
            over = train_alam.Ui_Dialog('도달한 최대 라운드는 '+str(self.round)+'라운드입니다.\n다시하시겠습니까?')
            aa = over.showModal()
            if aa:
                self.restart()
            else:
                self.go_back()
        except BaseException as b:
            print(str(b))
        
    @QtCore.pyqtSlot()
    def learning_data(self):
        epoch = self.round *5
        try:
            al = pingpong_alert.Ui_Dialog(self.training_data,self.label_data,epoch)
            aaa = al.showModal()
            if aaa:
                self.model = al.model
                self.play_ball()
        except BaseException as b:
            print(str(b))
    
    @QtCore.pyqtSlot(list)
    def move_ball(self,data):
        try:
            self.ball.move(data[0],data[1])
            self.label_3.setText("공의 각도 : "+str(data[2]))
            self.label_4.setText("공의 속도: "+str(data[3]))
        except BaseException as b:
            print(str(b))
            
    @QtCore.pyqtSlot(list)
    def call_ai(self,data):
        angle = data[0]
        ball_x = data[1]
        ball_y = data[2]
        speed = data[3]
        touched = False
        move_point = []
        lis = []
        try:
            while True:
                if self.low_screen==0:
                    cos_val = math.cos(math.radians(angle))
                    sin_val = math.sin(math.radians(angle))
                    pre_x = ball_x
                    pre_y = ball_y
                    ball_x = int(ball_x+(speed*cos_val))
                    ball_y = int(ball_y+(speed*sin_val))
                    bol, re = self.ball.sensing_touch(ball_x, ball_y)
                    if touched:
                        bol = False
                        touched = False
                    if bol:
                        self.touched = True
                        if re == 'x+':
                            ball_x = 1013
                            self.label_data.append(ball_y)
                            lis = lis[len(lis)-35:len(lis)-5]
                            self.training_data.append(lis)
                            break
                        elif re == 'y-':
                            ball_y = 1
                            if angle<270:
                                an = 90-(angle-180)
                                ball_x = int(pre_x - ((pre_y-ball_y)*(math.tan(math.radians(an)))))
                                angle = 360 - angle
                            else:
                                an = angle-270
                                ball_x = int(pre_x + ((pre_y-ball_y)*(math.tan(math.radians(an)))))
                                angle = 180 - (angle-180)
                        elif re == 'y+':
                            ball_y = 632
                            if angle<90:
                                an = 90-angle
                                ball_x = int(pre_x + ((ball_y-pre_y)*(math.tan(math.radians(an)))))
                                angle = 360 - angle
                            else:
                                an = angle-90
                                ball_x = int(pre_x - ((ball_y-pre_y)*(math.tan(math.radians(an)))))
                                angle = 180 + (180-angle)
                    lis.append(ball_y)
                else:
                    cos_val = math.cos(math.radians(angle))
                    sin_val = math.sin(math.radians(angle))
                    pre_x = ball_x
                    pre_y = ball_y
                    ball_x = int(ball_x+(speed*cos_val))
                    ball_y = int(ball_y+(speed*sin_val))
                    bol, re = self.ball.sensing_touch(ball_x, ball_y)
                    if touched:
                        bol = False
                        touched = False
                    if bol:
                        self.touched = True
                        if re == 'x+':
                            ball_x = 629
                            
                            self.label_data.append(ball_y)
                            lis = lis[len(lis)-35:len(lis)-5]
                            self.training_data.append(lis)
                            break
                        
                        elif re == 'y-':
                            ball_y = 1
                            if angle<270:
                                an = 90-(angle-180)
                                ball_x = int(pre_x - ((pre_y-ball_y)*(math.tan(math.radians(an)))))
                                angle = 360 - angle
                            else:
                                an = angle-270
                                ball_x = int(pre_x + ((pre_y-ball_y)*(math.tan(math.radians(an)))))
                                angle = 180 - (angle-180)
                        elif re == 'y+':
                            ball_y = 389
                            if angle<90:
                                an = 90-angle
                                ball_x = int(pre_x + ((ball_y-pre_y)*(math.tan(math.radians(an)))))
                                angle = 360 - angle
                            else:
                                an = angle-90
                                ball_x = int(pre_x - ((ball_y-pre_y)*(math.tan(math.radians(an)))))
                                angle = 180 + (180-angle)
                    lis.append(ball_y)
            if self.low_screen==0:
                if self.round==1 or self.model==None:
                    ball_x = 1013
                    ball_y = random.randint(0,490)
                    move_point = []
                    move_point.append(ball_x)
                    move_point.append(ball_y)
                else:
                    lis = np.asarray(lis)
                    lis = lis.reshape(1,30)
                    ball_y = self.model.predict(lis)
                    ball_x = 1013
                    move_point = []
                    move_point.append(ball_x)
                    move_point.append(ball_y)
                self.label_2.setText("공의 예상 좌표 : "+str(int(move_point[1])))
                self.ai_pannel.move(move_point[0],int(move_point[1])-85)
                self.ai_pannel.y = int(move_point[1])-85
            else:
                if self.round==1 or self.model==None:
                    ball_x = 629
                    ball_y = random.randint(0,260)
                    move_point = []
                    move_point.append(ball_x)
                    move_point.append(ball_y)
                else:
                    lis = np.asarray(lis)
                    lis = lis.reshape(1,30)
                    ball_y = self.model.predict(lis)
                    ball_x = 629
                    move_point = []
                    move_point.append(ball_x)
                    move_point.append(ball_y)
                self.label_2.setText("공의 예상 좌표 : "+str(int(move_point[1])))
                self.ai_pannel.move(move_point[0],int(move_point[1])-65)
                self.ai_pannel.y = int(move_point[1])-65
        except BaseException as b:
            print(str(b))
            pass
        
    def quit(self):
        try:
            if self.t1 != None:
                self.t1.break_game = 1
            self.close()
        except BaseException as b:
            print(str(b))
        
            
            
        
class ball_coord(QtCore.QThread):
    
    BallCoordSignal = QtCore.pyqtSignal(list)
    aiSignal = QtCore.pyqtSignal(list)
    LearinigSignal = QtCore.pyqtSignal()
    overSignal = QtCore.pyqtSignal()
    
    def __init__(self,ball,angle,player_pannel,ai_pannel,low_screen):
        super().__init__()
        self.break_game = 0
        self.ball = ball
        self.angle = angle
        self.radian = 0
        self.cos_val = 0
        self.sin_val = 0
        self.ball_x = 502
        self.ball_y = 316
        if low_screen==0:
            self.speed = 5
        else:
            self.speed = 3
        self.low_screen = low_screen
        self.touched = False
        self.player_pannel = player_pannel
        self.while_count = 0
        self.pre_y = []
        self.y = 0
        self.ai_pannel = ai_pannel
        
    def run(self):
        while True:
            try:
                if self.break_game==0:
                    ai_data = []
                    self.while_count+=1
                    if self.while_count%400==0:
                        self.speed +=0.5
                    self.y = self.player_pannel.get_y()
                    
                    if len(self.pre_y)<15:
                        self.pre_y.append(self.y)
                    else:
                        del self.pre_y[0]
                        self.pre_y.append(self.y)
                    compare = True
                    if len(self.pre_y)>1:
                        for step in range(len(self.pre_y)-1):
                            if self.pre_y[step]!=self.pre_y[step+1]:
                                compare = False
                                break
                    result = []
                    self.radian = math.radians(self.angle)
                    self.cos_val = math.cos(self.radian)
                    self.sin_val = math.sin(self.radian)
                    pre_x = self.ball_x
                    pre_y = self.ball_y
                    self.ball_x = int(self.ball_x+(self.speed*self.cos_val))
                    self.ball_y = int(self.ball_y+(self.speed*self.sin_val))
                    if self.low_screen==0:
                        bol=self.player_pannel.sensing_touch(self.ball_x, self.ball_y)
                        if self.touched:
                                bol = False
                                self.touched = False
                        if bol:
                            self.touched = True
                            if compare==False:
                                try:
                                    self.ball_x = 40
                                    self.ball_y = int(pre_y - ((pre_x-self.ball_x)*(math.tan(math.radians(self.angle-180)))))
                                    if self.angle<180:
                                        if self.player_pannel.get_direct()==1:
                                            if int(self.angle*0.9)>100:
                                                self.angle = 180 - int(self.angle*0.9)
                                            else:
                                                self.angle = 180 - self.angle
                                        else:
                                            if int(self.angle*1.1)<170:
                                                self.angle = 180 - int(self.angle*1.1)
                                            else:
                                                self.angle = 180 - self.angle
                                    else:
                                        if self.player_pannel.get_direct()==1:
                                            if int((self.angle-180)*1.1)<350:
                                                self.angle = 360 - int((self.angle - 180)*1.1)
                                            else:
                                                self.angle = 360 - (self.angle - 180)
                                        else:
                                            if int((self.angle-180)*0.9)>280:
                                                self.angle = 360 - int((self.angle - 180)*0.9)
                                            else:
                                                self.angle = 360 - (self.angle - 180)
                                except BaseException as b:
                                    print(str(b))
                            else:
                                try:
                                    self.ball_x = 40
                                    self.ball_y = int(pre_y - ((pre_x-self.ball_x)*(math.tan(math.radians(self.angle-180)))))
                                    if self.angle<180:
                                        self.angle = 180 - self.angle
                                    else:
                                        self.angle = 360 - (self.angle - 180)
                                except BaseException as b:
                                    print(str(b))
                            ai_data.append(self.angle)
                            ai_data.append(self.ball_x)
                            ai_data.append(self.ball_y)
                            ai_data.append(self.speed)
                            self.aiSignal.emit(ai_data)
                        else:
                            bol = self.ai_pannel.sensing_touch2(self.ball_x, self.ball_y)
                            if self.touched:
                                bol = False
                                self.touched = False
                            if bol:
                                self.touched = True
                                self.ball_x = 963
                                if self.angle>270:
                                    an = self.angle-270
                                    self.ball_y = int(pre_y - ((self.ball_x-pre_x)*(math.tan(math.radians(an)))))
                                    self.angle = 270 - (self.angle- 270)
                                else:
                                    an = 90-self.angle
                                    self.ball_y = int(pre_y + ((self.ball_x-pre_x)*(math.tan(math.radians(an)))))
                                    self.angle = 180 - self.angle
                            else:
                                bol, re = self.ball.sensing_touch(self.ball_x, self.ball_y)
                                if self.touched:
                                    bol = False
                                    self.touched = False
                                if bol:
                                    self.touched = True
                                    if re == 'x-':
                                        self.overSignal.emit()
                                        break
                                    elif re == 'x+':
                                        self.LearinigSignal.emit()
                                        break
                                    elif re == 'y-':
                                        self.ball_y = 1
                                        if self.angle<270:
                                            an = 90-(self.angle-180)
                                            self.ball_x = int(pre_x - ((pre_y-self.ball_y)*(math.tan(math.radians(an)))))
                                            self.angle = 360 - self.angle
                                        else:
                                            an = self.angle-270
                                            self.ball_x = int(pre_x + ((pre_y-self.ball_y)*(math.tan(math.radians(an)))))
                                            self.angle = 180 - (self.angle-180)
                                    elif re == 'y+':
                                        self.ball_y = 632
                                        if self.angle<90:
                                            an = 90-self.angle
                                            self.ball_x = int(pre_x + ((self.ball_y-pre_y)*(math.tan(math.radians(an)))))
                                            self.angle = 360 - self.angle
                                        else:
                                            an = self.angle-90
                                            self.ball_x = int(pre_x - ((self.ball_y-pre_y)*(math.tan(math.radians(an)))))
                                            self.angle = 180 + (180-self.angle)
                    else:
                        bol=self.player_pannel.sensing_touch(self.ball_x, self.ball_y)
                        if self.touched:
                                bol = False
                                self.touched = False
                        if bol:
                            self.touched = True
                            if compare==False:
                                try:
                                    self.ball_x = 30
                                    self.ball_y = int(pre_y - ((pre_x-self.ball_x)*(math.tan(math.radians(self.angle-180)))))
                                    if self.angle<180:
                                        if self.player_pannel.get_direct()==1:
                                            if int(self.angle*0.9)>100:
                                                self.angle = 180 - int(self.angle*0.9)
                                            else:
                                                self.angle = 180 - self.angle
                                        else:
                                            if int(self.angle*1.1)<170:
                                                self.angle = 180 - int(self.angle*1.1)
                                            else:
                                                self.angle = 180 - self.angle
                                    else:
                                        if self.player_pannel.get_direct()==1:
                                            if int((self.angle-180)*1.1)<350:
                                                self.angle = 360 - int((self.angle - 180)*1.1)
                                            else:
                                                self.angle = 360 - (self.angle - 180)
                                        else:
                                            if int((self.angle-180)*0.9)>280:
                                                self.angle = 360 - int((self.angle - 180)*0.9)
                                            else:
                                                self.angle = 360 - (self.angle - 180)
                                except BaseException as b:
                                    print(str(b))
                            else:
                                try:
                                    self.ball_x = 30
                                    self.ball_y = int(pre_y - ((pre_x-self.ball_x)*(math.tan(math.radians(self.angle-180)))))
                                    if self.angle<180:
                                        self.angle = 180 - self.angle
                                    else:
                                        self.angle = 360 - (self.angle - 180)
                                except BaseException as b:
                                    print(str(b))
                            ai_data.append(self.angle)
                            ai_data.append(self.ball_x)
                            ai_data.append(self.ball_y)
                            ai_data.append(self.speed)
                            self.aiSignal.emit(ai_data)
                        else:
                            bol = self.ai_pannel.sensing_touch2(self.ball_x, self.ball_y)
                            if self.touched:
                                bol = False
                                self.touched = False
                            if bol:
                                self.touched = True
                                self.ball_x = 599
                                if self.angle>270:
                                    an = self.angle-270
                                    self.ball_y = int(pre_y - ((self.ball_x-pre_x)*(math.tan(math.radians(an)))))
                                    self.angle = 270 - (self.angle- 270)
                                else:
                                    an = 90-self.angle
                                    self.ball_y = int(pre_y + ((self.ball_x-pre_x)*(math.tan(math.radians(an)))))
                                    self.angle = 180 - self.angle
                            else:
                                bol, re = self.ball.sensing_touch(self.ball_x, self.ball_y)
                                if self.touched:
                                    bol = False
                                    self.touched = False
                                if bol:
                                    self.touched = True
                                    if re == 'x-':
                                        self.overSignal.emit()
                                        break
                                    elif re == 'x+':
                                        self.LearinigSignal.emit()
                                        break
                                    elif re == 'y-':
                                        self.ball_y = 1
                                        if self.angle<270:
                                            an = 90-(self.angle-180)
                                            self.ball_x = int(pre_x - ((pre_y-self.ball_y)*(math.tan(math.radians(an)))))
                                            self.angle = 360 - self.angle
                                        else:
                                            an = self.angle-270
                                            self.ball_x = int(pre_x + ((pre_y-self.ball_y)*(math.tan(math.radians(an)))))
                                            self.angle = 180 - (self.angle-180)
                                    elif re == 'y+':
                                        self.ball_y = 389
                                        if self.angle<90:
                                            an = 90-self.angle
                                            self.ball_x = int(pre_x + ((self.ball_y-pre_y)*(math.tan(math.radians(an)))))
                                            self.angle = 360 - self.angle
                                        else:
                                            an = self.angle-90
                                            self.ball_x = int(pre_x - ((self.ball_y-pre_y)*(math.tan(math.radians(an)))))
                                            self.angle = 180 + (180-self.angle)  
                    result.append(self.ball_x)
                    result.append(self.ball_y)
                    result.append(self.angle)
                    result.append(self.speed)
                    self.BallCoordSignal.emit(result)
                    time.sleep(0.01)
                else:
                    break
            except BaseException as b:
                print(str(b))
                if self.angle <=0:
                    num = random.randint(10,40)
                    self.angle = num
                continue