#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 23:17:13 2017
爬好租网所有写字楼数据放到数据库中
@author: dustin
"""
import requests,pymysql
from bs4 import BeautifulSoup
import time
##连接数据库
conn = pymysql.connect(host='127.0.0.1',
                       port=3306, 
                       user='root', 
                       passwd='123456', 
                       db='haozu',
                       charset='utf8')
cur = conn.cursor()
##参数设置
head = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch' ,
        'Accept-Language' : 'zh-CN,zh;q=0.8' ,
        'Connection' : 'keep-alive' ,
        'Host' : 'www.haozu.com' ,
        'Upgrade-Insecure-Requests' : '1' ,
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'        
        }
#读取二级网页并写入    
def getinfo(soup):
    a6=''
    a10=''
    c=''
    d1 = []
    d2 = []
    d3 = []
    #上面
    a = soup.find('div',{'class':'fl detail-office-info'})
    a1 = a.find('span',{'class':'fl'}).text
    a2 = soup.find('a',{'class':'a1'}).text
    _a3 = a.p.find_all('span')
    a3 = _a3[0].find_all('a')[0].text
    a4 = _a3[0].find_all('a')[1].text
    a5 = _a3[0].text.split(']')[1]
    try:
        a6 = _a3[1].text.split('距离')[1].split('号')[0]
        a7 = _a3[1].text.split('号线')[1].split('约')[0]
        a8 = _a3[1].text.split('约')[1].split('米')[0]
    except :
        a7=''
        a8='' 
    x = len(_a3) - 1
    a9 = _a3[x].text.split('个')[0]
    if _a3[x].text.split('个')[x] == '户型)' :
        a10 = _a3[x].text.split('个')[1].split('(')[1]
    a11 = soup.find('div',{'class':'rightPrice'}).text.strip().split('元')[0]
    try:
        a12 = soup.find('div',{'class':'rightBor-txt'}).text.split('有')[1].split('人')[0]
    except:
        a12 = '0'
    #下面
    _b = soup.find('div',{'class':'detail-profile-box f14'}).ul
    _b1 = _b.find_all('div',{'class':'li-t'})
    _b2 = _b.find_all('span',{'class':'li-con'})
    b1 = []
    b2 = []
    for i in _b1:
        b1.append(i.text.strip().split(' ')[0])
    for i in _b2:
        b2.append(i.text)
    if soup.find('div',{'class':'detail-profile-text'}) != None:
        c = soup.find('div',{'class':'detail-profile-text'}).p.text
    #中间
    if soup.find('div',{'class':'nodata'}) == None :
        _d = soup.find('div',{'class':'soho'}).find_all('div',{'class':'fy-info'})
        for i in _d:
            d1.append(i.find('p',{'class':'p2'}).text.split('元')[0])
            d2.append(i.find('div',{'class':'yimg-r fr'}).text)
            d3.append(i.find('i',{'class':'fl f12'}).text)
    return a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,c,d1,d2,d3


#写入
y=[]


for i in range(33000,34000):
    if i % 20 ==0:
        #提交修改
        conn.commit()
        #关闭连接
        cur.close()
        conn.close()
        conn = pymysql.connect(host='127.0.0.1',
                       port=3306, 
                       user='root', 
                       passwd='123456', 
                       db='haozu',
                       charset='utf8')
        cur = conn.cursor()
        print('保存')
    try :
        m = str(i)
        url0 ='http://www.haozu.com/sh_xzl_'
        url = url0 + m
        r=requests.get(url,headers=head)
        soup=BeautifulSoup(r.text,'lxml')  
        if soup.title.text != '您访问的页面不存在！404！':
            info = ()
            info = getinfo(soup)
            info1 = info[12]
            info2 = info[13]
            info3 = info[15]
            info4 = info[16]
            info5 = info[17]
            b = {'写字楼等级':'','总楼层':'','占地面积':'','建筑面积':'','得房率':'','绿化率':'','标准层高':'','客梯数':'','开发商':'','物业公司':'','所属园区':'','已入驻企业':''}
            for i in range(len(info1)):
                b[info1[i]]=info2[i]
            sql1= "INSERT INTO 写字楼 (索引,写字楼,城市,区域,地标,地址,地铁线,地铁站,地铁距离,房源数,户型数,参考价,预约数,写字楼等级,总楼层,占地面积,建筑面积,得房率,绿化率,标准层高,客梯数,开发商,物业公司,所属园区,已入驻企业,简介) \
            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"  \
                   % (m,info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10],info[11],b['写字楼等级'],b['总楼层'],b['占地面积'],b['建筑面积'],b['得房率'],b['绿化率'],b['标准层高'],b['客梯数'],b['开发商'],b['物业公司'],b['所属园区'],b['已入驻企业'],info[14])             
            cur.execute(sql1) 
            for n in range(len(info3)):
                sql = "insert into 写字楼房源 (索引,写字楼,价格,面积,装修) values ('%s','%s','%s','%s','%s')"  % (m,info[0],info3[n],info4[n],info5[n])
                cur.execute(sql)            
            print(m)
            time.sleep(2)
    except :
        y.append(m)
        continue


#提交修改
conn.commit()
#关闭连接
cur.close()
conn.close()

