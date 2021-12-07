# -*- coding: utf8 -*-
# @rhming
import requests,logging,json,time
from random import randint
from utils.toutiao_reward import TouTiao


class dailySign:
    """
        联通日常签到
    """
    def _init_(self, client, user):
        self.useragent='Mozilla/5.0 (Linux; Android 9; RMX1901 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:' + user.get('username') + '};devicetype{deviceBrand:Realme,deviceModel:RMX1901};{yw_code:}'
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "accept": "application/json, text/plain, */*",
            "origin": "https://img.client.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://img.client.10010.com/SigininApp/index.html",
            "x-requested-with": "com.sinovatech.unicom.ui"
        })
        self.hasDouble = False
        self.toutiao = TouTiao(user.get('username'))

    def listTaskInfo(self):
        url = 'https://act.10010.com/SigninApp/convert/listTaskInfo'
        resp = self.session.post(url=url)
        result = resp.json()
        # logging.info(result)
        paramsList = result['data']['paramsList']
        logging.info("[气泡任务]")
        for item in paramsList:
            logging.info(f'{item["prizeName"]}: {"已完成" if int(item["accomplish"]) else "未完成"} {item.get("startTime","")} {item.get("prizePrice","")}')
        return paramsList

    def doTask(self, item, orderId):
        url = 'https://act.10010.com/SigninApp/task/doTask'
        data = {
            "markId": item['markId'],
            "orderId": orderId,
            "prizeType": item['prizeType'],
        }
        resp = self.session.post(url=url, data=data)
        try:
            logging.info(f"{resp['data']['prizeName']} {resp['data']['statusDesc']} {resp['data']['returnStr']}")
            logging.info(f"{resp['data']['taskLogo']}")
        except:
            logging.info(resp.json())


    def getIntegral(self):
        url = 'https://act.10010.com/SigninApp/signin/getIntegral'
        resp = self.session.post(url=url)
        logging.info(resp.json())

    def getContinuous(self):
        url = 'https://act.10010.com/SigninApp/signin/getContinuous'
        resp = self.session.post(url=url)
        result = resp.json()
        # logging.info(result)
        data = result['data']  # ['daySignList']
        # try:
        #     btnName=data['daySignList'].get('exitBtnInfo').get('btnName')
        #     name=data['daySignList'].get('exitBtnInfo').get('name')
        # except:
        #     btnName='no'
        #     name='no'
        # logging.info(f"{btnName} {name}")
        doubleBtn = data['doubleBtn']
        logging.info('[签到任务]')
        if int(doubleBtn['click']) == 1:
            self.hasDouble = True
            logging.info('红包翻倍: 未翻倍')
        else:
            logging.info('红包翻倍: 已翻倍')
        if int(data['todaySigned']) == 0:
            logging.info('每日签到: 已签到')
            return True
        logging.info('每日签到: 未签到')

    def getGoldTotal(self):
        url = 'https://act.10010.com/SigninApp/signin/getGoldTotal'
        resp = self.session.post(url=url)
        logging.info(resp.json().get('msg',resp.text))

    def signIn(self):
        url = 'https://act.10010.com/SigninApp/signin/daySign'
        resp = self.session.post(url=url)
        resp.encoding = 'utf8'
        data = resp.json()
        logging.info(data.get('msg',data))

    def bannerAdPlayingLogo(self, orderId):
        # signin
        url = 'https://act.10010.com/SigninApp/task/bannerAdPlayingLogo'
        data = {
            "orderId": orderId
        }
        resp = self.session.post(url=url, data=data)
        logging.info(resp.json().get('msg',resp.text))

    def run(self, client, user):
        self.session=client
        self._init_(client, user)

        # if self.last_login_time.find(self.now_date) == -1:
        #     self.onLine()
        if not self.getContinuous():
            self.signIn()
            # self.getGoldTotal()
            # self.getIntegral()
            self.getContinuous()
        if self.hasDouble:
            time.sleep(randint(10, 15))
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 945535743,
                'channelName': 'android-签到看视频翻倍得积分-激励视频',
                'remark': '签到成功看视频再得奖',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            self.bannerAdPlayingLogo(orderId)
        for item in self.listTaskInfo():
            if int(item['accomplish']) or not int(item['click']):
                continue
            time.sleep(randint(25, 30))
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 945558051,
                'channelName': 'android-签到气泡任务-激励视频',
                'remark': '签到页头气泡看视频得奖励',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            self.doTask(item, orderId)
        time.sleep(randint(3, 5))
        # self.message = ''
        self.getContinuous()
        self.listTaskInfo()
        # self.recordLog(self.message)


if __name__ == '__main__':
    pass
