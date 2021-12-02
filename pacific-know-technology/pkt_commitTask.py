#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cron: 5 15 * * *
new Env('太平洋知科技-日常任务');
入口: 太平洋知科技》我的
说明：完成签到，阅读文章等日常任务
环境变量：export pkt_cookie="common_session_id=xxxxxxxxxxxxxxx"
脚本内或环境变量填写，优先环境变量,多账号用&分割
青龙拉取命令：
ql repo 
'''
# 脚本内填写变量示例：
pkt_cookie="common_session_id=xxxxxxxxxxxxxxx"


import os,json,random,time,re,string,functools
import sys
sys.path.append('../../tmp')
sys.path.append(os.path.abspath('.')) 
try:
    import requests
except Exception as e:
    print(str(e) + "\n缺少requests模块, 请执行命令：pip3 install requests\n")
requests.packages.urllib3.disable_warnings()


run_send='no'              # yes或no, yes则启用通知推送服务
commitKey='HR1C1WQajK6qthd5kmM0XGzBIMxY1pgF%0A'


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
        cookie_list=get_env('pkt_cookie').split('&')
        return cookie_list
cookie_list=Judge_env().main_run()


## 获取通知服务
class Msg(object):
    def getsendNotify(self):
        url_list = [
            'https://mirror.ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py',
            'https://cdn.jsdelivr.net/gh/wuye999/myScripts@main/sendNotify.py',
            'https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py',
        ]
        for e,url in enumerate(url_list):
            try:
                response = requests.get(url,timeout=10)
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
                return
            except:
                if e >= (len(url_list)-1):
                    print('获取通知服务失败，请检查网络连接...')               
    def main(self,f=0):
        global send,msg,initialize
        sys.path.append(os.path.abspath('.'))
        for _ in range(2):
            try:
                from sendNotify import send,msg,initialize
                break
            except:
                self.getsendNotify()
        l=['BARK_PUSH', 'BARK_ARCHIVE', 'BARK_GROUP', 'BARK_SOUND', 'DD_BOT_SECRET', 'DD_BOT_TOKEN', 'FSKEY', 'GOBOT_URL', 'GOBOT_QQ', 'GOBOT_TOKEN', 'GOTIFY_URL', 'GOTIFY_TOKEN', 'GOTIFY_PRIORITY', 'IGOT_PUSH_KEY', 'PUSH_KEY', 'PUSH_PLUS_TOKEN', 'PUSH_PLUS_USER', 'QMSG_KEY', 'QMSG_TYPE', 'QYWX_AM', 'QYWX_KEY', 'TG_BOT_TOKEN', 'TG_USER_ID', 'TG_API_HOST', 'TG_PROXY_AUTH', 'TG_PROXY_HOST', 'TG_PROXY_PORT']
        d={}
        for a in l:
            try:
                d[a]=eval(a)
            except:
                d[a]=''
        try:
            initialize(d)
        except:
            if f < 2:
                f += 1
                self.getsendNotify()
                return self.main(f)
Msg().main()   # 初始化通知服务    


def taskPostUrl(functionId,body,cookie):
    # session = requests.session()
    url=f'https://pccoin.pconline.com.cn/intf/{functionId}?appVersion=6.6.0'
    session.headers={
        'App': 'PCONLINE_INFO_ANDR',
        'uid': '51581729',
        'Version': '6.6.0',
        'PC-Agent': 'PCGroup Android APP',
        'Channel': 'xiaomi',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36',
        'Appsession': 'ea1d08b2fa564578',
        'Cookie': cookie,
        'Cache-Control': 'no-cache',
        'Timestamp': '1638426271293',
        'X-Tingyun-Id': 'cTlf_IH5zc8;c=2;r=483635021;',
        'X-Tingyun': 'c=A|ClgvIjIIH_g;',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '1',
        'Host': 'pccoin.pconline.com.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    data=body
    res=session.post(url,data=data).json()
    return res
 


# 任务列表
def taskCenter(cookie):
    res=taskPostUrl('taskCenter','=',cookie)
    if res['code']==200:
        msg(res['data']['msg'])
        redpacketTask=res['data']['redpacketTask']      # 整点金币，每小时可以领取一次
        taskType=redpacketTask['taskType']              # 任务类型
        taskId=redpacketTask['taskId']                  # 任务id
        title=redpacketTask['title']                    # 任务标题
        msg(f'开始 {title}')
        commitTask(taskType,taskId,cookie)

        taskList=res['data']['taskList']                # 总任务合集
        for tasks in taskList:
            for task in taskList.get(tasks):
                # print(task)
                if isinstance(task, dict):
                    taskType=task['taskType']              # 任务类型
                    taskId=task['taskId']                  # 任务id
                    title=task['title']                    # 任务标题  
                    msg(f'开始 {title}')
                    commitTask(taskType,taskId,cookie)                     
    else:
        msg(f"错误\n{res}\n")


# 做任务
def commitTask(taskType,taskId,cookie):
    body=f"taskType={taskType}&commitKey={commitKey}&taskId={taskId}"
    res=taskPostUrl('commitTask',body,cookie)
    
    if res['code']==200:
        if res['data'].get('getCoins',''):
            msg(f"{res['data']['msg']} \n获取金币 {res['data']['getCoins']}")
        else:
            msg(f"{res['data']['msg']}")
    else:
        msg(f'失败\n{res}\n')                     



def main():
    msg('🔔太平洋知科技-日常任务，开始！\n')
    msg(f'====================共{len(cookie_list)}个账号Cookie=========\n')

    for e,cookie in enumerate(cookie_list):
        msg(f'******开始【账号 {e+1}】  *********\n')
        global session
        with requests.Session() as session:
            taskCenter(cookie)

    
    if run_send=='yes':
        send('太平洋知科技-日常任务')   # 通知服务


if __name__ == '__main__':
    main()

