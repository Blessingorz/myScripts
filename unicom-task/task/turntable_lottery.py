# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 22:30
# @Author  : wuye9999
# 转盘抽奖
# 入口：我的》转盘抽奖
import os,sys
sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/task')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/tenscf_rely')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'unicom-task/task')
import requests,login,logging,urllib.parse,util,re

class turntable_lottery:
    def run(self, client, user):
        self.client=client
        self.user=user
        self.client.headers.update({
            'x-requested-with': 'com.sinovatech.unicom.ui',
        })
        self.openPlatLineNew()  # 获取cookie
        self.powerTask()        # 做任务
        self.lottery()          # 抽奖


    # 获取cookie
    def openPlatLineNew(self):  
        url=f"https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url=https://account.bol.wo.cn/cuuser/open/openLogin/activetemplate?redirectUrl=https://atp.bol.wo.cn/atplottery/ACT202009101956022770009xRb2UQ&product=hfgo&ch=010&yw_code=&desmobile={self.user['username']}&version=android@8.0805"
        res=self.client.get(url)
    # 抽奖
    def lottery(self):
        url=f"https://atp.bol.wo.cn/atpapi/act/lottery/start/v1/actPath/ACT202009101956022770009xRb2UQ/0"
        res=self.client.get(url).json()
        try:
            if res['code']=='3000':
                logging.info(f"【转盘抽奖】：{res['message']}")
            elif res['code']=='0000':
                logging.info(f"【转盘抽奖】：抽到 {res['data']['prizeName']}")
                logging.info(f"【转盘抽奖】: {res['data']['prizeDesc']}")
                return self.lottery()
            else:
                logging.info(f"【转盘抽奖】：\n{res}")
        except:
            logging.error(f'【转盘抽奖】：出错\n{res}')
    # 任务列表
    def powerTask(self):
        url='https://atp.bol.wo.cn/atpapi/lottery/powerTask/517'
        res=self.client.get(url).json()
        try:
            for data in res['data']:
                name=data['name']
                description=data['description']     # 任务名称
                redirectUrl=data['redirectUrl']    
                targetActId=data['targetActId']     # 任务id
                if '签到' in description:
                    url=f"https://atp.bol.wo.cn/atpapi/act/actUserSign/everydaySign?actId={targetActId}"
                    res=self.client.get(url).json()
                    try:
                        logging.info(f"【转盘抽奖】：{res['message']}")
                    except:
                        logging.info(res)
        except:
            logging.error(f'【转盘抽奖】：出错')





