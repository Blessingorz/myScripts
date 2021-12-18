# -*- coding: utf-8 -*-
# @Time    : 2021/12/4 06:00
# @Author  : srcrs,wuye9999,rhming
import os,sys
import base64,time,requests,logging,traceback,random,json
from utils.encryption import encryption

# 设备ID(通常是获取手机的imei) 联通判断是否登录多台设备 不能多台设备同时登录 填写常用的设备ID
# 不填则使用随机imei
# 随机imei
def imei_random():
    value = '86' + ''.join(random.choices('0123456789', k=12))
    sum_ = 0
    parity = 1
    for i, digit in enumerate([int(x) for x in value]):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_ += digit
    value += str((10 - sum_ % 10) % 10)
    return value


#进行登录
#手机号和密码加密代码，参考自这篇文章 http://www.bubuko.com/infodetail-2349299.html?&_=1524316738826
def login(username,password,appId,imei):
    global session
    session = requests.Session()
    flag = False

    session.cookies.update({'devicedId':imei})
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'content-length': '796',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/4.4.0',
    }

    data={
        'simCount': '1',
        'yw_code': '',
        'deviceOS': 'android9',
        'mobile': encryption(username),
        'netWay': '4G',
        'deviceCode': imei,
        'isRemberPwd': 'true',
        'version': 'android@8.0805',
        'deviceId': imei,
        'password': encryption(password),
        'keyVersion': '1',
        'pip': '192.168.43.1',
        'provinceChanel': 'general',
        'appId': appId,
        'deviceModel': 'Redmi Note 7',
        'deviceBrand': 'Xiaomi',
        'timestamp': time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
    }
    
    response = session.post('https://m.client.10010.com/mobileService/login.htm', headers=headers, data=data)
    response.encoding='utf-8'
    try:
        result = response.json()
        if result['code'] == '0':
            logging.info('【账号密码登录】: ' + result['default'][:3]+'********')
            flag = True
        else:
            logging.info('【账号密码登录】: ' + result['dsc'])
    except Exception as e:
        print(traceback.format_exc())
        logging.info('【账号密码登录】: 发生错误，原因为: ' + str(e))

    if flag:
        value={
            'username': username,
            'password': password,
            'appId': appId,
            'imei': imei,
            'cookies': session.cookies.get_dict(),
            'token_online': result.get('token_online',''),
        }
        saveData(username+'login_login_cookies', value)   # 保存cookie
        session.headers = {
                'User-Agent': "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:"+str(username)+"};devicetype{deviceBrand:Xiaomi,deviceModel:Redmi Note 7};{yw_code:}",
        }
        return session
    else:
        return False


# 保存cookie
def saveData(key, value):
    try:
        if os.path.abspath('.')=='/var/user' and os.path.exists('/tmp'):
            logging.info('当前环境为云函数，无法保存数据')
            return
        with open(f"./utils/{key}.json",'w') as f:
            json.dump(value,f)
            logging.info(f'保存数据成功')
    except Exception as e:
        logging.error(f'保存数据失败\n{e}')


# 读取cookie
def readData(key):
    try:
        if not os.path.exists(f"./utils/{key}.json"):
            logging.info('数据文件不存在')
            return
        with open(f"./utils/{key}.json", 'r') as f:
            value = json.loads(f.read())
        if value:
            return value
        else:
            logging.info('数据为空')
            return value
    except Exception as e:
        logging.error(f'读取数据失败\n{e}')



# 获取login会话  
def get_loginSession(username,password,appId,imei):
    if not imei:    # 设备ID(通常是获取手机的imei) 联通判断是否登录多台设备 不能多台设备同时登录 填写常用的设备ID
        imei=imei_random()

    try:
        flag=True
        login_cookies=readData(username+'login_login_cookies')      # 读取cookie
        if login_cookies:       
            if username != login_cookies['username']: flag=False    # 对比账号信息是否更改
            if password != login_cookies['password']: flag=False    # 对比账号信息是否更改
            if appId != login_cookies['appId']: flag=False          # 对比账号信息是否更改
            if not login_cookies['imei']: flag=False                
            if not requests.utils.cookiejar_from_dict(login_cookies['cookies']): flag=False
            if not login_cookies['token_online']: flag=False 
        else:
            flag=False 
    except:
        flag=False 

    # 登录
    if flag:     
        session = onLine(username)      # cookie登录
        if session:    
            return session
        else:
            # 使用cookie登录失败，进行账号密码登录
            session=login(username,password,appId,imei)
            return session
    else:
        # cookie不存在或格式错误，进行账号密码登录
        session=login(username,password,appId,imei)
        return session


# cookie登录       
def onLine(username):
    logging.info(f'【cookie登录】 {username[:3]}******** ')

    login_cookies=readData(username+'login_login_cookies')      # 读取cookie
    username=login_cookies['username']
    password=login_cookies['password']
    appId=login_cookies['appId']
    imei=login_cookies['imei']
    cookies=requests.utils.cookiejar_from_dict(login_cookies['cookies'])        # 将dict形式cookies转换为RequestsCookieJar形式
    token_online=login_cookies['token_online']

    session = requests.Session()
    session.cookies.update({'devicedId':imei})
    url='https://m.client.10010.com//mobileService/onLine.htm'
    headers={
        'content-type': 'application/x-www-form-urlencoded',
        'content-length': '897',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/4.4.0',
    }
    data={
        'reqtime': time.time(),
        'provinceChanel': 'general',
        'appId': appId,
        'netWay': '4G',
        'deviceModel': 'Redmi Note 7',
        'step': 'bindlist',
        'deviceCode': imei,
        'version': 'android@8.0805',
        'deviceId': imei,
        'deviceBrand': 'Xiaomi',
        'flushkey': '1',
        'token_online': token_online,
    }
    res=session.post(url,headers=headers,data=data,cookies=cookies)
    try:
        result=res.json()
        # print(result)
        if result.get('token_online',None):
            logging.info(f'【cookie登录】 成功')

            value={
                'username': username,
                'password': password,
                'appId': appId,
                'imei': imei,
                'cookies': session.cookies.get_dict(),
                'token_online': result.get('token_online',''),
            }
            saveData(username+'login_login_cookies', value)   # 保存cookie

            session.headers = {
                'User-Agent': "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36; unicom{version:android@8.0805,desmobile:"+str(username)+"};devicetype{deviceBrand:Xiaomi,deviceModel:Redmi Note 7};{yw_code:}"
            }
            return session
        else:
            logging.info('cookie已失效')
    except:
        logging.info('cookie已失效')
