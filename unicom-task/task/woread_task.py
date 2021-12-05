# -*- coding: utf-8 -*-
# @Time    : 2021/12/1 23:30
# @Author  : rhming
# 沃阅读: 每日阅读抽奖大活动
import os,sys
import requests,login,logging,urllib.parse,util,re,execjs,time,random,re

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
        self.openbook_run()     # 抽奖
        self.readluchdraw_run()
        self.thanksgiving_run()

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

    # 登录 加密登陆数据
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

    # 登录 验证登录吗？
    def popupListInfo(self):
        url = 'https://st.woread.com.cn/touchextenernal/read/popupListInfo.action'
        resp = self.session.post(url=url)
        try:
            resp.json()
            logging.info('【沃阅读】: cookie登录成功')
            login.saveData(self.user['username']+'woread_task_popupListInfo_cookies', self.session.cookies.get_dict())
            return True
        except:
            # logging.error('【沃阅读】: cookie登录失败')
            return False

    # 沃阅读抽奖 运行
    def luckdraw_run(self):
        try:
            drawNum,currentSeevideoNum=self.seeadvertluckdraw()   # 获取 drawNum, currentSeevideoNum
            if currentSeevideoNum == -1 and drawNum < 2:
                
                url = f'https://st.woread.com.cn/touchextenernal/openbook/addUserSeeVideo.action?num={drawNum}&activityindex=NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI='
                resp = self.session.get(url=url)

                drawNum,currentSeevideoNum=self.seeadvertluckdraw()   # 获取 drawNum, currentSeevideoNum

            if drawNum == 0:
                logging.info('【沃阅读】: 抽奖次数已用完...')
                return
            logging.info(f'【沃阅读】: 第{6 - drawNum}次抽奖...')
            time.sleep(1.2)
            self.doDraw('NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI=')
            if drawNum == 2:
                time.sleep(1.2)
                self.doDraw('QjRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=')

            time.sleep(1.2)
            return self.luckdraw_run()

        except Exception as e:
            logging.error(f'【沃阅读】: 错误\n{e}')

    # 沃阅读抽奖 获取 drawNum, currentSeevideoNum
    def seeadvertluckdraw(self):
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
        return drawNum,currentSeevideoNum


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


    def openbook_run(self):
        try:
            drawNum, currentSeevideoNum = self.openbook_index()
            if currentSeevideoNum == -1 and drawNum < 3:
                self.openbook_addUserSeeVideo(str(drawNum))
                drawNum, currentSeevideoNum = self.openbook_index()
            if drawNum == 0:
                logging.info('【沃阅读】: 抽奖次数已用完...')
                return
            logging.info(f'【沃阅读】: 第{6 - drawNum}次抽奖...')
            time.sleep(1.2)
            self.openbook_doDraw(6 - drawNum)
            time.sleep(1.2)
            return self.openbook_run()
        except Exception as e:
            logging.error(e)        

    def openbook_index(self):
        url = 'https://st.woread.com.cn/touchextenernal/openbook/index.action?channelid=18566059'
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'

        self.categoryList = re.findall(r'cateIds.push\((\d+)\);', resp.text)
        drawNum = re.findall(r'var drawNum = (\d);', resp.text)[0]
        drawNum = int(drawNum)
        currentSeevideoNum = re.findall(
            r'var currentSeevideoNum = (-?\d);', resp.text
        )[0]
        currentSeevideoNum = int(currentSeevideoNum)
        return drawNum, currentSeevideoNum


    def openbook_addUserSeeVideo(self, drawNum):
        url = f'https://st.woread.com.cn/touchextenernal/openbook/addUserSeeVideo.action?num={drawNum}&activityindex=RUEyODEwMzkxQ0E1RTZGQTE0NUNGNTM2Nzk1M0NCMEM='
        resp = self.session.get(url=url)
        logging.info(resp.json())

    def openbook_doDraw(self, num):
        category = random.choice(self.categoryList)
        url = 'https://st.woread.com.cn/touchextenernal/openbook/doDraw.action'
        data = {
            'categoryId': category,
            'currentNum': '%d' % num
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        result['bookInfo'] = ''
        try:
            logging.info(f"【沃阅读】: 抽到 {result.get('prizedesc')} {result.get('usetypename','')}")
        except:
            logging.error(f'{result}')

    def readluchdraw_run(self):
        self.session.headers.update({
            "Referer": "https://st.woread.com.cn/touchextenernal/readluchdraw/index.action",
        })
        try:
            self.readluchdraw_index()
            if not self.isdrawtoday:
                self.readluchdraw_addDrawTimes()
            for acticeindex in [
                "NzFGQzM2Mjc4RDVGNUM4RTIyMzk4MkQ3OUNEMkZFOUE=",  # //默认
                "QjUxRUZCMURBRUUyMzM2NTgwNUY2NzZGRTgxRUZGQUQ=",  # //一次 看视频20日流量
                "OTJGMDkwNjk0Mjc4MjU2MkQyQjIyMzRGRDRGQzk4MzA=",  # //额外
            ]:
                logging.info(f'【沃阅读】: 抽奖')
                time.sleep(1.2)
                self.readluchdraw_doDraw(acticeindex)
                time.sleep(3)

        except Exception as e:
            logging.info(e)

    def readluchdraw_index(self):
        url = 'https://st.woread.com.cn/touchextenernal/readluchdraw/goldegg.action'
        resp = self.session.post(url=url)
        self.isdrawtoday = False

        # logging.info(resp.text)
        # e = etree.HTML(resp.text)
        # if e.xpath("//div[@class='cardStateTex']/span/text()")[2].find("今日 已打卡") > -1:
        #     self.isdrawtoday = True

        if "已打卡" in re.findall(f"<span>(.*?打卡)</span>", resp.text)[0]:
            self.isdrawtoday = True

        date_string_list = re.findall(r"fillDrawTimes\('(.*?)',",resp.text)
        for date_string in date_string_list:
            self.readluchdraw_fillDrawTimes(date_string)
            time.sleep(20)

    def readluchdraw_fillDrawTimes(self, date_string):
        """
        date_string 20210601
        补签
        """
        logging.info(f'【沃阅读】: {date_string}补签')
        url = f'https://st.woread.com.cn/touchextenernal/readluchdraw/fillDrawTimes.action?date={date_string}'
        resp = self.session.get(url=url)
        logging.info(f"【沃阅读】: {resp.json().get('message',resp.json())}")

    def readluchdraw_addDrawTimes(self):
        """
        打卡
        """
        url = 'http://st.woread.com.cn/touchextenernal/readluchdraw/addDrawTimes.action'
        resp = self.session.post(url=url)
        logging.info(f"【沃阅读】: {resp.json().get('message',resp.json())}")


    def readluchdraw_doDraw(self, acticeindex):
        """
        抽奖
        """
        url = 'https://st.woread.com.cn/touchextenernal/readluchdraw/doDraw.action'
        data = {
            "acticeindex": acticeindex
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        # logging.info(result)
        logging.info(f'【沃阅读】: {result.get("prizedesc",result["message"])}')


    def thanksgiving_run(self,f=0):
        try:
            self.session.headers.update({
                "Referer": "https://st.woread.com.cn/touchextenernal/thanksgiving/index.action",
            })
            drawNum = int(self.thanksgiving_index())
            # logging.info(drawNum)
            if not drawNum and f==0:
                cntindex = self.thanksgiving_getIntellectRecommend()
                for _ in range(1, 11):
                    # cntindex = '1840947'
                    chapterseno = _
                    # chapterseno = self.newRead(cntindex)
                    item = self.thanksgiving_getUpDownChapter(cntindex, chapterseno)
                    item = self.thanksgiving_ajaxchapter(item)
                    logging.info(f"【沃阅读】: 正在阅读<{item['cntname']}>-<{item['curChapterTitle']}>...")
                    time.sleep(1.2)
                    self.thanksgiving_reportLatestRead(item)
                    time.sleep(12)
            drawNum = int(self.thanksgiving_index())
            if drawNum and f<5:
                time.sleep(1.2)
                self.thanksgiving_doDraw()
                time.sleep(1.2)
                return self.thanksgiving_run(f+1)
            else:
                logging.info('【沃阅读】: 抽奖机会已用完')
        except Exception as e:
            logging.info(e)

    def thanksgiving_index(self):
        url = 'https://st.woread.com.cn/touchextenernal/thanksgiving/goldegg.action'
        data = {
            "allactiveindex": "MDMzMURDNTNDQzA0RDk5QTQ2RTI1RkQ5OEYwQzQ2RkI=",
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        # e = etree.HTML(resp.text)
        # drawNum = int(e.xpath('string(//span[@id="drawNum_id"]/text())'))
        # return drawNum
        drawNum=re.findall(r"<span id=\"drawNum_id\">(.*?)</span>", resp.text)[0]
        return drawNum

    def thanksgiving_getIntellectRecommend(self):
        url = 'https://st.woread.com.cn/touchextenernal/read/getIntellectRecommend.action'
        data = {
            "recommendid": "0",
            "cntsize": "6",
            "recommendsize": "1"
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        data = [
            [item['cntname'], item['cntindex']] for item in result['message']['catlist']
        ]
        book = random.choice(data)
        return book[1]

    def thanksgiving_getUpDownChapter(self, cntindex, chapterseno=1):
        url = "https://st.woread.com.cn/touchextenernal/read/getUpDownChapter.action"
        data = {
            "cntindex": cntindex,
            "chapterseno": str(chapterseno)
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        for item in result['message']:
            if int(item['chapterseno']) == chapterseno:
                # logging.info(item)
                return item

    def thanksgiving_ajaxchapter(self, item):
        url = 'https://st.woread.com.cn/touchextenernal/contentread/ajaxchapter.action'
        params = {
            "cntindex": item['cntindex'],
            "catid": "",
            "volumeallindex": item['volumeallindex'],
            "chapterallindex": item['chapterallindex'],
            "chapterseno": item['chapterseno'],
            "activityID": "",
            "pageIndex": "",
            "cardid": "",
            "_": int(time.time()*1000),
        }
        resp = self.session.get(url=url, params=params)
        resp.encoding = 'utf8'
        result = resp.json()
        result['contentInfo'] = ''
        result['listPreNextJSONArray'] = ''
        # logging.info(result)
        return resp.json()

    def thanksgiving_reportLatestRead(self, item):
        url = 'https://st.woread.com.cn/touchextenernal/contentread/reportLatestRead.action'
        data = {
            "cntindex": item['cntindex'],
            "chapterallindex": item['chapterallindex'],
            "catindex": item['catindex'],
            "cnttype": item['cnttype'],
            "cntname": item['cntname'],
            "cntrarflag": item['cntrarflag'],
            "chapterseno": item['chapterseno'],
            "chaptertitle": item['curChapterTitle'].replace(' ', '+'),
            "authorname": item['authorname'],
            "iconFile": "",
            "volumeallindex": item['volumeallindex'],
            "finishflag": "1"
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        logging.info(f"【沃阅读】: {resp.json().get('message',resp.json())}")

    def thanksgiving_doDraw(self):
        """
        抽奖
        """
        url = 'https://st.woread.com.cn/touchextenernal/thanksgiving/doDraw.action'
        data = {
            "acticeindex": "MDMzMURDNTNDQzA0RDk5QTQ2RTI1RkQ5OEYwQzQ2RkI="
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        try:
            logging.info(f'【沃阅读】: {result.get("prizedesc",result["message"])}')
        except:
            logging.info(f"【沃阅读】: {result}")

            