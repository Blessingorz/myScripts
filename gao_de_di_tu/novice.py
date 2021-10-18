# 小德果园
# 入口>高德地图
# 脚本功能为自动浇水，签到等功能，还在完善
# 环境变量wy_xdgy，抓包搜索'sns.amap.com',复制cookie,填入环境变量中，多账号用&分割
# export wy_xdgy="sessionid=xxxx;xxx=xxx;&第二个cookie&第三个cookie"
import time
import os
import re
import requests
import sys
requests.packages.urllib3.disable_warnings()


# 随机ua
def ua_random():
    ua='Android 11'
    return ua

# 10位时间戳
def gettimestamp():
    return str(int(time.time()))


## 获取cooie
class Judge_env(object):
    ## 判断运行环境
    def getcodefile(self):
        global sys
        if '/ql' in os.path.abspath(os.path.dirname(__file__)):
            print("当前环境青龙\n")
            sys.path.append(os.path.abspath(os.path.dirname(__file__)))
        else:
            print('第三方环境\n') 
        if os.path.abspath('.') not in sys.path:
            sys.path.append(os.path.abspath('.'))

    ## 批量提取pin,输出ckkk,path,pin_list
    def main_run(self):
        self.getcodefile()
        cookie_list=os.environ["wy_xdgy"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            print('请填写环境变量wy_xdgy\n')    
        return cookie_list


# headers
def headerss(cookie):
    a={
            'Cookie': cookie,
            'User-Agent': ua,
            'content-type': 'application/x-www-form-urlencoded',
            'x-t': gettimestamp(),
            'Host': 'sns.amap.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
    }
    return a

# 请求
def request_s(url,cookie,b=1):
    headers=headerss(cookie)
    for n in range(3):
        a=0
        try:
            time.sleep(1)
            res = requests.get(url=url, headers=headers, timeout=12,verify=False).json()
            a=1
            break
        except:
            print('请求失败，正在重试🌍...')
    if a==1 and b==1:
        processing_request_result(res)
    elif b==1:
        msg('❗任务失败...')
    return res


# 判断结果
def processing_request_result(res):
    result=res['result']
    if not result:
        msg('已完成或时间未到⭕\n')
    elif result:
        msg('任务完成✅')
        msg(f"获得水滴💧 {res['data']['rewards_list'][0]['amount']}\n")
    else:
        msg('❗️未知错误\n')

# 检查账号有效性
def getUserInfo(cookie):
    url='https://sns.amap.com/ws/activity/xiaode_garden/invite_token?ent=2&in=bTlkmqpRhIkqMLcHo71pGn3cINQtaO5WYoVQlCcApI2FaqJZaskXs2oGI4oysih5eyI8GV%2Fipm432TH7ICqYKPXsxrQHM1vyfD1QQ2%2Bv9D%2FyJIe%2Bm3hdvskTuH6tK5DMMzlgsQoZswzdPd92Iq1IPcGsB0EDG1JSacd6n%2BzT7Ba2Zz3mp7%2F7cLPIDVdaHM%2FyK3DY2iosKLN790JRluAzQBQ5JbHX9qssS48AUf6ZCz23EbHMMviohdSSVoiZVBoUGZrO0MQEmli%2FBNabEXkXnXTc7xvzDL86tBFylOJ1iOQ5ZuHX3eKaUdwKkzg5ctTGpH0tTUnRnbhyN6aobWOLskegbIq0JHGrbCSvCm6peeMFRKyJa5wLV0GWM98VWrcDq795IQ6gdafPwc618x9Ky0GJGjvln1WLIk1fafljtPOeNsKt6Ir1uS47Li0OV6dmKx2sljbvho9aXb0LzmSSTuFH7rRPNNRE8RiFaffnMOqBnwOYLHAPQmLrFmf3R9OoDwvqXXo5gh7fEGvbTLfFTfj4sjSB3m1chALdr%2BwveEKG%2FVEu7QcPd7QVoSQrcP54OsTCQ9%2F%2F9Fu3GwK7PN%2F0cZKsX29LUjUnWrjPUQY6eaU6J%2BmLLfefNrJof%2F8hV5NSOw9A1YpdvuYTxFPr9%2Fcz0SPFfag1A2XUeNZh6AePoobqgY7ZNlUAA108ml8bm6AGgTmT56CcleNN4nF1MCXZBb5LntEiXGCDsSF5SyyPWD37O7gU2YbYsyortVylXUcI%2F%2BM3eMrHU3fJpwd%2FDlxKwMOJM0K0Mnvw00PG53kgfKNvj5GrzWsO0LJwF%2FEJjS%2BC7r%2Bc5%2BR%2B8ozHB2eVz7RIRIuv9pVgrtndNx8EVLF%2BW9Nz33cfyCtwZtIkKygxUJFuetFJSmiTUE4EfUbU%2BBxTBEAyogZGlOngd%2FbOI0%2F9%2BGHkdx22zt8EySYjt0UW7hMHZplk%2FQfHdffk4QNi5yn2kyf3TdIx59CuaB1RyPU3MrPd7a%2B2HTdWuA%3D%3D&csid=3024dac4-b012-47ab-b9df-0ed6b2844afe'
    res = request_s(url,cookie,0)
    result=res['result']
    if not result:
        msg('❗️该账户cookie失效\n')
    return result


def one_click_water(cookie):
    # msg('一键领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_batch_reward?ent=2&in=mZjHCmSauK2hCMxfcYCvIiiWiC%2BhyqSdoQU3Jj%2BV4h1U9ydh6uC%2F4fRNhlMIwxpAMuJs4jrzvkXzjgPA5Ov6g%2FC0sPfnaiythSyh%2B6annrXR%2FNeAMuPFXy8yrO1v0DghlyhbsiXxYplsRCu7hYWIkpjcbCggcvskk%2FpleL7FhcznTdrnpZ0Y2O5HhnRelkw2JUbhSjlHKsNwT%2FaxqzZtNSo6PqU%2Fj2R0EZWJTzni8jMN1l1lfilTiFLmg0Mvkx9gBeonZ0y%2BkWXjr1ClaPoRDpCeBh3xhWGF70HPEpey5NwtYr%2FDRrqNDTCQq1ia5SMWMe7QRwMjX8O3NoN09OKkRzzBrmaZbhJXe6Tc%2F%2BKDO5IpH%2FW3gryeAE%2Bf%2FKbbHIX6fKKt7a31AMfJQOYyeILb3g8ARszRSduHMoedxGauWA7Js2EepvLHsSRM1zfDGnF%2Fe2nKY5o2m7IrN5b%2B6GHTrsIgFOcc%2Fkt6ms6DNdinevX2JzpLMOM04aCzOfe3zqccAVG3U18ora6REsHLJ8iurKq3BbrVBM3pDo7DmSt19pd296NSmAahV%2Fli4Y7UsenpQhBAbuor14PqjiZ8057hnsA0NWyLv5IC5%2Bh4sAaBy8ERKrcf8KZ4pjZBk6DNrOoDDTttHunqPlfe2ublbOlb72ynE3jiO2gQT5RiazlNdet5h3gDqKa6CmnZNsPpFzUgbDXae1ozlfLpcCqLDbROyZh7t5UnV3Ous3wt5I4eVbP6wTKMpc%2BKETdhseb35R04ey2CJ3XxuVolU1mLnNmvxMpHLRQAQC9CtIaUfTpi%2FOdotyQYlFTaMXvE%2FLpbQI6USVNPNZc3b2H9Noy5oNss97jgZBLD7stwtoFGkEbwEcPC%2BhJVHD%2FwvhtJBZcvhjF%2B3aEaBe5bVGZyasJQ0PkbyyMUJmuVCO%2F5DZmnyZSgP1AGi9QVt0V7YHYLbkKK4fI3ZV27BE7xnCcRuKrAroZEPRMo160guBi7&csid=9eebeb6f-1855-499c-aa80-c22e50baa628'
    res = request_s(url,cookie)

def log_in(cookie):
    msg('新人专享-登录打卡')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_tab_reward?ent=2&in=xFEAKTcRtOcEQFwfJ9LXDCqW725Wbuz6oPPV%2FWu5OWlttyEKIDuNOgmxBZPsSh%2FQF0uEkbRZ0l4BC7f2z4FphJUcQOfmnFeCbjKw9QCZTZ4nohDrkPHYAwcZJdnE8wzBKs3AY%2BRnDFWmtav7yUi5xB0Wf%2B5%2BIU9gNcL82dhT8%2Bilu737pJmYFp83Dw6s96IUnvveAtVkzEEk9EKHIaNOinJSzGyUprPol4LOnNuj9h2637L%2F9unsbXtCo4rDyglJskgc2Vd6D3aJ54LH8oi1sKrI1A6QTeDxdisTzdfwAkWil9fQaKtgZNK1B04gn0dN%2BOQzVZ3oQDjBSmow0qpNqstET2iaOJu8WDkgVoW8s2j6aw5LT6iZvqMX06w2qMTkVj9031k2hU2xHDvz5YNCvBvdA5K2KGuCwOchYBeTr7oZkXRQXLgM7BYQUCmz9G6uYJBMxAIwQFRp489iCroVLi7KpWE6Hp5fpoVvD%2BF4gJbTK3bTxaMmacY5AVo7LjZ2zaXl5MRG8icMLBgMdKSv0wr1aTiSjzTvRQAOqdflQiqNTtQ%2B9Er8ZBCoEYLL%2BnK%2B6yQ6muwF1ETxX0OtRwXtHlTUPwbxzbGGOXERKdRebVDz55Ic0ZzkxriivutOkbJDR2mYPmRgTaEsMjK%2F3ylZam3V27YrATZ92Gm0BvXEGM3MZQuWaspbDxwTSWtbJkvrO%2B2JlIVEQXZyh6L3ehvAHFFzo7QsVAJ%2BbCRiAM3OF5sIppPTJV5g7CcfmZiUmkIDd4nVC3PnURlMOyRj2y6hQZ7cla5bCmoiGMS9aLjkoYWS4zI35dtE7himrGDGURWVCJAc0B39KZ1qfEPIPVgAv0VpVAvyYaRN3ZoGzhUyAgc1a%2BTwK3hmyjhYbyV%2FE9GFY2NwBXCC3Ux83CFJTXv43upTPkiRl1EedkODJH%2FW2kRoeQbcabKeARPWI03uLmxsSs%2Fx6uVdIkQ6pANNgr5Kc7XsTusv3DCFJwsKbt%2FdHF8%3D&csid=748bf6a1-51c7-4d10-9939-4449d66e0f62'
    res = request_s(url,cookie)

def share_new(cookie):
    msg('新人专享-分享领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_tab_reward?ent=2&in=4I3qE4XiSt9AgBVHm2sxOpVYvlIaY8YYPAx3mdMYDDpNM1cf%2BPU3mPNuG%2FAZwqufq8qdtWtKPBA82fjAK2J3QsHcrjdDSnnfTSR8bkXzY7n8mLyYCHbcUtExa577O5TlWmwqJP8SGDxQiqgtOUwVwGaVRvpT46%2FiRh8fYt2rS7FZvMsBy52l9TIgtIDrt469Kflufwmd1BDxlu7vmbhlbzn1GKesfB9eNEIEa6mAI1leAs28PlMzsunT11Eyrp1rpe4aORBXi7OoaZazJd3HEtM9VUc0mCjtvqJDAo0aMRIQuz3QA%2B64Hti0%2FV2khK0lUKFPmFLjqVMJzvDdYKNU4w7yWGrUCjsjzLDe%2BXc6%2FLiiUkejMmtzpeAMKK8zv2zsOSi2kbwNfGElRjTqiaVWyjuS90mF509uG1ys3gYP8MX3ZMiuJ7CGLRv3o18XG0BqzX%2B4gEbZwUDCmnN47HF4s839LiJ9hbt8DMNHvcVMgs8uwaO1W9QjP%2F2abbzC9k63SxjmBlckfHpo1wW%2BH5kIcmGC9lCBhbTFH0N%2FfK%2BgjZX3dRPtF8bZ2ix6FJWx6R3TqgDYAMvGojlXaAMFhgknPsKXlkRzpfUTd5LLa%2BPNKczqLn%2BP2IVsqjNr60Jk60lEW0unuQgnIk8qZDewwkLwsh8kKZ67a64mJeirDX4NIBPwTH%2BQxUsZXSW5SJmU9RxzYPyE3YiUAC8mSH%2BfCUy2hGG9t2mDq6QiaO%2FaW4Dv2YpuRTbqz6IxT7kGkLl4zCJ0zutZh3McEx8FaG7L7fRFLgB3rKY0NhkCGTNbHayeaOhGN3yEA6WWS7n5nq%2F0RnLaK3CFJXQr%2Fgpkco7cGXCMS82J3%2B0kGuhnZJkuNJgwPvO4DJ8ygmb%2BKQBbq2ItP2f%2BpOquQndUO%2FmqI%2BwulriZ3vuu1Md4tObKXUwCaLLeK5NXBtlDsHU7BP2zSNUBMMjq5Z58jkj7%2FK0I%2B8ckwp0C90Mr3sxYTb5766n%2BABBmGIEShdiWKB5uHgNiXD1E%2FQb4TlOCUw%3D%3D&csid=378f0b14-b2dd-47c3-8845-5f363f102413'
    res = request_s(url,cookie)

def watering_new(cookie):
    msg('新人专享-浇水12次领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_tab_reward?ent=2&in=hHKGEbnCur6dNcB9QzSLI38tmPB2siCgmlLGqjCXI1cQGX52jFl2SssA4TDhKYeWKwpHgWnM1T0Wsb3v%2BQIbQCuaB3g12JYq1tBdx2v5xe4YLKnB9JQJLetNw58B41YmWGpJadL7gulClVpg4wMpFDvaPe%2BSLg7xHlmv1nn0IuB3tu9L7pYijY4tI8wF%2Bz4%2BM8Rl6Gois9wGbbKMq%2FElYrpJPD2Z0SwVmIVW9rJDwsqBHFD7w6udwf43qPEPL3JZD5tKqcjRvl%2FGsNtItB40%2BeNaOCPia6WC5XAlfRnCYKB7IyEDXVy03wDqHeeP7s9zGH%2FfcL1k3pnpXDRh0%2Fqhql6B%2BgKcLCnzQ2lXII8wJj7OnTrXAfXOOePcB%2Fdnr0ZLGxIOc2RTV51%2BXLoXKyUSbDqRKrcjLDRn1auduPXey8yU14YxxulH0nAJTie3rN7B65Fh%2F2C3QvNwymnZJ5k5HsF6pH%2FX4eL6ifqkU442ohJ1Qd9K8mU2CZlVqqq28PBDO6iMu%2FzLXLoSVMloRpapCfJhkIDQ4OHpXORcqcBfbfZpT%2FRwCX44jXhoMXDi3I8sM0hFw3a5AmPFWx4jJTLu6XiXHVkqdxxhD1bL6ANcXeWI5vb0VZlHTmFSpk%2B3HM2WBV47XDsAF7CjW%2FQDuXK1N3JTa47tTkauXWcqs%2B%2BXJ8RLLmg9KbXwl9p2IFK4PnMD5f%2FNll5IMMkaaEl8UXNskew2N8zNLC2GxSB8qAHvz6WvdtUEowX%2BmIJA95Y5QGyB%2BFWsF1jUKgxA1Gm2Anx8pS4kf7i1NRopXjodpwxd1tgzgNZgVY1dZLYhXMLZYlKBXzJ9qKyMdS3RFbc0oYt8ZteD0roSNh8Zegz7hG5AsUIBoEQ9hEv1F0lym3FTi%2B7lNbh9M5Z5wpNx4kAo8LWhQk3zTUfkBhe2M65XgielMLPrzUbIujdJfs4LzxDC%2FZViSyn0uqry%2By%2FYZdFk13EIod%2Fs7preJn8zo8bD9b%2BQsZDkcuvVMrqIgR5DuoV7nS8V1%2BBbLg%3D%3D&csid=07395523-595f-46c1-b3be-903425927cba'
    res = request_s(url,cookie)    

def grand_tota_new(cookie):
    msg('新人专享-累计完成任务领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_tab_reward?ent=2&in=miXMOjvp67K7HfB9C%2BDHSGArzXLBIY1AJXYpoPzxYOGQhhdfjch7f7%2BRR4DCKvQ0DnC2%2FJWrcAGk4QRyE%2FWrqwkf5cGu1sfNlpuKuhFM1wmgem2xjMtv1AiP0abVXlSZrXffmtXSElA7zoNHFGyMtMzJENCiduREDlyvZcd%2F8NRK6wTuWf9tB3fd5qHQphe7%2Bdt7mpPzLa2XXdq9gHhPiolaifKHjXZLeYenDIBHVMsqW8QwFbhU0d%2FRoIxpVR%2FkF%2B8lX3fRkFQ4qqKnwmu04yOnCPCKC1Ub9nMbB1Z%2F%2BujIibupIvCINTBONc%2BGhC7vL7q4gB1tiqVBpuQ6VTJao08%2Bd2%2B1F5oCXIRaIyxjO3KjRGpTWhTXwHNm2Thys1ltEm6xwBdjBMEu5ankS5OMnEIWmgXyzXXD2%2FWoR25FH8Z%2Bsz%2Bqpi75%2FqJoqApN8ybhaPJU8THxQePVxG3JP5akZcaM8FePJ4Ngy7QPTTTqUEeP1AxNt6uh1DvjwR09%2BFF9lTr8UjVstByzF9ZF%2FhOT3FF0rG84XY11QJ3gAB9LLd%2F1h4nm8ql6fvznq9W%2BJl0uVjEa9UZm7YnO8AxpFXzbRphyTGfOb2HJ80uBM1w%2FJeOqFqJ2Ms7VIGSH3EKOmXL3RnongDq%2Bb4YEF9YDwmbGSrBicmxzbeS0AvZawnVtZudMfkAT9pXeYnLOsbrfBWx3NgX2wOMW%2BZqti9gxrZuT77xqZEadIkB4Kvze%2B2akCN38zX2oRFPiYFFBxS9BoR19DLdfJcrGTGbVKz4O0jr31AsgLPEWCvHtqvtfOBff0%2Bi5haPjwGbF59rbKswKfpag78OcoLmbxwtdSWHdijs3%2FZ19JxfWZautaiXyOj8y2k%2FlQ3uq8hZSDVrh1sCsz7jrcuTUEZ1bW044ZMhhr3n4YH%2Bh7uACikr7%2BsZHKB6d6kiqXUtOpRvUhBZpC7SOAlNN6s7G6MG20f%2F5M%2Bk4gnHYuzjZn2XJcN%2Bak6%2BZ4swr8fk6NLBh4A1JhAgV0h%2FBSSAnIp%2FjwQ%3D%3D&csid=bb7a081c-d191-46f3-977c-792735b451aa'
    res = request_s(url,cookie)    

def doTask(cookie):
    a=getUserInfo(cookie)
    if not a:
        return
    log_in(cookie)
    share_new(cookie)
    watering_new(cookie)
    share_new(cookie)
    grand_tota_new(cookie)
    one_click_water(cookie)


## 获取通知服务
class Msg(object):
    def getsendNotify(self, a=1):
        try:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/myScripts/main/sendNotify.py'
            response = requests.get(url)
            with open('sendNotify.py', "w+", encoding="utf-8") as f:
                f.write(response.text)
            return
        except:
            pass
        if a < 5:
            a += 1
            return self.getsendNotify(a)

    def main(self):
        global send,msg,initialize
        cur_path = os.path.abspath('.')
        sys.path.append(cur_path)
        for n in range(3):
            if os.path.exists(cur_path + "/sendNotify.py"):
                try:
                    from sendNotify import send,msg,initialize
                    break
                except:
                    self.getsendNotify()
            else:
                self.getsendNotify()
        l=['BARK','PUSH_KEY','TG_BOT_TOKEN','TG_USER_ID','TG_API_HOST','TG_PROXY_HOST','TG_PROXY_PORT','DD_BOT_TOKEN','DD_BOT_SECRET','QQ_SKEY','Q_SKEY','QQ_MODE','QYWX_AM','PUSH_PLUS_TOKEN']
        d={}
        for a in l:
            try:
                d[a]=eval(a)
            except:
                d[a]=''
        initialize(d)   # 初始化        
Msg().main()   # 初始化通知服务  


if __name__ == '__main__':
    msg('🔔小德果园-新人专享任务，开始！\n')
    ua=ua_random()
    cookie_list=Judge_env().main_run()
    msg(f'====================共{len(cookie_list)}高德地图个账号Cookie=========\n')
    for e,cookie in enumerate(cookie_list,start=1):
        msg(f'******开始【账号 {e}】 做任务*********\n')
        doTask(cookie)
    send('🔔小德果园-新人专享任务')   # 启用通知服务
