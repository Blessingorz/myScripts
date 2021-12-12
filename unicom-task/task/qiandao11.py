# -*- coding: utf-8 -*-
# @Time    : 2021/12/11 16:30
# @Author  : wuye9999
# 百万积分-引爆1212
import os,sys
import requests,json,time,re,login,logging,traceback,os,random,datetime,util

class qiandao11:
    def run(self, client, user):
        self.client=client
        self.user=user
        self.ua='Mozilla/5.0 (Linux; Android 9; RMX1901 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:' + self.user.get('username') + '};devicetype{deviceBrand:Realme,deviceModel:RMX1901};{yw_code:}'

        self.openPlatLineNew() # 登录1
        self.saveQiandaoLog()
        self.startQiandao() # 签到

    # 登录1
    def openPlatLineNew(self):
        url=f"https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url=https://m.jf.10010.com/jf-order/avoidLogin/forActive/dbeo"   
        self.client.headers={
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'X-Requested-With': 'com.sinovatech.unicom.ui',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }  
        res=self.client.get(url)
        # logging.info(res.url)

    def startQiandao(self):
        url="https://m.jf.10010.com/jf-yuech/p/qiandao11/api/startQiandao"
        self.client.headers={
            'content-length': '59',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://m.jf.10010.com',
            'authorization': 'bearer ee52680a-0196-48de-9d12-733897160e60',
            'sec-fetch-dest': 'empty',
            'user-agent': self.ua,
            'x-requested-with': 'com.sinovatech.unicom.ui',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://m.jf.10010.com/cms/yuech/activity/dbe/index.html',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        data={"activityId":"Ac-leijiqiandao3","accountId":"15555555555"}
        res=self.client.post(url,json=data).json()
        # logging.info(res)
    def saveQiandaoLog(self):
        url="https://m.jf.10010.com/jf-yuech/p/qiandao11/api/saveQiandaoLog"
        self.client.headers={
            'content-length': '59',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://m.jf.10010.com',
            'authorization': 'bearer ee52680a-0196-48de-9d12-733897160e60',
            'sec-fetch-dest': 'empty',
            'user-agent': self.ua,
            'x-requested-with': 'com.sinovatech.unicom.ui',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://m.jf.10010.com/cms/yuech/activity/dbe/index.html',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        data={"activityId":"Ac-leijiqiandao3","buttonId":"主页-签到","type":1}
        res=self.client.post(url,json=data).json()
        if res['code']==0:
            logging.info('【百万积分-引爆1212】: 签到成功，获得积分 10')
        else:
            logging.info(f"【百万积分-引爆1212】: {res}")

