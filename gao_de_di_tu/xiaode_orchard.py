# 小德果园
# 入口>高德地图
# 脚本功能为自动浇水，签到等功能，还在完善
# 环境变量wy_xdgy，抓包搜索'sns.amap.com',复制cookie,填入环境变量中，多账号用&分割
# export wy_xdgy="你的cookie1&你的cookie2"
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

# 判断结果
def processing_request_result(res):
    result=res['result']
    if not result:
        msg('已完成或时间未到，跳过\n')
    elif result:
        msg('任务完成✅')
        msg(f"获得水滴 {res['data']['rewards_list'][0]['amount']}\n")
    else:
        msg('未知错误\n')


# 浇水
def watering(cookie):
    time.sleep(1)
    msg('开始浇水')
    url='https://sns.amap.com/ws/activity/xiaode_garden/watering?ent=2&in=2ErotOlY2vHtcyueLr29uaDQ0jwc6CPGDar5oGe%2F%2BbovvT5mg%2BTBse4zwD8P8GLyf9z6DGepLqgYIHJB3nssPqdMVfiatukY27Wa9%2FZm77Yi7cSPzaJ%2FLvGcKy1h27CSoAxVBNkmSKoH6QN8dlJQz1QgkCuhiVsvASvyo7FFcP4fkupbfKVHjo7KLMNwZLD%2BPRXJ1iV99IbfJzHAq7IYLlazpCXQKCxo714MrsaBtm6%2FO1lzVsbLeGVrKOLujZYKFwPcM8KHkCHtMguibPJ%2FuBY0YqjxNoO4VFi%2BP1tVLoeYOTlXzs%2BnNO9futMq5LmbEOpOESUg%2BTyfSFaYtRB9F%2BMb8BLdGoZK70kBIlqaADFk3kgTDzj5LM4kfsGhCLCitsni7U86yQTTH0ZxQAw0quWqMR49AkdUfe%2FY6MStrzZA9yJt7GVozRv1Zo0833SKTpiluKcQqirKgW%2BtTfw9slRqllxj7PSesCSDNpcodSYCRcO1jt%2Bnrz%2F7M0CZjR0V5SxF%2FYhw%2B5flf%2Bzh7O8A6fUOs8ezcLe3gaXVViD%2Bk8ioeD2CokY9rvFqviurgVrX1kZkb%2FoQnkpiXIEXr26lOXBT4PLbK56BWjyzsJ3eSVCJak0C8vfELnbSutEnBy7Xv3NyLJ64x%2FNdpt%2FEk1d%2B8uusl6xcFQK1PSJ0nSWPBChv0BgMT1vDU6wDA%2BeKyyPoQDH8oFcbzuEt%2FNJosHKmStlLixqzLILs0t8FGNxp%2FzHBht9jTmk%2F7pp3%2FnL%2BtcJssH7tr1HNy79BKSxTThLDxxCCfb4mhMojQv34xq9TE19m%2FE8BV9r02%2BSbNew3GdxY%2BjZzNFQRloY8%2BPlXpeAJFeB7T2flAG1%2BQcAPl1szdClQq37aceZitzEBzx%2Bju2TyEELzwV%2FpXGBTheLB9HQxduDdYmlADogxmfhiC2NSCsM5hHuOLNZYuMXTC02ChQkcwZRrfAnudnsceFooZU8KTtUHi4Qh4vllqssBa6oFatY%3D&csid=c971673e-22bc-47b9-9d3a-a0c4d26c7b81'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    code=res['code']
    if code=='1':
        msg(f"浇水成功，剩余水滴 {res['data']['left_water']}")
        if res['data']['left_water']>30:
            watering(cookie)
        else:
            msg("剩余水滴不足30，浇水结束\n")
    elif code=='107':
        msg('剩余水滴不足,跳过浇水\n')
    else:
        msg('未知错误\n')


