import time
import os
import re
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()

# 京喜财富岛抢100
# 环境变量优先于脚本内部变量,不填的项默认脚本内部变量
wuye9999_cycless = '1'          # 重复请求次数
wuye9999_ask_sleep = '0.05'     # 请求间隔为0.05秒
wy_ck=''                        # 哪个账号需要请求，不填则全部cookie都请求
# export wuye9999_cycless="1"
# export wuye9999_ask_sleep="1.85"
# export wy_ck="1&3"            # 仅cookie1，cookie3运行此脚本


# 读取环境变量
def get_env(env):
    try:
        if env in os.environ:
            a=os.environ[env]
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            a=v4_env(env)
        else:
            a=eval(env)
    except:
        a=''
    return a
def v4_env(env):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']', re.I)
    with open('/jd/config/config.sh', 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except:
                pass
    return c 


# 13位时间戳
def gettimestamp():
    return str(int(time.time() * 1000)) 

# 随机ua
def ua_random():
    sys.path.append(os.path.abspath('.'))
    global ua
    for n in range(3):
        try:
            from jdUA import jdUA as ua
            break
        except:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/jd/jdUA.py'
            response = requests.get(url)
            with open('jdUA.py', "w+", encoding="utf-8") as f:
                f.write(response.text)


## 获取cooie
class Judge_env(object):
    ## 判断运行环境
    def getcodefile(self):
        global sys
        if '/ql' in os.path.abspath(os.path.dirname(__file__)):
            print("当前环境青龙\n")
            sys.path.append(os.path.abspath(os.path.dirname(__file__)))
        else:
            print('第三方环境\n') 
        if os.path.abspath('.') not in sys.path:
            sys.path.append(os.path.abspath('.'))

    ## 批量提取pin,输出ckkk,path,pin_list
    def main_run(self):
        self.getcodefile()
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


def ask_api(cookie):
    url='https://m.jingxi.com/jxbfd/user/ExchangePrize?strZone=jxbfd&bizCode=jxbfd&source=jxbfd&dwEnv=7&_cfd_t=1632924011248&ptag=7155.9.47&dwType=3&dwLvl=3&ddwPaperMoney=100000&strPoolName=jxcfd2_exchange_hb_202110&strPgtimestamp=1632924011216&strPhoneID=3f092daf5202a681&strPgUUNum=d18883c067ad1fd1299545f0b0786143&_stk=_cfd_t%2CbizCode%2CddwPaperMoney%2CdwEnv%2CdwLvl%2CdwType%2Cptag%2Csource%2CstrPgUUNum%2CstrPgtimestamp%2CstrPhoneID%2CstrPoolName%2CstrZone&_ste=1&h5st=20210929220011248%3B9225930342578161%3B10032%3Btk01w9b641bbb30nTfJ9PqOZbo7j2qUoj77OqQf4JbpxQFpJGNX0TUHzeZJs0tTkF697FsOBgFlP9%2Fm%2FPMVZwV5pOxwC%3Bb1759a02c174496e076cb0ccfad0ce0a0c5c9aeb22054de4f8c7116fd6a38f05&_=1632924011249&sceneval=2&g_login_type=1&callback=jsonpCBKUUU&g_ty=ls'    
    headers = {
        'Host': 'm.jingxi.com',
        'sec-fetch-mode': 'no-cors',
        'user-agent': ua(),
        'accept': '*/*',
        'x-requested-with': 'com.jd.pingou',
        'sec-fetch-site': 'same-site',
        'referer': 'https://st.jingxi.com/fortune_island/index2.html?ptag=7155.9.47&sceneval=2',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie,
    }
    try:      
        res = requests.get(url=url, headers=headers, verify=False)
    except:
        print('请求失败,原因未知\n')
    print(f'{res.text}\n')
    sys.stdout.flush()
    time.sleep(wuye9999_ask_sleep)


if __name__ == '__main__':
    ua_random()
    cookie_list=Judge_env().main_run()
    wuye9999_cycless=int(get_env('wuye9999_cycless'))
    wuye9999_ask_sleep=float(get_env('wuye9999_ask_sleep'))
    wy_ck=get_env('wy_ck')
    if len(wy_ck)>0:
        wy_ck=wy_ck.split('&')
        a=[]
        for n in wy_ck:
            n=int(n)
            a.append(cookie_list[n-1])
        cookie_list=a
    print(f'====================共{len(cookie_list)}个账号Cookie=========\n')
    for n in range(wuye9999_cycless):
        print(f'====================第{n+1}次循环=========\n')
        for e,cookie in enumerate(cookie_list,start=1):
            print(f'******开始【账号 {e}】*********\n')
            ask_api(cookie)

