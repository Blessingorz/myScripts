# 在tg bot提交助力码后，要使用作者的脚本才能激活
# 运行本脚本后即可激活已提交的助力码，无需运行作者的脚本
# 暂支持 he1pu, helloworld ，PasserbyBot, ddo 

import sys
import os
import functools
import time
import re
import hashlib
from  multiprocessing import Pool
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装: pip3 install requests")
    exit(3)

## 判断运行环境
class Judge_env(object):
    ## 判断文件位置
    def getcodefile(self):
        if '/ql' in os.path.abspath(os.path.dirname(__file__)):
            print("当前环境青龙\n")
            sys.path.append('/ql/scripts')
            if os.path.exists('/ql/log/.ShareCode'):
                return '/ql/log/.ShareCode'
            else:
                return '/ql/log/code'
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            print("当前环境V4\n")
            sys.path.append('/jd/scripts')
            return '/jd/log/jcode'
        else:
            print('自行配置path,cookie\n')

    ## 批量提取pin,输出ckkk,path,pin_list
    def main_run(self):
        path=self.getcodefile()
        if path != '/jd/log/jcode':
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        else:
            cookie_list=Get_env().get_env_nofixed('Cookie')     # 获取cookie_list的合集
        pin_list=[re.findall(r'pt_key=(.+);pt_pin=(.+);', cookie)[0][1] for cookie in cookie_list]  # 提取cookie中的pin
        ckkk=len(cookie_list)      
        return path,cookie_list,pin_list,ckkk


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


# 自定义正则匹配模块
class Match_cus(object):
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
            return self.codes[name_list[0]]

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
               self.codes[self.name_list[e]]=''

    # 根据self.match_list中的关键字读取文件中的助力码
    def read_code(self,files,match,name):
        a=[]
        n=0
        re_match=re.compile(match, re.I)
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


# 青龙，v4，本地，第三方等环境变量获取
class Get_env(object):
    # 需要导入自定义正则模块
    def __init__(self,class_match='Match_cus'):
        if isinstance(class_match,str):
            self.search=eval(f'{class_match}()')
        else:
            self.search=class_match()
        self.env={}

    # 读取固定环境变量,返回的是字符串
    def get_env(self,env):
        try:
            if env in os.environ:
                a=os.environ[env]
            elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
                a=self.search.set_var([env],[r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']'],['/jd/config/config.sh'],1)[0]
            else:
                a=eval(env)
        except:
            print(f'不存在环境变量 {env} \n')
            return
        if len(a)<1:
            print(f'环境变量 {env} 为空\n')
            return
        self.env[env]=a
        return a

    # 读取不固定环境变量,返回的是list
    def get_env_nofixed(self,env):
        a=[]
        for n in range(1,999):
            try:
                if f'{env}_1' in os.environ:
                    b=os.environ[f'{env}_{n}']
                elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
                    b=self.search.set_var([f'{env}_{n}'],[r'(?:export )?'+f'{env}_?{n}'+r' ?= ?[\"\'](.*?)[\"\']'],['/jd/config/config.sh'],1)
                else:
                    b=eval(f'{env}_{n}')
                a.append(b)
            except:
                break
        a=[i for i in a if len(i)>1]
        if len(a)<1:
            print(f'环境变量 {env} 不存在或为空\n')
            return    
        self.env[env]=a
        return a

# 合成url
class Composite_urls(object):
    def __init__(self, data_pack):
        self.data_pack=data_pack
        self.name_value_dict,self.biaozhi = data_pack(0)
        self.import_prefix=codes.codes
    
    ## 根据助力码和self.value通过data_pack组合出url_list,输出结果
    def main_run(self):
        url_list=[]
        for name,value in self.name_value_dict.items():
            data_pack2=functools.partial(self.data_pack, value=value)
            decode_list=self.import_prefix[name]
            for e,decode in enumerate(decode_list):
                if decode == '' or decode == ' ':
                    print(f'{self.biaozhi}_{value}: {name}{str(e+1)} 为空\n')
                    continue
                url=data_pack2(decode)
                url_list.append(url)
        return url_list,self.biaozhi