# 检查账号有效性
def getUserInfo(cookie):
    time.sleep(1)
    url='https://sns.amap.com/ws/activity/xiaode_garden/invite_token?ent=2&in=bTlkmqpRhIkqMLcHo71pGn3cINQtaO5WYoVQlCcApI2FaqJZaskXs2oGI4oysih5eyI8GV%2Fipm432TH7ICqYKPXsxrQHM1vyfD1QQ2%2Bv9D%2FyJIe%2Bm3hdvskTuH6tK5DMMzlgsQoZswzdPd92Iq1IPcGsB0EDG1JSacd6n%2BzT7Ba2Zz3mp7%2F7cLPIDVdaHM%2FyK3DY2iosKLN790JRluAzQBQ5JbHX9qssS48AUf6ZCz23EbHMMviohdSSVoiZVBoUGZrO0MQEmli%2FBNabEXkXnXTc7xvzDL86tBFylOJ1iOQ5ZuHX3eKaUdwKkzg5ctTGpH0tTUnRnbhyN6aobWOLskegbIq0JHGrbCSvCm6peeMFRKyJa5wLV0GWM98VWrcDq795IQ6gdafPwc618x9Ky0GJGjvln1WLIk1fafljtPOeNsKt6Ir1uS47Li0OV6dmKx2sljbvho9aXb0LzmSSTuFH7rRPNNRE8RiFaffnMOqBnwOYLHAPQmLrFmf3R9OoDwvqXXo5gh7fEGvbTLfFTfj4sjSB3m1chALdr%2BwveEKG%2FVEu7QcPd7QVoSQrcP54OsTCQ9%2F%2F9Fu3GwK7PN%2F0cZKsX29LUjUnWrjPUQY6eaU6J%2BmLLfefNrJof%2F8hV5NSOw9A1YpdvuYTxFPr9%2Fcz0SPFfag1A2XUeNZh6AePoobqgY7ZNlUAA108ml8bm6AGgTmT56CcleNN4nF1MCXZBb5LntEiXGCDsSF5SyyPWD37O7gU2YbYsyortVylXUcI%2F%2BM3eMrHU3fJpwd%2FDlxKwMOJM0K0Mnvw00PG53kgfKNvj5GrzWsO0LJwF%2FEJjS%2BC7r%2Bc5%2BR%2B8ozHB2eVz7RIRIuv9pVgrtndNx8EVLF%2BW9Nz33cfyCtwZtIkKygxUJFuetFJSmiTUE4EfUbU%2BBxTBEAyogZGlOngd%2FbOI0%2F9%2BGHkdx22zt8EySYjt0UW7hMHZplk%2FQfHdffk4QNi5yn2kyf3TdIx59CuaB1RyPU3MrPd7a%2B2HTdWuA%3D%3D&csid=3024dac4-b012-47ab-b9df-0ed6b2844afe'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    result=res['result']
    if not result:
        msg('该账户cookie失效\n')
    return result


