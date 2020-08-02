import sys
import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

total_width=1000;
total_height=800;

def generate_data_index(): #更新data_index.json
    diary_names=[] #所有的路径的名字
    current_page=0
    for i in os.listdir("data"):
        diary_names.append(i)
        current_page=current_page+1
    current_page=current_page-1
    print(diary_names)
    with open("data_index.json","w",encoding="utf-8") as outfile:
        json.dump(diary_names,outfile)
    with open("current_page.json","w",encoding="utf-8") as outfile:
        json.dump(current_page,outfile)
    return(diary_names,current_page)

def load_data_index():
    diary_names=json.load(open("data_index.json","r",encoding="utf-8"))
    current_page=json.load(open("current_page.json","r",encoding="utf-8"))
    return(diary_names,current_page)

class DiaryPage(QWidget):#一页日记
    def __init__(self,parent,on_page):
        super().__init__(parent)        
        self.initUI(on_page)

    def initUI(self,on_page):
        self.setGeometry(10,50,total_width*0.6,total_height*0.8)
        self.path="data/"+diary_names[on_page]+"/"
        with open(self.path+diary_names[on_page]+".txt","r",encoding="utf-8") as txtfile:
            self.text=txtfile.read()
        image_paths=[]
        for i in os.listdir("data/"+diary_names[on_page]):
            if (i[-3]!='t'):
                image_paths.append("data/"+diary_names[on_page]+"/"+i)
        print(image_paths)
        whole_layout=QVBoxLayout()
        scroll=QScrollArea() #内容部分，包括文字和图片，多了可以滚动
        content_area=QWidget() #纵向排列
        content_area.setMaximumWidth(total_width*0.55)
        content_layout=QVBoxLayout()
        content_area.setLayout(content_layout)

        self.text_box=QLabel(self)
        self.text_box.setText(self.text)
        self.text_box.setWordWrap(True)
        self.text_box.setStyleSheet("font-size: 30px;")
        content_layout.addWidget(self.text_box,alignment=Qt.AlignCenter)

        for p in image_paths:
            piclab=QLabel()
            piclab.setFixedSize(total_width*0.5,total_height*0.5)
            piclab.setScaledContents(True)
            pic=QPixmap(p)
            piclab.setPixmap(pic)
            content_layout.addWidget(piclab)

        scroll.setWidget(content_area)
        whole_layout.addWidget(scroll)
        self.setLayout(whole_layout)
        self.show()    

class MyMainWindow(QMainWindow):
    def __init__(self,on_page,diary_names):
        super().__init__()
        self.on_page=on_page
        self.diary_names=diary_names
        self.max_page_num=len(self.diary_names)
        self.initUI(on_page)

    def initUI(self,on_page):
        self.resize(total_width,total_height)
        self.setWindowTitle('本地空间浏览器')
        self.setStyleSheet("background-color:#FFFFFF")
        
        self.diary_page=DiaryPage(self,on_page)
        self.diary_page.show()

        self.btp=QPushButton('上一页',self)
        self.btp.clicked.connect(self.turn_to_last_page)
        self.btp.setGeometry(0,0,100,50)

        self.jumpinput=QLineEdit(self)
        self.jumpinput.setGeometry(200,0,50,50)
        
        self.max_page_label=QLabel(self)
        self.max_page_label.setText("/"+str(self.max_page_num))
        self.max_page_label.setGeometry(260,0,50,40)

        self.jumpbutton=QPushButton("确定跳转",self)
        self.jumpbutton.clicked.connect(self.jump)
        self.jumpbutton.setGeometry(300,0,100,50)
    
        self.btn=QPushButton('下一页',self)
        self.btn.clicked.connect(self.turn_to_next_page)
        self.btn.setGeometry(500,0,100,50)
    
    def turn_to_page(self,page_num):
        if (page_num>=self.max_page_num or page_num<0):
            return
        del self.diary_page
        self.on_page=page_num
        self.diary_page=DiaryPage(self,self.on_page)
        self.diary_page.show()

    def jump(self):
        msg=self.jumpinput.text()
        if (msg.isdigit()):
            self.turn_to_page(int(msg))

    def turn_to_last_page(self):
        self.turn_to_page(self.on_page-1)

    def turn_to_next_page(self):
        self.turn_to_page(self.on_page+1)
    
if __name__=='__main__':
    app=QApplication(sys.argv)
    (diary_names,current_page)=generate_data_index()
    on_page=current_page
    win=MyMainWindow(on_page,diary_names)
    win.show()
    sys.exit(app.exec_())