# He1pu_cfd的url合集
class He1pu_pin_urls(Composite_urls):
    ## 根据助力码和self.value通过data_pack组合出url_list,输出结果
    def main_run(self):
        url_list=[]
        for name,value in self.name_value_dict.items():
            data_pack2=functools.partial(self.data_pack, value=value)
            decode_list=self.import_prefix[name]
            for e,decode in enumerate(decode_list):
                try:
                    pin=pin_list[e]
                except:
                    print(f'{self.biaozhi}_{value}: {name}{str(e+1)} 对应的pin不存在\n')
                    continue
                if decode == '' or decode == ' ':
                    print(f'{self.biaozhi}_{value}: {name}{str(e+1)} 为空\n')
                    continue
                url=data_pack2(decode,pin=pin)
                url_list.append(url)
                # sys.stdout.flush()
        return url_list,self.biaozhi


# Helloworld_cfd的url合集
class Helloworld_x_urls(Composite_urls):
    ## 根据助力码和self.value通过data_pack组合出url_list,输出结果
    def main_run(self):
        url_list=[]
        for name,value in self.name_value_dict.items():
            data_pack2=functools.partial(self.data_pack, value=value)
            decode_list=self.import_prefix[name]
            farm_code_list=self.import_prefix['Fruit']
            bean_code_list=self.import_prefix['Bean']
            for e,decode in enumerate(decode_list):
                try:
                    pin=pin_list[e]
                    farm_code=farm_code_list[e]
                    bean_code=bean_code_list[e]
                except:
                    print(f'{self.biaozhi}_{value}: {name}{str(e+1)} 对应的数据不存在\n')
                    continue
                if decode == '' or decode == ' ':
                    print(f'{self.biaozhi}_{value}: {name}{str(e+1)} 为空\n')
                    continue
                url=data_pack2(decode,pin=pin,farm_code=farm_code, bean_code=bean_code)
                url_list.append(url)
                # sys.stdout.flush()
        return url_list,self.biaozhi

## 将url_list进行批量请求，判断结果
class Bulk_request(object):
    def __init__(self, url_list, biaozhi):
        self.url_list = url_list
        self.biaozhi = biaozhi
        self.g=0
        self.log=[]
    
    ##批量请求流程
    def main_run(self):
        for url in self.url_list:
            self.g = 0
            self.log=[]
            self.request_process(url)
            a=''
            for i in self.log:
                a=a+'\n'+i
            print(a)

    ## 单个url请求，判断结果，是否重试的流程
    def request_process(self,url):  
        code,self.value,pin=self.regular_extract(url)
        if self.g == 0:
            self.log.append(f'{self.biaozhi}_{self.value}: 开始上报 {code} {pin}')
        res=self.single_request(url)
        state=self.processing_request_result(res)
        self.judge_Retry(state,url) 
        # sys.stdout.flush()

    # 正则提取信息
    def regular_extract(self,url):
        if self.biaozhi=='he1pu' or self.biaozhi=='helloworld':
            a=re.match(r'.*?=(.*?)&.*?=(.*)',url)
            code=a.group(1)
            value=a.group(2)
            pin=''
        elif self.biaozhi=='passerbyBot':
            a=re.match(r'.*?activeJd(.*?)\?.*?=(.*)',url)
            code=a.group(2)
            value=a.group(1)
            pin='' 
        elif 'he1pu_pin' in self.biaozhi:
            a=re.match(r'.*?=(.*?)&.*?=(.*?)&(.*)',url)
            code=a.group(1)
            value=a.group(2)
            pin=a.group(3)    
        elif 'helloworld_pin' in self.biaozhi:
            a=re.match(r'.*?autoInsert/(.*)\?.*?=(.*?)&.*?=(.*)',url)
            code=a.group(2)
            value=a.group(1)
            pin=a.group(3) 
        elif 'helloworld_x' in self.biaozhi:
            
            a=re.match(r'.*?autoInsert/(.*?)\?.*?=(.*?)&.*?=(.*?)&.*?=(.*?)&(.*)',url)
            code=a.group(2) 
            value=a.group(1) 
            pin=a.group(5)
        elif 'ddo' in self.biaozhi:
            a=re.match(r'.*?upload/(.*?)\?.*?=(.*?)&(.*)',url)
            code=a.group(2) 
            value=a.group(1) 
            pin=a.group(3)
        return code,value,pin

    # 单个url进行请求得出结果
    def single_request(self,url):
        time.sleep(0.5)
        try:
            if requisition=='get':
                res = requests.get(url, timeout=2)
            else:
                res = requests.post(url, timeout=2)
            return res.text
        except:
            res='Sever ERROR'
            return res

    # 判断请求结果
    def processing_request_result(self,res):
        state=0
        biaozhi=self.biaozhi.split('_')[0]
        if 'Sever ERROR' in res:
            self.log.append(f'{self.biaozhi}_{self.value}: 连接超时🌚')
            state=1
            return state
        if biaozhi == 'he1pu':
            if 'Type ERROR' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 提交类型无效')
                state=1
            elif '\"code\":300' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 重复提交\n')
            elif '\"code\":200' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 提交成功✅\n')
            else:
                self.log.append(f'{self.biaozhi}_{self.value}: 服务器连接错误')
                state=1
        elif biaozhi=='helloworld':
            if '1' in res or '200' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 激活成功✅\n')
            elif '0' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 请在tg机器人处提交助力码后再激活\n')
            else:
                self.log.append(f'{self.biaozhi}_{self.value}: 服务器连接错误')
                state=1
        elif biaozhi=='passerbyBot':
            if 'Cannot' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 提交类型无效')
                state=1
            elif '激活成功' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 激活成功✅\n')
            elif '激活失败' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 请在tg机器人处提交助力码后再激活\n')
            else:
                self.log.append(f'{self.biaozhi}_{self.value}: 服务器连接错误')
                state=1
        elif biaozhi=='ddo':
            if 'OK' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 提交成功✅\n')
            elif 'error' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 助力码格式错误，乱玩API是要被打屁屁的')
                state=1
            elif 'full' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 车位已满，请等待下一班次\n')
            elif 'exist' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 助力码已经提交过了\n')
            elif 'not in whitelist' in res:
                self.log.append(f'{self.biaozhi}_{self.value}: 提交助力码失败，此用户不在白名单中\n')
            else:
                self.log.append(f'{self.biaozhi}_{self.value}: 未知错误')
                state=1
        else:
            self.log.append(res+'\n')
        return state  

    # 根据判断过的请求结果判断是否需要重新请求
    def judge_Retry(self,state,url):
        if state == 1:
            if self.g >= 3:
                self.log.append(f'{self.biaozhi}_{self.value}: 放弃挣扎')
                return
            self.g += 1
            self.log.append(f'{self.biaozhi}_{self.value}: 第{self.g}次重试中🌐...')
            time.sleep(0.5)
            return self.request_process(url)


