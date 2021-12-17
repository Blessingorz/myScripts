#!/usr/bin/python3
import os,sys
import json,time,re,random,logging,string,urllib
import requests
import smtplib
import copy
from email.mime.text import MIMEText
from email.header import Header
requests.packages.urllib3.disable_warnings()


# 邮箱推送
# 变量
inbox="xxxxxxxx@qq.com"     # 收信箱
mail_host="smtp.163.com"    # smtp服务器
mail_port="25"              # smtp服务端口
mail_user="xxx@163.com"    # 登录账号
mail_pass="xxx"            # 登录密码


# 调用
title="邮件标题"
content="邮件内容"
# sendmail(title, content)   # 邮箱推送


def sendmail(title, content):
    if not inbox or inbox=='xxxxxxxx@qq.com': 
        print('未配置收信箱')
        return
    sender = mail_user
    receivers = [inbox]
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
    message['From'] = mail_user
    message['To'] =  inbox

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, int(mail_port)) 
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print ("Error: 无法发送邮件")
        print(e)
