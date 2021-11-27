# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28

import sys
import os, re
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse

# 通知服务
push_config={
    'BARK' : '',                   # bark服务,自行搜索;
    'SCKEY' : '',                  # Server酱的SCKEY;
    'TG_BOT_TOKEN' : '',           # tg机器人的TG_BOT_TOKEN;
    'TG_USER_ID' : '',             # tg机器人的TG_USER_ID;
    'TG_API_HOST' : '',            # tg 代理api
    'TG_PROXY_HOST' : '',          # tg机器人的TG_PROXY_HOST;
    'TG_PROXY_PORT' : '',          # tg机器人的TG_PROXY_PORT;
    'DD_BOT_TOKEN' : '',           # 钉钉机器人的DD_BOT_TOKEN;
    'DD_BOT_SECRET' : '',          # 钉钉机器人的DD_BOT_SECRET;
    'QQ_SKEY' : '',                # qq机器人(qmsg 酱)的QQ_SKEY;
    'QQ_MODE' : '',                # qq机器人(qmsg 酱)的QQ_MODE;
    'QYWX_AM' : '',                # 企业微信应用
    'PUSH_PLUS_TOKEN' : '',        # 微信推送Plus+
    'PUSH_PLUS_USER' : '',         # plus+群组编码,可为空
# 
    'FSKEY' : '',                  # 飞书机器人的 FSKEY
    'GOBOT_URL' : '',              # go-cqhttp  # 推送到个人QQ：http://127.0.0.1/send_private_msg  # 群：http://127.0.0.1/send_group_msg
    'GOBOT_QQ' : '',               # go-cqhttp 的推送群或用户  # GOBOT_URL 设置 /send_private_msg 时填入 user_id=个人QQ  # /send_group_msg   时填入 group_id=QQ群
    'GOBOT_TOKEN' : '',            # go-cqhttp 的 access_token
}


message_info = ''''''
push_config_s=dict()         # 整合通知服务本地和环境变量  


# 整合通知服务本地和环境变量
def initialize(d):
    global message_info,push_config_s
    message_info = ''''''
    for push_key in d.keys():   
        if push_key in os.environ and os.environ[push_key]:
            push_config_s[push_key]=os.environ[push_key]
        elif push_config[push_key]:
            push_config_s[push_key]=push_config[push_key]
        else:
            push_config_s[push_key]=d[push_key]
initialize(push_config)     # 初始化


def msg(*args):
    global message_info
    a=''.join([str(arg) for arg in args])
    print(a)
    message_info = f"{message_info}\n{a}"
    sys.stdout.flush()


def bark(title, content):
    if not push_config_s['BARK']:
        print("bark服务的bark_token未设置!!\n取消推送")
        return
    print("bark服务启动")
    try:
        response = requests.get(
            f"""https://api.day.app/{push_config_s['BARK']}/{title}/{urllib.parse.quote_plus(content)}""").json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except:
        print('推送失败！')

def serverJ(title, content):
    if not push_config_s['SCKEY']:
        print("server酱服务的SCKEY未设置!!\n取消推送")
        return
    print("serverJ服务启动")
    data = {
        "text": title,
        "desp": content.replace("\n", "\n\n")
    }
    response = requests.post(f"https://sc.ftqq.com/{push_config_s['SCKEY']}.send", data=data).json()
    if response['errno'] == 0:
        print('推送成功！')
    else:
        print('推送失败！')

# tg通知
def telegram_bot(title, content):
    try:
        bot_token = push_config_s['TG_BOT_TOKEN']
        user_id = push_config_s['TG_USER_ID']
        if not bot_token or not user_id:
            print("tg服务的bot_token或者user_id未设置!!\n取消推送")
            return
        print("tg服务启动")
        if push_config_s['TG_API_HOST']:
            if 'http' in push_config_s['TG_API_HOST']:
                url = f"{push_config_s['TG_API_HOST']}/bot{push_config_s['TG_BOT_TOKEN']}/sendMessage"
            else:
                url = f"https://{push_config_s['TG_API_HOST']}/bot{push_config_s['TG_BOT_TOKEN']}/sendMessage"
        else:
            url = f"https://api.telegram.org/bot{push_config_s['TG_BOT_TOKEN']}/sendMessage"

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'chat_id': str(push_config_s['TG_USER_ID']), 'text': f'{title}\n\n{content}', 'disable_web_page_preview': 'true'}
        proxies = None
        if push_config_s['TG_PROXY_HOST'] and push_config_s['TG_PROXY_PORT']:
            proxyStr = "http://{}:{}".format(push_config_s['TG_PROXY_HOST'], push_config_s['TG_PROXY_PORT'])
            proxies = {"http": proxyStr, "https": proxyStr}
        try:
            response = requests.post(url=url, headers=headers, params=payload, proxies=proxies).json()
        except:
            print('推送失败！')
        if response['ok']:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)

