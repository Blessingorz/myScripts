# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 22:30
# @Author  : wuye9999
#位置: 我的 --> 天天领现
import os,sys
sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/task')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/tenscf_rely')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/unicom-task/task')
import requests,json,time,re,login,logging,traceback,os,random,datetime,string
from lxml.html import fromstring

class everyday_way:
    def run(self, client, user):
        client.headers.update({
            'accept': 'application/json',
            'origin': 'https://epay.10010.com',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded',
        })
        try:
            # 登录天天领现金
            index_url=self.partyServer(client)                      # 获取登录链接
            token=self.woauth2_login(client, index_url)             # 获取token
            rptid=self.woauth2_sjyyt_new(client, token)             # 获取rptid
            wap_sessionid=self.web_loginNew(client,rptid)           # web登录,验证rptid，获取wap_sessionid
            # 任务
            self.unifyDraw(client,user,wap_sessionid)       # 打卡
            self.userDrawInfo(client,user,wap_sessionid)    # 查余额
        except Exception as e:
            logging.error(f'【天天领现金】：错误\n{e}')
       
    # 获取登录链接
    def partyServer(self,client):
        data='bizFrom=225&activityId=TTLXJ20210330&loginId=&response_type=web_token&device_digest_token_id=&rptid=null&end_url=clockIn%2Findex.html%3Fchannel%3D225%26channelType%3Dnull%26uid%3D'
        res=client.post('https://epay.10010.com/partyServer/login/loginNew.do',data=data).json()
        if res['returnCode']=='-11':
            if res['index_url']:
                return res['index_url']
        logging.error(f'【天天领现金】：获取登录链接失败\n{res}')
    # 获取token
    def woauth2_login(self,client,index_url):
        res=client.get(index_url).text  
        if '正在跳转' in res:
            token=re.findall(r'token = "(.*?)";', res)[0]
            return token
        else:
            logging.error(f'【天天领现金】：获取token失败\n{res}')
    # 获取rptid
    def woauth2_sjyyt_new(self,client,token):
        url=f'https://epay.10010.com/woauth2/sjyyt-new/try-login-using-usid?device_digest_trace_id=c494f11d82b548b08c14a28382676878&device_digest_token_id=chinaunicom-pro-1637487108522-9963debb40c83&token={token}&token2={token}'
        res=client.get(url)
        if '<title>天天领现金</title>' in res.text:
            rptid=re.findall(r'rptid=(.*)', res.url)[0]
            return rptid
        logging.error(f'【天天领现金】：获取rptid失败\n{res.text}')
    # web登录,验证rptid，获取wap_sessionid
    def web_loginNew(self,client,rptid):
        data=f'bizFrom=225&activityId=TTLXJ20210330&loginId=&response_type=web_token&rptid={rptid}&end_url=clockIn%2Findex.html%3Fchannel%3D225%26channelType%3Dnull%26uid%3D'
        res=client.post('https://epay.10010.com/partyServer/login/loginNew.do',data=data).json()
        if res['returnCode']=='0':
            logging.info(f"【天天领现金】：{res['returnMsg']}")
            return res['wap_sessionid']
        logging.error(f"【天天领现金】：{res['returnMsg']}")
    # 打卡
    def unifyDraw(self,client,user,wap_sessionid):
        for drawType in string.ascii_uppercase:
            data=f"loginId={user['username']}&activityId=TTLXJ20210330&wap_sessionID={wap_sessionid}&version=3.0.0&bizFrom=225&channelType=null&markerName=ttlxj&validatorId=1&drawType={drawType}"
            res=client.post('https://epay.10010.com/partyServer/ttlxj/unifyDraw.do',data=data).json()
            if res['returnCode']=='0':
                logging.info(f"【天天领现金】：打卡成功获得 {res['amount']}")
                return
            # logging.error(f"【天天领现金】：{res['returnMsg']}") 
        logging.error(f"【天天领现金】：已经签到过了，或打卡失败")
    # 查余额
    def userDrawInfo(self,client,user,wap_sessionid):
        data=f"loginId={user['username']}&activityId=TTLXJ20210330&wap_sessionID={wap_sessionid}&version=3.0.0&bizFrom=225"
        res=client.post('https://epay.10010.com/partyServer/ttlxj/userDrawInfo.do',data=data).json()
        if res['returnCode']=='0':
           logging.info(f"【天天领现金】：总余额 {res['countAmount']}")
           return
        logging.error(f"【天天领现金】：{res['returnMsg']}")        


        



        







