# -*- coding: utf-8 -*-
# @Time    : 2021/11/30 16:30
# @Author  : wuye9999
# 天天抽红包
# 入口》我的》天天抽红
import os,sys
sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/task')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/tenscf_rely')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/unicom-task/task')
import requests,json,time,re,login,logging,traceback,os,random,datetime,util
from lxml.html import fromstring

class every_day_redEnvelope:
    def run(self, client, user):
        self.client,self.user=client,user
        self.session=requests.session()
        self.session.headers.update({
            'Connection': 'keep-alive',
            'Content-Length': '462',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'https://canting.17wo.cn',
            'ckc': 'CODE',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; RMX1901 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:' + self.user['username'] + '};devicetype{deviceBrand:Realme,deviceModel:RMX1901};{yw_code:}',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Dest': 'empty',
            'token': '',
            'X-Requested-With': 'com.sinovatech.unicom.ui',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://canting.17wo.cn/mealticket-activities/lucky-draw/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        cookies_dict = requests.utils.dict_from_cookiejar(self.client.cookies)
        ecs_token=cookies_dict['ecs_token']

        userId,userCustId,cityCode=self.login_getUserInfo(ecs_token)        # 获取userId
        token=self.login_nologin(ecs_token,userId)                          # 登录获取token

        self.lottery_lottery(token,userCustId,cityCode)     # 抽奖

    # 获取userId
    def login_getUserInfo(self,ecs_token):
        url='https://canting.17wo.cn/share-center-activity/login/getUserInfo'
        data={
            "data":{"token":ecs_token+"="},
            "channelId":"","randomCode":"","sdt":"","sign":"","time":int(time.time() * 1000),"useChannel":"ANDROID","version":""
        }
        res=self.session.post(url,json=data).json()
        try:
            if res['code']=='200':
                userId=res['data']['userId']
                userCustId=res['data']['userCustId']
                cityCode=res['data']['cityCode']
                return userId,userCustId,cityCode
            else:
                logging.info('获取userId失败')
        except:
            logging.error(f'错误\n{res}')

    # 登录获取token
    def login_nologin(self,ecs_token,userId):
        url='https://canting.17wo.cn/share-center-activity/login/nologin'
        data={
            "data":{"code":ecs_token+"=","phone":userId},
            "channelId":"","randomCode":"","sdt":"","sign":"","time":int(time.time() * 1000),"useChannel":"ANDROID","version":""
        }
        res=self.session.post(url,json=data).json()
        try:
            if res['code']=='200':
                token=res['data']['token']
                return token
            else:
                logging.info('获取token失败')
        except:
            logging.error(f'错误\n{res}')

    # 抽奖
    def lottery_lottery(self,token,userCustId,cityCode):
        url='https://canting.17wo.cn/share-center-activity/lottery/lottery'
        self.session.headers.update({
            'token':token,
        })
        data={
            "data":{"custId":userCustId,"regionCode":cityCode,"submitCityLocation":cityCode},
            "channelId":"","randomCode":"","sdt":"","sign":"","time":int(time.time() * 1000),"useChannel":"ANDROID","version":""
        }
        res=self.session.post(url,json=data).json()
        try:
            if res['code']=='200':
                msg=res['msg']
                if not msg:
                    logging.info(f"抽到 {res['data']['desc']}")
                else:
                    logging.info(msg)
            else:
                logging.info(res)
        except:
            logging.error(f'错误\n{res}')


