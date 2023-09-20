from PyQt5 import QtCore, QtGui, QtWidgets
import custom_widgets as cw
import ctypes
from tensorflow.keras.models import load_model
import cv2
import numpy as np

class Ui_MainWindow(QtWidgets.QMainWindow):
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self,m_window):
        super().__init__()
        self.cam = None
        self.capture = 0
        self.cam_stop = 0
        self.model = load_model('./_models/unet_no_drop.h5')
        self.frame=[]
        self.frame2=[]
        self.synthesis = 0
        self.synimg = []
        self.m_window = m_window
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.setupUi()
        self.label_4.setText('원본사진의 사람을 오려서\n배경사진에 붙혀줍니다.')
    
    def setupUi(self):
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.setWindowIcon(QtGui.QIcon('./image/logo.png'))
        self.program_height = 700
        self.program_width = 1200
        self.border_px = int((2/1020)*screen_height)
        self.setStyleSheet('background-color: rgb(170, 170, 255);')
        self.setFixedSize(self.program_width, self.program_height)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setWindowTitle("  ")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(self.program_width*0.05,self.program_height*0.15,self.program_width*0.3,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/40))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("border-style:solid;\n"
                                 "color:white;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        self.ori_label = cw.ImageViewer(self)
        self.ori_label.setGeometry(QtCore.QRect(self.program_width*0.05,self.program_height*0.3,self.program_width*0.3,self.program_width*0.3))
        self.ori_label.setStyleSheet("border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.program_width*0.05,self.program_height*0.31+self.program_width*0.3,self.program_width*0.14,self.program_height*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_2.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("border-style:solid;\n"
                                 "color:black;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.setGeometry(QtCore.QRect(self.program_width*0.21,self.program_height*0.31+self.program_width*0.3,self.program_width*0.14,self.program_height*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_7.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("border-style:solid;\n"
                                 "color:black;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(self.program_width*0.02, self.program_width*0.02, self.program_width*0.08, self.program_width*0.04))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_pt = int(self.program_width/55)
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
        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(self.program_width*0.4, self.program_width*0.02, self.program_width*0.2, self.program_width*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/55))
        self.pushButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color:white;\n")
        
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(self.program_width*0.4, self.program_height*0.45, self.program_width*0.2, self.program_width*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/55))
        self.pushButton_5.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("border-style:solid;\n"
                                        "color:white;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        
        self.label_2 = cw.ImageViewer(self)
        self.label_2.setGeometry(QtCore.QRect(self.program_width*0.65,self.program_height*0.3,self.program_width*0.3,self.program_width*0.3))
        self.label_2.setStyleSheet("border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(self.program_width*0.36, self.program_height*0.82, self.program_width*0.28, self.program_width*0.1))
        self.label_4.setStyleSheet("border-style:solid;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n")
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_width/80))
        self.label_4.setFont(font)
        
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(self.program_width*0.65,self.program_height*0.31+self.program_width*0.3,self.program_width*0.14,self.program_height*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_6.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("border-style:solid;\n"
                                        "color:black;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        self.pushButton_8 = QtWidgets.QPushButton(self)
        self.pushButton_8.setGeometry(QtCore.QRect(self.program_width*0.81,self.program_height*0.31+self.program_width*0.3,self.program_width*0.14,self.program_height*0.06))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/50))
        self.pushButton_8.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet("border-style:solid;\n"
                                        "color:black;\n"
                                         "border-color:black;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(self.program_width*0.65,self.program_height*0.15,self.program_width*0.3,self.program_height*0.1))
        font = QtGui.QFont()
        font.setFamily("휴먼엑스포")
        font.setPointSize(int(self.program_height/40))
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setStyleSheet("border-style:solid;\n"
                                 "color:white;\n"
                                         "border-color:white;\n"
                                         "border-width:"+str(self.border_px)+"px;\n"
                                         "border-radius:"+str(self.border_px*10)+"px;")
        
        self.pushButton_8.setText("파일열기")
        self.pushButton_6.setText("그 림 저 장")
        self.pushButton.setText("도 움 말")
        self.pushButton_5.setText("사진 합성하기")
        self.pushButton_2.setText("캠열기")
        self.pushButton_3.setText("이전")
        self.pushButton_4.setText("종료")
        self.pushButton_7.setText("파일열기")
        self.label.setText("원 본 사 진")
        self.label_3.setText("배 경 사 진")
        
        
        self.pushButton_6.clicked.connect(self.save_img)
        self.pushButton_8.clicked.connect(self.open_bg)
        self.pushButton_7.clicked.connect(self.open_ori)
        self.pushButton_2.clicked.connect(self.set_cam)
        self.pushButton_3.clicked.connect(self.go_back)
        self.pushButton_4.clicked.connect(self.quit)
        self.pushButton_5.clicked.connect(self.subtract_image)
        self.VideoSignal1.connect(self.ori_label.setImage)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def postprocess(self,img_ori, pred):
        h, w = img_ori.shape[:2]
        
        mask_ori = (pred.squeeze()[:, :, 1] > 0.5).astype(np.uint8)
        max_size = max(h, w)
        result_mask = cv2.resize(mask_ori, dsize=(max_size, max_size))
    
        if h >= w:
            diff = (max_size - w) // 2
            if diff > 0:
                result_mask = result_mask[:, diff:-diff]
        else:
            diff = (max_size - h) // 2
            if diff > 0:
                result_mask = result_mask[diff:-diff, :]
            
        result_mask = cv2.resize(result_mask, dsize=(w, h))
        
        result_mask *= 255
    
        result_mask = cv2.GaussianBlur(result_mask, ksize=(9, 9), sigmaX=5, sigmaY=5)
        
        return result_mask
    def save_img(self):
        try:
            if self.synthesis==0:
                self.label_4.setText("먼저 합성을 해야합니다.")
                return
            file = QtWidgets.QFileDialog.getSaveFileName()
            if file[0]:
                self.synimg = cv2.cvtColor(self.synimg, cv2.COLOR_BGR2RGB)
                cv2.imwrite(file[0]+'.jpg',self.synimg)
                self.synthesis=0
                self.label_4.setText('저장되었습니다.')
        except BaseException as b:
            print(str(b))
    def preprocess(self,img):
        im = np.zeros((256, 256, 3), dtype=np.uint8)
    
        if img.shape[0] >= img.shape[1]:
            scale = img.shape[0] / 256
            new_width = int(img.shape[1] / scale)
            diff = (256 - new_width) // 2
            img = cv2.resize(img, (new_width, 256))
    
            im[:, diff:diff + new_width, :] = img
        else:
            scale = img.shape[1] / 256
            new_height = int(img.shape[0] / scale)
            diff = (256 - new_height) // 2
            img = cv2.resize(img, (256, new_height))
    
            im[diff:diff + new_height, :, :] = img
            
        return im
    
    def subtract_image(self):
        try:
            if len(self.frame)==0:
                self.label_4.setText('원본이미지가 없습니다.')
                return
            if len(self.frame2)==0:
                self.label_4.setText('배경이미지가 없습니다.')
                return
            self.synthesis = 1
            img = self.frame
            img_ori = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
            img = self.preprocess(img)
    
            input_img = img.reshape((1, 256, 256, 3)).astype(np.float32) / 255.
    
            pred = self.model.predict(input_img)
            mask = self.postprocess(img_ori, pred)
    
            converted_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
            result_img = cv2.subtract(converted_mask, img_ori)
            result_img = cv2.subtract(converted_mask, result_img)
            bg_img = self.frame2
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2RGB)
            bg_img = cv2.resize(bg_img,(360,360))
        
            overlay_img = cv2.resize(result_img, dsize=(320,240), fx=0.4, fy=0.4)
            resized_mask = cv2.resize(mask, dsize=(320,240), fx=0.4, fy=0.4)
        
            out_img = self.overlay_transparent(bg_img, overlay_img, resized_mask, 186, 230)
            self.synimg = out_img.copy()
            qt_image1 = QtGui.QImage(out_img.data,
                                        360,
                                        360,
                                        out_img.strides[0],
                                        QtGui.QImage.Format_RGB888)
            self.label_2.setImage(qt_image1)
        except BaseException as b:
            print(str(b))
    
    def open_ori(self):
        try:
            fname = QtWidgets.QFileDialog.getOpenFileName(self)
            if fname[0]:
                try:
                    img = cv2.imread(fname[0],cv2.IMREAD_COLOR)
                    _,_,b = img.shape
                    if b==4:
                        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                except:
                    self.label_4.setText('이미지파일이 아닙니다.')
                    return
                if self.cam!=None:
                    self.cam_stop = 1
                    self.capture = 0
                    self.cam.release()
                    self.cam = None
                    self.pushButton_2.setText("캠열기")
                height, width, _ = img.shape
                if height>=width:
                    img = cv2.resize(img,(360,int(height*(360/width))))
                    height, width, _ = img.shape
                    img = img[int((height-width)/2):int(((height-width)/2)+360),:,:]
                else:
                    img = cv2.resize(img,(int(width*(360/height)),360))
                    height, width, _ = img.shape
                    img = img[:,int((width-height)/2):int(((width-height)/2)+360),:]
                self.frame = img.copy()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(img.data,
                                                360,
                                                360,
                                                img.strides[0],
                                                QtGui.QImage.Format_RGB888)
                self.ori_label.setImage(qt_image1)
        except BaseException as b:
            print(str(b))
    def open_bg(self):
        try:
            fname = QtWidgets.QFileDialog.getOpenFileName(self)
            if fname[0]:
                try:
                    img = cv2.imread(fname[0],cv2.IMREAD_COLOR)
                    _,_,b = img.shape
                    if b==4:
                        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                except:
                    self.label_4.setText('이미지파일이 아닙니다.')
                    return
                if self.cam!=None:
                    self.cam_stop = 1
                    self.capture = 0
                    self.cam.release()
                    self.cam = None
                    self.pushButton_2.setText("캠열기")
                height, width, _ = img.shape
                if height>=width:
                    img = cv2.resize(img,(360,int(height*(360/width))))
                    height, width, _ = img.shape
                    img = img[int((height-width)/2):int(((height-width)/2)+360),:,:]
                else:
                    img = cv2.resize(img,(int(width*(360/height)),360))
                    height, width, _ = img.shape
                    img = img[:,int((width-height)/2):int(((width-height)/2)+360),:]
                self.frame2 = img.copy()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                qt_image1 = QtGui.QImage(img.data,
                                                360,
                                                360,
                                                img.strides[0],
                                                QtGui.QImage.Format_RGB888)
                self.label_2.setImage(qt_image1)
        except BaseException as b:
            print(str(b))
    def overlay_transparent(self,background_img, img_to_overlay_t, mask, x, y, overlay_size=None):
        img_to_overlay_t = cv2.cvtColor(img_to_overlay_t, cv2.COLOR_RGB2RGBA)
        bg_img = background_img.copy()
        
            # convert 3 channels to 4 channels
        if bg_img.shape[2] == 3:
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_RGB2RGBA)
        
        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)
                
        
        mask = cv2.medianBlur(mask, 5)
        
        h, w, _ = img_to_overlay_t.shape
        roi = bg_img[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)]
        
    
        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)
    
        bg_img[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)] = cv2.add(img1_bg, img2_fg)
    
        # convert 4 channels to 4 channels
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_RGBA2RGB)
    
        return bg_img


    def set_cam(self):
        if self.capture==0:
            self.frame=[]
            self.cam_stop=0
            self.capture=1
            self.pushButton_2.setText('사진촬영')
            try:
                self.cam = cv2.VideoCapture(0)
                self.cam.set(3,640)
                self.cam.set(4,480)
            except BaseException as b:
                print(str(b))
                self.label_4.setText("캠을 찾지 못했습니다.")
                
            try:
                _, image = self.cam.read()
                self.height, self.width = image.shape[:2]
            except BaseException as b:
                print(str(b))
                self.label_4.setText("캠에 문제가 있습니다.")
            
            while True:
                try:
                    if self.cam_stop==1:
                        break
                    ret, self.frame = self.cam.read()
                    if ret:
                        self.frame = cv2.flip(self.frame,1)
                        height,width = self.frame.shape[:2]
                        frame = cv2.resize(self.frame,dsize=(int(width*(self.program_width*0.3)/height),int(self.program_width*0.3)))
                        height,width = frame.shape[:2]
                        start_width = int((width-(self.program_width*0.3))/2)
                        frame = frame[:,start_width:int(start_width+(self.program_width*0.34)),:]
                        color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        qt_image1 = QtGui.QImage(color_swapped_image.data,
                                                    self.program_width*0.3,
                                                    self.program_width*0.3,
                                                    color_swapped_image.strides[0],
                                                    QtGui.QImage.Format_RGB888)
                        self.VideoSignal1.emit(qt_image1)
                        
                    loop = QtCore.QEventLoop()
                    QtCore.QTimer.singleShot(10, loop.quit)
                    loop.exec_()
                except BaseException as b:
                    print(str(b))
                    continue
        else:
            self.cam_stop = 1
            self.capture = 0
            self.cam.release()
            self.cam = None
            self.pushButton_2.setText("캠열기")
    def clear_widget(self):
        try:
            self.ori_label.clear()
        except BaseException as b:
            print(str(b))
    
    def go_back(self):
        try:
            if self.cam!=None:
                self.cam_stop=1
                self.cam.release()
                self.cam=None
                self.capture = 0
                self.pushButton_2.setText("캠열기")
            self.label_4.setText('')
            self.hide()
            self.m_window.show()
            self.m_window.init_cursor()
        except BaseException as b:
            print(str(b))
            
        
    def quit(self):
        if self.cam!=None:
            self.cam_stop=1
            self.cam.release()
        self.close()