#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:44:01 2017

@author: dustin
"""

import requests,pymysql
conn = pymysql.connect(host='127.0.0.1',
                       port=3306, 
                       user='root', 
                       passwd='123456', 
                       db='coworking',
                       charset='utf8')
cur = conn.cursor()

url="http://i.krspace.cn/api/krspace-gateway-wap/portals/get-community-info?cityId=0&source="
r=requests.get(url)
a=r.json()
for i in a['data']['items']:
    dlprice=0
    kfprice=0
    stationList = i["stationList"]
    for x in stationList:
        if x['typeName']=="独立工作区" and len(x)==3:
            dlprice=x['price']
        elif x['typeName']=="开放工作区" and len(x)==3:
            kfprice=x['price']
    communityName = i['communityName']
    cityName = i['cityName'].split('市')[0]
    detailAddress = i['detailAddress']
    area = i['area']
    stationNum = i['stationNum']
    communityDesc = i['communityDesc'] 
    try:
        sql= "INSERT INTO 空间 (id,空间名,城市,地址,面积,工位数,开放租金,独立租金,其他) VALUES ('氪空间','%s','%s','%s','%s','%s','%s','%s','%s')" % (communityName,cityName,detailAddress,area,stationNum,kfprice,dlprice,communityDesc)
        cur.execute(sql)  
    except:
        continue

#提交修改
conn.commit()
#关闭连接
cur.close()
conn.close()