# 咸鱼任务
def fish(cookie):
    time.sleep(1)
    msg('开始咸鱼任务')
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=wSndMnNDq25yX1%2BE1y%2FYHOjeyT%2BTfwjdpgI1dLe9E8qE%2FiVxK0YVi2FUTZtc4GZ2zOxpkk86%2Bmggh70Uv%2BrX43yWZ2LqRnhTn%2FXlNGZGv3V6Hi9tetNAfJUWFtaATGfwK4U7LLr1yGO8sETBKP0zgyY3zrQVG%2FML95m6%2BEXSj9jRSsTHJCzCY0r1vva6CgLlIjWTyYc9F4RP70zAgLDsKvF6MEcflVEo89NQmlO5O1HlWbnm5KeTMC50mBKmw1QlAbV47TudjgL%2BOacejRhpjZriVltUaYS6GfK5THhZBJJwIXh72d%2FmS89lvzY%2Fhiyp2Ki7U1QXR55w%2FBOeydPANUXTit15mD7IJ%2FzTY32y0bC%2FIoTtkZa9g1rJHvzvZS43qjK1Bo1phrYT05qts6%2F2DfEk3RwcRREanAwgcYH2yfCKXeeenSpUT5jIWrbK0e94cw276GGQ%2BJlwklM3OE6ushPQKVzTckjBMJaZ75J8U6iKtE6%2BL1s%2FQy2KjOCtfCA%2FhdW8PQ89fjE6jSx6cDlaMtryR2sNLF7V0e%2FXC0I1jk%2BP9xpUHXSQaC16JshA6qiac21j7XFQfZkhrgUEYUAN7NC7Dgro2fCtBrRDY2DYqJAuGxFcKeAnMrCVnXGrMlJS15JnxTbDQMfKgA4koocc9RdcNh2rseS4FgIRkjdw6LOGckxWioHa1O0B%2F8gHd6Ym9qhAIqELUzvvCmiZ9w9aAkue8p41LIkMjoQmqmdR550U4oROG1IfmKIk7t4PKiKnhske0rrMqjYvWumbp82GZPeaQydub%2FtZggi4vRzb4HRr7HAgAo8p870wo5mViXdXdYd93CbvdXe%2FrzDBTXt%2B8UtJSlHG3i6SbAzj7SNsFeCsu3ZIJ67ucz3a5dVsVtzqh2qDWjiJXVE9RYHEy7tFdQpbSf2HtTJNmZDGyGHHWA90Q5H8evSb65Z1oji6ceGMZ1V%2BLELEuEFYIM%2FVBr7%2BW%2Bxrb77vGWNTNql80MrTHLb9TszuFdlzyzqDHidMaqTaOWngLiArksaf%2FApE1pcwLOHTdXWcYyLnQX9Vyg%3D%3D&csid=a5530f5a-cbf2-4e45-b359-11b60b9ef368'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=3b%2BfKRvfKuSMY%2FZqD9%2BY5QlNLRzmBom8CQyRk6sTcG7zBtdrsyhwAMjSMG4zWW%2Bv3ebjhWlkJluLhgIHAaBn36G5H%2BuXWcMuEj8z5NPjEqgO5Okp5mSRSRrafvfbn2q%2FlD16jKy4LVsatkE1M5FNr%2BHzpjr32qML%2FP3LpSOfDBBMx8clXOavH%2B7Utci%2B%2FGEYxcKMpiuenJ4Q8WXeHp8wohh7UYRUdpaZMxjmzzn%2FRhJiTZZFpu7vvM6imd5SACDJtGpge4gr1fvvkIkkh8bTtPQ3KdedaS6GNVdSEJjabNllCq0EnIySE8nd17aju8j6uk8G8dwWBe%2FxDMaW%2BP%2FcaVsn49Z6BDRt%2BiQiJTmrOjt%2BEivKQ57O6SZpd1crpous55C9hKAP9kiISZsDfdVlBlO8ActMaXuyfq8zIEVmcR6qyY63VGTlDBHipTHFCTwQ%2FUKEpQqaIWP2uOb9IqRbvDtGfMofbe%2BnFAo4MLXdR%2BWbdQwYn%2Bd7c4p4FJTNQA018tg3kWXnkAGvyIKiiBxmDzpt4SuVJEydiFvuqRxQNCkuR7pptBZ4hAPr98UEiGba%2BLJK5QPIcfwuPDrJSuQCKGIwTCXlIy8ir15uAQJACOaYmKfpp7dQcoxo55BKc9%2BwHlpF3dy%2BLq2vy%2FWxnmt%2BsxEgANrllPw0CK%2Brr%2B4QI97f9OKStZyrStLYZHwESdcW6xB9Kbqh%2BfHtzcEVUX3cAYJ%2Bh1EIMaidjqeE8YRWE66ZSdNNXAqcoo02GzfyuVa%2FvoY%2FJDwxhjTJGilBkXc21%2BZJF8FG68OabN0CHElw879Sxesg1IrobdBENFW9SA9ixfzvFqZfmOdNyjvAHaqK41TkTaBOYyzczwp1HbbT%2Bs6RBFUwpubOkUOrn4Pld5P%2BvGN7zYw62KqLhz%2FvQMlvouR5djS%2BTdaCwDEvme8%2FKaavO2wyu3Unq3NBEGRa6LgvmhD90iedqK%2F2iDsnXGzE6HH2hwhg5fgW0gY6NbYe8BHrnjlPNSgIgeFz85WyTEFCLfG8ULlFTQTQuguEDpLaFA%3D%3D&csid=7001cafc-c36d-4b43-8ff5-7ac62ee56b21'
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    processing_request_result(res)


