'''
cron: 5 16 * * *
new Env('金榜年终奖');
入口: 金榜年终奖
功能：完成任务，互助
账号1助力作者，其余账号按顺序内部互助
青龙拉取命令：ql raw https://raw.githubusercontent.com/wuye999/myScripts/main/jd/jd_golden_yearendBonus.py
2021/12/06 22:30
'''

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


# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')


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


## 获取通知服务
class Msg(object):
    def getsendNotify(self):
        url_list = [
            'https://mirror.ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py',
            'https://cdn.jsdelivr.net/gh/wuye999/myScripts@main/sendNotify.py',
            'https://raw.fastgit.org/wuye999/myScripts/main/sendNotify.py',
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


def taskPostUrl(body, cookie):
    url=f'https://api.m.jd.com//client.action'
    headers={
        'Cookie': cookie,
        "User-Agent": ua(),
        'Host': 'api.m.jd.com',
        'origin': 'https://h5.m.jd.com',
        'sec-fetch-mode': 'cors',
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'com.jingdong.app.mall',
        'sec-fetch-site': 'same-site',
        'referer': 'https://h5.m.jd.com/babelDiy/Zeus/4YHatHgm4VUm5QMxfVx32wJi71eJ/index.html?babelChannel=ttt9&inviteId=T0225KkcR0hKo1GEKRyikaFYfACjRQmoaX5kRrbA&sid=deb80695a25d65e0beec1ddcfc4e1f6w&un_area=4_134_19915_0',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data=body
    try:
        res=requests.post(url,headers=headers,data=data).json()
        return res
    except Exception as e:
        msg('API请求失败，请检查网路重试❗')  
        msg(e)


# 任务列表
def splitHongbao_getHomeData(cookie):
    body='functionId=splitHongbao_getHomeData&body={"appId":"1EFVXxg","taskToken":""}&client=wh5&clientVersion=1.0.0'
    res=taskPostUrl(body, cookie)
    if not res:
        return
    try:
        taskVos=res['data']['result'].get('taskVos')
        return taskVos
    except Exception as e:
        msg('获取任务列表失败')
        msg(e)


# 获取助力码
def helpcode(task,cookie):
    try:
        global inviteCode_list
        assistTaskDetailVo=task['assistTaskDetailVo']
        taskToken=assistTaskDetailVo['taskToken']
        msg(f'{get_pin(cookie)}的助力码：{taskToken}')
        inviteCode_list.append(taskToken)
    except Exception as e:
        msg('获取助力码失败')
        msg(e)


# 完成任务
def harmony_collectScore(task,cookie):
    taskId=task['taskId']
    taskName=task.get('taskName',None)
    shoppingActivityVos=task.get('shoppingActivityVos',None)
    for shoppingActivity in shoppingActivityVos:
        try:
            title=shoppingActivity.get('title',None)
            advId=shoppingActivity['advId']
            taskToken=shoppingActivity['taskToken']
            body='functionId=harmony_collectScore&body={"appId":"1EFVXxg","taskToken":"'+taskToken+'","taskId":'+taskId+',"itemId":"'+advId+'","actionType":"1"}&client=wh5&clientVersion=1.0.0'
        except Exception as e:
            msg('获取任务数据失败')
            msg(e)
            continue
        msg(f'开始 {title}')
        res=taskPostUrl(body, cookie)
        if res['code']==0:
            msg(res['data'].get('bizMsg',None))
        else:
            msg('任务失败')
        res=taskPostUrl(body, cookie)
        if res['code']==0:
            msg(res['data'].get('bizMsg',None))
        else:
            msg('任务失败')

# 助力
def splitHongbao_getHomeData_helpcode(cookie,inviteCode):
    body='functionId=splitHongbao_getHomeData&body={"appId":"1EFVXxg","taskToken":"'+inviteCode+'"}&client=wh5&clientVersion=1.0.0'
    res=taskPostUrl(body, cookie)
    try:
        msg(f"{get_pin(cookie)}去助力 {res['data']['result']['guestlnfo']}")
        msg(res['data'].get('bizMsg',None))
    except Exception as e:
        msg(f"{get_pin(cookie)}去助力 {inviteCode}")
        msg(res['data'].get('bizMsg',None))


# 账号1助力作者
def author_helpcode(cookie):
    url_list = [
        'https://mirror.ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/jd/helpcode/helpcode.json',
        'https://cdn.jsdelivr.net/gh/wuye999/myScripts@main/jd/helpcode/helpcode.json',
        'https://raw.fastgit.org/wuye999/myScripts/main/jd/helpcode/helpcode.json',
        'https://raw.githubusercontent.com/wuye999/myScripts/main/jd/helpcode/helpcode.json',
    ]
    for url in enumerate(url_list):
        try:
            response = requests.get(url,timeout=10).json()
            break
        except:
            if e >= (len(url_list)-1):
                print('获取助力码，请检查网络连接...')   
    helpcode_list=res['jd_golden_yearendBonus'] 
    for helpcode_ssssss in helpcode_list:
        body='functionId=splitHongbao_getHomeData&body={"appId":"1EFVXxg","taskToken":"'+helpcode_ssssss+'"}&client=wh5&clientVersion=1.0.0'
        res=taskPostUrl(body, cookie)
        try:
            msg(f"{get_pin(cookie)}去助力 作者")
            msg(res['data'].get('bizMsg',None))
        except Exception as e:
            msg(f"{get_pin(cookie)}去助力 作者")
            msg(res['data'].get('bizMsg',None))        


def main():
    msg('🔔金榜年终奖，开始！\n')
    msg(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')

    global inviteCode_list
    inviteCode_list=list()

    for e,cookie in enumerate(cookie_list):
        msg(f'******开始【账号 {e+1}】 {get_pin(cookie)} *********\n')
        taskVos=splitHongbao_getHomeData(cookie)
        if not taskVos:
            continue
        for f,task in enumerate(taskVos):
            if f==len(taskVos)-1:
                helpcode(task,cookie)
                continue
        if e==0:
            author_helpcode(cookie)
        harmony_collectScore(task,cookie)    

    msg(f'====================内部互助=========\n')
    for e,cookie in enumerate(cookie_list):
        for inviteCode in inviteCode_list:
            splitHongbao_getHomeData_helpcode(cookie,inviteCode)



if __name__ == '__main__':
    main()



