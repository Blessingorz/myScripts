# -*- coding: utf-8 -*-

'''
cron: 16 6,16 * * * *
new Env('联通日常任务');
变量: unicom_config_x，通知服务变量
脚本内或环境变量填写，环境变量优先
通知推送服务环境变量请查看：https://github.com/wuye999/myScripts/blob/main/send.md
环境变量示例：
export unicom_config_1="手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫"
export unicom_config_2="手机号2<<<服务密码2<<<appId2<<<抽奖次数(0-30)中奖几率渺茫"
export unicom_womail_1="沃邮箱登陆Url1<<<手机号1(可留空)<<<沃邮箱密码（可留空）"
export unicom_womail_2="沃邮箱登陆Url2<<<手机号2(可留空)<<<沃邮箱密码（可留空）"
export PUSH_PLUS_TOKEN="微信推送Plus+(通知服务示例，可留空或不填)"
'''
# 脚本内示例：
unicom_config_1="18825802580<<<888888<<<appppppp8888888888iiiddd<<<0"
unicom_womail_1="https://nyan.mail.wo.cn/cn/sign/index/index?mobile=aaa&userName=&openId=bbb"
PUSH_PLUS_TOKEN=""


import os,sys
def abspath(p=''):  # 返回项目所在目录
    if '/ql' in os.path.abspath(os.path.dirname(__file__)):
        return os.path.abspath('./unicom-task/'+p)      # 青龙
    elif os.path.abspath('.')=='/var/user' and os.path.exists('/tmp'):
        return os.path.abspath('./'+p)                  # 腾讯云函数
    else:
        return os.path.abspath(os.path.dirname(f'{__file__}/{p}'))      # 其他
os.chdir(abspath())  # 修改当前工作目录为项目目录

sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('./task')
sys.path.append('./tenscf_rely')
sys.path.append('./utils')
import json,time,re,traceback,random,datetime,util,sys,login,logging,importlib
import pytz,requests,rsa,lxml     # 导入 pytz,requests,rsa,lxml 模块，出错请先安装这些模块：pip3 install xxx
from lxml.html import fromstring
try:
    import execjs
except Exception as e:
    print(str(e) + "\n缺少execjs模块, 请执行命令：pip3 install PyExecJS\n")
    exit()
requests.packages.urllib3.disable_warnings()


run_send='yes'      # yes或no,是否启用推送
#用户登录全局变量
client = None


# 腾讯云函数可写日志目录
def log_path(p=''):
    if os.path.abspath('.')=='/var/user' and os.path.exists('/tmp'):
        return f'/tmp/{p}'
    else:
        return f'./utils/{p}'


#日志基础配置
def log():
    # 创建一个logger
    global logger,logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_path('log.txt'), mode='a', encoding='utf-8')   # 创建一个handler，用于写入日志文件
    fh.setFormatter(logging.Formatter("%(filename)s: %(message)s"))
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(filename)s: %(message)s"))     # 创建一个handler，输出到控制台
    logger.addHandler(ch)
log() 


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

# 读取环境变量
def get_env_nofixed(env):
    a=[]
    for n in range(1,999):
        b=get_env(f'{env}_{n}')
        if b:
            a.append(b)
        else:
            break
    return a
    

#读取用户配置信息
#错误原因有两种：格式错误、未读取到错误
def readJson():
    users=list()
    try:
        unicom_config_list=get_env_nofixed('unicom_config')
        if not unicom_config_list:
            logging.error('未读取到账号信息')

        for unicom_config in unicom_config_list:
            user_list=[v for v in unicom_config.split('<<<')]
            user_dict={
                "username": user_list[0],
                "password": user_list[1],
                "appId": user_list[2],
            }
            if len(user_list) > 3:
                if user_list[3] and user_list[3] != '0' and user_list[3] != ' ' :
                    user_dict['lotteryNum']=user_list[3]              
            users.append(user_dict)
    except:
        logging.error('账号变量填写错误')

    womails=list()
    try:
        womail_list=get_env_nofixed('unicom_womail')
        if not unicom_config_list:
            logging.error('未读取到沃邮箱url')

        for womail_str in womail_list:
            womail_str_list=[v for v in womail_str.split('<<<')]
            womail_str_dict={
                "woEmail": womail_str_list[0],
            }
            if len(womail_str_list) > 1:
                if womail_str_list[1] and womail_str_list[1] != ' ' :
                    womail_str_dict['username']=womail_str_list[1]
            if len(womail_str_list) > 2:
                if womail_str_list[2] and womail_str_list[2] != ' ' :
                    womail_str_dict['woEmail_password']=womail_str_list[2]
            womails.append(womail_str_dict)
    except:
        logging.error('沃邮箱变量填写错误')
    return users,womails 

#运行任务
def runTask(client, user):
    with os.scandir(os.path.abspath('./task')) as entries:
        for entry in entries:
            if entry.is_file(): 
                if entry.name=='email_task.py':
                    continue
                task_module = importlib.import_module('task.'+entry.name[:-3])
                task_class = getattr(task_module, entry.name[0:-3])
                task_obj = task_class()
                task_obj.run(client, user)

# 沃邮箱
def runTas_2(womail):
    with os.scandir(os.path.abspath('./task')) as entries:
        for entry in entries:
            if entry.is_file():
                if entry.name != 'email_task.py':
                    continue  
                task_module = importlib.import_module('task.'+entry.name[:-3])
                task_class = getattr(task_module, entry.name[:-3])
                task_obj = task_class()
                task_obj.run(womail)


# 云函数通知服务
class sendNotice:   
    def getsendNotify(self):
        url_list = [
            'https://mirror.ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py',
            'https://cdn.jsdelivr.net/gh/wuye999/myScripts@main/sendNotify.py',
            'https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py',
        ]
        for e,url in enumerate(url_list):
            try:
                response = requests.get(url,timeout=10)
                with open(scf_path('sendNotify.py'), "w+", encoding="utf-8") as f:
                    f.write(response.text)
                return
            except:
                if e >= (len(url_list)-1):
                    print('获取通知服务失败，请检查网络连接...')
    def main(self,f=0):
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

        content = ''
        with open(scf_path('log.txt'), encoding='utf-8') as f:
            for line in f.readlines():
                content += line
        send('unicom_task',content)


#腾讯云函数入口
def main_handler(event, context):
    users,womails = readJson()
    for user in users:
        # 清空上一个用户的日志记录
        with open(log_path('log.txt'),mode='w',encoding='utf-8') as f:
            pass
        global client
        logging.info('--------------账号分割线---------------')
        client = login.login(user['username'],user['password'],user['appId'])
        #获取账户信息
        util.getIntegral(client)
        if client != False:
            runTask(client, user)
        if run_send=='yes':
            sendNotice().main()

    global womail
    for e,womail in enumerate(womails):
        # 清空上一个用户的日志记录
        with open(log_path('log.txt'),mode='w',encoding='utf-8') as f:
            pass 
        if womail["woEmail"]:
            logging.info('--------------账号分割线---------------')
            runTas_2(womail)
        if run_send=='yes':
            sendNotice().main()

        

#主函数入口
if __name__ == '__main__':
    main_handler("","")
