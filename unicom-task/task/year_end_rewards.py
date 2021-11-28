# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 22:30
# @Author  : wuye9999
# 年终亿元回馈活动
# 入口：我的》摇亿元大
import os,sys
sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/task')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/tenscf_rely')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'unicom-task/task')
import requests,login,logging,urllib.parse,util,re

class year_end_rewards:
    def run(self, client, user):
        self.client=client
        self.user=user
        self.client.headers.update({
            'origin': 'https://img.client.10010.com',
            'x-requested-with': 'com.sinovatech.unicom.ui',
            'referer': 'https://img.client.10010.com/2021shuangshiyi/index.html',
        })
        allRemainTimes=self.feedback_feed()    # 查询抽奖次数
        if not allRemainTimes:
            allRemainTimes=0
        self.lottery(allRemainTimes)      # 抽奖

    # 查询抽奖次数
    def feedback_feed(self):  
        url=f"https://m.client.10010.com/feedback/feed/index?invitationCode=&channel=PPHX01&imei={self.user['username']}"
        res=self.client.get(url).json()
        try:
            logging.info(f"【年终亿元回馈】：剩余抽奖次数 {res['data']['allRemainTimes']}")
            return int(res['data']['allRemainTimes'])
        except:
            logging.error(f'【年终亿元回馈】：获取抽奖次数失败\n{res.text}')
    # 抽奖
    def lottery(self,allRemainTimes):
        if allRemainTimes<1:
            return
        url=f"https://m.client.10010.com/feedback/back/lottery?imei={self.user['username']}"
        res=self.client.get(url).json()
        try:
            if res['respCode']=='0000':
                logging.info(f"【年终亿元回馈】：抽到 {res['data']['prizeName']}")
            elif res['respCode']=='0004':
                logging.info(f"【年终亿元回馈】：抽到 {res['respDesc']}")
            else:
                logging.info(f"【年终亿元回馈】：\n{res}")
        except:
            logging.error(f'【年终亿元回馈】：出错\n{res}')
        return self.lottery(int(res['data']['allRemainTimes']))