def get_md5(s):
    return hashlib.md5(str(s).encode('utf-8')).hexdigest()

## he1pu数据
def he1pu(decode, *, value=0):
    name_value_dict={'Fruit':'farm','Bean':'bean','Pet':'pet','DreamFactory':'jxfactory','JdFactory':'ddfactory','Sgmh':'sgmh','Health':'health'}
    biaozhi = 'he1pu'
    global requisition
    requisition='get'
    r=f'http://www.helpu.cf/jdcodes/submit.php?code={decode}&type={value}'
    if decode==0:
        return name_value_dict, biaozhi
    else:
        return r  

## helloworld数据
def helloworld(decode, *, value=0):
    name_value_dict={'Fruit':'farm','Bean':'bean','Pet':'pet','DreamFactory':'jxfactory','JdFactory':'ddfactory','Sgmh':'sgmh','Health':'health'}
    biaozhi='helloworld'
    global requisition
    requisition='get'
    r=f'https://api.jdsharecode.xyz/api/runTimes?sharecode={decode}&activityId={value}'
    if decode==0:
        return name_value_dict, biaozhi
    else:
        return r        

## passerbyBot数据
def passerbyBot(decode, *, value=0):
    name_value_dict={'Fruit':'FruitCode','JdFactory':'FactoryCode', 'Cfd':'CfdCode'}
    biaozhi='passerbyBot'
    global requisition
    requisition='get'
    r=f'http://51.15.187.136:8080/activeJd{value}?code={decode}'
    if decode==0:
        return name_value_dict, biaozhi
    else:
        return r 

## he1pu_pin数据
def he1pu_pin(decode, *, pin=0, value=0):
    name_value_dict={'Cfd':'jxcfd','5G超级盲盒':'mohe','京喜财富岛合珍珠':'jxcfdm','88红包':'jxlhb'}
    biaozhi = 'he1pu_pin'
    global requisition
    requisition='get'
    r=f'http://www.helpu.cf/jdcodes/submit.php?code={decode}&type={value}&user={pin}'
    if value==0:
        return name_value_dict, biaozhi
    else:
        return r

