from selenium import webdriver
from time import sleep
import os
import re
import urllib.request


day_count={}#day_count[i]是第i天已经爬进来的说说数

def make_title(date_str):
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
        print(str(0))
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
can_go_next=True;
page_cnt=1

while (can_go_next):
    sleep(5)
    feeds=driver.find_elements_by_class_name("feed")
    print(feeds)
    for f in feeds: #f是说说“整体”
        content=f.find_element_by_css_selector(".content").text #文本内容
        time=f.find_element_by_css_selector(".info").text #发布时间
        folder_title=make_title(time)
        os.makedirs("data/"+folder_title)
        with open("data/"+folder_title+"/"+folder_title+".txt","w",encoding="UTF-8") as openfile:
            openfile.write(content) #把文本写入txt
        try:
            im_cnt=0
            images=f.find_element_by_xpath('./div[3]/div[3]/div[1]/div').find_elements_by_tag_name('a')
            for im in images:
                try:
                    link=im.get_attribute('href')
                    print(link)
                    urllib.request.urlretrieve(link,"data/"+folder_title+"/"+folder_title+"_"+str(im_cnt)+".jpg")
                    im_cnt+=1
                except:
                    pass
        except:
            pass

    #点击"下一页"键
    try:
        driver.find_element_by_link_text("下一页").click()
        print("已完成第"+str(page_cnt)+"页")
        page_cnt+=1
    except:
        can_go_next=False
    #driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[1]/div/div[3]/ol/li[1]/div[3]/div[2]/a").click()
    


print("Pages all turned")
print(page_cnt)
d=0