def dingding_bot(title, content):
    timestamp = str(round(time.time() * 1000))  # 时间戳
    secret_enc = push_config_s['DD_BOT_SECRET'].encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, push_config_s['DD_BOT_SECRET'])
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))  # 签名
    print('开始使用 钉钉机器人 推送消息...', end='')
    url = f"https://oapi.dingtalk.com/robot/send?access_token={push_config_s['DD_BOT_TOKEN']}&timestamp={timestamp}&sign={sign}"
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'text',
        'text': {'content': f'{title}\n\n{content}'}
    }
    response = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=15).json()
    if not response['errcode']:
        print('推送成功！')
    else:
        print('推送失败！')


def coolpush_bot(title, content):
    """
    使用 qmsg 推送消息。
    """
    if not push_config_s.get("QMSG_KEY") or not push_config_s.get("QMSG_TYPE"):
        print("qmsg 的 QMSG_KEY 或者 QMSG_TYPE 未设置!!\n取消推送")
        return
    print("qmsg 服务启动")

    url = f'https://qmsg.zendee.cn/{push_config_s.get("QMSG_TYPE")}/{push_config_s.get("QMSG_KEY")}'
    payload = {"msg": f'{title}\n\n{content.replace("----", "-")}'.encode("utf-8")}

    try:
        response = requests.post(url=url, params=payload, timeout=15)
        try:
            datas = response.json()
            if response.get("code") == 0:
                print("qmsg 推送成功！")
            else:
                print(f'qmsg 推送失败！错误信息：{datas.get("reason")}')
        except json.JSONDecodeError:
            print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response.text}")
    except requests.exceptions.RequestException:
        print(f"网络异常，请检查你的网络连接、推送服务器和代理配置。\n{traceback.format_exc()}")
    except Exception:
        print(f"其他错误信息：\n{traceback.format_exc()}")
    

# push+推送
def pushplus_bot(title, content):
    try:
        if not push_config_s['PUSH_PLUS_TOKEN']:
            print("push+ 服务的token未设置!!\n取消推送")
            return
        data={
            "token": push_config_s['PUSH_PLUS_TOKEN'],
            "title": title,
            "content": content,
            "topic": push_config_s['PUSH_PLUS_USER'],
        }
        print("push+ 服务启动")
        url='https://www.pushplus.plus/send'
        headers={
            "Content-Type":"application/json"
		}
        data=json.dumps(data).encode(encoding='utf-8')
        response = requests.post(url=url, data=data, headers=headers).json()
        if response['code']==200:
            print(f"push+ 推送成功！")
        else:
            print(f"push+ 推送失败！")
            print(response) 
    except Exception as e:
        print(e)

# 企业微信 APP 推送
def wecom_app(title, content):
    try:
        if not push_config_s['QYWX_AM']:
            print("push_config_s['QYWX_AM'] 并未设置！！\n取消推送")
            return
        QYWX_AM_AY = re.split(',', push_config_s['QYWX_AM'])
        if 4 < len(QYWX_AM_AY) > 5:
            print("push_config_s['QYWX_AM'] 设置错误！！\n取消推送")
            return
        print("企业微信应用服务启动")
        corpid = QYWX_AM_AY[0]
        corpsecret = QYWX_AM_AY[1]
        touser = QYWX_AM_AY[2]
        agentid = QYWX_AM_AY[3]
        try:
            media_id = QYWX_AM_AY[4]
        except:
            media_id = ''
        wx = WeCom(corpid, corpsecret, agentid)
        # 如果没有配置 media_id 默认就以 text 方式发送
        if not media_id:
            message = title + '\n\n' + content
            response = wx.send_text(message, touser)
        else:
            response = wx.send_mpnews(title, content, media_id, touser)
        if response == 'ok':
            print('推送成功！')
        else:
            print('推送失败！错误信息如下：\n', response)
    except Exception as e:
        print(e)