# 忘了名字的一个任务
def anonymous(cookie):
    time.sleep(1)
    msg('开起新大陆？？？')
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=qttewDlIpmGHK%2BTvNpJUmXbVnZqdU8ClLRUBPBRJXprGMopAFXd%2FP%2B2fmWdUjJAq79XYtrmxukx8WbSLSF%2BwK6iXIzvHuOVeunwvSO9GCSE3KQNFAR4%2B%2Bb%2BqNZj%2BHXpI%2FFcL3hy0n9fdHVGXxw1Lz4uZeBvW2PdTQ591SgUO36x6CpWGJT0abX8fPNE0T%2FBPbOJ7Ryj3ZC28OpEX9hm1EclZQQoNEuH%2FuvzS3fuApBRaf%2FlYPhQ6CVxqHRRoWnK8vgonELb%2F8aCDufTGE%2B5KrGKZGDmQd2HFlMPFfxr9A%2BL5%2BcJy4%2Bng8ilK88tCmo16RBI5xgz8pJRna3xClVVio4QxKUPO9bJfoyp1qsM%2BWEV8%2Bbz7eHNmGS6GpTw63j%2BHj4y3pRmtz1SS3E7pf6RmzXVdf%2FEyDJeFxTjTHeFLOo6vSPX0uW8NXRjQ%2FY8H6tQMfKALY7LLMqwHKoGixkPIxMlEf1y4GAk8WcyuKShHOo4NEWHXBmTW48tohxvYye7g4Kt0JaMhlESC%2F5axPxZuiEid6H10oOqKmPETSL445R3oeyVfMjsVlvMosMiMUudP2duwVToxOyQGWIFWhH9ccAPOVzHtmAB68Tq95SF6TV3oV7KZCC1iMhVMClIUoBlZbTF%2BRxEG980Jx%2BryWCrK%2B%2F2XFaV36QRdLkydwcgVAu9ZEdwTX9QI5Y0isFt2N4WeALFkbjp0XUIjFO8j5fmyGKfTJYfjYA2lb%2FTYzyct7jCBs22tnOZmrGLQ14eD4fMwSBy%2F7stiqoqWGKTeO7Py7%2FQrOvbSQ2ecCLkPEjv%2FpftX7A9yKneFU%2FuSFxcZ2zoSlVxJJEuzpbRJZYwT3%2FFexb1mrb%2BXz5NQ59QLottjym1jczrWCTTFbWhOB2EyF%2B3YEcLCgnOxuYLAJqSkmZ0ZquuRy58s80L8M9kzi%2FhpH4mrLs6xEkGczSi73%2BM5%2F194QQTjAonehGV4uAo69hlcLs%2BhDIUYqAeym%2Bzc7Nv9NVy27MaHcI6SrfUPgMkJMAdygDPqTTT1Kr1U8lOirKlzmXhmPem5BADpfu%2F5A2RSdLvu2Ww9JVqmg991TZ4rpuP%2F&csid=39fa84ae-1162-455e-8afd-46a9041e881a'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=nFkyIAqF8cHefEc%2BV564nrIuLkJ%2Fspawt7lMhCzL7IyUp5caG16qqd32t1KJdFuc9oDkRKK5WWalFZR4MbHXpRyQn1dVqI9SGqlBOJF3Ti%2Fn0l7IH4zuz0AhNg5n3ME0Ii3fSPmM%2FM1F8lRqFoyE68bRRrO6R7MdQ0UU910gV2odpmsL7VvwzNwypM9ryoqIL%2FB6XUOYMBtezvwpPSNxKr3uxoA%2BZf0ZXiUnvHMwiVfUdDMLP3gR3kAjIGf45mHhfO1M8%2Fivho5SjZs0OG%2B9MJuwTV%2FulurBBcYMsumAqoJzsG4pybAJCGpt84LUfepbgyDftS2M8VGtg2YSAFDSbZ0Qph%2B0CZby6CUNjqi0clB%2B1PYiGR8NPJ8nTNhvZ%2FfOX9HmCdS1x1%2BQ0PetkE8uXkTVvIOIVCjLmrTGoLJvG59NEfqo5b116nzGKWqBexudiWxpWGJmvEadQiU%2FXj9QFqQp50WT0f7LqlfuQc8bpCU%2BtsSGcPGUlD3l0E8MTpVyKwjWk4rIahUN7tEhBsQeRP1uyd0EZuLme1kbeIG6yKOcSBwAar%2BHZ5D40ErZ19%2BpFUU6cJiwDAgcYR16yf4TmAkoeV%2BvK5MYaM%2B7Hj3jh0Yf5In04rrSRg6SMtYr4PyZi6DodJv3nbWP%2FQAg2xZgcGN%2FMFLYrmK16ds%2BfUMTHwbqdjRY2vJCLZf%2BxJ1jzSvX9DMPjw58dpqzbbvISGUEZwxTqnpaZ%2Fj12KknKQblYn4NON3slMirjiU8SimKL14tQgzl1h91LKgk5imkuSJqkJz8ZcvCEQudhaUCnhnzlw3JgewPh1x0J0HMl83Egyvrd6oClxIAQamNAtOgIaS0Zkzfqh6zcB3pyYUyOS83bdB0o4q0EWu95rKzyH0%2B8JECVV8v%2F7EgRZIWySOn9ZPqq3v5Ky52U6uKNAgCBzOLpJc%2FEABrIsW3vTOqf4xR%2B5LIdfnN0bheHW1w%2BmqH0SFiqeN05ZwgrQbh0rnsbNl4g4zDtq9PKAbbzKM4jCSIWYqJeART7PC%2BEUnobxO6Zi%2BgqvvHILU%3D&csid=b6e36910-3685-4481-8137-e9c4a1ca335b'
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    processing_request_result(res)



