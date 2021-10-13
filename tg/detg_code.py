# 脚本为tg 定时发送消息，第一次请在命令行运行 python3 /目录/xxxxxx.py 登陆tg获取密钥,验证码在tg内查看

# 优先使用环境变量
tg_api_id = '12345'    # 申请的TG API ID
tg_api_hash = '0123456789abcdef0123456789abcdef'    # 申请的TG API hash
# export tg_api_id="12345"    
# export tg_api_hash="0123456789abcdef0123456789abcdef"  


import os
import functools
import time
import re
try:
    from telethon import TelegramClient, events, sync
except:
    print("\n缺少telethon 模块，请执行命令安装：pip3 install telethon")
    exit(3)


# 读取api
def get_tg_api():
    if 'tg_api_id' in os.environ:
        a=int(os.environ['tg_api_id'])
        b=os.environ['tg_api_hash']
    elif os.path.exists('/jd/log/jcode'):
        a=int(codes.set_var(['tg_api_id'],[r'export tg_api_id.*?="(.*?)"'],['/jd/config/config.sh'],1))
        b=codes.set_var(['tg_api_hash'],[r'export tg_api_hash.*?="(.*?)"'],['/jd/config/config.sh'],1)
    else:
        a=int(tg_api_id)
        b=tg_api_hash
    return a,b


## 判断运行环境
class Judge_env(object):
    ## 判断文件位置
    def getcodefile(self):
        if os.path.abspath('.')=='/ql/scripts':
            print("当前环境青龙\n")
            if os.path.exists('/ql/log/.ShareCode'):
                return '/ql/log/.ShareCode'
            else:
                return '/ql/log/code'
        elif os.path.exists('/jd/log/jcode'):
            print("当前环境V4\n")
            return '/jd/log/jcode'
        else:
            print('自行配置path,cookie\n')

    ## 批量提取pin,输出ckkk,path,pin_list
    def main_run(self):
        path=self.getcodefile()
        if path != '/jd/log/jcode':
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        else:
            cookie_list=self.v4_cookie()      # 获取cookie_list的合集
        pin_list=[re.match(r'.+pin=(.+)\;', cookie).group(1) for cookie in cookie_list]  # 提取cookie中的pin
        ckkk=len(cookie_list)      
        return path,pin_list,ckkk

    def v4_cookie(self):
        a=[]
        re_match=re.compile(r'Cookie'+'.*?=\"(.*?)\"')
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    b=re_match.match(line).group(1)
                    a.append(b)
                except:
                    pass
        return a


# 生成path_list合集
class Import_files(object):
    def __init__(self,path):
        self.path=path
    
    def path_list(self):
        name_list=['Health', 'MoneyTree', 'JdFactory', 'DreamFactory', 'Cfd', 'Carni', 'TokenJxnc', 'Jxnc', 'Joy', 'City', 'Bean', 'Cash', 'Pet', 'BookShop', 'Jdzz', 'Sgmh', 'Fruit']
        match_list=[r'.*?'+name+r'.*?\'(.*?)\'' for name in name_list]
        if self.path=='/ql/log/.ShareCode':   
            path_list=[self.path+'/'+name+'.log' for name in name_list]
        else:
            path_list = [self.path+'/'+x for x in os.listdir(self.path) if os.path.isfile(self.path+'/'+x)]
            path_list = sorted(path_list, reverse=True)
            path_list = [path_list[0]]*len(name_list)
        return name_list,match_list,path_list


# 自定义正则匹配类
class Look_log_code(object):
    def __init__(self, name_list=0, match_list=0, path_list=0, stop_n=0):
        self.name_list=name_list 
        self.match_list=match_list      
        self.path_list = path_list
        self.stop_n=stop_n
        self.codes={}

    def set_var(self, name_list, match_list, path_list, stop_n):
        self.name_list=name_list 
        self.match_list=match_list      
        self.path_list = path_list
        self.stop_n=stop_n
        self.main_run()
        if len(name_list)==1:
            return self.codes[name_list[0]][0]

    ## 需要导入的文件组合成list
    def file_list(self):
        if os.path.isdir(self.path):
            files = [self.path+'/'+x for x in os.listdir(self.path) if os.path.isfile(self.path+'/'+x)]
            files = sorted(files, reverse=True)
            files = files[0]
        elif os.path.isfile(self.path):
            files=self.path
        else:
            print(f'文件夹或日志 {self.path} 不存在\n')
            files=False
        return files

    ## 将list里的文件全部读取
    def main_run(self):
        for e,self.path in enumerate(self.path_list):
            files = self.file_list()
            if files:
                self.read_code(files,self.match_list[e],self.name_list[e])
            else:
               self.codes[self.name_list[e]]=' '

    # 根据self.match_list中的关键字读取文件中的助力码
    def read_code(self,files,match,name):
        a=[]
        n=0
        re_match=re.compile(match)
        with open(files, 'r') as f:
            for line in f.readlines():
                try: 
                    b=re_match.match(line).group(1)
                    a.append(b)
                    n+=1
                except:
                    pass
                if n==self.stop_n:
                    break
        self.codes[name]=a


