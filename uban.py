#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 23:17:13 2017

@author: dustin
"""
import requests,pymysql
from bs4 import BeautifulSoup

##连接数据库
conn = pymysql.connect(host='127.0.0.1',
                       port=3306, 
                       user='root', 
                       passwd='123456', 
                       db='uban',
                       charset='utf8')
cur = conn.cursor()
#读取二级网页并写入
def wr(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'lxml')
    try:
        a=soup.find('div',{'class':'title_tag'})
        a1=a.h1.text
        a2=a.i.text
        '''
        b=soup.find_all('em',{'class':'font26'})
        b1=b[0].text
        b2=b[1].text
        c=soup.find_all('em',{'style':'width:178px'})
        c1=c[0].text.split('个')[0]
        c2=c[1].text.split('个')[0]
        d=soup.find_all('em',{'class':'bor_r_none'})
        d1=d[0].text.split('m')[0]
        d2=d[1].text.split('m')[0]
        '''
        e=soup.find_all('dd')
        e1=e[1].text.split('：')[1].split('m')[0]
        e2=e[1].text.split('：')[2].split('层')[0]
        e3=e[2].text.split('：')[1].split('m')[0]
        e4=e[2].text.split('：')[2].split('m')[0]
        e5=e[3].text.split('：')[1].split('%')[0]
        e6=e[3].text.split('：')[2]
        f=soup.find('p',{'class':'t2 text-justify'}).text.strip()
        #写入
        sql= "INSERT INTO 空间 (空间名,地址,建筑面积,层数,平均工位面积,净层高,公共空间占比,物业,简介) VALUES ('%s','%s',%s,%s,%s,%s,%s,'%s','%s')"  % (a1,a2,e1,e2,e3,e4,e5,e6,f)    
        cur.execute(sql)  
    except:
        print(url)
#读取uban_list
url0='http://sh.uban.com'
url="http://sh.uban.com/lianhebangong-k2/#officelist"
r=requests.get(url)
soup=BeautifulSoup(r.text,'lxml')
office=soup.find('ul',{'class':'jppyul'}).find_all('a')
for i in office:
    x=i.attrs['href']
    x=url0 + x
    wr(x)
    

#提交修改
conn.commit()
#关闭连接
cur.close()
conn.close()