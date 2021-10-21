# 脚本为tg 定时发送消息，第一次请在命令行运行 cd /ql/scripts && python3 xxx 登陆tg获取密钥,验证码在tg内查看

# 脚本内填写 ,例：
# 向群't.me/iKuuuu_VPN' 发送 '长大了就不要笑得那么开心', 向机器人'@JD_ShareCode_Bot' 发送 '/help'。
tg_api_id="123456789"
tg_api_hash="12345678996f5e170474abcd4fe"
tg_send_messages_1="@JDhlep_Bot<<</help"
tg_send_messages_2="@xiaoyu002_bot<<</help"
# 更多变量请查看：https://github.com/wuye999/myScripts/blob/main/tg/README.md

# 环境变量填写 ,会优先读取环境变量。
# export tg_api_id="12345"
# export tg_api_hash="0123456789abcdef0123456789abcdef"
# export tg_send_messages_1="@iKuuuu_VPN<<<长大了就不要笑得那么开心"
# export tg_send_messages_2="@JD_ShareCode_Bot<<</help"
# export tg_send_messages_n="@某用户<<<需要发送的消息"   #按自然数顺序填写，最多999条

import os,sys
import re
import asyncio
import time
from multiprocessing import Pool
try:
    from telethon.sync import TelegramClient, events
except:
    print("\n缺少telethon 模块，请执行命令安装：pip3 install telethon")
    exit(3)


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

# 读取不固定环境变量,返回的是list
def get_env_nofixed(env):
    a=[]
    for n in range(1,999):
        b=get_env(f'{env}_{n}')
        if b:
            a.append(b)
        else:
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


async def myme():
    me = await app.get_me()
    print(f'登录成功，欢迎 \n ')


# 发送消息
async def send_message():
    async def __send_message(a):
        try:
            await app.send_message(a[0],a[1])
            print(f'{a[0]}  {a[1]}')
            print('ok\n')
        except ValueError as e:
            print(f'{a[0]}  {a[1]}')
            print(e)
            print(f'找不到用户名 {a[0]} 或群组 {a[0]} \n')
    tasks=[]
    for username_information in tg_send_messages:
        a=username_information.split('<<<')
        tasks.append(__send_message(a))
    await asyncio.wait(tasks)


# 发送文件
async def send_file():
    async def __send_file(a):
        if len(a)==2:
            a.append('') 
        try:
            await app.send_file(a[0], a[1], caption=a[2])
            print(f'{a[0]}  文件备注：{a[2]}')
            print('ok\n')
        except ValueError as e:
            print(f'{a[0]}  文件备注：{a[2]}')
            print(e)
            print(f'找不到用户名 {a[0]} 或群组 {a[0]} \n')
    tasks=[]
    for username_information in tg_send_file:
        a=username_information.split('<<<')
        tasks.append(__send_file(a))
    await asyncio.wait(tasks)


# 发送语音消息
async def send_voice():
    async def __send_voice(a):
        try:
            await app.send_file(a[0], a[1], voice_note=True)
            print(f'{a[0]}  语音消息')
            print('ok\n')
        except ValueError as e:
            print(f'{a[0]}  语音消息')
            print(e)
            print(f'找不到用户名 {a[0]} 或群组 {a[0]} \n')
    tasks=[]
    for username_information in tg_send_voice:
        a=username_information.split('<<<')
        tasks.append(__send_voice(a))
    await asyncio.wait(tasks)


# 下载文件
async def download_media():
    async def __download_media(a):
        try:
            async for message in app.iter_messages(a[0],limit=10):
                path = await message.download_media()
                if path:
                    break
            await message.download_media(a[1])
            print(f'{a[0]}  下载文件{path}到{a[1]}')
            print('ok\n')
        except ValueError as e:
            print(f'{a[0]}  下载文件{path}到{a[1]}')
            print(e)
            print(f'找不到用户名 {a[0]} 或群组 {a[0]} \n')
    tasks=[]
    for username_information in tg_download_media:
        a=username_information.split('<<<')
        tasks.append(__download_media(a))
    await asyncio.wait(tasks)


# 监控特定用户或频道消息，一旦出现新文件就下载
async def download_monitor( event: events.NewMessage.Event):
    message = event.message
    a=tg_download_media[0].split('<<<')
    path = message.download_media()
    if path:
        print(f'{a[0]}  下载文件{path}到{a[1]}')
        try:
            await message.download_media(a[1])
            print('ok\n')
        except:
            print(f'下载失败\n')
    if tg_stop:
        if int(time.time()-start)>int(tg_stop)*60:
            app.run_until_disconnected()
            time.sleep(2)
            print('断开连接\n')
            exit()
    sys.stdout.flush()


