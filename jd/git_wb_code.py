#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cron: 30 0,15 * * *
new Env('发财挖宝内部互助');
活动入口: 京东极速版>我的>发财挖宝
脚本功能为: 内部互助
由于每个号1次助力机会, 30次助力之后要99人才能加一血 
所以按ck顺序助力, 每个号最多吃30个助力
账号1助力作者
地址: https://raw.githubusercontent.com/wuye999/myScripts/main/jd/jd_wabao_help.py
'''
import os,json,random,time,re,string,functools,asyncio,hashlib,hmac
import sys
sys.path.append('../../tmp')
try:
    import requests
except Exception as e:
    print(str(e) + "\n缺少requests模块, 请执行命令: pip3 install requests\n")
requests.packages.urllib3.disable_warnings()


run_send='no'          # yes或no, yes则启用通知推送服务
linkId="pTTvJeSTrpthgk9ASBVGsw"


# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')

# 读取环境变量
def get_env(env):
    try:
        if env in os.environ:
            a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/ql/config/config.sh')
            except:
                a=eval(env)
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/jd/config/config.sh')
            except:
                a=eval(env)
        else:
            a=eval(env)
    except:
        a=''
    return a

# v4
def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']', re.I)
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except:
                pass
    return c 


# 随机ua
def ua():
    sys.path.append(os.path.abspath('.'))
    try:
        from jdEnv import USER_AGENTS as a
    except:
        a='jdpingou;android;5.5.0;11;network/wifi;model/M2102K1C;appBuild/18299;partner/lcjx11;session/110;pap/JA2019_3111789;brand/Xiaomi;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36'
    return a

# 13位时间戳
def gettimestamp():
    return str(int(time.time() * 1000))

## 获取cooie
class Judge_env(object):
    def main_run(self):
        if '/jd' in os.path.abspath(os.path.dirname(__file__)):
            cookie_list=self.v4_cookie()
        else:
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            print('请填写环境变量JD_COOKIE\n')    
        return cookie_list

    def v4_cookie(self):
        a=[]
        b=re.compile(r'Cookie'+'.*?=\"(.*?)\"', re.I)
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    regular=b.match(line).group(1)
                    a.append(regular)
                except:
                    pass
        return a
cookie_list=Judge_env().main_run()  


def taskGetUrl(url, cookie):
    url=url
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://bnzf.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json, text/plain, */*',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        res=requests.get(url,headers=headers).json()
        return res
    except:
        print('API请求失败，请检查网路重试❗\n')   


# 助力码
def inviteCode(cookie):
    global inviteCode_1_list,inviteCode_2_list
    body={"linkId":linkId}
    url=get_h5st_url(body,'happyDigHome')
    res=taskGetUrl(url, cookie)
    if not res:
        return
    try:
        if res['success']:
            print(f"账号{get_pin(cookie)}助力码为{res['data']['inviteCode']}")
            inviteCode_1_list.append(res['data']['inviteCode'])
            print(f"账号{get_pin(cookie)}助力码为{res['data']['markedPin']}")
            inviteCode_2_list.append(res['data']['markedPin'])
        else:
            print('快去买买买吧')
    except:
        print(f"错误\n{res}\n")


# post请求，将参数timestamp, md5_file，body, typeid上传, 计算url的h5st, 返回带h5st的url
def get_h5st_url(body,typeid):
    time.sleep(0.5)
    with open(os.path.abspath(__file__), 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        md5_file = md5obj.hexdigest()
        # print(md5_file)
    body=body
    typeid=typeid
    timestamp=gettimestamp()
    md5_file=hmac.new(timestamp.encode('utf-8'), md5_file.encode('utf-8'), digestmod=hashlib.md5).hexdigest()
    url='http://121.4.99.83:5000/get_h5st'
    data={'timestamp': timestamp, 'md5_file': md5_file, 'body': body, 'typeid': typeid}
    res=requests.post(url,json=data).json()
    if res['code']=='200':
        return res['url']
    else:
        print('请求h5st失败')

def main():
    global cookie_list
    print('🔔获取助力码，开始!\n')
    print('获取助力码\n')
    global inviteCode_1_list,inviteCode_2_list
    inviteCode_1_list=list()
    inviteCode_2_list=list()
    for cookie in cookie_list[:3]:
        inviteCode(cookie) 


if __name__ == '__main__':
    main()
    