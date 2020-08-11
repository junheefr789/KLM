# -*- coding:euc-kr -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("이미지가 없습니다.")
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.image = image
        self.update()
        
class PicButton(QtWidgets.QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class MoveLabel(QtWidgets.QLabel):
    def __init__(self,parent = None):
        super(MoveLabel,self).__init__(parent)
        self.y = 0
        self.direct = 0
        self.low_screen = 0
        
    def move_down(self):
        if self.low_screen==0:
            if 194+self.y<=683:
                self.y += 50
                self.move(0,self.y)
                self.direct =1 
                return 
            else:
                return
        else:
            if 150+self.y<=424:
                self.y += 30
                self.move(0,self.y)
                self.direct =1 
                return 
            else:
                return
    def move_up(self):
        if self.low_screen==0:
            if self.y-50>=0:
                self.y -= 50
                self.move(0,self.y)
                self.direct = 2
                return 
            else:
                return
        else:
            if self.y-30>=-5:
                self.y -= 30
                self.move(0,self.y)
                self.direct = 2
                return 
            else:
                return
    
    def move_point(self,x,y):
        self.move(x,y)
    def get_direct(self):
        return self.direct
        
    def sensing_touch(self,x,y):
        if self.low_screen==0:
            if x<=40 and x>0:
                if y+35>self.y and y<self.y+174:
                    return True
            return False
        else:
            if x<=30 and x>0:
                if y+20>self.y and y<self.y+130:
                    return True
            return False
    def sensing_touch2(self,x,y):
        if self.low_screen==0:
            if x+50>=1013 and x+50<1053:
                if y+35>self.y and y<self.y+174:
                    return True
            return False
        else:
            if x+35>=634 and x+35<664:
                if y+20>self.y and y<self.y+130:
                    print('check')
                    return True
            return False
    
    def get_y(self):
        return self.y
        

class Ball(QtWidgets.QLabel):
    def __init__(self,parent = None):
        super(Ball,self).__init__(parent)
        self.low_screen = 0
        
    def sensing_touch(self,x,y):
        if self.low_screen==0:
            if x<=0:
                return True,'x-'
            elif x+50>=1053:
                return True, 'x+'
            if y <= 0:
                return True, 'y-'
            elif y+50>=683:
                return True, 'y+'
        else:
            if x<=0:
                return True,'x-'
            elif x+35>=664:
                return True, 'x+'
            if y <= 0:
                return True, 'y-'
            elif y+35>=424:
                return True, 'y+'
        return False, ''

class DrawingWidget(QtWidgets.QWidget):

    def __init__(self,parent=None):
        super(DrawingWidget,self).__init__(parent)
        self.image = QtGui.QImage(QtCore.QSize(400,400), QtGui.QImage.Format_RGB32)
        self.image.fill(QtCore.Qt.black)
        self.drawing = False
        self.brush_size = 5
        self.brush_color = QtCore.Qt.white
        self.last_point = QtCore.QPoint()
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        self.drawed = 0
        
    def set_image_size(self,width,height):
        self.image = self.image.scaled(width,height)
    
    def save_image(self):
        self.image.save('asdfi.jpg')
        


    def paintEvent(self, e):
        canvas = QtGui.QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()
            self.drawed = 1

    def mouseMoveEvent(self, e):
        if (e.buttons() & QtCore.Qt.LeftButton) & self.drawing:
            painter = QtGui.QPainter(self.image)
            painter.setPen(QtGui.QPen(self.brush_color, self.brush_size, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.drawing = False


    def clear(self):
        self.drawed = 0
        self.image.fill(QtCore.Qt.black)
        self.update()