## helloworld_pin数据
def helloworld_pin(decode, *, pin=0, value=0):
    name_value_dict={'全民开红包':'redPacket'}
    biaozhi = 'helloworld_pin'
    global requisition
    requisition='get'
    pin=get_md5(pin)
    r=f'https://api.jdsharecode.xyz/api/autoInsert/{value}?sharecode={decode}&pin={pin}'
    if value==0:
        return name_value_dict, biaozhi
    else:
        return r

## helloworld_x数据
def helloworld_x(decode, *, pin=0, farm_code=0, bean_code=0, value=0):
    name_value_dict={'Cfd':'jxcfd','京喜牧场':'jxmc','京喜牧场红包码':'jxmchb','88红包':'hb88'}
    biaozhi='helloworld_x'
    global requisition
    requisition='get'
    pin=get_md5(pin)
    r=f'https://api.jdsharecode.xyz/api/autoInsert/{value}?sharecode={decode}&bean={bean_code}&farm={farm_code}&pin={pin}'
    if value==0:
        return name_value_dict, biaozhi
    else:
        return r

def ddo(decode, *, pin=0, value=0):
    name_value_dict={'Cfd':'cfd'}
    biaozhi='ddo'
    global requisition
    requisition='post'
    r=f'http://transfer.nz.lu/upload/{value}?code={decode}&ptpin={pin}'
    if value==0:
        return name_value_dict, biaozhi
    else:
        return r    


def main_run(data_pack):
    url_list,biaozhi=Composite_urls(data_pack).main_run()
    Bulk_request(url_list, biaozhi).main_run()

## helloworld master函数
def helloworld_x_main_run(data_pack):
    url_list,biaozhi=Helloworld_x_urls(data_pack).main_run()
    Bulk_request(url_list, biaozhi).main_run()

## he1pu master函数
def he1pu_pin_main_run(data_pack):
    url_list,biaozhi=He1pu_pin_urls(data_pack).main_run()
    Bulk_request(url_list, biaozhi).main_run()

if __name__=='__main__':
    path,cookie_list,pin_list,ckkk=Judge_env().main_run()
    name_list,match_list,path_list=Import_files(path).path_list()
    codes=Match_cus()
    codes.set_var(name_list,match_list,path_list,ckkk)
    name_list=[
        '5G超级盲盒',
        '京喜牧场',
        '京喜牧场红包码',
        '88红包',
        '全民开红包'    
    ]
    match_list=[
        r'.*?5G超级盲盒好友互助码\】(.*)',
        r'.*?互助码\：(.*)',
        r'红包邀请码:(.*)',
        r'获取助力码成功：(.*)',
        r'当前待拆红包ID:(.*?)，进度.*'
    ]
    path_list=[
        '/ql/log/shufflewzc_faker2_jd_mohe',
        '/ql/log/shufflewzc_faker2_jd_jxmc',
        '/ql/log/shufflewzc_faker2_jd_jxmc',
        '/ql/log/shufflewzc_faker2_jd_jxlhb',
        '/ql/log/shufflewzc_faker2_jd_redPacket'
    ]
    codes.set_var(name_list,match_list,path_list,ckkk)
    codes.codes['京喜财富岛合珍珠']=codes.codes['Cfd']
    pool = Pool(3)
    pool.apply_async(func=he1pu_pin_main_run,args=(ddo,))   ## 创建ddo提交任务
    pool.apply_async(func=main_run,args=(passerbyBot,))   ## 创建passerbyBot激活任务
    pool.apply_async(func=main_run,args=(he1pu,))   ## 创建he1pu提交任务
    pool.apply_async(func=main_run,args=(helloworld,))  ## 创建helloworld激活任务
    pool.apply_async(func=he1pu_pin_main_run,args=(he1pu_pin,))  ## 创建he1pu_pin活任务
    pool.apply_async(func=he1pu_pin_main_run,args=(helloworld_pin,))  ## 创建helloworld_pin激活任务
    pool.apply_async(func=helloworld_x_main_run,args=(helloworld_x,))  ## 创建helloworld_x激活任务
    pool.close()
    pool.join()

    # 测试   
    # main_run(passerbyBot)
    # main_run(he1pu)
    # main_run(helloworld)
    # he1pu_pin_main_run(ddo)
    # he1pu_pin_main_run(he1pu_pin)
    # he1pu_pin_main_run(helloworld_pin)
    # helloworld_x_main_run(helloworld_x)
    # 测试
    # print(codes.codes)
    # print(name_list,'\n',match_list,'\n',path_list)
    # print(law_code.codes)
    # print(log_code.codes)
    # print(codes_dict)

    print('wuye9999')


