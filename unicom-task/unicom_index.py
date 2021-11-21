# -*- coding: utf-8 -*-

'''
cron: 16 6,16 * * * *
变量: unicom_config_x,unicom_woEmail_x,通知服务变量
脚本内或环境变量填写，环境变量优先
通知推送服务环境变量请查看：https://github.com/wuye999/myScripts/blob/main/send.md
环境变量示例：
export unicom_config_1="手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫<<<沃邮箱登陆Url1（可留空）<<<沃邮箱密码（可留空）"
export unicom_config_2="手机号2<<<服务密码2<<<appId2<<<抽奖次数(0-30)中奖几率渺茫<<<沃邮箱登陆Url2（可留空）<<<沃邮箱密码（可留空）"
export PUSH_PLUS_TOKEN="微信推送Plus+(通知服务示例，可留空或不填)"
'''
# 脚本内示例：
unicom_config_1="18825802580<<<888888<<<appppppp8888888888iiiddd<<<0<<<https://nyan.mail.wo.cn/cn/sign/index/index?mobile=aaa&userName=&openId=bbb<<<ccc"
unicom_config_2="19925902590<<<999999<<<appppppp9999999999iiiddd<<<5<<< <<< "
PUSH_PLUS_TOKEN=""


import os,sys
sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/task')
import json,time,re,traceback,random,datetime,util,sys,login,logging
try:
    from lxml.html import fromstring
    import pytz,importlib,requests,rsa
except Exception as e:
    print(str(e) + "\n缺少lxml,pytz,requests,rsa模块中的一个, 请执行命令：pip3 install xxx\n")
requests.packages.urllib3.disable_warnings()


run_send='yes'      # yes或no,是否启用推送
#用户登录全局变量
client = None


# 云函数可写目录
def scf_path(p):
    if __name__ == '__main__':
        return './'+p
    else:
        return '/tmp/'+p
   
#日志基础配置
def log():
    # 创建一个logger
    global logger,logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 创建一个handler，用于写入日志文件
    # w 模式会记住上次日志记录的位置
    fh = logging.FileHandler(scf_path('log.txt'), mode='a', encoding='utf-8')
    fh.setFormatter(logging.Formatter("%(filename)s: %(message)s"))
    logger.addHandler(fh)
    # 创建一个handler，输出到控制台
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(filename)s: %(message)s"))
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
        for unicom_config in unicom_config_list:
            user_list=[v for v in unicom_config.split('<<<')]
            user_dict={
                "username": user_list[0],
                "password": user_list[1],
                "appId": user_list[2],
            }
            if user_list[3] and user_list[3] != '0' and user_list[3] != ' ' :
                user_dict['lotteryNum']=user_list[3]
            if user_list[4] and user_list[4] != ' ' :
                user_dict['woEmail']=user_list[4]
            if user_list[5] and user_list[5] != ' ' :
                user_dict['woEmail_password']=user_list[5]                
            users.append(user_dict)
        return users
    except:
        logging.error('变量填写错误')

#运行任务
def runTask(client, user):
    with os.scandir(os.path.abspath(os.path.dirname(__file__))+'/task') as entries:
        for entry in entries:
            if entry.is_file():
                if entry.name == '__init__.py':
                    continue
                if entry.name == 'login.py':
                    continue
                if entry.name == 'sendNotify.py':
                    continue
                if entry.name == 'util.py':
                    continue 
                task_module = importlib.import_module('task.'+entry.name[:-3])
                task_class = getattr(task_module, entry.name[0:-3])
                task_obj = task_class()
                task_obj.run(client, user)

# 通知服务
class sendNotice:   
    def getsendNotify(self, a=1):
        try:
            url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py'
            response = requests.get(url,timeout=10)
            with open(scf_path('sendNotify.py'), "w+", encoding="utf-8") as f:
                f.write(response.text)
            return
        except:
            pass
        if a < 5:
            a += 1
            return self.getsendNotify(a)

    def main(self,f=1):
        for n in range(3):
            try:
                from sendNotify import send,msg,initialize
                break
            except:
                self.getsendNotify()
        l=['BARK','SCKEY','TG_BOT_TOKEN','TG_USER_ID','TG_API_HOST','TG_PROXY_HOST','TG_PROXY_PORT','DD_BOT_TOKEN','DD_BOT_SECRET','Q_SKEY','QQ_MODE','QYWX_AM','PUSH_PLUS_TOKEN','PUSH_PLUS_USER']
        d={}
        for a in l:
            try:
                d[a]=eval(a)
            except:
                d[a]=''
        try:
            initialize(d)
        except:
            self.getsendNotify()
            if f < 5:
                f += 1
                return self.main(f)
            else:
                print('获取通知服务失败，请检查网络连接...')

        content = ''
        with open(scf_path('log.txt'), encoding='utf-8') as f:
            for line in f.readlines():
                content += line
        send('unicom_task',content)


#腾讯云函数入口
def main_handler(event, context):
    users = readJson()
    for user in users:
        # 清空上一个用户的日志记录
        with open(scf_path('log.txt'),mode='w',encoding='utf-8') as f:
            pass
        global client
        client = login.login(user['username'],user['password'],user['appId'])
        #获取账户信息
        util.getIntegral(client)
        if client != False:
            runTask(client, user)
        if run_send=='yes':
            sendNotice().main()

#主函数入口
if __name__ == '__main__':
    main_handler("","")
