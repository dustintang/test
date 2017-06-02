#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 19:50:18 2017

@author: dustin
"""

import requests,pymysql
from bs4 import BeautifulSoup

##连接数据库
conn = pymysql.connect(host='127.0.0.1',
                       port=3306, 
                       user='root', 
                       passwd='123456', 
                       db='coworking',
                       charset='utf8')
cur = conn.cursor()
'''
###优客工场官网____________
url0='https://www.urwork.cn'
url="https://www.urwork.cn/workshop"
r=requests.get(url)
soup=BeautifulSoup(r.text,'lxml')
a=soup.find_all('a',{'target':'_blank'})
##写入所需空间的“其他”
for i in a:
    url1=url0+i.attrs['href']
    r1=requests.get(url1)
    soup1=BeautifulSoup(r1.text,'lxml')
    b=soup1.find('div',{'class':'slide-text'}).h1.text
    c=soup1.find('div',{'class':'floor-body areas-intro'}).p.text.strip()
    if c == "" :
        c=soup1.find('div',{'class':'floor-body areas-intro'}).p.next_sibling.text.strip()
    try:
        sql = 'update 空间 set 其他="' + c + '" where 空间名 ="' + b + '"'
        cur.execute(sql)  
    except:
        continue

###侠客岛写入____________
url='http://www.hi-coffice.com/Space/space_list.html'
r=requests.get(url)
soup=BeautifulSoup(r.text,'lxml')
a=soup.find_all('div',{'class':'padding-20 padding-t-none'})
b=soup.find_all('p',{'class':'text-gray space-list-item-introduction'})
for i in range(len(a)):
    a1=a[i].h3.text
    b1=a[i].p.text
    c1=b[i].text
    sql= "INSERT INTO 空间 (id,空间名,地址,其他) VALUES ('侠客岛','%s','%s','%s')" % (a1,b1,c1)
    cur.execute(sql)  
'''
##米域写入________________
url0='http://api.mixpace.com/index.php/api/space/sitespace/lan/zh/spaceid/'
for i in range(1,10):
    url=url0 + str(i)
    r=requests.get(url)
    web = r.json()
    a=web['result'][0]['mixpace_name']
    b=web['result'][0]['mixpace_address'].split('：')[1]
    c=web['result'][0]['mixpace_num1']
    d=web['result'][0]['mixpace_num4']
    e=web['result'][0]['mixpace_content']
    sql= "INSERT INTO 空间 (id,城市,空间名,地址,工位数,面积,其他) VALUES ('米域','上海','%s','%s','%s','%s','%s')" % (a,b,c,d,e)
    cur.execute(sql)  

#提交修改
conn.commit()
#关闭连接
cur.close()
conn.close()