# 首页进入小德果园
def front_page(cookie):
    time.sleep(1)
    msg('开始首页进入小德果园任务')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=hBL8qV3voRJ4OcDweRv4WLA4vrPxmrPvYHfOuc99eAajoWOIXMM4UuouWiKFa9o6Pa5E9zpVs2KhQ%2FXy19NiFQfGJ%2BiCHFwS%2BbU7E7cLe8yZzR%2BoxLH%2FneiWYBhduh2liVklLNItgXs%2FBg0JcMw7gPG4l2YZBnS9IsiWY90CRus87NJVfFtUON2Nh3%2FRIFV0Kfae8UX81SUIfq32HEyEZ846Ry6PSQXKJmGKo%2FArhZ086l9QkVSEcxUK2%2Fgmq5uZcuKJeFUD4UhLCC2lc7kl%2BXGITbcJEtJYEhDEdKF0FO9UFqHfVXeMrPyzRxQkRNnorNx%2FR%2F%2FsV1ucK9yRitQ0K7NY9PTuzYrmvgt7T%2B1rMEudtDcSkM5mE8XkYiMIfbT%2BeHXUNPeF5Qzpn%2Fp9DxP1i7An3Y36BR%2B2JipdgJbnR%2BZV7uOjPJmgE0HYtUNBPNmdE1JeWx%2B6iXd2iGOjI6QgOT5HI9HuuQM1aDXSV3JKn1Vg0VBN1uaVIunbssWSAiWIpAsC3D%2FK5bAM5yJu0EEVxiRdrdxC4HP1Jn3KVsYCVy8L58xsojJuqNNR4p%2FH17OUsYyUbL3X2M%2B%2BR1K8rvZ7qoYU98l1mewLhPBw2LIzc2G4apNe1MzPDnLpoA%2B7rBM%2FhnwylKb728Va41Ouc9f5nTxym8Mkj0ZDxQlGXCy24hKC86zQvCWj0uTFcEuBlPPrpEbe0z5NYyr7Aejq6zvoRACF1ey%2F0layWyL5CWwW8FWQeh1%2FjYG21BizeUGMEqDn1SaEG1996HnrgVtOXGkRHWtdTB0UkeA7fRChlazDF4IoXdbFk372Erzb9YGE1brGHRd15qLgAH0kXogBhXtVf3otH5OT1NSp6RdaIYbTuLmRGKwV%2BUpVlJmEZnzctj5WcInBz64%2B7QP9hYIJNkXB%2FLEFUpHH5spcBr3usT4agID7IrbSP0j%2BEyoXpG2IZMrNOEVBbD%2BFSREH1EkOqTIQiphUk1Rb3g71pu21PQlwQRy5M0wEAepxMdOjoGlX9AJyaVebhg%3D%3D&csid=6b2fc58b-7341-4e18-b1cd-bad78c2315ca'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    processing_request_result(res)


