
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
            pass
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

class ScrollLabel(QtWidgets.QLabel):

    def __init__(self,parent):
        super(ScrollLabel,self).__init__(parent)
     

    def createScroll(self):
        height = self.height()
        QtWidgets.QScrollBar()
        width = self.width()
        self.vertical_scrollbar = QtWidgets.QScrollBar(self)
        self.vertical_scrollbar.setGeometry(QtCore.QRect(width-(width//40),1,width//40,height-2))
        self.horizon_scrollbar = QtWidgets.QScrollBar(self)
        self.horizon_scrollbar.setOrientation(QtCore.Qt.Horizontal)
        self.horizon_scrollbar.setGeometry(QtCore.QRect(1,height-(width//40),width-(width//40+1),width//40))
        self.vertical_scrollbar.valueChanged.connect(self.move_vertical_scroll)
        self.horizon_scrollbar.valueChanged.connect(self.move_horizontal_scroll)
        self.message_label = QtWidgets.QLabel(self)
        self.message_label.move(0,0)
        self.message_label.stackUnder(self.vertical_scrollbar)
        self.vertical_scrollbar.stackUnder(self.horizon_scrollbar)
        self.message_label.setMinimumSize(width-(width//40),height-(width//40))
    
    @QtCore.pyqtSlot()
    def move_vertical_scroll(self):
        scoll_position=self.vertical_scrollbar.value()
        label_height = self.message_label.height()
        if self.message_label.height()<self.height():
            self.vertical_scrollbar.setValue(0)
            return
        per_height = (label_height-self.height())//100
        move_posision = scoll_position*per_height*-1
        self.message_label.move(0,move_posision)

    
    @QtCore.pyqtSlot()
    def move_horizontal_scroll(self):
        scoll_position=self.horizon_scrollbar.value()
        label_width = self.message_label.width()
        if self.message_label.width()<self.width():
            self.horizon_scrollbar.setValue(0)
            return
        per_width = (label_width-self.width())//100
        move_posision = scoll_position*per_width*-1
        self.message_label.move(move_posision,3)

    def setText(self,message):
        if type(message)!=str:
            return
        before_height = self.message_label.height()
        font_size_point = self.message_label.font().pointSize()
        message_list = message.split('\n')
        count = 0
        index = 0
        for step in range(len(message_list)):
            if len(message_list[step])>count:
                count = len(message_list[step])
                index = step
        blank_count = []
        for step in range(len(message_list)):
            co = 0
            for step2 in range(len(message_list[step])):
                if message_list[step][len(message_list[step])-step2-1:len(message_list[step])-step2]==' ':
                    co+=1      
                else:
                    blank_count.append(co)
                    break
        for step in range(len(blank_count)):
            message_list[step] = message_list[step][:len(message_list[step])-blank_count[step]]
        message = '\n'.join(message_list)
        blank = 0
        word = 0
        sign = 0
        for w in list(message_list[index]):
            if w in ["\"","'",",",".","?","!"]:
                sign+=1
            elif w == " ":
                blank += 1
            else:
                word += 1
        width = int((font_size_point*word*1.5)+(font_size_point*blank*0.5)+(font_size_point*sign*0.3))
        height = int(font_size_point*len(message_list)*1.6)
        self.message_label.setFixedSize(width,height)
        parent_height = self.height()-(self.width()//40)
        self.message_label.setText(message)
        after_height = self.message_label.height()
        self.horizon_scrollbar.setValue(0)
        if after_height>parent_height and after_height>before_height:
            move_height = parent_height-after_height
            self.message_label.move(0,move_height)
            self.vertical_scrollbar.setValue(100)
        else:
            self.message_label.move(0,0)
            self.vertical_scrollbar.setValue(0)
        self.message_label.setFixedSize(width,height)

    def setStyleSheet(self,style):
        self.message_label.setStyleSheet(style)  


