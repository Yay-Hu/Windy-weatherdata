#-*-coding:UTF-8-
###########################################说明##################################################
##                                                                                             ##
##                      (Ⅰ)若没有安装beautifulsoup4、selenium、pandas、openpyxl库,               ##                                                                  
##                          安装方法为在window搜索栏或者win+R输入cmd，回车，依次输入以下代码安装:   ##                                                                            
##                          pip install beautifulsoup4                                         ##                                         
##                          pip install selenium                                               ##                                     
##                          pip install pandas                                                 ##                                 
##                          pip install openpyxl                                               ##                                     
##                      (Ⅱ)需要安装浏览器驱动Microsoft Edge WebDriver，可自行百度下载安装         ##                                                                     
##                      (Ⅲ)若输出的数据不完整，尝试运行多几次，或可增加强制停滞时间 （第51行）      ##
##                                                                                             ##
#################################################################################################

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By  

###########################################输入网址及文件路径#########################################
url='https://www.windy.com/21.622/124.014/waves?20.849,124.014,8'     #输入网址（附带地址信息）
filepath='D:\\Users\\1111\Desktop\\天气预测.xlsx'          #文件保存路径
email='qqq@email.com'       #账户
password='1234'             #密码

###########################################登录操作##################################################
#登录网址
driver=webdriver.Edge()     #打开浏览器
driver.get(url)
#等待页面加载
driver.maximize_window()  
driver.implicitly_wait(60)
#跳转至登录页面
login_button = driver.find_element(By.CSS_SELECTOR, 
            '.rhpane__top-icons__login-button.size-s[data-do="rqstOpen,login"]')        #登录按钮定位
login_button.click()            #点击登录按钮
#输入账户
username_input = driver.find_element(By.ID, 'email')  # 修改为实际的元素ID  
username_input.send_keys(email)  
#输入密码
password_input = driver.find_element(By.ID, 'password')  # 修改为实际的元素ID  
password_input.send_keys(password)  
#点击登录
login_button1 = driver.find_element(By.ID, 'submitLogin')  
login_button1.click()  
#等在加载完成
time.sleep(10)        #若因为网络原因，可以输入强制等待时间

#点击未来10天预测
wait = WebDriverWait(driver, 90)  # 等待最多50秒  
button=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
     ".extended.bg-red.fg-white.inlined.clickable.svelte-5s8s97.extended--vertical[data-icon-after='g']")))  
button.click() 
time.sleep(5)        #若因为网络原因，可以输入强制等待时间

#获取网页源代码
html=driver.page_source
#退出浏览器
driver.quit()
time.sleep(2)        #强制停滞时间
###########################################网页数据提取##################################################
#print(html)
#解析网页源代码
soup=BeautifulSoup(html,'html.parser') 
#查找定位数据
days=soup.find('tr',class_='td-days height-days')
hours=soup.find('tr',class_='td-hour height-hour d-display-waves')
temp=soup.find('tr',class_='td-temp height-temp d-display-waves')
wind=soup.find('tr',class_='td-windCombined height-windCombined d-display-waves')
waves=soup.find('tr',class_='td-waves height-waves d-display-waves')
swell=soup.find('tr',class_='td-swell1 height-swell1 d-display-waves')
swellPeriod=soup.find('tr',class_='td-swell1Period height-swell1Period d-display-waves')

tr_tagsday=days.select('tr td')               #天数
tr_tagshour=hours.select('tr td')               #小时
tr_tagstemp1=temp.select('tr td')               #温度
tr_tagstwind2=wind.get_text()  #风
tr_tagstwind1=wind.select('small')  #阵风
tr_tagswaves1=waves.select('tr td')                #海浪
tr_tagsswell11=swell.select('tr td')             #涌浪
tr_tagsswell1Period1=swellPeriod.select('tr td')   #涌浪周期

########################################数据处理（提取成数列，便于输出）#######################################
#天
listdays=[]
for i in range(len(tr_tagsday)):
    listdays.append(tr_tagsday[i].get_text())
    pass