# 监控特定用户或频道消息，一旦出现消息就转发
async def forward_messages( event: events.NewMessage.Event):
    message = event.message
    a=tg_forward_messages[0].split('<<<')
    if a[2] in message.text:
        b=await app.forward_messages(a[0], message)
        print(f"转发成功,消息为 {message.text}")
    if tg_stop:
        if int(time.time()-start)>int(tg_stop)*60:
            app.run_until_disconnected()
            time.sleep(2)
            print('断开连接\n')
            exit()
    sys.stdout.flush()

# 代理
def app_proxy():
    # socks5 或者 http 或者 MTProxy
    anon=tip()
    tg_api_id=get_env('tg_api_id')
    tg_api_hash=get_env('tg_api_hash')
    tg_proxy_type=get_env('tg_proxy_type')
    tg_proxy_add=get_env('tg_proxy_add')
    tg_proxy_port=get_env('tg_proxy_port')
    tg_proxy_auth=get_env('tg_proxy_auth')
    if len(tg_proxy_auth)>3:
        tg_proxy=True
        a=tg_proxy_auth.split('<<<')
    else:
        tg_proxy=False
    if tg_proxy_type:
        global socks
        try:
            import socks
        except:
            print("\n缺少socks 模块，请执行命令安装：pip3 install PySocks \n请执行命令安装：pip3 install socks")
        if 'socks4' in tg_proxy_type:
            print('启用socks4代理\n')
            if tg_proxy:
                app=TelegramClient(
                    anon,tg_api_id,tg_api_hash,
                    proxy=(socks.SOCKS4, tg_proxy_add, int(tg_proxy_port), True, a[0], a[1])
                    )
            else:
                app=TelegramClient(
                    anon,tg_api_id,tg_api_hash,
                    proxy=(socks.SOCKS4, tg_proxy_add, int(tg_proxy_port))
                    )
        elif 'socks5' in tg_proxy_type:
            print('启用socks5代理\n')
            if tg_proxy:
                app=TelegramClient(
                    anon,tg_api_id,tg_api_hash,
                    proxy=(socks.SOCKS5, tg_proxy_add, int(tg_proxy_port), True, a[0], a[1])
                    )
            else:
                app=TelegramClient(
                    anon,tg_api_id,tg_api_hash,
                    proxy=(socks.SOCKS5, tg_proxy_add, int(tg_proxy_port))
                    )
        elif 'http' in tg_proxy_type:
            print('启用http代理\n')
            if tg_proxy:
                app=TelegramClient(
                    anon,tg_api_id,tg_api_hash,
                    proxy=(socks.HTTP, tg_proxy_add, int(tg_proxy_port), True, a[0], a[1])
                    )
            else:
                app=TelegramClient(
                    anon,tg_api_id,tg_api_hash,
                    proxy=(socks.HTTP, tg_proxy_add, int(tg_proxy_port))
                    )
        else:
            print(f'不存在的代理方式{tg_proxy_type}\n')
            app=TelegramClient(anon, tg_api_id, tg_api_hash)
    else:
        app=TelegramClient(anon, tg_api_id, tg_api_hash)
    return app


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


def main():
    global tg_send_messages,tg_send_file,tg_send_voice,tg_download_media,tg_stop,tg_forward_messages,app
    tg_send_messages=get_env_nofixed('tg_send_messages')  
    tg_send_file=get_env_nofixed('tg_send_file')
    tg_send_voice=get_env_nofixed('tg_send_voice')
    tg_download_media=get_env_nofixed('tg_download_media')
    tg_forward_messages=get_env_nofixed('tg_forward_messages')
    tg_monitor=get_env('tg_monitor')
    tg_stop=get_env('tg_stop')
    app=app_proxy()
    try:
        with app:
            pass
    except:
        print('网络环境出错, 或tg_api出错，或验证出错')
    taskss=[]
    if (not tg_monitor) or tg_monitor=='no':
        taskss.append(myme())
        if len(tg_send_messages)>0:
            taskss.append(send_message())
        if len(tg_send_file)>0:
            taskss.append(send_file())
        if len(tg_send_voice)>0:
            taskss.append(send_voice())
        if len(tg_download_media)>0:
            taskss.append(download_media())
    if tg_monitor and tg_monitor=='yes':
        global start
        start = time.time()
        print('监控启动')
        if tg_download_media:
            with app:
                a=tg_download_media[0].split('<<<')
                print(f'正在监控 {a[0]}\n')
                sys.stdout.flush()
                app.add_event_handler(callback=download_monitor, event=events.NewMessage(chats=a[0]))
                app.run_until_disconnected()
        if tg_forward_messages:
            with app:
                a=tg_forward_messages[0].split('<<<')
                print(f'正在监控 {a[1]}\n')
                sys.stdout.flush()
                app.add_event_handler(callback=forward_messages, event=events.NewMessage(chats=a[1]))
                app.run_until_disconnected()  
    else:
        with app:
            app.loop.run_until_complete(asyncio.wait(taskss))
    print('\nwuye9999')


if __name__=='__main__':
    main()