# 热门活动领水滴
def hotDoing(cookie):
    time.sleep(1)
    msg('开始热门活动领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=ZmMrPwrxz0vBdqlRUi9tqfIg8ZOUChXs07wTrtEzJW9YrtO0FGjs%2FPf2n8%2BaXWxAhdpq0pfGQBdIjeMKDmtwn2BNZevgzIcR29g0wJoFLxlqYzDqe%2B%2F7d9tp0hAeEATfG312HBG9YJ1nE8V1gg%2FOXMb11CngLSgLby%2FPkFNDAFRwfyWkJXnCQM%2Fty8wJXmqlikA03zDKoH1oRfWM16ExLs%2BTBmFajrBhvmoUs40hTd0fox2eUXmEffsiM1tcBZfmLpMq9RQ1UmFc%2FMbAASZmu%2Fe2vfP46JKYV4tvjORnRn6oRUVhTtfKeMrQRzXYJy%2F753c1t%2FQT2yNTI3IJBHWQRVdMsDkb9etIhtjGi8SqgClKcdNqUa41OYzE5TyTEnDmKpM1noMW%2BPFoVHVosSfKkimX0OZEqyaKoFqAzr7LGxM8dsk0Uy5jk9FW%2BId9ZTRr0XAVZdDyunCo%2F%2FgLgTB%2BgVGmlezGo3b2cwOjCP%2BeSjecDqqXvYEPI%2F6zTLZJ0uRle2JEXgB7a1iGSJPAKKHwMLo1tdoGkKuDmlPP%2FJ3GL1mx%2BlXXWie8lfGp47JOG5G9jRKGdUuftlhT5%2BJezz39GQVOLf4fbtAcK%2FGPCNGYU6vj7LILOO%2FWt16QeJpasT9r6O4iQRYQ4iw4GLy34TvM1toskUC8Bej9jDc%2B82CUadB73rjmw%2FE3Wq4O6LI%2F4xABCmFq6Gs6R6%2FXkqU3Xt4HZ0MUM0QNu90ZYN6ruEjygIMvRQetFPmKU%2BU1DFY7tYMqQrMWx%2B%2FAcUimKryeUc5RdOXfIKweYSo%2BnL6tMYeVxLFE5fnZmVrrcUz%2BuDddA%2B2A%2FbZ484lTOk8bJA2jCugNxUO4W1RkMWX1GEgEVt%2B2fOVyvAfR4GSiJqC8bF%2BjbHLHbrvmRZIGBMEKvky2Mp4USsUC1VkeA5oiDOWpZ7hADg0Fh5NPcnSNzXgRDvNsqa3Iw4KY0IZGqGZ5HmfbQ8zvIzqgSj%2BVFyQHZYFlU27dYR3uyXcPUbn5MD6aszS2mIJcKwAyJk7sdmGNVkTqZFb4a2m%2FEIc%3D&csid=c05640c3-e554-4a09-b0a7-f7f6d559e9cf'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    processing_request_result(res)


# 一日三餐领水滴
def threeWater(cookie):
    time.sleep(1)
    msg('开始一日三餐领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=RVBgMC3rDAa%2B6rKrqxx3mPMSgMilMHIQKu5zhIwvqo28R3TDPFE8QGO9AS9ZO4lOinpol5USg%2FpjTLDTDYk7fbuFVZgMUfB%2BM8yBZffQPeg4EnBJnVa7AD4kMs7%2B5PEMfRWzL7uTY0S%2B8ZYFubEkDX%2FxkxTY2SakfJy2PMMMdr%2F3JH3ZNy09Xrk9UuYUhfr30AgB%2B8eRv80KkH1qiMp8E6RkGCsr0w7v6rrkGdjZJerR%2BgjN3UNIKj3ZXUQegOX7FUURkapkHuKo%2Bcma693CzUmtci%2FqE1GdgLhNftISsBBIhW%2F720x%2Bi3mSwG2Ze4IlERzfHqUE1w2YPQ2iYhRNftCx2FLTRszkMJ1K%2BHi1pUNioSYIAHNDtRt4EAwsEe37vas2jRcWyGopDgh8qnvzrK%2FfRjSXtA6KlsN%2BgKmcIMeOVPL5gE7KhrTPBOv06OTNwJ%2BZ0R4BaVmvALTZPKTCVBY875o2GUhRXE4BK5aB%2BunGx7dSe0imCjv%2FWFAVLI3aUZaKhGdqS%2FrxCf6jpCK4byqgCaVRRyTFYNJmxbEJwsZtGRx1FXgPVAXBEkZlmwuMw7JO7i5oY1CgFXzeZEr%2BtxXhgkIGysqlnlZEND8sjMWg%2BQcKSfuk4H7Ugic1%2BiG9onKWzuAbBgeuaGfK4sDvcyoivLZsux6%2Bu8DGC1TdIPlr8Zqgf0dD%2B9ypZwMbzRPBzZH0m9HvdDXQzfx5AOgljulAdvijo68xURHVtCKAP%2Fqg3dJjlGcIb6jH8yOu4MuuPMMk%2FY%2FppmqKTHUcSQqt4aQpWZ7s24YlfcaZmJcPal%2FUJpR5OstOTXABM%2FcYLqssN3CgrmywMKv6Nd%2FA6yg%2F6L7lOSlf7qZ5slWLKjvooLAlmhqyAPKV7h6UqchlVFEd04cEjOPPZ6B%2BklTM3PKtNBMLUgMWTRCHVUqDQ9iTC27wdRmmn8bhoQnX%2BzY4gL7WL6j%2Bo6OW22BOYhlPEQV7%2FKpE52VTcSvxcQEaAbZXYQVkYHOgKTQdxIpGgmxgKgS1gYcOKBR3Ee5kpTsx&csid=880aa606-c566-4871-a5c4-bbc520c6616b'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    processing_request_result(res)

# 签到
def keepSign(cookie):
    time.sleep(1)
    msg('开始签到')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=bdEfO5l9%2B1IceQTpZXkY83y3PGoGZIw%2BftEv3p6yVrYRwtu%2FOjHK7GuvVSkeGwPWEIYs%2F34WiMUMSt2UPjmm07LzSWpbx%2FosUNaRrkXuk1Dagl9a2CtNfiv5B9dxfj0phhz7dJBf6BnCloWnuAuMUCdz5JmkJ4yn%2BxilINb5lYXExsmsKr1ADVtPp%2FXjOK1FoUcQw0D%2FSM%2B1t0FuhM%2BPjPUQB4OodPtns3nZN2cvPIe7UcfwOW4%2FNGf7ES50z13Bm%2BGFFuSKYZXR2bOMUtBaZq51yjvUFSu3OSItQKf6GKnC6TxO9pUrHf5e03JQ4UWIa9lFi9z8hwWcyDCAqEYJu5UEqAJGajcwx6LyzWlRsevNlySBqiuDck3cqXaYQTsyRFxwOqjkvt1RmWVKfoOroaDLieh1b%2FkeIKjknvy%2BCC3DFuHOe0U9EapCFWWpOpCybmXL%2Fey%2FE5WJbWP8jvgwKYidEHTZssaZQxxi59RV%2BuBX9otM5yfxuhu3TxAGfQBnvZBEbene4EfOGKVmqcQ%2F2wtSkdBgzv1hzT4gHRaWlt8ddcRNgVSt49gbMB2K4P7z9XK9mvzKyjQldaJYmGX%2BnUcgB1D5KThTb%2BTdzFlR7JQ%2F0Ew69h%2BTOcNagw4dMp%2BKQVLkaQ1Q5ke%2FtMN7D6CcTGLzc0WbUljj10q5P2pTBkBDvHGy1t%2Bs9IpJbuuOQIJa0VnD%2BmrSacX3ABfFV0cyUM7r19Ij%2BDcFx6OmrivkGH9EYWUrB6ducrL42svivJXA1%2Fhx18OSWX1Mac7NH8GChCE2XkV4nQ5hr9876xXntBqfiZPkPL7OW3Lohc8t6FUV3lIXrflRHOyrouL6Uy2DisQCNutzbDgZsP3G3WldJAsJkYYevXRb7QS2PlfONCznG2nqGU2qyInIDJkhpT9aZt5wYHn8WTYjjdJyQXsulhA1cHTYan2o%2FbOSxxN%2FPH2VsH3J%2BfEES3asqLVCnRaFOXF%2B8HRDVP1fura9cCvC9ON3R%2Buncux4eML%2BRaF5fjICMz0nEMzaVNzr9U6%2Fpdgd9cir3OM%3D&csid=820e3549-594f-4923-8949-ac416eec4618'
    headers=headerss(cookie)
    res = requests.get(url=url, headers=headers, timeout=2,verify=False).json()
    processing_request_result(res)


def doTask(cookie):
    a=getUserInfo(cookie)
    if not a:
        return
    keepSign(cookie)
    threeWater(cookie)
    hotDoing(cookie)
    front_page(cookie)
    anonymous(cookie)
    fish(cookie)
    watering(cookie)


## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.message()
    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = f'{msg_info}\n{self.str_msg}'
        except:
            msg_info = f'{self.str_msg}'
        sys.stdout.flush()
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://ghproxy.com/https://raw.githubusercontent.com/wuye999/jd/main/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath('.')
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")
                
msg("").main()  # 初始化通知服务



if __name__ == '__main__':
    print('-----小德果园-----\n')
    ua=ua_random()
    cookie_list=Judge_env().main_run()
    for e,cookie in enumerate(cookie_list,start=1):
        print(f'第 {e} 个账号开始做任务')
        doTask(cookie)
    send('### 小德果园 ###', msg_info)   # 启用通知服务

