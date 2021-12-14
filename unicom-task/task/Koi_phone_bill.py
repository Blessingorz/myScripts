# -*- coding: utf-8 -*-
# @Time    : 2021/12/11 16:30
# @Author  : wuye9999
# 手厅 沃邮箱12.12锦鲤送话费
import os,sys
import requests,json,time,re,login,logging,traceback,os,random,datetime,util

class Koi_phone_bill:
    def run(self, client, user):
        self.client=client
        self.user=user
        self.ua="Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:"+self.user["username"]+"};devicetype{deviceBrand:Xiaomi,deviceModel:Redmi Note 7};{yw_code:}"

        try:
            mobile,refererurl=self.openPlatLineNew() # 登录1
            self.summer1login(refererurl)
            self.callback(mobile,refererurl)    # 获取token
            self.userInfo()
            self.user_chance()
            self.overtask()                     # 做任务
            self.draw()                         # 抽奖
        except Exception as e:
            logging.error(f"【锦鲤送话费】:错误\n{e}")

    # 登录1
    def openPlatLineNew(self):
        url=f"https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url=https://user.mail.wo.cn/cu-email/mobile/jump11&yw_code=&desmobile={self.user['username']}&version=android@8.0805"   
        headers={
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': self.ua,
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'x-requested-with': 'com.sinovatech.unicom.ui',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }  
        res=self.client.get(url,headers=headers)
        logging.info(res)
        try:
            mobile=re.findall(r'mobile=(.*?)&', res.url)[0]
            mobile=re.sub(r'\+', '%2B', mobile)
            # logging.info(mobile)
            # logging.info(res.url)
            return mobile,res.url
        except Exception as e:
            logging.error(f"【锦鲤送话费】:验证登录失败\n{e}")

    def summer1login(self,url):
        # self.client.headers={
        #     'pragma': 'no-cache',
        #     'cache-control': 'no-cache',
        #     'accept': '*/*',
        #     'sec-fetch-dest': 'empty',
        #     'x-requested-with': 'XMLHttpRequest',
        #     'user-agent': self.ua,
        #     'sec-fetch-site': 'same-origin',
        #     'sec-fetch-mode': 'cors',
        #     'accept-encoding': 'gzip, deflate',
        #     'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        # }
        self.client.get(url)

    # 获取token
    def callback(self,mobile,refererurl):
        # self.session=requests.session()
        self.client.headers.update({
            'referer': refererurl
        })
        url=f"https://activity.mail.wo.cn/cn/summer1/login/callback.do?mobile={mobile}"
        res=self.client.get(url)
        if 'Set-Cookie' in res.headers or 'set-cookie' in res.headers:
            return True
        else:
            logging.info("【锦鲤送话费】: 获取token失败")

    def userInfo(self):
        url=f"https://activity.mail.wo.cn/cn/summer1/login/userInfo.do?t={str(int(time.time() * 1000))}"
        res=self.client.get(url)

    def user_chance(self):
        url=f"https://activity.mail.wo.cn/cn/summer1/user/chance.do?t={str(int(time.time() * 1000))}"
        res=self.client.get(url)

    # 已完成任务列表
    def overtask(self):
        tasks_dict={
            'loginmail': '每日首次进入邮箱',
            'knowmail': '查看沃邮箱5大优势',
            'wodisk': '速览沃云盘优势',
        }
        overtask_list=list()
        url=f"https://activity.mail.wo.cn/cn/summer1/user/overtask.do?t=?t={str(int(time.time() * 1000))}"
        res=self.client.get(url).json()

        for task in res['result']:
            # logging.info(task)
            taskName=task.get('taskName','')
            overtask_list.append(taskName)

        for taskName,taskid in tasks_dict.items():
            logging.info(f"【锦鲤送话费】:开始任务 {taskid}")
            if taskName not in overtask_list:
                self.dotask(taskName)
            else:
                logging.info("【锦鲤送话费】: 任务已做过了")

    # 做任务
    def dotask(self,taskName):
        url=f"https://activity.mail.wo.cn/cn/summer1/user/doTask.do?taskName={taskName}"
        res=self.client.get(url).json()
        if res['msg']==None:
            logging.info("【锦鲤送话费】: 任务成功")
        else:
            logging.info(f"【锦鲤送话费】: {res.get('msg','任务失败')}")

    # 抽奖
    def draw(self):
        url=f"https://activity.mail.wo.cn/cn/summer1/draw/draw.do?t={str(int(time.time() * 1000))}"
        res=self.client.get(url).json()
        if res['success']:
            logging.info(f"【锦鲤送话费】: 抽到 {res['result'].get('prizeTitle','空气')}")
            return self.draw()
        else:
            logging.info(f"【锦鲤送话费】:{res['msg']}")
