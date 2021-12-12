# -*- coding: utf-8 -*-
# @Time    : 2021/12/12 16:30
# @Author  : Blessing,wuye9999
# 手厅 签到页面 超简单任务和大奖励任务
import os,sys
import requests,json,time,re,login,logging,traceback,os,random,datetime,util

class dailySign_2:
    def run(self, client, user):
        self.client=client
        self.user=user
        self.ua="Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:"+self.user["username"]+"};devicetype{deviceBrand:Xiaomi,deviceModel:Redmi Note 7};{yw_code:}"
        self.client.headers={
            'content-length': '19',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://img.client.10010.com',
            'sec-fetch-dest': 'empty',
            'user-agent': self.ua,
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'com.sinovatech.unicom.ui',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://img.client.10010.com/SigininApp/index.html',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        try:
            self.getIntegral()  # 获取set-cookie: SigninApp
            self.signin_daySign()   # 签到
            self.superEasy_getTask()   # 超简单任务列表 
            self.bigRew_getTask()       # 大奖励任务
        except Exception as e:
            logging.error(f"【签到任务】: 错误\n{e}")

    # 获取set-cookie: SigninApp
    def getIntegral(self):
        # url="https://act.10010.com/SigninApp/signin/getIntegral"
        # self.client.post(url)
        url = 'https://act.10010.com/SigninApp/signin/getContinuous'
        resp = self.client.post(url=url)

    # 签到
    def signin_daySign(self):
        res=self.client.post("https://act.10010.com/SigninApp/signin/daySign").json()
        logging.info(f"【签到任务】: {res}")

    # 超简单任务列表
    def superEasy_getTask(self,f=0):
        # 做任务
        url=f"https://act.10010.com/SigninApp/superSimpleTask/getTask"   
        data='floorMark=superEasy'
        res=self.client.post(url,data=data).json()
        for task in res['data']:
            achieve=task.get('achieve','0')
            title=task.get('title',None)
            taskId=task.get('taskId',False)
            taskType=task.get('taskType','1')
            allocation=task.get("allocation",'1')
            logging.info(f"【签到任务】: 开始任务 {title}")
            if achieve!=allocation and taskId:
                try:
                    self.superEasy_accomplishDotask(taskId,title,taskType)
                    if f<10:
                        return self.superEasy_getTask(f+1)
                except Exception as e:
                    logging.error(f"【签到任务】: 错误\n{e}")
            else:
                logging.info(f"【签到任务】: 任务已经做过了")

        # 领取奖励
        url=f"https://act.10010.com/SigninApp/superSimpleTask/getTask"   
        data='floorMark=superEasy'
        res=self.client.post(url,data=data).json()
        for task in res['data']:
            achieve=task.get('achieve','1')
            title=task.get('title',None)
            taskId=task.get('taskId',False)
            taskType=task.get('taskType','1')
            allocation=task.get("allocation",'1')
            logging.info(f"【签到任务】: 开始领取奖励 {title}")
            if int(achieve)>0 and taskId:
                try:
                    self.superEasy_doTaskS(taskId,taskType)
                except Exception as e:
                    logging.error(f"【签到任务】: 错误\n{e}")
            else:
                logging.info(f"【签到任务】: 奖励已经领取过了")     


    # 完成超简单任务
    def superEasy_accomplishDotask(self,taskId,title,taskType):
        url= "https://act.10010.com/SigninApp/simplyDotask/accomplishDotask"

        data={"taskId":taskId,"systemCode":"QDQD","orderId":"","taskName":title,"taskType":taskType}
        res=self.client.post(url,json=data).json()
        logging.info(f"【签到任务】: {res}")

        data={"taskId":taskId,"systemCode":"QDQD","orderId":"","taskName":title,"taskType":"1"}
        res=self.client.post(url,json=data).json()
        logging.info(f"【签到任务】: {res}")

    # 完成超简单任务后领取奖励
    def superEasy_doTaskS(self,taskId,taskType):
        url="https://act.10010.com/SigninApp/simplyDotask/doTaskS"

        data=f"taskId={taskId}&taskType={taskType}"
        res=self.client.post(url,data=data).json()
        logging.info(f"【签到任务】: {res}")

        data=f"taskId={taskId}&taskType=1"
        res=self.client.post(url,data=data).json()
        logging.info(f"【签到任务】: {res}")
        
    # 大奖励任务列表
    def bigRew_getTask(self,f=0):
        url=f"https://act.10010.com/SigninApp/superSimpleTask/getTask"   
        data='floorMark=bigRew'
        res=self.client.post(url,data=data).json()
        for task in res.get('data'):
            achieve=task.get('achieve','0')
            title=task.get('title',None)
            taskId=task.get('taskId',False)
            taskType=task.get('taskType','1')
            allocation=task.get("allocation",'1')
            logging.info(f"【签到任务】: 开始任务 {title}")
            if achieve!=allocation and taskId:
                try:
                    self.bigRew_doTaskS(taskId)
                    if f<10:
                        return self.bigRew_getTask(f+1)
                except Exception as e:
                    logging.error(f"【签到任务】: 错误\n{e}")
            else:
                logging.info(f"【签到任务】: 任务已经做过了")

    # 完成大奖励任务后领取奖励
    def bigRew_doTaskS(self,taskId):
        url="https://act.10010.com/SigninApp/simplyDotask/doTaskS"

        data=f"taskId={taskId}"
        res=self.client.post(url,data=data).json()
        logging.info(f"【签到任务】: {res}")