class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace('\n', '<br/>'),
                        "digest": message
                    }
                ]
            }
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

def feishu_bot(title, content):
    """
    使用 飞书机器人 推送消息。
    """
    if not push_config_s.get("FSKEY"):
        print("飞书 服务的 FSKEY 未设置!!\n取消推送")
        return
    print("飞书 服务启动")

    url = f'https://open.feishu.cn/open-apis/bot/v2/hook/{push_config_s.get("FSKEY")}'
    data = {"msg_type": "text", "content": {"text": f"{title}\n\n{content}"}}
    try:
        response = requests.post(url, data=json.dumps(data), timeout=15)
        try:
            datas = response.json()
            if datas.get("StatusCode") == 0:
                print("飞书 推送成功！")
            else:
                print(f"飞书 推送失败！响应数据：{datas}")
        except json.JSONDecodeError:
            print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response.text}")
    except requests.exceptions.RequestException:
        print(f"网络异常，请检查你的网络连接、推送服务器和代理配置。\n{traceback.format_exc()}")
    except Exception:
        print(f"其他错误信息：\n{traceback.format_exc()}")

def go_cqhttp(title, content):
    """
    使用 go_cqhttp 推送消息。
    """
    if not push_config_s.get("GOBOT_URL") or not push_config_s.get("GOBOT_QQ") or not push_config_s.get("GOBOT_TOKEN"):
        print("go-cqhttp 服务的 GOBOT_URL 或 GOBOT_QQ 或 GOBOT_TOKEN 未设置!!\n取消推送")
        return
    print("go-cqhttp 服务启动")

    url = f'{push_config_s.get("GOBOT_URL")}?access_token={push_config_s.get("GOBOT_TOKEN")}&{push_config_s.get("GOBOT_QQ")}&message=标题:{title}\n内容:{content}'

    try:
        response = requests.get(url, timeout=15)
        try:
            datas = response.json()
            if datas.get("status") == "ok":
                print("go-cqhttp 推送成功！")
            else:
                print(f"go-cqhttp 推送失败！响应数据：{datas}")
        except json.JSONDecodeError:
            print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response.text}")
    except requests.exceptions.RequestException:
        print(f"网络异常，请检查你的网络连接、推送服务器和代理配置。\n{traceback.format_exc()}")
    except Exception:
        print(f"其他错误信息：\n{traceback.format_exc()}")

def send(title,text=''):
    """
    使用 bark, telegram bot, dingding bot, serverJ 发送手机推送
    :param title:
    :param content:
    :return:
    """
    if text:
        content=text+'\n'+message_info
    else:
        content=message_info
    content += '\nBy: https://github.com/wuye999/myScripts'

    if push_config_s['BARK']:
        bark(title, content)

    if push_config_s['SCKEY']:
        serverJ(title, content)

    if push_config_s['DD_BOT_TOKEN'] and push_config_s['DD_BOT_SECRET']:
        dingding_bot(title, content)

    if push_config_s['TG_BOT_TOKEN'] and push_config_s['TG_USER_ID']:
        telegram_bot(title, content)

    if push_config_s['QQ_SKEY'] and push_config_s['QQ_MODE']:
        coolpush_bot(title, content)

    if push_config_s['PUSH_PLUS_TOKEN']:
        pushplus_bot(title, content)

    if push_config_s['QYWX_AM']:
        wecom_app(title, content)

    if push_config_s['FSKEY']:
        feishu_bot(title, content)

    if push_config_s["GOBOT_URL"] and push_config_s["GOBOT_QQ"] and push_config_s['GOBOT_TOKEN']:
        go_cqhttp(title, content)


def main():
    send('title', 'content')


if __name__ == '__main__':
    main()
