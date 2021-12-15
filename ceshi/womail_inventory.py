#!/usr/bin/python3
import os,sys
import json,time,re,random,logging,string,urllib
import requests
import smtplib
import copy
from email.mime.text import MIMEText
from email.header import Header
requests.packages.urllib3.disable_warnings()


# cron: */10 * * * *
# new Env('沃邮箱公众号商品监控');
# 当前监控商品的数据与上次监控的数据比较，如果出现变化，则发送通知服务
# 环境变量或脚本内填写以下变量
unicom_inbox="xxxxxxxx@qq.com"     # 收信箱
unicom_womail=""                   # 沃邮箱url
unicom_keyword="话费&腾讯视频"      # 监控商品关键字多个以&隔开


inventory_old=dict()    # 旧的库存数据
inventory_new=dict()    # 新的库存数据


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


# 保存数据
def saveData(key, value):
    try:
        if os.path.abspath('.')=='/var/user' and os.path.exists('/tmp'):
            print('当前环境为云函数，无法保存数据')
            return
        with open(f"./{key}.json",'w') as f:
            json.dump(value,f)
            print(f'保存数据成功')
    except Exception as e:
        print(f'保存数据失败\n{e}')


# 读取数据
def readData(key):
    try:
        if not os.path.exists(f"./{key}.json"):
            print('数据文件不存在')
            return
        with open(f"./{key}.json", 'r') as f:
            value = json.loads(f.read())
        if value:
            return value
        else:
            print('数据为空')
            return value
    except Exception as e:
        print(f'读取数据失败\n{e}')


def sendmail(title, content):
    if not get_env('unicom_inbox') or get_env('unicom_inbox')=='xxxxxxxx@qq.com': 
        print('未配置收信箱')
        return
    mail_host="smtp.163.com"
    mail_user="kirisame_marisas@163.com"
    mail_pass="NKVLOJKWETGENOKY"
    sender = 'kirisame_marisas@163.com'
    receivers = [get_env('unicom_inbox')]
    mail_msg='''
        <html>

        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        </head>

        <body>
            <div style="line-height:1.6;font-family:'雾雨魔理沙','雾雨魔理沙','sans-serif';"><br>'''+content.replace('\n','<br>')+'''<br></div>
            <div class="ne-quoted"> <a href="https://mail-online.nosdn.127.net/wzpmmc/90fda2a455c37350f9fa0e4f988027df.jpg"
                    display:block;background:#fff; max-width: 400px; _width: 400px;padding:15px 0 10px 0;text-decoration: none;
                    outline:none;-webkit-tap-highlight-color:transparent;-webkit-text-size-adjust:none
                    !important;text-size-adjust:none !important;">
                                  <table cellpadding="0"
                        style="width: 100%; max-width: 100%; table-layout: fixed; border-collapse: collapse;color: #9b9ea1;font-size: 14px;line-height:1.3;-webkit-text-size-adjust:none !important;text-size-adjust:none !important;">
                        <tbody
                            style="font-family: 'PingFang SC', 'Hiragino Sans GB','WenQuanYi Micro Hei', 'Microsoft Yahei', '4', verdana !important; word-wrap:break-word; word-break:break-all;-webkit-text-size-adjust:none !important;text-size-adjust:none !important;">
                            <tr>
                                <td width="38" style="padding:0; box-sizing: border-box; width: 38px;">
                                    <img width="38" height="38"
                                        style="vertical-align:middle; width: 38px; height: 38px; border-radius:50%;"
                                        src="https://mail-online.nosdn.127.net/wzpmmc/90fda2a455c37350f9fa0e4f988027df.jpg">
                                </td>
                                <td style="padding: 0 0 0 10px; color: #31353b;">
                                    <div
                                        style="font-size: 16px;font-weight:bold; width:100%; white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                        雾雨魔理沙</div>
                                    <div
                                        style="font-size: 14px;width:100%; margin-top: 3px; white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                        邮差</div>
                                </td>
                            </tr>
                            <tr width="100%" style="font-size: 14px !important; width: 100%;">
                                <td colspan="2" style="padding:10px 0 0 0; font-size:14px !important; width: 100%;">
                                    <div
                                        style="width: 100%;font-size: 14px !important;word-wrap:break-word;word-break:break-all;">
                                        kirisame_Marisa</div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </a>
                <html>

                <body></body>

                </html>
            </div>
        </body>

        </html>
    '''
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['Subject'] = title
    message['From'] = "kirisame_marisas@163.com"
    message['To'] =  get_env('unicom_inbox')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print ("Error: 无法发送邮件")
        print(e)


