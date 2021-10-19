#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author:fugui
import os,re
import requests
import sys
sys.path.append('../../tmp')
requests.packages.urllib3.disable_warnings()
'''
云函数环境变量填写，环境变量优先
| key               | value                                 | 说明
| script_add        | https://ghproxy.com/xxxx/xxx/xxx.py   | 需要运行的脚本地址，仅支持我的库的一部分脚本      |
| script_update     | no                                    | 每次运行时是否强制更新脚本，yes或no,不填则为no    |

接着填写你需要运行的xxx.py脚本所需要的环境变量
推送通知变量请查看： https://github.com/wuye999/myScripts/blob/main/send.md
'''

# 读取环境变量
def get_env(env):
    if env in os.environ:
        a=os.environ[env]
    else:
        pass 
    return a

# 获取脚本
def get_script():
    url=get_env('script_add')
    for n in range(3):
        try:
            response = requests.get(url,timeout=3)
            with open('../../tmp/task.py', "w+", encoding="utf-8") as f:
                f.write(response.text)
            a=1
            break
        except:
            a=0
            pass 
    if a!=1:
        print('获取脚本失败\n')

# 导入脚本
def impp():
    global task
    script_update="no"
    try:
        script_update=get_env('script_update')
    except:
        pass
    if script_update=="yes":
        get_script()
    for n in range(3):
        if os.path.exists("../../tmp/task.py"):
            try:
                from task import main as task
                break
            except:
                get_script()
        else:
            get_script()



## 获取通知服务
class Msg(object):
    def getsendNotify(self, a=1):
        try:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py'
            response = requests.get(url,timeout=3)
            with open('../../tmp/sendNotify.py', "w+", encoding="utf-8") as f:
                f.write(response.text)
            return
        except:
            pass
        if a < 5:
            a += 1
            return self.getsendNotify(a)

    def main(self):
        script_update="no"
        try:
            script_update=get_env('script_update')
        except:
            pass
        if script_update=="yes":
            self.getsendNotify()
        if not os.path.exists("../../tmp/sendNotify.py"):
            self.getsendNotify()
Msg().main()   # 初始化通知服务 
    

#腾讯云函数入口
def main_handler(event, context):
    impp()
    task()
    


#主函数入口
if __name__ == '__main__':
    main_handler("","")


