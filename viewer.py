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

def get_date(diary_title):
    return(diary_title[0:4]+"年"+diary_title[4:6]+"月"+diary_title[6:8]+"日")

class RepostPage(QWidget):#一页日记
    def __init__(self,parent,page_title):
        super().__init__(parent)
        self.page_title=page_title
        self.initUI()

    def initUI(self):
        self.path="data/"+self.page_title+"/repost"
        with open(self.path+"/repost_text.txt","r",encoding="utf-8") as txtfile:
            self.text=txtfile.read()
        image_paths=[]
        for i in os.listdir(self.path):
            if (i[-3]!='t'):
                image_paths.append(self.path+"/"+i)
        whole_layout=QVBoxLayout()
        self.setStyleSheet("background-color:#EEEEFF")
        self.setMaximumWidth(int(total_width*0.55))
        
        self.text_box=QLabel(self)
        self.text_box.setText(self.text)
        self.text_box.setWordWrap(True)
        self.text_box.setStyleSheet("font-size: 20px;")
        self.text_box.setFixedWidth(int(total_width*0.55))
        whole_layout.addWidget(self.text_box)#,alignment=Qt.AlignCenter)

        if (len(image_paths)==1):#只有一个就放大图
            for p in image_paths:
                piclab=QPushButton()
                piclab.setFixedSize(int(total_width*0.5),int(total_height*0.5))
                pic_style="QPushButton{border-image:url("+p+")}"
                piclab.setStyleSheet(pic_style)
                piclab.clicked.connect(lambda:self.show_big_pic(image_paths,0))
                whole_layout.addWidget(piclab)
        
        elif (len(image_paths)<=4):#<=4张就一行放两个
            
            for i in range(0,len(image_paths)):
                p=image_paths[i]
                if (i%2==0):
                    hbox=QWidget()
                    hlayout=QHBoxLayout()
                piclab=QPushButton()
                piclab.setFixedSize(int(total_width*0.25),int(total_height*0.25))
                pic_style="QPushButton{border-image:url("+p+")}"
                piclab.setStyleSheet(pic_style)
                piclab.clicked.connect(lambda:self.show_big_pic(image_paths,i))
                hlayout.addWidget(piclab)
                if (i%2==1 or i==len(image_paths)-1):                    
                    hbox.setLayout(hlayout)
                    whole_layout.addWidget(hbox)

        else:#>4张就一行放三个
            for i in range(0,len(image_paths)):
                p=image_paths[i]
                if (i%3==0):
                    hbox=QWidget()
                    hlayout=QHBoxLayout()
                piclab=QPushButton()
                piclab.setFixedSize(int(total_width*0.16),int(total_height*0.16))
                pic_style="QPushButton{border-image:url("+p+")}"
                piclab.setStyleSheet(pic_style)
                piclab.clicked.connect(lambda:self.show_big_pic(image_paths,i))
                hlayout.addWidget(piclab)
                if (i%3==2 or i==len(image_paths)):
                    hbox.setLayout(hlayout)
                    whole_layout.addWidget(hbox)
                

        self.setLayout(whole_layout)    

    def show_big_pic(self,path_list,init_index):
        self.see_big_pic=big_pic(path_list,init_index)
        self.see_big_pic.show()


class big_pic(QWidget):
    def __init__(self,path_list,init_index):
        super().__init__()
        self.path_list=path_list
        self.cur_index=init_index
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("查看大图")
        self.setGeometry(100,100,1000,1000)
        self.loadPic()
        self.show()

    def loadPic(self):
        self.picture_area=QWidget()
        self.picture_layout=QVBoxLayout()
        self.picture_scroll=QScrollArea(self)

        self.picture=QLabel()
        self.picture.setScaledContents(True)
        self.picture.setMaximumWidth(900)
        pic_path=self.path_list[self.cur_index]
        self.picture.setPixmap(QPixmap(pic_path))
        
        self.picture_layout.addWidget(self.picture)

        self.picture_area.setLayout(self.picture_layout)
        self.picture_scroll.setWidget(self.picture_area)
        self.picture_scroll.setFixedWidth(1000)
        self.picture_scroll.setFixedHeight(900)


