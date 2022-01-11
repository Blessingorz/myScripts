#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cron: 30 20 * * *
new Env('膨胀助力');
export wuye9999_pengzhang="0"     # 需要膨胀的助力码,多个用&连接
账号1助力作者
'''
import os,json,random,time,re,string,functools,asyncio,hashlib,hmac
import sys
import requests
requests.packages.urllib3.disable_warnings()


cookie_findall=re.compile(r'pin=(.+?);')
def get_pin(cookie):
    try: return cookie_findall.findall(cookie)[0]
    except: print('ck格式不正确，请检查')
def get_env(env):
    try:
        if env in os.environ: a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            try: a=v4_env(env,'/ql/config/config.sh')
            except: a=eval(env)
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try: a=v4_env(env,'/jd/config/config.sh')
            except: a=eval(env)
        else: a=eval(env)
    except: a=''
    return a
def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']')
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except: pass
    return c 
def ua():
    try: from jdEnv import USER_AGENTS as a
    except: a='jdpingou;android;5.5.0;11;network/wifi;model/M2102K1C;appBuild/18299;partner/lcjx11;session/110;pap/JA2019_3111789;brand/Xiaomi;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36'
    return a
def gettimestamp():
    return str(int(time.time() * 1000))
## 返回cookie_list
class Judge_env(object):
    def main_run(self):
        if '/jd' in os.path.abspath(os.path.dirname(__file__)): cookie_list=self.v4_cookie()
        else: cookie_list=os.environ["JD_COOKIE"].split('&')
        if len(cookie_list)<1: print('请填写环境变量JD_COOKIE\n')    
        return cookie_list
    def v4_cookie(self):
        a=[]
        b=re.compile(r'Cookie'+'.*?=\"(.*?)\"', re.I)
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    regular=b.match(line).group(1)
                    a.append(regular)
                except: pass
        return a
cookie_list=Judge_env().main_run()


def taskPostUrl(functionId,body,cookie):
    url=f"https://api.m.jd.com/client.action?functionId={tigernian_pk_collectPkExpandScore}"
    headers={
        "accept": "application/json,text/plain,*/*",
        "origin": "https://wbbny.m.jd.com",
        "user-agent": ua(),
        "sec-fetch-mode": "cors",
        "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "com.jingdong.app.mall",
        "sec-fetch-site": "same-site",
        "referer": "https://wbbny.m.jd.com/babelDiy/Zeus/41AJZXRUJeTqdBK9bPoPgUJiodcU/index.html?babelChannel=syfc&shareType=expandHelp&inviteId=PKASTT0225KkcRh8R8gGCdhrywKUPfQCTdWnIaRzTwjeQOc&mpin=RnE1kDYLa2KLndRP--txXPzFsU58iNUp0qGd&from=sc&sid=969fd853761bcb783711b1433735b7dw&un_area=4_134_19915_0",
        "accept-encoding": "gzip,deflate,br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": cookie,
    }
    try:
        res=requests.post(url,headers=headers,data=body).text
        print(res)
    except:
        print('API请求失败，请检查网路重试❗\n')   


def tigernian_pk_collectPkExpandScore(inviteId,cookie):
    print(f'{get_env(cookie)} 去助力{inviteId}')
    body='functionId=tigernian_pk_collectPkExpandScore&body={"ss":"{"extraData":{"log":"1641903307862~1aGP5AHnUmnMDF2a1JYSzAxMQ%3D%3D.R11maXJGWGBge09SayY%2FLC0zb3kuMx5pNUdHZXRyWlosajVHFTQgeDk%2FID15NCIjICRAHxcpeQBaZzoKCA%3D%3D.676448d8~9%2C1~84527E3D5A0191FFC5A026B8D7BA3C60E3A50F33~0labbky~C~TkRCWBsMbT4UFxBbWhoPbhRSAEsDPxpxdBp6OXcZVRsHCAUZQhQZRFFRGwNgGnIuFHk%2BbBsJGwUGBhkSF0oUUQgbADkUcSoZegl6GUMaQURoShRSS1gUWQkZRkZEGg8XBwABVwxWBQcBBgdbAQxcAQYaGRdBU1FED0RCQU1CQgVNU0YZFU9QVBQMFwBTEkJBTUNXQRQXFFFZGg9uDxoBVxlUGgYVBxpWZRlGX10aDwQaFFYVF1wUUF0PUlpcVgcBUlxRAwEHVgUFUQQFXQZSUQABUwwDAQcXGhRbFhdcFHlQWEMbGFQWWEEAWRcaFEFED1cAAQgPBlALBVMNAQoZF1xdF1wXSwINX1JXUAgMUVABXhgNUlBXVgYCBFRcBlJUXAABFxsaU0VUFA9EUx4Fem1EU1F6fBVNWA5BcEcEQ1cABHcXFRRYFRoPRnJYV1JZUxZ8CFZIFBkbWFcVGg9GDAYPDAAUGhcVVhQUD2IOA1IUBl0GahQXR1kUDz0XNFNRVF8WLVdBARUAGhkXV1hRFFoPUhcVFA9BFBdVBRkLGwUUGhdfBFEPABsaFFsLAVIDAQoDBQUFBlIDVAUYCAADVQgGUAMACwEDAwUAUBdKFAQbaxpBUVoFFw0aU1NQUFMAQRIUGRtXXEECFxEXGxpWXBQMFxEGSAIbCRQaQVtTO0MVAhcFBxQZRFcCFA8bRFcNXFoJCAMJBAICAwZSF0oUWFMUDDgJGVQZB2UZF1RaWgEXXBQEDwIHWggGVgMADwYGSAdkJX0qAUxLf0UJdXEiR2Rvc0JhXHQeeAELCBdhWFpuZDN7VV0Eb35XcywBMGcATGFYFFRnHQV%2Belx3fnx3V1khB01OZAUEXmcNZ1Z2TV5gVWEBVyNlfBZ9fldMZSYNQXdmBXV9UiNsJFpGbXR1KnVmJXhRe0JGRn9fI0MtXHx1cWIidXQdWlp7dlIAZmYBeCtkcG9yZ1NJeA1SD3FcXmB9TCdUM1xBVnl0InRkDQBjdFlwAG9PDQEvUXNIdHciDHo1dERyZ1l3d0IFVCl3eA1mXCZqcx1FUWhhQVRwBD8GSAFRDVRQUV0FGk8bCUtLSHRLMmcscHNOB3Q1eUYtcltqUWdwA3g%2BcxZvdGtnVyVucDJidWlmck5SYDdkV3F3e29gJVR%2FNmVicW1xBm9yJE0zVXNrb2MgUGAndHF5cGddXWIzcD9icWx3cyRpYyNyX2pUZHRgbCB0J3F3aFJ0JAhsI21lS3pwB2RnIVIFVGNRZHodCQYJWUBBBRcaFFgVUkQMFxtL~09som6a","sceneid":"ZNSZLh5"},"secretp":"m2BozUgoCkFA7V2mIr7RW8pdp0Q","random":"41174534"}","inviteId":"'+inviteId+'"}&client=wh5&clientVersion=1.0.0'
    taskPostUrl("tigernian_pk_collectPkExpandScore",body,cookie)


# 返回一个作者的助力码, 账号1助力作者,
def author_helpcode():
    url_list = ['https://raw.fastgit.org/wuye999/myScripts/main/jd/helpcode/helpcode.json',
        'https://mirror.ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/jd/helpcode/helpcode.json',
        'https://cdn.jsdelivr.net/gh/wuye999/myScripts@main/jd/helpcode/helpcode.json',
        'https://raw.githubusercontent.com/wuye999/myScripts/main/jd/helpcode/helpcode.json']
    for e,url in enumerate(url_list):
        try:
            response = requests.get(url,timeout=10).json()
            break
        except:
            if e >= (len(url_list)-1): print('获取助力码, 请检查网络连接...')   
    helpcode_list=response['pengzhang']
    helpcode=random.choice(helpcode_list)
    return helpcode


def main():
    print('🔔膨胀助力, 开始!\n')
    inviteId_list=get_env("wuye9999_pengzhang").split('&')
    print(f"共 {len(inviteId_list)} 个助力码")
    for e,inviteId in enumerate(inviteId_list) :
        print(f'-------------------开始助力 {inviteId}-------------------')
        for f,cookie in enumerate(cookie_list):
            if e==0 and f==0 :
                print('账号1助力作者')
                inviteId=author_helpcode()
                tigernian_pk_collectPkExpandScore(inviteId,cookie)
            else:
                tigernian_pk_collectPkExpandScore(inviteId,cookie)

if __name__ == '__main__':
    main()