def womail_login():
    print('沃邮箱url登录')
    unicom_womail=get_env('unicom_womail')
    if not unicom_womail:
        print('未配置沃邮箱url')
        return False
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(unicom_womail).query))
    params = (
        ('mobile', query['mobile'].replace(' ', '+')),
        ('userName', ''),
        ('openId', query['openId'].replace(' ', '+')),
    )
    global session
    session=requests.Session()
    session.headers={
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'X-Requested-With': 'com.tencent.mm',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://club.mail.wo.cn/clubwebservice/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    url="https://club.mail.wo.cn/clubwebservice"
    session.get(url=url, params=params)  # 登录
    value={'unicom_womail':unicom_womail, 'cookies': session.cookies.get_dict()}
    saveData('womail_inventory_cookies', value)
    

def womail_cookies_login():
    unicom_womail=get_env('unicom_womail')
    if not unicom_womail:
        print('未配置沃邮箱url')
        return False
    cookies=readData('womail_inventory_cookies')
    if cookies.get('unicom_womail','')!=unicom_womail:
        print('账号信息发生改变')
        return 
    global session
    session=requests.Session()
    session.headers={
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'X-Requested-With': 'com.tencent.mm',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://club.mail.wo.cn/clubwebservice/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    if cookies.get('cookies',''):
        print('cookies登录')
        session.cookies=requests.utils.cookiejar_from_dict(cookies['cookies']) 
        jifen=get_person_centre()
        value={'unicom_womail':unicom_womail, 'cookies': session.cookies.get_dict()}
        saveData('womail_inventory_cookies', value)
        if jifen: return jifen
        else: 
            print('cookies登录失败')
            return
    else: return   


# 查询积分
def get_person_centre():
    global session
    try:
        url = "https://club.mail.wo.cn/clubwebservice/growth/get-person-centre"
        res = session.get(url).json()
        memberUser=res['data']['memberUser']
        phoneNum=f'账号 {memberUser["phoneNum"][:3]}********'
        levelName=f'俱乐部会员等级 {memberUser["levelName"]}'
        growthValue=f'俱乐部成长值 {memberUser["growthValue"]}'
        score=f'剩余积分 {res["data"].get("score",None)}'
        # print(f"{phoneNum}\n{levelName}\n{growthValue}\n{score}")
        return f"{phoneNum}\n{levelName}\n{growthValue}\n{score}\n"
    except:
        print('登录失败')


# 商品详情页
num_findall=re.compile(r'<span class="num">(.*?)</span>')
num_closingDate_findall=re.compile(r'<span class="num closingDate">(.*?)</span>')
show_exchange_styleclass_findall=re.compile(r'"exchange-dd show-exchange-style" name=".*?">(.*?)</p>')
def exchange_goods(name,url):
    global inventory_new
    session.headers.update({'Referer': 'https://club.mail.wo.cn/clubwebservice/score-exchange/into-score-exchange'})
    res = session.get(url).text
    num=re.findall(num_findall, res)[0]         # 库存
    num_closingDate=re.findall(num_closingDate_findall, res)[0]     # 截至日期
    show_exchange_styleclass=re.findall(show_exchange_styleclass_findall, res)[0]       # 兑换方式
    inventory_new[name]={
        '库存': num,
        '截至日期': num_closingDate,
        '兑换方式': show_exchange_styleclass
    }


# 商品列表
dd_findall=re.compile(r'<dd>(.*?)</dd>',re.M|re.S)
goods_split=re.compile(r'(?:<p>)|(?:</p>)')
goods_findall=re.compile(r'<ahref="(.*?)">')
def into_score_exchange():
    url="https://club.mail.wo.cn/clubwebservice/score-exchange/into-score-exchange"
    session.headers.update({'Referer': 'https://club.mail.wo.cn/clubwebservice'})
    res = session.get(url).text
    goods_dict=dict()
    goods_list=re.findall(dd_findall, res)      # 提取所有商品信息
    goods_list=[goods.replace(' ','') for goods in goods_list]      # 去除所有空格
    for goods in goods_list:
        goods=re.split(goods_split,goods)           # 分割商品名称和商品链接
        goods_dict[goods[1]]=re.findall(goods_findall, goods[3])[0]     # 以字典形式写入 商品名称: 商品链接
    unicom_keyword_list=get_env('unicom_keyword').split('&')
    goods_dict_keyword=dict()
    for k,v in goods_dict.items():
        for keyword in unicom_keyword_list:
            if keyword in k:
                goods_dict_keyword[k]=v
    return goods_dict_keyword


def main():
    cookies=readData('womail_inventory_cookies')
    if cookies:
        if womail_cookies_login(): pass
        else: womail_login()              # 登录 
    else: womail_login()              # 登录
    
    jifen=get_person_centre()   # 查询积分
    if not jifen: return   

    goods_dict_keyword=into_score_exchange()     # 商品列表
    for name,url in goods_dict_keyword.items():
        exchange_goods(name,url)        # 商品详情页

    global inventory_old,inventory_new
    inventory_new=json.dumps(inventory_new)   
    inventory_new=json.loads(inventory_new)
    inventory_old=readData('womail_inventory_old')
    if not inventory_old==inventory_new:
        inventory_old=copy.deepcopy(inventory_new)
        saveData('womail_inventory_old', inventory_old)
        title='沃邮箱话费商品变动报告'
        content=''''''
        content+=f"当前时间: {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))}\n"     # 打印时间
        content+=jifen
        for name,value in inventory_old.items():
            content+='---------------\n'
            content+=f'商品名称: {name}\n'        # 打印商品名称
            for k,v in value.items():
                content+=f'{k}: {v}\n'           # 打印商品各属性
        content+="\n"
        sendmail(title, content)                    # 邮箱推送
    else:
        content=''''''
        content+=f"当前时间: {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))}\n"     # 打印时间
        content+=jifen
        for name,value in inventory_old.items():
            content+='---------------\n'
            content+=f'商品名称: {name}\n'        # 打印商品名称
            for k,v in value.items():
                content+=f'{k}: {v}\n'           # 打印商品各属性
        content+="\n"

    print(content)
    sys.stdout.flush()


if __name__ == '__main__':
    main()
