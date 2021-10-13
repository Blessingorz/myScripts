#!/usr/bin/env python3
# -*- coding: utf-8 -*
# 环境变量JD_WSCK
import linecache
import random
import requests
import time
import json
import re
import uuid
import os
requests.packages.urllib3.disable_warnings()

    
def gettimestamp():
    return str(int(time.time() * 1000))
    

def getckitem(key):
    url = "http://127.0.0.1:5700/api/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()
    r = s.get(url)
    try:
        for i in json.loads(r.text)["data"]:
            if key in i["value"]:
                return i
    except:
        return []


# 随机ua
def cloud_info():
    url = 'https://hellodns.coding.net/p/sign/d/jsign/git/raw/master/check_api'
    g=0
    while g<3:
        g+=1
        try:
            res = requests.get(url=url, verify=False, timeout=20).text
            break
        except requests.exceptions.ReadTimeout:
            print("\n获取ua超时, 正在重试!")
            time.sleep(1) 
    try:
        ua=json.loads(res)['User-Agent']
    except:
        print('随机ua出错，使用固定ua')
        ua='jdpingou;android;5.5.0;11;network/wifi;model/M2102K1C;appBuild/18299;partner/lcjx11;session/110;pap/JA2019_3111789;brand/Xiaomi;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36'
    return ua


# 网络请求sign
def get_sign():
    url = 'https://hellodns.coding.net/p/sign/d/jsign/git/raw/master/sign'
    g=0
    while g<3:
        g+=1
        try:
            res = requests.get(url=url, verify=False, timeout=20)
            break
        except requests.exceptions.ConnectTimeout:
            print("\n获取Sign超时, 正在重试!" + str(i))
            time.sleep(1)
    sign_list = json.loads(res.text)
    svv = sign_list['sv']
    stt = sign_list['st']
    suid = sign_list['uuid']
    jign = sign_list['sign']
    return svv, stt, suid, jign


## 网络接口
def genToken(wskey):
    ua = cloud_info()
    sv, st, uuid, sign = get_sign()
    headers = {
        'cookie': wskey,
        'User-Agent': ua,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate'
    }
    params = {
        'functionId': 'genToken',
        'clientVersion': '10.1.2',
        'client': 'android',
        'uuid': uuid,
        'st': st,
        'sign': sign,
        'sv': sv
    }
    url = 'https://api.m.jd.com/client.action'
    data = 'body=%7B%22action%22%3A%22to%22%2C%22to%22%3A%22https%253A%252F%252Fplogin.m.jd.com%252Fcgi-bin%252Fm%252Fthirdapp_auth_page%253Ftoken%253DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%2526client_type%253Dandroid%2526appid%253D879%2526appup_type%253D1%22%7D&'
    g=0
    while g<3:
        g+=1
        time.sleep(0.5)
        try:
            res = requests.post(url=url, params=params, headers=headers, data=data, verify=False, timeout=10)
            res_json = json.loads(res.text)
            tokenKey = res_json['tokenKey']
            break
        except:
            print('获取tokenkey失败')
            return 'pt_key=fake_re6EXBLOwPpclAvmNEydn12TItLWog7P;pt_pin=%2A%2A%2A%2A%2A%2A'
    return getJDCookie(tokenKey,ua)


def getJDCookie(tokenKey,ua):
    headers = {
        'User-Agent': ua,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    }
    params = {
        'tokenKey': tokenKey,
        'to': 'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page?token=AAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg',
        'client_type': 'android',
        'appid': 879,
        'appup_type': 1,
    }
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
    try:
        time.sleep(0.5)
        res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False, timeout=20)
        res_set = res.cookies.get_dict()
    except:
        res_set={'pt_key':'fake_re6EXBLOwPpclAvmNEydn12TItLWog7P','pt_pin':'%2A%2A%2A%2A%2A%2A'} 
    # print('res_set: ',res_set)
    pt_key = 'pt_key=' + res_set['pt_key']
    pt_pin = 'pt_pin=' + res_set['pt_pin']
    jd_ck = str(pt_key) + ';' + str(pt_pin) + ';'
    # print('jd_ck: ',jd_ck)
    return jd_ck
    # except:
        # print("接口转换失败, 默认wskey失效\n")
        # print('出错位置： getJDCookie(tokenKey,ua)')


