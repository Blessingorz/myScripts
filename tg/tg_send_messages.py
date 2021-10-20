# 脚本为tg 定时发送消息，第一次请在命令行运行 cd /ql/scripts && python3 tg_send_messages.py 登陆tg获取密钥,验证码在tg内查看

# 脚本内填写 
# 向群't.me/iKuuuu_VPN' 发送 '长大了就不要笑得那么开心', 向机器人'@JD_ShareCode_Bot' 发送 '/help'。
tg_api_id = '12345'
tg_api_hash = '0123456789abcdef0123456789abcdef'
tg_send_messages_1='@iKuuuu_VPN<<<早'
tg_send_messages_2='@JD_ShareCode_Bot<<</help' 
# tg_send_messages_n='@某用户<<<需要发送的消息'       #按自然数顺序填写，最多999条

# 环境变量填写 ,会优先读取环境变量。
# export tg_api_id="12345"    
# export tg_api_hash="0123456789abcdef0123456789abcdef"  
# export tg_send_messages_1="@iKuuuu_VPN<<<长大了就不要笑得那么开心"
# export tg_send_messages_2="@JD_ShareCode_Bot<<</help"
# export tg_send_messages_n="@某用户<<<需要发送的消息"    #按自然数顺序填写，最多999条

import os
import re
try:
    from telethon import TelegramClient, events, sync
except:
    print("\n缺少telethon 模块，请执行命令安装：pip3 install telethon")
    exit(3)


# 读取环境变量
def get_env(env):
    try:
        if env in os.environ:
            a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            a=v4_env(env,'/ql/config/config.sh')
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            a=v4_env(env,'/jd/config/config.sh')
        else:
            a=eval(env)
    except:
        print(f'环境变量 {env} 不存在\n')    
    return a

# 读取不固定环境变量,返回的是list
def get_env_nofixed(env):
    a=[]
    for n in range(1,999):
        try:
            if f'{env}_1' in os.environ:
                b=os.environ[f'{env}_{n}']
            elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
                a=v4_env(f'{env}_{n}','/ql/config/config.sh')
            elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
                b=v4_env(f'{env}_{n}','/jd/config/config.sh')
            else:
                b=eval(f'{env}_{n}')
            a.append(b)
        except:
            break
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

# 发送消息
def send_mess(tg_send_messages):
    with TelegramClient(anon, tg_api_id, tg_api_hash) as client:
        client.start()
        for username_information in tg_send_messages:
            a=username_information.split('<<<')
            print(f'{a[0]}: {a[1]}')
            try:
                client.send_message(a[0],a[1])
                print('ok\n')
            except ValueError as e:
                print(e)
                print(f'找不到用户名 {a[0]} 或群组 {a[0]} \n')

# 提示
def tip():
    if '/ql' in os.path.abspath(os.path.dirname(__file__)):
        print("当前环境青龙\n")
        print('第一次请在命令行运行 cd /ql/scripts && python3 xxxxxx.py 登陆tg获取密钥\n')
        anon='anon'
    elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
        print("当前环境V4\n")
        print('第一次请在命令行运行 cd /jd/scripts && python3 xxxxxx.py 登陆tg获取密钥\n')
        anon='/jd/scripts/anon'
    else:
        print('运行目录下 python3 /运行目录/xxxxxx.py 登陆tg获取密钥\n')
        anon='anon'
    return anon


if __name__=='__main__':
    tg_api_id=get_env('tg_api_id')
    tg_api_hash=get_env('tg_api_hash')
    tg_send_messages=get_env_nofixed('tg_send_messages')  
    anon=tip()
    try:
        with TelegramClient(anon, tg_api_id, tg_api_hash) as client:
            client.start()    
    except:
        print('网络环境出错, 或tg_api出错，或验证出错')
    send_mess(tg_send_messages)
    print('\nwuye9999')
