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

        url=self.new_auth() # 登录1
        self.deal(url)      # 登录2
        self.startQiandao() # 签到


    # 登录1
    def new_auth(self):
        url=f"https://uac.10010.com/oauth2/new_auth?req_time={str(int(time.time() * 1000))}"   
        headers={
            'content-length': '305',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'origin': 'https://uac.10010.com',
            'x-requested-with': 'XMLHttpRequest',
            'sec-fetch-dest': 'empty',
            'user-agent': self.ua,
            'content-type': 'application/x-www-form-urlencoded',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://uac.10010.com/oauth2/new_auth?display=wap&page_type=06&redirect_uri=http%3A%2F%2Fm.jf.10010.com%2Fdeal&app_code=ECS-JF&_v=1&state=https%3A%2F%2Fm.jf.10010.com%2Fcms%2Fyuech%2Factivity%2Fdbe%2Findex.html%23%2F%3FsharePhone%3D15555555555_WX_711',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }  
        data=f"app_code=ECS-JF&user_id={self.user.get('username')}&user_pwd={self.user.get('password')}&user_type=01&pwd_type=01&display=web&response_type=code&redirect_uri=http%3A%2F%2Fm.jf.10010.com%2Fdeal&is_check=1&verifyCKCode=822653&state=https%3A%2F%2Fm.jf.10010.com%2Fcms%2Fyuech%2Factivity%2Fdbe%2Findex.html%23%2F%3FsharePhone%3D15555555555_WX_711"
        res=self.client.post(url,headers=headers,data=data).json()
        try:
            redirectUri=res['redirectUri']
            code=res['code']
            url=redirectUri+'?ticket='+code
            return url
        except:
            logging.error('登录失败')

    def deal(self,url):
        headers={
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
        res=self.client.get(url,headers=headers).text
        logging.info(res)
        res=self.client.get(url,headers=headers).text
        logging.info(res)

    def startQiandao(self):
        url="https://m.jf.10010.com/jf-yuech/p/qiandao11/api/startQiandao"
        headers={
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
        res=self.client.post(url,headers=headers,data=data).json()
        logging.info(res)