# 合成需要发送的消息
class Composite_urls(object):
    def __init__(self, data_pack):
        self.data_pack=data_pack
        self.name_value_dict,self.biaozhi = data_pack(0)
        self.import_prefix=codes.codes
    
    ## 根据助力码和self.value通过data_pack组合出url_list,输出结果
    def main_run(self):
        a=[]
        for name,value in self.name_value_dict.items():
            data_pack2=functools.partial(self.data_pack, value=value)
            decode_list=self.import_prefix[name]
            codes_filter=[decode+'&' for decode in decode_list if len(decode)>5]
            if len(codes_filter)>5:
                codes_filter=codes_filter[:5]
            tg_codes=''.join(codes_filter)
            tg_codes=tg_codes[:-1]
            if len(tg_codes)==0:
                print(f'找不到 {name} 助力码\n')
            else:
                tg_information=data_pack2(tg_codes)
                a.append(tg_information)
        return a


# 发送消息
def send_mess(tg_send_messages_list):
    with TelegramClient(anon, tg_api_id, tg_api_hash) as client:
        client.start()
        for username_information in tg_send_messages_list:
            a=username_information.split('<<<')
            print(f'{a[0]}: {a[1]}')
            try:
                client.send_message(a[0],a[1])
                print('ok\n')
            except ValueError as e:
                print(e)
                print(f'找不到用户名 {a[0]} 或群组 {a[0]} \n')


# 回调函数1
def JD_ShareCode_Bot(tg_codes,*,value=0):
    biaozhi='@JD_ShareCode_Bot'
    name_value_dict={'Fruit':'/farm','Bean':'/bean','Pet':'/pet','DreamFactory':'/jxfactory','JdFactory':'/ddfactory','Sgmh':'/sgmh','Health':'/health','jxmc':'/jxmc'}
    tg_information=f'{biaozhi}<<<{value} {tg_codes}'
    if value==0:
        return name_value_dict,biaozhi
    else:
        return tg_information

def passerbybbot(tg_codes,*,value=0):
    biaozhi='@passerbybbot'
    name_value_dict={'Fruit':'/jd_fruit','DreamFactory':'/jx_factory'}
    tg_information=f'{biaozhi}<<<{value} {tg_codes}'
    if value==0:
        return name_value_dict,biaozhi
    else:
        return tg_information

def LvanLamCommitCodeBot(tg_codes,*,value=0):
    biaozhi='@LvanLamCommitCodeBot'
    name_value_dict={'Cash':'/jdcash','Joy':'/jdcrazyjoy','Jdzz':'/jdzz'}
    tg_information=f'{biaozhi}<<<{value} {tg_codes}'
    if value==0:
        return name_value_dict,biaozhi
    else:
        return tg_information


# 主函数
def main_run(data_pack):
    tg_send_messages_list=Composite_urls(data_pack).main_run()
    send_mess(tg_send_messages_list)

# 提示
def tip():
    if os.path.abspath('.')=='/ql/scripts':
        print("当前环境青龙\n")
        print('第一次请在命令行运行 cd /ql/scripts && python3 xxxxxx.py 登陆tg获取密钥\n')
        anon='anon'
    elif os.path.exists('/jd/log/jcode'):
        print("当前环境V4\n")
        print('第一次请在命令行运行 cd /jd/scripts && python3 xxxxxx.py 登陆tg获取密钥\n')
        anon='/jd/scripts/anon'
    else:
        print('运行目录下 python3 /运行目录/xxxxxx.py 登陆tg获取密钥\n')
        anon='anon'
    return anon


if __name__=='__main__':
    anon=tip()
    codes=Look_log_code()
    tg_api_id,tg_api_hash=get_tg_api()
    try:
        with TelegramClient(anon, tg_api_id, tg_api_hash) as client:
            client.start()    
    except:
        print('网络环境出错, 或tg_api出错，或验证出错')
    path,pin_list,ckkk=Judge_env().main_run()
    name_list,match_list,path_list=Import_files(path).path_list()
    codes.set_var(name_list,match_list,path_list,ckkk)
    name_list=['mohe', 'jxmc']
    match_list=[r'.*?5G超级盲盒好友互助码\】(.*?)\n',r'.*?互助码\：(.*?)\n']
    path_list=['/ql/log/shufflewzc_faker2_jd_mohe', '/ql/log/shufflewzc_faker2_jd_jxmc']
    codes.set_var(name_list,match_list,path_list,ckkk)
    main_run(JD_ShareCode_Bot)    # 向@JD_ShareCode_Bot发送消息
    main_run(passerbybbot)    # 向@passerbybbot发送消息
    main_run(LvanLamCommitCodeBot)    # 向@LvanLamCommitCodeBot发送消息
    print('\nwuye9999')