print(listdays)
#小时
listhour=[]
for i in range(len(tr_tagshour)):
    listhour.append(tr_tagshour[i].get_text())
    pass

#温度
listTemp=[]
for i in range(len(tr_tagstemp1)):
    listTemp.append(tr_tagstemp1[i].get_text())
    pass

#风向 
soupwind = BeautifulSoup(str(wind), 'html.parser')  
divswind = soupwind.find_all('div')  
# 遍历div元素，并提取rotate()函数中的角度值  
angleswind = []  
# 遍历div元素，并提取rotate()函数中的角度值  
for div in divswind:  
    # 检查div的style属性是否存在  
    style = div.get('style')  
    if style:  
        # 使用正则表达式查找rotate()函数中的角度值  
        pattern = r'rotate\((\d+)deg\)'  
        match = re.search(pattern, style)  
        # 如果找到了匹配项，则将其添加到angles列表中  
        if match:  
            angleswind.append(int(match.group(1)))  
print(angleswind)
#阵风
listsmallWind=[]
for i in range(len(tr_tagstwind1)):
    listsmallWind.append(tr_tagstwind1[i].get_text())
    pass

#风
listWind=tr_tagstwind2.split('#')
listWind=list(filter(None, listWind))       #删除空值
for i in range(len(listWind)):
    listWind[i]=listWind[i][:len(listWind[i])-len(listsmallWind[i])]
    pass

#海浪
listwaves=[]
for i in range(len(tr_tagswaves1)):
    listwaves.append(tr_tagswaves1[i].get_text())
    listwaves[i]=listwaves[i].strip('#')
    pass

#海浪方向
soupwaves = BeautifulSoup(str(waves), 'html.parser')  
divswaves = soupwaves.find_all('div')   
angleswaves = []  
for div in divswaves:  
    # 检查div的style属性是否包含rotate  
    if 'rotate' in div.get('style', ''):  
        # 使用正则表达式从style属性中提取角度值  
        import re  
        pattern = r'rotate\((\d+)deg\)'  
        matches = re.findall(pattern, div.get('style'))  
        # 假设我们只对第一个rotate值感兴趣（如果有多个的话）  
        if matches:  
            angleswaves.append(matches[0])
            pass
        pass
    pass
print(angleswaves)

#涌浪
listswell11=[]
for i in range(len(tr_tagsswell11)):
    listswell11.append(tr_tagsswell11[i].get_text())
    listswell11[i]=listswell11[i].strip('#')
    pass
print(len(listswell11))

#涌浪方向
soupswell = BeautifulSoup(str(swell), 'html.parser')  
divsswell = soupswell.find_all('div')   
anglesswell = []  
for div in divsswell:  
    # 检查div的style属性是否包含rotate  
    if 'rotate' in div.get('style', ''):  
        # 使用正则表达式从style属性中提取角度值  
        import re  
        pattern = r'rotate\((\d+)deg\)'  
        matches = re.findall(pattern, div.get('style'))  
        # 假设我们只对第一个rotate值感兴趣（如果有多个的话）  
        if matches:  
            anglesswell.append(matches[0])
            pass
        pass
    pass
print(len(anglesswell))

#涌浪周期
well1Period1=tr_tagsswell1Period1
listwell1Period1=[]
for i in range(len(tr_tagsswell1Period1)):
    listwell1Period1.append(tr_tagsswell1Period1[i].get_text())
    pass

#整合数据
df = pd.DataFrame({
    '小时':listhour,
    '温度': listTemp,  
    '阵风': listsmallWind,  
    '风': listWind, 
    '风向':angleswind,
    "海浪":listwaves,
    '海浪方向':angleswaves,
    "浪涌":listswell11,
    '浪涌方向':anglesswell,
    "浪涌周期":listwell1Period1
    })
print(df)
print(listdays)

########################################数据输出#######################################
# 将DataFrame写入Excel文件，不保存索引  
with pd.ExcelWriter(filepath, engine='openpyxl') as writer:  
    df.to_excel(writer, sheet_name='Sheet1', index=False)  
    pass
