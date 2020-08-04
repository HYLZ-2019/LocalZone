from selenium import webdriver
from time import sleep
import os
import re
import urllib.request
import datetime

first_page=1
last_page=100
first_page=input("请输入开始页号")
last_page=input("请输入结束页号")
first_page=int(first_page)
last_page=int(last_page)

day_count={}#day_count[i]是第i天已经爬进来的说说数

def make_title(date_str):
    if (date_str[0:2]=="今天"):
        date_str=str(datetime.date.today())
        date=date_str[0:4]+date_str[5:7]+date_str[8:10]
    elif (date_str[0:2]=="昨天"):
        date_str=str(datetime.date.today()-datetime.timedelta(days=1))
        date=date_str[0:4]+date_str[5:7]+date_str[8:10]
    else:
        nums=re.split(r'年|月|日',date_str)
        year=nums[0]
        month=nums[1]
        day=nums[2]
        if (len(month)<2):
            month="0"+month;
        if (len(day)<2):
            day="0"+day;
        date=year+month+day
    title=date+"_"
    if (not date in day_count):
        title=title+str(0)
        day_count[date]=1
    else:
        title=title+str(day_count[date])
        day_count[date]+=1
    return (title)

#登录部分

try:
    driver=webdriver.Chrome()
    #要安装chromedriver：https://www.jianshu.com/p/dc0336a0bf50
    driver.set_window_position(20,40)
    driver.set_window_size(1000,800)
    options=webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver.implicitly_wait(10) #最多等十秒加载
    driver.get("http://i.qq.com")
    driver.switch_to.frame('login_frame')
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[8]/div/a[1]').click() #点击头像登录进空间
    sleep(10) #这里的元素貌似是一个一个加载出来的，所以要干等一会再找“说说”键
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/div[1]/div/ul/li[5]/a').click() #点击“说说”
except:
    print("说说页面打开失败！")
    
sleep(10)
driver.switch_to.frame(0)
sleep(5)

for page_num in range (last_page,first_page-1,-1):
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[1]/div/div[3]/div[4]/div/p[2]/span/input").send_keys(str(page_num))
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[1]/div/div[3]/div[4]/div/p[2]/span/button").click() #跳转到第page_num页
    sleep(5)
    feeds=driver.find_elements_by_class_name("feed")
    #print(feeds)
    for f in reversed(feeds): #f是说说“整体”
        content=f.find_element_by_css_selector(".content").text #文本内容
        diary_time=f.find_elements_by_css_selector(".info")[-1].text #发布时间
        print(diary_time)
        folder_title=make_title(diary_time)
        os.makedirs("data/"+folder_title)
        with open("data/"+folder_title+"/"+folder_title+".txt","w",encoding="UTF-8") as openfile:
            openfile.write(content) #把文本写入txt
        try:
            #找找看有没有图片
            im_cnt=0
            images=f.find_element_by_xpath('./div[3]/div[3]/div[1]/div').find_elements_by_tag_name('a')
            for im in images:
                try:
                    link=im.get_attribute('href')
                    #print(link)
                    urllib.request.urlretrieve(link,"data/"+folder_title+"/"+folder_title+"_"+str(im_cnt)+".jpg")
                    im_cnt+=1
                except:
                    pass
        except: pass
        try:
            #看看是不是转发
            repost_box=f.find_element_by_css_selector("[class='md rt_content']")
            print(repost_box)
            os.makedirs("data/"+folder_title+"/repost")
            with open("data/"+folder_title+"/repost/repost_text.txt","w",encoding="UTF-8") as txtfile:
                author=repost_box.find_element_by_xpath('./div[1]/div[1]/a[1]')
                author_name=author.text
                print(author_name)
                author_qq=author.get_attribute("profileuin")
                print(author_qq)
                original_text=repost_box.find_element_by_xpath('./div[1]/div[1]/pre').text
                print(original_text)
                repost_str=str(author_name)+"("+str(author_qq)+"):\n"+original_text
                print(repost_str)
                txtfile.write(repost_str)
            try:
                #看看转发里有没有图
                repost_pics=repost_box.find_elements_by_css_selector('[class="img-attachments-inner clearfix"]')[0].find_elements_by_tag_name('a')
                repost_im_cnt=0
                for pic in repost_pics:
                    try:
                        link=pic.get_attribute('href')
                        urllib.request.urlretrieve(link,"data/"+folder_title+"/repost/"+str(repost_im_cnt)+".jpg")
                        repost_im_cnt+=1
                    except: pass
            except: pass
        except: pass

    with open("crawl_log.txt","a",encoding="UTF-8") as openfile:
        openfile.write(str(datetime.datetime.now())[:-7])
        openfile.write("已爬取第"+str(page_num)+"页。这一页的最后一条说说是"+folder_title+"。\n")
    print("已爬取第"+str(page_num)+"页。")


print("Pages all turned")
