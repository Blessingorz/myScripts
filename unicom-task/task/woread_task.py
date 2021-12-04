# -*- coding: utf-8 -*-
# @Time    : 2021/12/1 23:30
# @Author  : rhming
# 沃阅读: 每日阅读抽奖大活动
import os,sys
import requests,login,logging,urllib.parse,util,re,execjs,time

class woread_task:
    def run(self, client, user):
        self.client,self.user=client,user
        self.session=requests.session()
        self.session.headers= {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; RMX1901 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:' + self.user['username'] + '};devicetype{deviceBrand:Realme,deviceModel:RMX1901};{yw_code:}',
            'Origin': 'http://st.woread.com.cn',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        cookies_dict=login.readData(self.user['username']+'woread_task_popupListInfo_cookies')  # 读取cookie
        if cookies_dict:
            cookies=requests.utils.cookiejar_from_dict(cookies_dict)
            self.session.cookies=cookies

        if self.popupListInfo():    # 验证登录吗？
            pass
        else:
            if not self.login():    # 登录
                return
            if not self.popupListInfo():    # 验证登录吗？
                return 

        self.luckdraw_run()     # 抽奖

    # 登录
    def login(self):
        phonenum=self.getEncryptMobile()
        if not phonenum:
            return
        url = 'https://st.woread.com.cn/touchextenernal/common/shouTingLogin.action'
        data = {
            'phonenum': phonenum
        }
        resp = self.session.post(url=url, data=data)
        if not self.session.cookies.get('useraccount', False):
            logging.error('【沃阅读】: 登录失败,结束执行任务')
            return
        else:
            logging.info('【沃阅读】: 登录成功')
            return True

    # 加密登陆数据
    def getEncryptMobile(self):
        with open('./utils/security.js', 'r', encoding='utf8') as fr:
            securityJs = fr.read()
        scriptText = '''
        function getEncryptMobile(mobile) {
            var modulus = "00A828DB9D028A4B9FC017821C119DFFB8537ECEF7F91D4BC06DB06CC8B4E6B2D0A949B66A86782D23AA5AA847312D91BE07DC1430C1A6F6DE01A3D98474FE4511AAB7E4E709045B61F17D0DC4E34FB4BE0FF32A04E442EEE6B326D97E11AE8F23BF09926BF05AAF65DE34BB90DEBDCEE475D0832B79586B4B02DEED2FC3EA10B3";
            var exponent = "010001";
            var key = window.RSAUtils.getKeyPair(exponent, '', modulus);
            mobile = window.RSAUtils.encryptedString(key, mobile);
            return mobile
        }
        '''
        scriptText = 'var window = {};' + securityJs + scriptText
        try:
            ctx = execjs.compile(scriptText)
            EncryptMobile = ctx.call('getEncryptMobile', self.user['username'])
        except:
            logging.error("【沃阅读】: 没有找到运行JavaScript的环境，退出")
            return
        return EncryptMobile

    # 验证登录吗？
    def popupListInfo(self):
        url = 'https://st.woread.com.cn/touchextenernal/read/popupListInfo.action'
        resp = self.session.post(url=url)
        try:
            resp.json()
            login.saveData(self.user['username']+'woread_task_popupListInfo_cookies', self.session.cookies.get_dict())
            logging.info('【沃阅读】: cookie登录成功')
            return True
        except:
            # logging.error('【沃阅读】: cookie登录失败')
            return False

    # 沃阅读抽奖 运行
    def luckdraw_run(self):
        try:
            drawNum, currentSeevideoNum = self.seeadvertluckdraw_index()  # 获取 drawNum, currentSeevideoNum
            if currentSeevideoNum == -1 and drawNum < 2:
                self.addUserSeeVideo(str(drawNum))
                drawNum, currentSeevideoNum = self.seeadvertluckdraw_index()  # 获取 drawNum, currentSeevideoNum
            if drawNum == 0:
                logging.info('【沃阅读】: 抽奖次数已用完...')
                return
            logging.info(f'【沃阅读】: 第{6 - drawNum}次抽奖...')
            self.doDraw('NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI=')
            if drawNum == 2:
                self.doDraw('QjRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=')
            time.sleep(1)
            return self.luckdraw_run()
        except Exception as e:
            logging.error(f'【沃阅读】: 错误\n{e}')


    # 沃阅读抽奖 获取 drawNum, currentSeevideoNum
    def seeadvertluckdraw_index(self):
        url = f'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/index.action?channelid=18000687'
        self.session.headers.update({
            'Referer': 'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/index.action?channelid=18000687',
        })
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'
        drawNum = re.findall(r'var drawNum = (\d);', resp.text)[0]
        drawNum = int(drawNum)
        currentSeevideoNum = re.findall(r'var currentSeevideoNum = (-?\d);', resp.text)[0]
        currentSeevideoNum = int(currentSeevideoNum)
        return drawNum, currentSeevideoNum

    # 沃阅读抽奖 ？
    def addUserSeeVideo(self, drawNum):
        url = f'https://st.woread.com.cn/touchextenernal/openbook/addUserSeeVideo.action?num={drawNum}&activityindex=NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI='
        resp = self.session.get(url=url)
        # logging.info(resp.json())

    # 沃阅读抽奖 抽奖
    def doDraw(self, acticeindex):
        url = 'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/doDraw.action'
        '''
                5-21(over): jRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=
                6-21(over): QjRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=
                6-21(start): NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI=
        '''
        data = {
            'acticeindex': acticeindex
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        logging.info(f'【沃阅读】: {result["prizedesc"]}')