def wstopt(wskey):    
    time.sleep(10)
    r = genToken(wskey)
    # r = getJDCookie(tokenKey,ua)
    return r


def update(text, qlid):
    url = "http://127.0.0.1:5700/api/envs?t=%s" % gettimestamp()
    s.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    data = {
        "name": "JD_COOKIE",
        "value": text,
        "_id": qlid
    }
    r = s.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def insert(text):
    url = "http://127.0.0.1:5700/api/envs?t=%s" % gettimestamp()
    s.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    data = []
    data_json = {
        "value": text,
        "name": "JD_COOKIE"
    }
    data.append(data_json)
    r = s.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def ask_cookie(count,i):
    global JD_COOKIE_str   
    r = wstopt(i)
    ptck = r
    global g
    g+=1
    wspin = re.findall(r"pin=(.*?);", i)[0]
    if 'fake' in ptck:
        print("第%s个wskey可能过期了,pin为%s" % (count, wspin))
        state=1
    elif ptck == "wskey错误":
        print("第%s个wskey可能过期了,pin为%s" % (count, wspin))
        state=1
    elif ptck == "未知错误" or ptck == "error":
        print("第%s个wskey发生了未知错误,pin为%s" % (count, wspin))
        state=1
    elif "</html>" in ptck:
        print("你的ip被cloudflare拦截")
        state=1
    else:
        ptpin = re.match(r'.+pin=(.+)\;', ptck).group(1)
        item = getckitem("pt_pin=" + ptpin)
        if item != []:
            qlid = item["_id"]
            if update(ptck, qlid):
                print("第%s个wskey更新成功,pin为%s\n" % (count, wspin))
                if JD_COOKIE_str!='':
                    JD_COOKIE_str=JD_COOKIE_str+'&'+r
                else:
                    JD_COOKIE_str=r
                state=0
            else:
                print("第%s个wskey更新失败,pin为%s" % (count, wspin))
                state=1
        else:
            if insert(ptck):
                print("第%s个wskey添加成功\n" % count)
                if JD_COOKIE_str!='':
                    JD_COOKIE_str=JD_COOKIE_str+'&'+r
                else:
                    JD_COOKIE_str=r  
                state=0
            else:
                print("第%s个wskey添加失败" % count)
                state=1
    if g==3:
        print(f'放弃第 {count} 个wskey\n')
        return
    if state==1:
        return ask_cookie(count,i)
            
def main_run_1(wskeys):
    count = 1
    for i in wskeys:
        global g
        g=0
        ask_cookie(count,i)
        count += 1


def env_var(key):
    return os.environ[key].split('&')


# 返回值 Token
def ql_login():
    path = '/ql/config/auth.json'
    if os.path.isfile(path):
        with open(path, "r") as file:
            auth = file.read()
            file.close()
        auth = json.loads(auth)
        username = auth["username"]
        password = auth["password"]
        token = auth["token"]
        if token == '':
            url = "http://127.0.0.1:5700/api/login"
            payload = {
                "username": username,
                "password": password
            }
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                res = requests.post(url=url, headers=headers, data=payload, verify=False)
                token = json.loads(res.text)['token']
            except:
                print("青龙登录失败, 请检查面板状态!")
                exit(1)
            else:
                return token
        else:
            return token
    else:
        print("没有发现auth文件, 你这是青龙吗???")
        exit(0)

def local_wskey():
    b=[]
    n=0
    while n<15:
        n+=1
        try:
            a=eval(f'wskey_list_{n}[0]')
            if len(a)>5:
                b.append(a)
        except:
            pass
    return b


ver = 916


if __name__ == '__main__':
    JD_COOKIE_str=''
    token=ql_login()
    if 'JD_WSCK' in os.environ:
        wskeys=env_var('JD_WSCK')
    else:
        wskeys=local_wskey()
    s = requests.session()
    s.headers.update({"authorization": "Bearer " + token})
    s.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    main_run_1(wskeys)
    with open('/ql/config/code/JD_COOKIE.txt', 'w') as f:
        f.write(JD_COOKIE_str)