class DiaryPage(QWidget):#一页日记
    def __init__(self,parent,on_page):
        super().__init__(parent)        
        self.initUI(on_page)

    def initUI(self,on_page):
        self.setGeometry(10,50,int(total_width*0.6),int(total_height*0.8))
        self.path="data/"+diary_names[on_page]+"/"
        with open(self.path+diary_names[on_page]+".txt","r",encoding="utf-8") as txtfile:
            self.text=txtfile.read()
        image_paths=[]
        for i in os.listdir("data/"+diary_names[on_page]):
            if (i[-3]!='t' and i[-4]=='.'):
                image_paths.append("data/"+diary_names[on_page]+"/"+i)
        print(image_paths)
        whole_layout=QVBoxLayout()
        scroll=QScrollArea() #内容部分，包括文字和图片，多了可以滚动
        content_area=QWidget() #纵向排列
        content_area.setMaximumWidth(int(total_width*0.55))
        content_layout=QVBoxLayout()
        content_area.setLayout(content_layout)
        content_area.setStyleSheet("background-color:#FFFFFF")

        post_time=get_date(diary_names[on_page])
        self.time_tag=QLabel(self)
        self.time_tag.setText(post_time)
        content_layout.addWidget(self.time_tag)

        self.text_box=QLabel(self)
        self.text_box.setText(self.text)
        self.text_box.setWordWrap(True)
        self.text_box.setStyleSheet("font-size: 20px;")
        self.text_box.setFixedWidth(int(total_width*0.55))
        content_layout.addWidget(self.text_box)#,alignment=Qt.AlignCenter)

        if (len(image_paths)==1):#只有一个就放大图
            for p in image_paths:
                piclab=QPushButton()
                piclab.setFixedSize(int(total_width*0.5),int(total_height*0.5))
                pic_style="QPushButton{border-image:url("+p+")}"
                piclab.setStyleSheet(pic_style)
                piclab.clicked.connect(lambda:self.show_big_pic(image_paths,0))
                content_layout.addWidget(piclab)
        
        elif (len(image_paths)<=4):#<=4张就一行放两个
            
            for i in range(0,len(image_paths)):
                p=image_paths[i]
                if (i%2==0):
                    hbox=QWidget()
                    hlayout=QHBoxLayout()
                piclab=QPushButton()
                piclab.setFixedSize(int(total_width*0.25),int(total_height*0.25))
                pic_style="QPushButton{border-image:url("+p+")}"
                piclab.setStyleSheet(pic_style)
                piclab.clicked.connect(lambda:self.show_big_pic(image_paths,i))
                hlayout.addWidget(piclab)
                if (i%2==1 or i==len(image_paths)-1):                    
                    hbox.setLayout(hlayout)
                    content_layout.addWidget(hbox)

        else:#>4张就一行放三个
            for i in range(0,len(image_paths)):
                p=image_paths[i]
                if (i%3==0):
                    hbox=QWidget()
                    hlayout=QHBoxLayout()
                piclab=QPushButton()
                piclab.setFixedSize(int(total_width*0.16),int(total_height*0.16))
                pic_style="QPushButton{border-image:url("+p+")}"
                piclab.setStyleSheet(pic_style)
                piclab.clicked.connect(lambda:self.show_big_pic(image_paths,i))
                hlayout.addWidget(piclab)
                if (i%3==2 or i==len(image_paths)):
                    hbox.setLayout(hlayout)
                    content_layout.addWidget(hbox)
                
        if (os.path.exists(self.path+"repost/")):
            repo=RepostPage(self,diary_names[on_page])
            content_layout.addWidget(repo)

        scroll.setWidget(content_area)
        whole_layout.addWidget(scroll)
        self.setLayout(whole_layout)
        self.show()    

    def show_big_pic(self,path_list,init_index):
        self.see_big_pic=big_pic(path_list,init_index)
        self.see_big_pic.show()

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
        self.setStyleSheet("background-color:#CCCCFF")
        
        self.diary_page=DiaryPage(self,on_page)
        self.diary_page.show()

        self.btp=QPushButton('上一页',self)
        self.btp.clicked.connect(self.turn_to_last_page)
        self.btp.setGeometry(0,0,100,50)

        self.jumpinput=QLineEdit(self)
        self.jumpinput.setGeometry(200,0,50,50)
        self.jumpinput.setText(str(self.on_page))
        
        self.max_page_label=QLabel(self)
        self.max_page_label.setText("/"+str(self.max_page_num-1))
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
        self.jumpinput.setText(str(self.on_page))

    def jump(self):
        msg=self.jumpinput.text()
        if (msg.isdigit()):
            self.turn_to_page(int(msg))

    def turn_to_last_page(self):
        self.turn_to_page(self.on_page-1)

    def turn_to_next_page(self):
        self.turn_to_page(self.on_page+1)
    


app=QApplication(sys.argv)
(diary_names,current_page)=generate_data_index()
on_page=current_page
win=MyMainWindow(on_page,diary_names)
win.show()
sys.exit(app.exec_())
