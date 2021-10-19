import os
import requests
import sys
requests.packages.urllib3.disable_warnings()

# 读取环境变量
def get_env(env):
    if env in os.environ:
        a=os.environ[env]
        print(f'环境变量 {env} 不存在\n')    
    return a

# 随机ua
def get_script():
    script_add=get_env('script_add')
    print(script_add)
    # sys.path.append(os.path.abspath('.'))
    # global ua
    # for n in range(3):
    #     try:
    #         from jdUA import jdUA as ua
    #         break
    #     except:
    #         url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/jd/jdUA.py'
    #         response = requests.get(url)
    #         with open('jdUA.py', "w+", encoding="utf-8") as f:
    #             f.write(response.text)

#腾讯云函数入口
def main_handler(event, context):
    get_script()


#主函数入口
if __name__ == '__main__':
    main_handler("","")


