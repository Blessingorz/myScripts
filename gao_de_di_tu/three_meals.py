# 小德果园
# 入口>高德地图
# 脚本功能为自动浇水，签到等功能，还在完善
# 环境变量wy_xdgy，抓包搜索'sns.amap.com',复制cookie,填入环境变量中，多账号用&分割
# export wy_xdgy="sessionid=xxxx;xxx=xxx;&第二个cookie&第三个cookie"
import time
import os
import re
import requests
import sys
requests.packages.urllib3.disable_warnings()


# 随机ua
def ua_random():
    ua='Android 11'
    return ua

# 10位时间戳
def gettimestamp():
    return str(int(time.time()))


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
        cookie_list=os.environ["wy_xdgy"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            print('请填写环境变量wy_xdgy\n')    
        return cookie_list


# headers
def headerss(cookie):
    a={
            'Cookie': cookie,
            'User-Agent': ua,
            'content-type': 'application/x-www-form-urlencoded',
            'x-t': gettimestamp(),
            'Host': 'sns.amap.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
    }
    return a

# 请求
def request_s(url,cookie,b=1):
    headers=headerss(cookie)
    for n in range(3):
        a=0
        try:
            time.sleep(1)
            res = requests.get(url=url, headers=headers, timeout=12,verify=False).json()
            a=1
            break
        except:
            print('请求失败，正在重试🌍...')
    if a==1 and b==1:
        processing_request_result(res)
    elif b==1:
        msg('❗任务失败...')
    return res


# 判断结果
def processing_request_result(res):
    result=res['result']
    if not result:
        msg('已完成或时间未到⭕\n')
    elif result:
        msg('任务完成✅')
        msg(f"获得水滴💧 {res['data']['rewards_list'][0]['amount']}\n")
    else:
        msg('❗️未知错误\n')

# 检查账号有效性
def getUserInfo(cookie):
    url='https://sns.amap.com/ws/activity/xiaode_garden/invite_token?ent=2&in=bTlkmqpRhIkqMLcHo71pGn3cINQtaO5WYoVQlCcApI2FaqJZaskXs2oGI4oysih5eyI8GV%2Fipm432TH7ICqYKPXsxrQHM1vyfD1QQ2%2Bv9D%2FyJIe%2Bm3hdvskTuH6tK5DMMzlgsQoZswzdPd92Iq1IPcGsB0EDG1JSacd6n%2BzT7Ba2Zz3mp7%2F7cLPIDVdaHM%2FyK3DY2iosKLN790JRluAzQBQ5JbHX9qssS48AUf6ZCz23EbHMMviohdSSVoiZVBoUGZrO0MQEmli%2FBNabEXkXnXTc7xvzDL86tBFylOJ1iOQ5ZuHX3eKaUdwKkzg5ctTGpH0tTUnRnbhyN6aobWOLskegbIq0JHGrbCSvCm6peeMFRKyJa5wLV0GWM98VWrcDq795IQ6gdafPwc618x9Ky0GJGjvln1WLIk1fafljtPOeNsKt6Ir1uS47Li0OV6dmKx2sljbvho9aXb0LzmSSTuFH7rRPNNRE8RiFaffnMOqBnwOYLHAPQmLrFmf3R9OoDwvqXXo5gh7fEGvbTLfFTfj4sjSB3m1chALdr%2BwveEKG%2FVEu7QcPd7QVoSQrcP54OsTCQ9%2F%2F9Fu3GwK7PN%2F0cZKsX29LUjUnWrjPUQY6eaU6J%2BmLLfefNrJof%2F8hV5NSOw9A1YpdvuYTxFPr9%2Fcz0SPFfag1A2XUeNZh6AePoobqgY7ZNlUAA108ml8bm6AGgTmT56CcleNN4nF1MCXZBb5LntEiXGCDsSF5SyyPWD37O7gU2YbYsyortVylXUcI%2F%2BM3eMrHU3fJpwd%2FDlxKwMOJM0K0Mnvw00PG53kgfKNvj5GrzWsO0LJwF%2FEJjS%2BC7r%2Bc5%2BR%2B8ozHB2eVz7RIRIuv9pVgrtndNx8EVLF%2BW9Nz33cfyCtwZtIkKygxUJFuetFJSmiTUE4EfUbU%2BBxTBEAyogZGlOngd%2FbOI0%2F9%2BGHkdx22zt8EySYjt0UW7hMHZplk%2FQfHdffk4QNi5yn2kyf3TdIx59CuaB1RyPU3MrPd7a%2B2HTdWuA%3D%3D&csid=3024dac4-b012-47ab-b9df-0ed6b2844afe'
    res = request_s(url,cookie,0)
    result=res['result']
    if not result:
        msg('❗️该账户cookie失效\n')
    return result


# 一日三餐领水滴
def threeWater(cookie):
    msg('开始一日三餐领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=RVBgMC3rDAa%2B6rKrqxx3mPMSgMilMHIQKu5zhIwvqo28R3TDPFE8QGO9AS9ZO4lOinpol5USg%2FpjTLDTDYk7fbuFVZgMUfB%2BM8yBZffQPeg4EnBJnVa7AD4kMs7%2B5PEMfRWzL7uTY0S%2B8ZYFubEkDX%2FxkxTY2SakfJy2PMMMdr%2F3JH3ZNy09Xrk9UuYUhfr30AgB%2B8eRv80KkH1qiMp8E6RkGCsr0w7v6rrkGdjZJerR%2BgjN3UNIKj3ZXUQegOX7FUURkapkHuKo%2Bcma693CzUmtci%2FqE1GdgLhNftISsBBIhW%2F720x%2Bi3mSwG2Ze4IlERzfHqUE1w2YPQ2iYhRNftCx2FLTRszkMJ1K%2BHi1pUNioSYIAHNDtRt4EAwsEe37vas2jRcWyGopDgh8qnvzrK%2FfRjSXtA6KlsN%2BgKmcIMeOVPL5gE7KhrTPBOv06OTNwJ%2BZ0R4BaVmvALTZPKTCVBY875o2GUhRXE4BK5aB%2BunGx7dSe0imCjv%2FWFAVLI3aUZaKhGdqS%2FrxCf6jpCK4byqgCaVRRyTFYNJmxbEJwsZtGRx1FXgPVAXBEkZlmwuMw7JO7i5oY1CgFXzeZEr%2BtxXhgkIGysqlnlZEND8sjMWg%2BQcKSfuk4H7Ugic1%2BiG9onKWzuAbBgeuaGfK4sDvcyoivLZsux6%2Bu8DGC1TdIPlr8Zqgf0dD%2B9ypZwMbzRPBzZH0m9HvdDXQzfx5AOgljulAdvijo68xURHVtCKAP%2Fqg3dJjlGcIb6jH8yOu4MuuPMMk%2FY%2FppmqKTHUcSQqt4aQpWZ7s24YlfcaZmJcPal%2FUJpR5OstOTXABM%2FcYLqssN3CgrmywMKv6Nd%2FA6yg%2F6L7lOSlf7qZ5slWLKjvooLAlmhqyAPKV7h6UqchlVFEd04cEjOPPZ6B%2BklTM3PKtNBMLUgMWTRCHVUqDQ9iTC27wdRmmn8bhoQnX%2BzY4gL7WL6j%2Bo6OW22BOYhlPEQV7%2FKpE52VTcSvxcQEaAbZXYQVkYHOgKTQdxIpGgmxgKgS1gYcOKBR3Ee5kpTsx&csid=880aa606-c566-4871-a5c4-bbc520c6616b'
    res = request_s(url,cookie)


def doTask(cookie):
    a=getUserInfo(cookie)
    if not a:
        return
    threeWater(cookie)


## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.message()
    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = f'{msg_info}\n{self.str_msg}'
        except:
            msg_info = f'{self.str_msg}'
        sys.stdout.flush()
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/jd/main/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath('.')
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")
                
msg("").main()  # 初始化通知服务


if __name__ == '__main__':
    msg('🔔小德果园-一日三餐领水滴，开始！\n')
    ua=ua_random()
    cookie_list=Judge_env().main_run()
    msg(f'====================共{len(cookie_list)}高德地图个账号Cookie=========\n')
    for e,cookie in enumerate(cookie_list,start=1):
        msg(f'******开始【账号 {e}】 做任务*********\n')
        doTask(cookie)
    send('🔔小德果园-一日三餐领水滴', msg_info)   # 启用通知服务

