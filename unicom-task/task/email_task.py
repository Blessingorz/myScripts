# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 22:30
# @Author  : wuye9999
# 沃邮箱
import os,sys
import json,time,re,traceback,random,datetime,util,sys,login,logging,importlib,urllib
import pytz,requests,rsa     # 导入 pytz,requests,rsa 模块，出错请先安装这些模块: pip3 install xxx
import execjs
requests.packages.urllib3.disable_warnings()

class email_task:
    def dotask(self):
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.8897817905278955"
            res = self.email.post(url).json()
            wxName = res.get("result").get("wxName")
            userMobile = res.get("result").get("userMobile")
            logging.info(f"【沃邮箱】: 登录账号 {wxName} ")
            logging.info(f'【沃邮箱】: 剩余积分 {res.get("result").get("clubScore")} ')
            logging.info(f"【沃邮箱】: 活动获得积分 {res.get('result').get('totalScore')} ")
        except Exception as e:
            logging.error("【沃邮箱】: 沃邮箱获取用户信息失败", e)

        try:
            url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.2967650751258384"
            res = self.email.post(url=url).json()
            keepSign=int(res['result']['keepSign'])
            logging.info(f"【沃邮箱签到】: 已连续签到{keepSign}天")
        except:
            logging.error('【沃邮箱签到】: 查询签到天数错误')
            keepSign=0

        try:   
            if keepSign >= 21:
                logging.info('【沃邮箱签到】: 连续签到天数大于等于21天,暂停签到')
            else:
                url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
                res = self.email.post(url=url).json()
                result = res.get("result")
                if result == -2:
                    logging.info("【沃邮箱签到】: 已签到")
                elif result is None:
                    logging.info("【沃邮箱签到】: 签到失败")
                else:
                    logging.info(f"【沃邮箱签到】: 签到成功~已签到{result}天！")
        except Exception as e:
            logging.error(f"【沃邮箱签到】: 错误 \n{e}")

        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            data_params = {
                "沃邮箱每日首次登录": {"taskName": "loginmail"},
                "浅秋领福利": {"taskName": "clubactivity"},
                "下载沃邮箱app": {"taskName": "download"},
                "去用户俱乐部逛一逛": {"taskName": "club"},
            }
            for key, data in dict.items(data_params):
                try:
                    res = self.email.post(url=url, data=data).json()
                    result = res.get("result")
                    if result == 1:
                        logging.info(f"【{key}】: 做任务成功")
                    elif result == -1:
                        logging.info(f"【{key}】: 任务已做过")
                    elif result == -2:
                        logging.info(f"【{key}】: 请检查登录状态")
                    else:
                        logging.info(f"【{key}】: 未知错误")
                except Exception as e:
                    logging.info(f"【沃邮箱】: 沃邮箱执行任务【{key}】错误\n{e}")
        except Exception as e:
            logging.error(f"【沃邮箱】: 沃邮箱执行任务错误\n{e}")

    def dotask_2(self):
        #查询成长值
        try:
            url = "https://club.mail.wo.cn/clubwebservice/growth/get-person-centre"
            res = self.email.get(url=url).json()
            memberUser=res['data']['memberUser']
            logging.info(f'【沃邮箱】: 俱乐部会员等级 {memberUser["levelName"]}')
            logging.info(f'【沃邮箱】: 俱乐部成长值 {memberUser["growthValue"]}')
        except Exception as e:
            logging.error(f'【沃邮箱】: 获取俱乐部信息失败 \n{e}')

        #查询签到天数
        try:
            url = "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/query-continuous-sign-record"
            res = self.email.get(url=url).text
            newContinuousDay=int(re.findall(r'"newContinuousDay":(.*?),', res)[0])
            logging.info(f'【沃邮箱】: 已连续签到 {newContinuousDay} 天')
        except Exception as e:
            logging.error(f'【沃邮箱】: 查询签到天数错误 \n{e}')
            newContinuousDay=0

        #任务签到
        try:
            if newContinuousDay >= 21:
                logging.info('【沃邮箱签到】: 连续签到天数大于等于21天,暂停签到')
            else:
                url = 'https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create?channelId='
                res = self.email.get(url=url).json()
                logging.info(f"【沃邮箱】: 成长值签到结果: {res['description']}")
        except Exception as e:
            logging.error(f'【沃邮箱】: 签到失败 \n{e}')

        #积分任务
        try:
            url = 'https://club.mail.wo.cn/clubwebservice/growth/queryIntegralTask?channelId=club'
            res = self.email.get(url=url).json()
            for data in res['data']:
                if data['irid'] == None or data['irid'] == 339 or data['taskState'] == 1:
                    logging.info(f"【沃邮箱】: 跳过{data['resourceName']}")
                    continue
                url = 'https://club.mail.wo.cn/clubwebservice/growth/addIntegral?resourceType='+urllib.parse.quote(str(data['resourceFlag']))
                ress = self.email.get(url=url).json()
                logging.info(f"【沃邮箱】: 执行任务: {data['resourceName']} ")
                logging.info(f"【沃邮箱】: 状态: {ress['description']}")
        except Exception as e:
            logging.error(f'【沃邮箱】: 积分任务出错 \n{e}')

        #成长值任务
        try:
            url = 'https://club.mail.wo.cn/clubwebservice/growth/queryGrowthTask'
            res = self.email.get(url=url).json()
            for data in res['data']:
                if data['irid'] == None or data['irid'] == 576 or data['taskState'] == 1:
                    logging.info(f"【沃邮箱】: 跳过{data['resourceName']}")
                    continue
                url = 'https://club.mail.wo.cn/clubwebservice/growth/addGrowthViaTask?resourceType='+urllib.parse.quote(str(data['resourceFlag']))
                ress = self.email.get(url=url).json()
                logging.info(f"【沃邮箱】: 执行任务: {data['resourceName']}")
                logging.info(f"【沃邮箱】: 状态: {ress['description']}")
        except Exception as e:
            logging.error(f'【沃邮箱】: 成长值任务出错 \n{e}')

    def dotask_3(self,uid,sid):
        #app
        upcookies=requests.utils.cookiejar_from_dict({
            'Coremail.sid': sid,
            'domain':'domain=mail.wo.cn',
        }) 
        self.email.cookies.update(upcookies)      
        self.email.headers.update({
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "com.asiainfo.android"
        }) 
        #增加积分
        try:
            integral_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
            }
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"integral"}
                res = self.email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】: {key}app积分结果:{res['code']}")
        except Exception as e:
            logging.error(f'【沃邮箱扩展任务】: app沃邮箱执行任务错误\n{e}')

        #增加成长值
        try:
            growth_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
            }            
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"growth"}
                res = self.email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】: {key}app成长值结果:{res['code']}")
        except Exception as e:
            logging.error(f'【沃邮箱扩展任务】: app沃邮箱执行任务错误\n{e}')

        #网页
        upcookies=requests.utils.cookiejar_from_dict({
            'CoremailReferer':'https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Fhxphone%2F',
        }) 
        self.email.cookies.update(upcookies) 
        self.email.headers.update({
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "com.tencent.mm",
        })
        #增加积分
        try:
            integral_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
                "上传文件到中转站": 'uploadFile',
            }            
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"integral"}
                res = self.email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】: {key}网页端积分结果:{res['code']}")
        except Exception as e:
            logging.error(f'【沃邮箱扩展任务】: 网页端沃邮箱执行任务错误\n{e}')
                
        #增加成长值
        try:
            growth_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
                "上传文件到中转站": 'uploadFile',
            }   
            for key, userAction in integral_data.items():             
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"growth"}
                res = self.email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】: {key}网页端成长值结果:{res['code']}")
        except Exception as e:
            logging.error(f'【沃邮箱扩展任务】: 网页端沃邮箱执行任务错误\n{e}')

        #电脑
        upcookies=requests.utils.cookiejar_from_dict({
            'domain':'',
            'CoremailReferer':'https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Findex.jsp%3Fcus%3D1'
        }) 
        self.email.cookies.update(upcookies)         
        self.email.headers.update({
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "XMLHttpRequest",
        })
        #增加积分
        try:
            integral_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
                "上传文件到中转站": 'uploadFile',
            }            
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"userAction":userAction}
                response = self.email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】: {key}电脑端积分结果:{response['code']}")
        except Exception as e:
            logging.error(f'【沃邮箱扩展任务】: 电脑端沃邮箱执行任务错误\n{e}')


    def run(self,womail):
        if "woEmail" not in womail:
            return False
        try:
            mobile=re.findall('mobile=(.*?)&', womail["woEmail"])[0]
            openId=re.findall('openId=(.*)', womail["woEmail"])[0]
        except:
            logging.error('沃邮箱url错误')
            return

        ua={
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(womail["woEmail"]).query))
        params = (
            ('mobile', query['mobile'].replace(' ', '+')),
            ('userName', ''),
            ('openId', query['openId'].replace(' ', '+')),
        )

        with requests.Session() as self.email:
            self.email.headers.update(ua)
            url='https://nyan.mail.wo.cn/cn/sign/index/index'
            self.email.get(url=url, headers=headers, params=params)      # 登录
            url = 'https://nyan.mail.wo.cn/cn/sign/wap/index.html'
            self.email.get(url=url)   # 登录
            self.dotask()


        with requests.Session() as self.email:
            self.email.headers.update(ua)
            url="https://club.mail.wo.cn/clubwebservice"
            self.email.get(url=url, headers=headers, params=params)  # 登录
            self.dotask_2()


        with requests.Session() as self.email:
            url="https://mail.wo.cn/coremail/s/json?func=user:login"

            if womail['username'] and womail['woEmail_password']:
                woEmail_uid=womail['username']+'@wo.cn'
                woEmail_password=womail['woEmail_password']
            else:
                logging.error("【沃邮箱扩展任务】: 未找到沃邮箱手机号或密码")
                return

            self.email.headers.update({
                    "Accept": "text/x-json",
                    "Content-Type": "text/x-json",
                    "X-CM-SERVICE": "PHONE",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
            })
            data={"uid": woEmail_uid, "password": woEmail_password}
            res=self.email.post(url=url, json=data).json()
            logging.info(f"【沃邮箱扩展任务】: 登录沃邮箱结果 {res['code']}")
            try:
                self.dotask_3(res['var']['uid'],res['var']['sid'])
            except:
                logging.error(f"【沃邮箱扩展任务】: 登录失败，沃邮箱扩展任务跳过")
