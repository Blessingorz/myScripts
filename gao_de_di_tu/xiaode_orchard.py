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


# 浇水
def watering(cookie):
    msg('开始浇水💦')
    url='https://sns.amap.com/ws/activity/xiaode_garden/watering?ent=2&in=2ErotOlY2vHtcyueLr29uaDQ0jwc6CPGDar5oGe%2F%2BbovvT5mg%2BTBse4zwD8P8GLyf9z6DGepLqgYIHJB3nssPqdMVfiatukY27Wa9%2FZm77Yi7cSPzaJ%2FLvGcKy1h27CSoAxVBNkmSKoH6QN8dlJQz1QgkCuhiVsvASvyo7FFcP4fkupbfKVHjo7KLMNwZLD%2BPRXJ1iV99IbfJzHAq7IYLlazpCXQKCxo714MrsaBtm6%2FO1lzVsbLeGVrKOLujZYKFwPcM8KHkCHtMguibPJ%2FuBY0YqjxNoO4VFi%2BP1tVLoeYOTlXzs%2BnNO9futMq5LmbEOpOESUg%2BTyfSFaYtRB9F%2BMb8BLdGoZK70kBIlqaADFk3kgTDzj5LM4kfsGhCLCitsni7U86yQTTH0ZxQAw0quWqMR49AkdUfe%2FY6MStrzZA9yJt7GVozRv1Zo0833SKTpiluKcQqirKgW%2BtTfw9slRqllxj7PSesCSDNpcodSYCRcO1jt%2Bnrz%2F7M0CZjR0V5SxF%2FYhw%2B5flf%2Bzh7O8A6fUOs8ezcLe3gaXVViD%2Bk8ioeD2CokY9rvFqviurgVrX1kZkb%2FoQnkpiXIEXr26lOXBT4PLbK56BWjyzsJ3eSVCJak0C8vfELnbSutEnBy7Xv3NyLJ64x%2FNdpt%2FEk1d%2B8uusl6xcFQK1PSJ0nSWPBChv0BgMT1vDU6wDA%2BeKyyPoQDH8oFcbzuEt%2FNJosHKmStlLixqzLILs0t8FGNxp%2FzHBht9jTmk%2F7pp3%2FnL%2BtcJssH7tr1HNy79BKSxTThLDxxCCfb4mhMojQv34xq9TE19m%2FE8BV9r02%2BSbNew3GdxY%2BjZzNFQRloY8%2BPlXpeAJFeB7T2flAG1%2BQcAPl1szdClQq37aceZitzEBzx%2Bju2TyEELzwV%2FpXGBTheLB9HQxduDdYmlADogxmfhiC2NSCsM5hHuOLNZYuMXTC02ChQkcwZRrfAnudnsceFooZU8KTtUHi4Qh4vllqssBa6oFatY%3D&csid=c971673e-22bc-47b9-9d3a-a0c4d26c7b81'
    res = request_s(url,cookie,0)
    code=res['code']
    if code=='1':
        msg(f"浇水成功，剩余水滴💧 {res['data']['left_water']}")
        if res['data']['left_water']>30:
            watering(cookie)
        else:
            msg("剩余水滴不足30，浇水结束\n")
    elif code=='107':
        msg('剩余水滴不足,跳过浇水\n')
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


# 咸鱼任务
def fish(cookie):
    msg('开始咸鱼任务')
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=wSndMnNDq25yX1%2BE1y%2FYHOjeyT%2BTfwjdpgI1dLe9E8qE%2FiVxK0YVi2FUTZtc4GZ2zOxpkk86%2Bmggh70Uv%2BrX43yWZ2LqRnhTn%2FXlNGZGv3V6Hi9tetNAfJUWFtaATGfwK4U7LLr1yGO8sETBKP0zgyY3zrQVG%2FML95m6%2BEXSj9jRSsTHJCzCY0r1vva6CgLlIjWTyYc9F4RP70zAgLDsKvF6MEcflVEo89NQmlO5O1HlWbnm5KeTMC50mBKmw1QlAbV47TudjgL%2BOacejRhpjZriVltUaYS6GfK5THhZBJJwIXh72d%2FmS89lvzY%2Fhiyp2Ki7U1QXR55w%2FBOeydPANUXTit15mD7IJ%2FzTY32y0bC%2FIoTtkZa9g1rJHvzvZS43qjK1Bo1phrYT05qts6%2F2DfEk3RwcRREanAwgcYH2yfCKXeeenSpUT5jIWrbK0e94cw276GGQ%2BJlwklM3OE6ushPQKVzTckjBMJaZ75J8U6iKtE6%2BL1s%2FQy2KjOCtfCA%2FhdW8PQ89fjE6jSx6cDlaMtryR2sNLF7V0e%2FXC0I1jk%2BP9xpUHXSQaC16JshA6qiac21j7XFQfZkhrgUEYUAN7NC7Dgro2fCtBrRDY2DYqJAuGxFcKeAnMrCVnXGrMlJS15JnxTbDQMfKgA4koocc9RdcNh2rseS4FgIRkjdw6LOGckxWioHa1O0B%2F8gHd6Ym9qhAIqELUzvvCmiZ9w9aAkue8p41LIkMjoQmqmdR550U4oROG1IfmKIk7t4PKiKnhske0rrMqjYvWumbp82GZPeaQydub%2FtZggi4vRzb4HRr7HAgAo8p870wo5mViXdXdYd93CbvdXe%2FrzDBTXt%2B8UtJSlHG3i6SbAzj7SNsFeCsu3ZIJ67ucz3a5dVsVtzqh2qDWjiJXVE9RYHEy7tFdQpbSf2HtTJNmZDGyGHHWA90Q5H8evSb65Z1oji6ceGMZ1V%2BLELEuEFYIM%2FVBr7%2BW%2Bxrb77vGWNTNql80MrTHLb9TszuFdlzyzqDHidMaqTaOWngLiArksaf%2FApE1pcwLOHTdXWcYyLnQX9Vyg%3D%3D&csid=a5530f5a-cbf2-4e45-b359-11b60b9ef368'
    res = request_s(url,cookie,0)
    # url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=3b%2BfKRvfKuSMY%2FZqD9%2BY5QlNLRzmBom8CQyRk6sTcG7zBtdrsyhwAMjSMG4zWW%2Bv3ebjhWlkJluLhgIHAaBn36G5H%2BuXWcMuEj8z5NPjEqgO5Okp5mSRSRrafvfbn2q%2FlD16jKy4LVsatkE1M5FNr%2BHzpjr32qML%2FP3LpSOfDBBMx8clXOavH%2B7Utci%2B%2FGEYxcKMpiuenJ4Q8WXeHp8wohh7UYRUdpaZMxjmzzn%2FRhJiTZZFpu7vvM6imd5SACDJtGpge4gr1fvvkIkkh8bTtPQ3KdedaS6GNVdSEJjabNllCq0EnIySE8nd17aju8j6uk8G8dwWBe%2FxDMaW%2BP%2FcaVsn49Z6BDRt%2BiQiJTmrOjt%2BEivKQ57O6SZpd1crpous55C9hKAP9kiISZsDfdVlBlO8ActMaXuyfq8zIEVmcR6qyY63VGTlDBHipTHFCTwQ%2FUKEpQqaIWP2uOb9IqRbvDtGfMofbe%2BnFAo4MLXdR%2BWbdQwYn%2Bd7c4p4FJTNQA018tg3kWXnkAGvyIKiiBxmDzpt4SuVJEydiFvuqRxQNCkuR7pptBZ4hAPr98UEiGba%2BLJK5QPIcfwuPDrJSuQCKGIwTCXlIy8ir15uAQJACOaYmKfpp7dQcoxo55BKc9%2BwHlpF3dy%2BLq2vy%2FWxnmt%2BsxEgANrllPw0CK%2Brr%2B4QI97f9OKStZyrStLYZHwESdcW6xB9Kbqh%2BfHtzcEVUX3cAYJ%2Bh1EIMaidjqeE8YRWE66ZSdNNXAqcoo02GzfyuVa%2FvoY%2FJDwxhjTJGilBkXc21%2BZJF8FG68OabN0CHElw879Sxesg1IrobdBENFW9SA9ixfzvFqZfmOdNyjvAHaqK41TkTaBOYyzczwp1HbbT%2Bs6RBFUwpubOkUOrn4Pld5P%2BvGN7zYw62KqLhz%2FvQMlvouR5djS%2BTdaCwDEvme8%2FKaavO2wyu3Unq3NBEGRa6LgvmhD90iedqK%2F2iDsnXGzE6HH2hwhg5fgW0gY6NbYe8BHrnjlPNSgIgeFz85WyTEFCLfG8ULlFTQTQuguEDpLaFA%3D%3D&csid=7001cafc-c36d-4b43-8ff5-7ac62ee56b21'
    # res = request_s(url,cookie)
    one_click_water(cookie)


# 忘了名字的一个任务
def anonymous(cookie):
    msg('开起新大陆？？？')
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=qttewDlIpmGHK%2BTvNpJUmXbVnZqdU8ClLRUBPBRJXprGMopAFXd%2FP%2B2fmWdUjJAq79XYtrmxukx8WbSLSF%2BwK6iXIzvHuOVeunwvSO9GCSE3KQNFAR4%2B%2Bb%2BqNZj%2BHXpI%2FFcL3hy0n9fdHVGXxw1Lz4uZeBvW2PdTQ591SgUO36x6CpWGJT0abX8fPNE0T%2FBPbOJ7Ryj3ZC28OpEX9hm1EclZQQoNEuH%2FuvzS3fuApBRaf%2FlYPhQ6CVxqHRRoWnK8vgonELb%2F8aCDufTGE%2B5KrGKZGDmQd2HFlMPFfxr9A%2BL5%2BcJy4%2Bng8ilK88tCmo16RBI5xgz8pJRna3xClVVio4QxKUPO9bJfoyp1qsM%2BWEV8%2Bbz7eHNmGS6GpTw63j%2BHj4y3pRmtz1SS3E7pf6RmzXVdf%2FEyDJeFxTjTHeFLOo6vSPX0uW8NXRjQ%2FY8H6tQMfKALY7LLMqwHKoGixkPIxMlEf1y4GAk8WcyuKShHOo4NEWHXBmTW48tohxvYye7g4Kt0JaMhlESC%2F5axPxZuiEid6H10oOqKmPETSL445R3oeyVfMjsVlvMosMiMUudP2duwVToxOyQGWIFWhH9ccAPOVzHtmAB68Tq95SF6TV3oV7KZCC1iMhVMClIUoBlZbTF%2BRxEG980Jx%2BryWCrK%2B%2F2XFaV36QRdLkydwcgVAu9ZEdwTX9QI5Y0isFt2N4WeALFkbjp0XUIjFO8j5fmyGKfTJYfjYA2lb%2FTYzyct7jCBs22tnOZmrGLQ14eD4fMwSBy%2F7stiqoqWGKTeO7Py7%2FQrOvbSQ2ecCLkPEjv%2FpftX7A9yKneFU%2FuSFxcZ2zoSlVxJJEuzpbRJZYwT3%2FFexb1mrb%2BXz5NQ59QLottjym1jczrWCTTFbWhOB2EyF%2B3YEcLCgnOxuYLAJqSkmZ0ZquuRy58s80L8M9kzi%2FhpH4mrLs6xEkGczSi73%2BM5%2F194QQTjAonehGV4uAo69hlcLs%2BhDIUYqAeym%2Bzc7Nv9NVy27MaHcI6SrfUPgMkJMAdygDPqTTT1Kr1U8lOirKlzmXhmPem5BADpfu%2F5A2RSdLvu2Ww9JVqmg991TZ4rpuP%2F&csid=39fa84ae-1162-455e-8afd-46a9041e881a'
    res = request_s(url,cookie,0)
    # url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=nFkyIAqF8cHefEc%2BV564nrIuLkJ%2Fspawt7lMhCzL7IyUp5caG16qqd32t1KJdFuc9oDkRKK5WWalFZR4MbHXpRyQn1dVqI9SGqlBOJF3Ti%2Fn0l7IH4zuz0AhNg5n3ME0Ii3fSPmM%2FM1F8lRqFoyE68bRRrO6R7MdQ0UU910gV2odpmsL7VvwzNwypM9ryoqIL%2FB6XUOYMBtezvwpPSNxKr3uxoA%2BZf0ZXiUnvHMwiVfUdDMLP3gR3kAjIGf45mHhfO1M8%2Fivho5SjZs0OG%2B9MJuwTV%2FulurBBcYMsumAqoJzsG4pybAJCGpt84LUfepbgyDftS2M8VGtg2YSAFDSbZ0Qph%2B0CZby6CUNjqi0clB%2B1PYiGR8NPJ8nTNhvZ%2FfOX9HmCdS1x1%2BQ0PetkE8uXkTVvIOIVCjLmrTGoLJvG59NEfqo5b116nzGKWqBexudiWxpWGJmvEadQiU%2FXj9QFqQp50WT0f7LqlfuQc8bpCU%2BtsSGcPGUlD3l0E8MTpVyKwjWk4rIahUN7tEhBsQeRP1uyd0EZuLme1kbeIG6yKOcSBwAar%2BHZ5D40ErZ19%2BpFUU6cJiwDAgcYR16yf4TmAkoeV%2BvK5MYaM%2B7Hj3jh0Yf5In04rrSRg6SMtYr4PyZi6DodJv3nbWP%2FQAg2xZgcGN%2FMFLYrmK16ds%2BfUMTHwbqdjRY2vJCLZf%2BxJ1jzSvX9DMPjw58dpqzbbvISGUEZwxTqnpaZ%2Fj12KknKQblYn4NON3slMirjiU8SimKL14tQgzl1h91LKgk5imkuSJqkJz8ZcvCEQudhaUCnhnzlw3JgewPh1x0J0HMl83Egyvrd6oClxIAQamNAtOgIaS0Zkzfqh6zcB3pyYUyOS83bdB0o4q0EWu95rKzyH0%2B8JECVV8v%2F7EgRZIWySOn9ZPqq3v5Ky52U6uKNAgCBzOLpJc%2FEABrIsW3vTOqf4xR%2B5LIdfnN0bheHW1w%2BmqH0SFiqeN05ZwgrQbh0rnsbNl4g4zDtq9PKAbbzKM4jCSIWYqJeART7PC%2BEUnobxO6Zi%2BgqvvHILU%3D&csid=b6e36910-3685-4481-8137-e9c4a1ca335b'
    # res = request_s(url,cookie)
    one_click_water(cookie)


# 首页进入小德果园
def front_page(cookie):
    msg('开始首页进入小德果园任务')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=hBL8qV3voRJ4OcDweRv4WLA4vrPxmrPvYHfOuc99eAajoWOIXMM4UuouWiKFa9o6Pa5E9zpVs2KhQ%2FXy19NiFQfGJ%2BiCHFwS%2BbU7E7cLe8yZzR%2BoxLH%2FneiWYBhduh2liVklLNItgXs%2FBg0JcMw7gPG4l2YZBnS9IsiWY90CRus87NJVfFtUON2Nh3%2FRIFV0Kfae8UX81SUIfq32HEyEZ846Ry6PSQXKJmGKo%2FArhZ086l9QkVSEcxUK2%2Fgmq5uZcuKJeFUD4UhLCC2lc7kl%2BXGITbcJEtJYEhDEdKF0FO9UFqHfVXeMrPyzRxQkRNnorNx%2FR%2F%2FsV1ucK9yRitQ0K7NY9PTuzYrmvgt7T%2B1rMEudtDcSkM5mE8XkYiMIfbT%2BeHXUNPeF5Qzpn%2Fp9DxP1i7An3Y36BR%2B2JipdgJbnR%2BZV7uOjPJmgE0HYtUNBPNmdE1JeWx%2B6iXd2iGOjI6QgOT5HI9HuuQM1aDXSV3JKn1Vg0VBN1uaVIunbssWSAiWIpAsC3D%2FK5bAM5yJu0EEVxiRdrdxC4HP1Jn3KVsYCVy8L58xsojJuqNNR4p%2FH17OUsYyUbL3X2M%2B%2BR1K8rvZ7qoYU98l1mewLhPBw2LIzc2G4apNe1MzPDnLpoA%2B7rBM%2FhnwylKb728Va41Ouc9f5nTxym8Mkj0ZDxQlGXCy24hKC86zQvCWj0uTFcEuBlPPrpEbe0z5NYyr7Aejq6zvoRACF1ey%2F0layWyL5CWwW8FWQeh1%2FjYG21BizeUGMEqDn1SaEG1996HnrgVtOXGkRHWtdTB0UkeA7fRChlazDF4IoXdbFk372Erzb9YGE1brGHRd15qLgAH0kXogBhXtVf3otH5OT1NSp6RdaIYbTuLmRGKwV%2BUpVlJmEZnzctj5WcInBz64%2B7QP9hYIJNkXB%2FLEFUpHH5spcBr3usT4agID7IrbSP0j%2BEyoXpG2IZMrNOEVBbD%2BFSREH1EkOqTIQiphUk1Rb3g71pu21PQlwQRy5M0wEAepxMdOjoGlX9AJyaVebhg%3D%3D&csid=6b2fc58b-7341-4e18-b1cd-bad78c2315ca'
    res = request_s(url,cookie,0)
    url='https://sync.amap.com/ws/sync?ent=2&csid=73ffba58-fac6-41ab-963e-611360cf7449'
    data='tO8YBKHYY/EyXL50ClbkE/3vmNVeifh+5Q+KcN0ao3adGkdqhJdWMwpvXeCHRpuSEM5D7BGmizQJ57Xm4XiZbJGpRnz4V8JKUtk8NE3phXQ81MZB/skrk8yqWzyEzZ6f8FAN6YwZnFizaG1fnfFM2tbHSFPvJwMIZyCWFRe/DYHXBYZANOjT7Y2GdmqrK9y3le4RMRzz1h3Fln4W/1QFSLXPBFDUpsODeYa33QkWlWfhDbtt9PAGtcmOANQzDbmlkJASaKsqkfSGs9RgKvxq9in1civnwDYfP8wkFGYJAxMLGJFEYS8DTWHHJxTtnsZ9n+CULA=='
    headers=headerss(cookie)  
    for n in range(3):
        a=0
        try:
            time.sleep(1)
            res = requests.get(url=url, headers=headers, data=data, timeout=2,verify=False).json()
            a=1
            break
        except:
            print('请求失败，正在重试🌍...')
    if a!=1:
        msg('❗任务失败...')
    one_click_water(cookie)


def pug_map(cookie):
    msg('开始 足迹地图...')
    url='https://sns.amap.com/ws/activity/xiaode_garden/index?ent=2&in=9txZCzOmhBVo7XO6%2BGZijRbncsa8lzfvYYEzYyZmjLyarWMsfv4vsSaw1%2Fka1ZZQjp3RB5W0fPAG9irCDqJFMDFe9TLg6gd2CbDdqym1pyiwvQZw9tDWd4onPQ49xUnB6ANwmX5YxUwFofmhYcO%2FcjluGK9N6PC%2FEo987drwthriFSnejaEWbNY%2FgwNm%2Bkdf%2FgBrN9aX8kW7nzFkGdo30mW%2BKKEX4yCnxco2Y%2FJydoDj8iRITVwo9%2F%2BKz1k0A9iK82j6aVRS%2Fa6Hyepk%2BV1VXzTcS9LpfjAVSWFRrpHJgs74wjtpZyt%2BmJLwDKLIeRpLA2IqgNSiLsCj5TYRXD3B9apwqlvyXK4vtXY8o5NX4jNc5jhGR8ot4U1QpuxLudNHXbb6WnWeepXWG0cyGhInv0EqiPwehs1RseHYR9txBulfd5er4EjdMLeqZO61jvAPg0UYKSX9t2xQoqyNLGhBuUL1jj9no6E6TfJoNGHkyeci64tLyKPkC7U7nTiXhex51o45r8%2BXTXBG8p2cbNrvpPb%2FOiy1XLGvlR5kIPaCYN%2FTaSxtjBeqpMAvrAAyJ2BRCPd88ODA2AtLTVVPLjQ97s9yuXYRAjkx7zK%2FB7lCMjCOxLq5tYIRBkpPFjR7vXQ3MDLjEXqwggd6Z9uOy3eJNE77EzWwltgZOy8Q%2Bm0o%2Bp6VhWtA6bfFtWsGjSibHRUYV3%2Bj1uXRIREtWywq85PxrOQKQb0egsVhXdgXzLtZk4VY2k%2BNvKsgK95OouInH7WOOtDb7Q2IskEykUh3oDxxZAlkuF7u4VpnAsO%2BdB9JbpxQwIvDiWrVLprEgXxHgSJj4%2FAAZh%2FHYbqpB%2FznoXcdEEXFMNzZWTd3L0psNlC%2Bw5RXGjv4ZfqJouCBz2Y50hpG%2F8IiX9E%2F%2FYxtDoOmClCrZP%2Fuw2rbXLM%2BwXdqTb0aM2iNHUXuCdizz1P74RnzDerbg0uz5VYVw8%2BK5fnCHY8oJFzGrOq7xLwB&csid=780c9740-182d-4947-a8d7-9e6580ce9e59'
    res = request_s(url,cookie,0)
    one_click_water(cookie)

def visit_hotel(cookie):
    msg('开始 逛酒店20s...')
    url='https://sns.amap.com/ws/activity/xiaode_garden/index?ent=2&in=0OzWVfNh8dvdr7Q73pekyF%2B4nbEjcEiVj05xCYWI1aHmx54hOppwBvDCNi2lFZkEwWudYM4ib2xRJ1EGPs7kumY7qFGNKM1mh8LU%2BvP11ozkyKouh%2BE5M23QtP4k14xForP4I%2BQCeV2YiExGZfcM42cWEFUcMpxbwJITd%2FGEMVx7KZFKiJG3NPcc7ItwxBzaOWQgmZSOsbTo4DqX1DUht2KZ7tOrXAHGfrqa9bMomkHnKAm75r2FTyVQ1T8gnlP1sCq4X%2FKYzNZwcnKye5H5PYh6o6TnnMtuWsA4TMknZUExhziISh1f%2Fl9l0WCTTSSXYAAeAMIo3XPOSZRUo%2FQGDEloSv4KbHEhyxpsboobT9BPv5zuOwvJr2QuoC%2Fw4s8j99JW41bvWoMCYe6Zb5FwL558ghYmjleEJe1UMXxGb7st4zmuK28uNKTSEslyQtXchmpbD%2B6O63bmI2413stg027Fe%2BT7mFfc8Hu7R2N3BSxVhwqL6z%2BwPyKuPx5E1IGmcuWBk%2BV8FmrQJw1PLuO7VqvllG9ks%2BBA%2FI6pkftbjNxocjEr5GAEb1YHFtZeKyw06kXew9UMdN9ici1zUWGu%2FnezY6Tsg0pRqtApVA77EnHGS6YndsnwsklQxON2I2DRyCHmcWyt2TSR%2BJwyvwfgnLy%2B3L095h7ooY%2FfeoMqGbjfjhDdvn5QA028ATanH91r4FSUQwjD8LPVzfYoG4FMaKtsZAOACPuJyRxpqG3exY%2F4br9%2BLemrr0ZAkHjNpDRPfU9Skcf9bxjP41daw%2BGO%2FUlgSv2vi2rOhd2BAuPJxGXi46mnmD9BsdDUrPijTfngRwhfytw301SQ6X6FbizL51pDw9SQwhbJI6mGMrcDCVIRgoPFVAss0nICDNHbCx0OGhaqfHOOjIoJvEAEenJmaiMi2tAc5k%2Fhu2VAdRQ7a%2B6KMIiv8XmBECwZI%2BcB5eMpAj0%2FBP8j9IPkfaWK2TWHyAUzHLobNJPi&csid=5c1b78b4-85a2-4418-ad2d-224d167c4572'
    res = request_s(url,cookie,0)
    time.sleep(10)
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=hEjmWMi6DxUFAqg4XLnOtBakbFc1skmo3wvrprfCygsY4Pl%2F3bq9I62%2FW03Juk%2BNlPRCH6hQBzNst9U%2FX3SA2Ip7muNqsNWkWv5Mo0jVWBsUa3dXuvh0MemPesfV%2F0wnWHWOiBsXIxqp2K2nVnxzn0Tm7riv03TCwOikd9bV3oZpMyC6OtKHjz7OZRvYy%2Fr%2BCoIKN%2FN5R%2Fke1i9yhRTXg%2FmWFMCtKtOzNvo6z1MWy3NEIVLzqRM9E%2B9OgeWXtBNgIlR5sZkUU72ODJCS1n6srZxASxR8%2FGDLLDQj18FnVH%2FE4YtxHlyh41tioOWgCczeJbeZRsnwC%2BZ%2BUDziGJsoDyvMoPzcmv%2FckqFSNXyKIBCIB2OySgTIU1IPlWp0%2BCsm0K4KMdfTSfuKaf4NcAteX%2FkZd%2BS7r2leumrw1D6fcc0MUa8l7FfZ1VtfeCJfaZagFRWzwLjgf6kCBZgZkRwFNhtkhFIYPLW4TJsB1P8KJXpqK8CUuai5b%2BDpqQn%2BCIbWQ7mvCvoEGYDHSqTJmj9tzWoCreoeJ6WhnInZIxBotzjjDKR6m6XdVwhLTYRgDgEPoMDp0Q%2BIZc%2F7tl36aDneXbJ7Q1NIlFeSjKbbsfNtWRhtUnNP8H9m4FR9bkmYAK2ISqkYvo3qkCpQMs34Dpc990uxI69HZoMTfyGJlBCCqkxVCY%2Bk8J4MRF44i33MKUNEe%2B%2BFJgHi6zXZ810w6KpbBlUIzmi8xwtcHgZhkFMlDWpzylfidSPi3w85B3bmbsauoQatbfsMxCvffMViyU4JePEfqIdg9z5xRY9wiJRH0TtexF87pDrpd8Bb%2FS2BZoo7TmZLp9FAw%2Fa5KiYIIHaVw%2FXtK%2FEoVo%2F8TVjD%2BN12fybPpm1F2%2B5sk16H0QFQ%2B%2FMqX7DLbjgUPbWDebmGt%2Bbk2zr1NKoFu0yBQsfHj24%2FIqw7OjoZ%2BAEBnzuTSvFjVAKzauITxh7Hx7fE17JgKC5MV968D5I7ZRPWkjRby%2FBYjD1WWO7RXHOGE73lFZqYZQGFk7a1%2Bi7J%2BV1m3jU6F2e2FJpmm8%2Bbp%2BlUdajzA8RGxkw%3D&csid=117b4487-4f12-4b9b-9b9e-d974bc8d321d'
    res = request_s(url,cookie,0)
    time.sleep(10)
    one_click_water(cookie)


def scan_nearby(cookie):
    msg('开始 浏览附近30s...')
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=ewnKrVyktRixw%2FsbE25IFTTaKm4GkWRmwIjfk9zDnB2kIYwUcefZR%2B5PLNs8NVtO2vBT5IhG4gMDGf83EhAd4P5p%2F%2FAhLlCPYY8rXspmzJEeZDyu9QlGXv8d%2FS6cJm%2B%2BDR8XelGuQ5TcYw%2BMGJ2r8v2C0i1gwH4qKGJQEWiwCjcGRh0qcRKvcaRRWF%2FhEIGAXCW2EJSGTi7mKksVCYjrXe5vEO%2BQ5YY8E8lCIc5yR0kTmfGDIBTw7Op4hVQMxsdUr11D9ErRzlfYzKQw7hnGWZQ0P%2B0Pwb1t7fMQSdctgwQQx6%2FETrXy6oirVSQIIZllbwkQNCPFNuK%2BRPiy0yeyQ07vTqANvL7exKbVOBlk72RekueNrwTe85xQuAfCtzf%2BqZl1OYIp0dxWiXPuQ9UTjeTuiOUXqU%2BTsBwLjQnuHTtPPm%2Fnfgb1Sv4lGO%2BLbKVMTsCCeEe2ZtqnhN0y6rQZ3gzsI%2BCXEnqE%2FTsPFGW886CClsb3DKF%2BCr3e7kl04OrUerrpbcGUwki2FbHN6Ifi%2BMERGyfuTJe9gCv%2B9B2UdCbgZIjVmwrOr4WZXWW1X6%2B5yOJs2m%2BmPHDEDnNu9Vu%2ByD%2FZQ6960%2FdRHCqXmt0htnFHi0j0L%2F18L3YuYGBfwWGennQuczl6XTC%2BVbF%2BlNdmTADLEx1x8mvzL%2F3NLvNKJPXPOzZm9AT%2FZBqXv3GXSsDvHO1ql0qPdK%2B2IPWCiOnuWvzK%2BP0XOS2Cb8YV30MrQzLIekcSk5eQTDRgccktlMOTvXA6BxqgiDk7esfoPL33ntXfTdEkWQT%2F1LROy35MhwsrLAYvmsROzIiBa26H069VuvEF4PeRBrW06cVkGl3LuksX59cFFaHZzy2LyY6WRw4gzxP4rKe%2B1zH3ictdW1wEcYyXcfbMQPU1FDB8ScQi%2B35SIFUWI9KlTAilpegzIlYrWhe8PoI8GYQ2qkwpFfWbwB9eVqP8PXW6v4b6fDp%2FG5X4rICzfC1gzp%2BZF8wGgvSN5HdrhY7nrcyGLlDdDJe6&csid=8b98f0e8-3a98-4a67-ac66-d878c405ed82'
    res = request_s(url,cookie,0)
    time.sleep(10)
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=3qCZUzNLLNbkL2SxAOaXVr5sbKYWgd%2F8b0n62YkftzXgx5NJ2y5azu0%2BkzeUhAP6v1sTOGtamyWUlgeLcP9GRPyJZPl6tgwI2BTX7QdguS0juSLqm%2FNd%2FEN%2BXdVXH69kFMGhzgI%2F%2BMItyyCz%2Fmxhsy6BtqsH1gBU1SKbedwZaOQXib6HTTM8ux42j092BLeScnVx3vR5p4MKJwa9CWaG7jEkpate1u9D5Z%2Fnbet84qwqcxFhqR2mGrnHfSpunQu%2BaCFocuyJgecNT5pQNBKOEVfnB0B5UBboAvd7qPKFcmC5pBfmg%2BKggBH4L39XiXoyV07oaQq5XenRNI7St6tha4caisoOgKxZYKjY1WugLog8faYz1nW5KBSD7Lyi6Ud1ETbmkxqFf9P%2BBAqrngULFlOqcHdTuYlbcMQfu0WG4Nej6MpSTD5laAm3yId76av7ejyouQE0mpVd6OP6VfhhJBICseRgxlNcb%2BHuKpKNY5AltpBYrPucbd5SFHIxqQ2cFqz5jyFqcop908v33elvyXkXKV5ObEztU6CMiWYVX7EP1LoUG6iV4jXouExvY83T%2B9u09yC8eeXyQOgCtye62WBq9S3Cm8oMEJ1xzqZkZ903a%2FbSXIpGEXbkbfubzMmppsSwvsU8hlAGcVrlOfyPem505cyYlyrp57cecwb236pSU%2B7rALaqgtZGKgWdEVNroK5iov1bPQ0ek0QtNKU5pH5%2FBXGp55fMgY%2BBtIZjI2ekSDbYbqSOHwNpJJL1aNR9qDRCFgL0MELckcmpGS9rmKkgu0PJG3AQpNezh4rquZb8LuQi4a9UNpXPHxrseYdJW2iz0TFKphrRoBA3e0rlgux3qKeVxs6KeREU%2FlIlMnrRrexWfKt7rs3WZcSKjuJqz3a3oHGtg2D%2F2TmbtoR6WbkKDNmo0iuNpdu39U%2Bdq%2FaCm2gkPhl6uiqXnX448W7vS3nAHpDOgg7k8%2FfpxwZ4XI5%2BxN5z%2F9OwOjjNmISI5bC%2BgEe99vFnokkEWVJyMTXhwlwZxLg7p7s%3D&csid=055d8a7b-92df-44ab-97e5-eb81b95654df'
    res = request_s(url,cookie,0)
    time.sleep(10)
    url='https://sns.amap.com/ws/activity/xiaode_garden/index?ent=2&in=ab7Pei1CpP5ppbbm5WrnODNUQRCtR%2BWArM%2FUHShuPs1k%2FnP2In5wSK0kDlBNGQZoKo5epcT5A7NYX4ZaH6coxkhHGDmoH4PtN7fXuf9mzyttwoPgSOzTJdb3AqS45CKM%2BipsJTqc5q2KVXUKWggoW3zjxYebx8tQTZ4QHeC12aFupQuwsfTg2E8AJ27KhkSrzY%2BH4KuEY7xqGWyzbYw8U2L%2FoghVgKqrG6aPICOKCk6W372MDBwiZcCRg5SUvx9XG0XzFtdVlNiw8A%2FttIAEQXSLvga7%2FHh52T8%2FM0SLM8qVbxYqr770YmeIFjEFx5dMToUJP7s5rdB%2FR%2Bneb9Pxl%2Fusl%2FW%2FaJuUNDAqd6Ahg6LRAspoKK1P5I6eD44iAHQUueq%2Br0cu6otICHjefIC9CYCqR3oYdwRhnykP0zMfXWbjY85ENbqzMR4PLXUEX%2BALj4RQlz2OI20%2F0J770Lfx3qkBk0C3sEITZyETtm7SDTTGqXFH3uXX4OldrIhQefdV%2Fgy5RKUgrUeWJCzxD4xPzApFnUI49RGbywhAJz86W1BYN9ZK4RDdWapwShndQv1H6kKjyd3fz037v6frUrWg1pnno0u4ONVYBt6vEtPOKlHHWqmWHcxBREdNu6wiL3cjoecdS8nk8ZL3DTSNVA3vkYjkFz5vBVGdS59D7cC3TTATw526mUusMksxZ%2FFsAIrKNZq8Hjn7T7HiGI900XkJ14RC5Hn%2FGkcvKeJT3hGzfWUYkbTRpuhWrkmWVabZ%2F1Xq8m4koIzBG80RultotpzhaDymvOZW%2BCnv7A%2FBRrFQXoDkzppr5pvY%2FSUY1xPU6PpscGMR0awcLS358H%2FL2NiIa1Zx8KsCfgkkvD5%2BCtWY830tGjRd3cf2rSLwhdIT%2BxJ9CmmWgV9ms%2FcBUD1siN6QiqFdPdiOLjhtCifxl3G7w87cSKM0PtTmrVxgHgn7bFXGCIlPvnlB9QIpsG9i7BXIXxqyolnrudplTZqVwQ%3D%3D&csid=f1c5d6a0-e399-4da2-95bd-39f49206663b'
    res = request_s(url,cookie,0)
    time.sleep(10)    
    one_click_water(cookie)


def share(cookie):
    msg('开始 分享领水滴')
    url='https://sns.amap.com/ws/activity/basic/task_center/report?ent=2&in=tdPzrcm0%2BPKDTpWZ8qQxHyIKGOdNSQ83oWGM9lPkqFnKJL94Qit7ESAS25CfNY7sakMEVipGQNUwB3YENUzrbd65pJm1f57EwXsWKcce5GTZLBw8co2SUVLAeoPa4lFA66xdJvlp%2BhWKRGCn6ai452VK8690EZHcOvPygWL9qK2RFWcDJkNHY7by%2F7yGsfhoLRj%2BmNUcaHpO3RPkoYa58Sm1x1mmOF53BRTqfyXmdto9fxLTpAFYGih8R5fWuJEtT6BPi2hwYb%2F6ZIRTi2tBw7liVk2iyTNMeSN7KlbNXXmLBZ84MVdK1dKzYBMAe3F5twOC2eiORCR4pliGcqATMmhxldBeAdL4tRE8xKpKOmbUDYxvYiVg1E2EYTOvjnUbxRhDMjwDipSlQukJw%2FBuXovIsXyOibwAFwD1E3jmAUqL6feCAttCFXlEpUQXbvLgupDUOP7FY6eunB5BPvUAOMtxsQywko%2FsYV%2B%2FCoFGGOzGtHluSG2%2FNKyG35buz3wdxYVK7PG22yujsmZr6ORoQ2tNWhT0kuDRCCQZIqFdOtJ6bGCZTqyrr20S3FxFnKPUOtcNsDSzPUqKraBv%2FFF%2FVbtB%2FJbasFlOCjSloTQOqLLQI6F9oC6KKgp%2Fr1RAiEmrZF6Y%2BY5Xniw6OUmGFJyXS1UW6Mu9L%2Fa7fEAmD%2B7nE68Z%2BB%2F69bwV1Hu6TTcfOSzuNfBXN%2FwRJmCbEpTpKcozp8AvFbu8g0onTXMFyD26UnaWxCljHsK9rt9QLGNyL2nFQWz97LX17fDVIb4V0PjS%2Bxv0QlXlirFxwSiBf6ssj1bVpEDd20noIuQji6asz%2FyuFXicfJ%2Fe%2B9QW0IJjWO%2F4FG64M5Omf1mqutUJMV8bQT8ZZQP3s2wG4uR88Q5hHaiRrq6VkamRGQ1HUaboVTSnypqOKabDksctRR451wVCNPfcuX6pj4yblVxfgcNbMWZ2%2FJasEPO%2FtsL1N14mC9O%2FoNDumC%2BKgek54fXMhuj7kbqMsYQGOjBDNtIaxDvZfWgIhmkQ7KId%2B55Wil%2FdW5kf9%2BAl7EvHnb8l70ItKg%3D%3D&csid=35b1e04f-f0ad-4c1d-9ce1-56e859929abb'
    res = request_s(url,cookie,0)
    url='https://sns.amap.com/ws/oss/maplayer/list?ent=2&in=1HB8qvijDs9XJ1dY55PqD284tijMwLxBqAvNa6FALwhB%2B0%2Bvdx9VQFzA9GnrmZ6YiZ9b1tQ2WD%2F5rjmTmjm87RCWPwma%2BfItXS5bX8LDbENakjStZ1dD4jwCTxX9K%2FnxqpBMeyBNGqqhWDZisH%2Fh1CBTuFwVGuvGfpl9s4Sp7PuHayZahlLMGD5UP6C7bdZiR%2F1dRBHAEn6cS6lE2dXrjAhTAAjzXZRgnpizxU6NobnBXow88DfmpPhqig9BmAniN%2FBdWWPfnYWzTJ119zkR%2BNDUeNJU1j9E1BFFIsRyViEm7fRiS0HpFMbrEMglpgwXg3mQuB9%2BtyrfPlWhXsYCCjaAxjB9Suu1Ws%2FOJvfXas93l8TArLkkvS9DPGnpCB6N3vOgR93YOWdJIA38c%2B6wTqTn8pxCBzGXr0gNmEWLfR00LuGQ%2BJDm69WPdUW3a%2FykOu76jqKawQoojsrt0cTELVHGG9kpVnbZ8oyUraECMrcGdDq57Y2Pzh3VSFVvEaFvOhTUCT0tKTEO0azP%2FfniYD0CCr9AEsqHX7eEyMY3P%2FUlCpHkR2Dcbj%2Bx5iTzGcAUaS9O%2BmSQsn1ge5TJUyRIsSbz4WmvzZbvRuQF6IvdxAUPOjt1SoXYqgGcsv0jFtllPHYlR1beXeZxmYCbrKKrkXJ6xqnHDQkYVgd%2BhieqItqva5uhXR9OKcbcu8SkoqRjbtsRS%2BylxKvIqBm5qYWH%2BQ7%2FkD97fA4HE9AdkJtbKtDeJAO9JCu6SPJNysqkD8oW3UbCnL3HNGTiLxi81SR0NF8ykRkAS%2F8CydfvZdGXEMJaq%2FGTymjTbfyH%2F8xAuUF%2BolHnPfacG%2BurvdVmf4zXCo0%2FEm3eunKBwAwmVYqeIoOMRyWRPU0VKbDZwayKE8ufRwu5q16hQ810X%2F3fuAS8r0oOW7Rw%2BaiZwBwz2rnpvKVmzrRAnQsVmNhP3CVFItKDzS%2Bnbm%2Ba7%2B1Dmglj%2BOiBDtowRsTJhUuGjtF2ZfSDS0Q%3D&csid=23784e17-60fc-4cf4-bb61-549905c03334'
    res = request_s(url,cookie,0)
    url='https://sns.amap.com/ws/activity/xiaode_garden/index?ent=2&in=%2FFFIh5ndsRQTiafAAN8jRpquEmp%2FDhTHd20iCq2h4xBsTUQEakoVgX2Lxltqa9A27ZvUesFLgauiMbokbPmXtg0Way6aMmXqwj%2FOErP%2BKttpb72CI0VMZM8eDlHqBkvo7FY3YuzJKCuiU8sMir6zO7%2FrP7yG23%2Fs0Y78W2UslnXqvGzcNNCYnzVpnY0BkewdV5iELThVt%2F%2BKCnuwaKZuMiptiNnzhwHfjL2KV8nMP0xqQVPaf31O6V%2FI41vJyFjLSh2Lgcy8r7HcboQzYB9KHlCveMSb1itvcIUzjBwcyIG5HxhPNQWwKsGaJrOGSa7Py51s4q8Cd5DtvcvkKMgaViP%2FVHp4KKVOzFMvywR9zSewbtRIX%2FSp9YuOWqYLHQ8r9%2FUOMsFjWBVxJwEUBCj5HG6wBACHG%2FUdJfdln22G%2BC%2Faa5R8x%2B2CLmaxOSnxUl0eknv6u%2Bf5rO9EpseuOLXj1MTP8bOHlIjeV%2F6EC%2BvQAr%2BqTKuuXBEtsCuj7801kWFwqAbAd%2F7kGrA9oywSEnlXCK%2FC3Sy2hVdk%2BRxbdoKzY0pkaNLLO8Rv3iniiSbiQg2SjU1HbV72vfIK9NqLJ5lgxvA4JQfZ8R%2Fsdom2xMtOVt%2BOCWWppH76BucKmLQ4pT%2Fs5inkHsts9B4Q9C8QNUVQQ9MnsO%2Fdv2ClCGKSvemUzVF15YY5k6YXCdYXqER8VBnnFAT6p4xdOngAuAOZ0JtPoJVhiZQ9uooef7zFCkmeZqyduxfiTCH%2BaBtEXQeSOGizxEHfGcUYIuUbIxZDj2MzWOCKwNmaij51aFRNkA5bXtG%2BpLbtdpda6N5vux0XBRWKY837dQj8JpPNOewnDcH1jJmDIwWTbBuCUmmFuObkFgQgyc0jX%2BsiVCzxfWCLFTdjJ5UQd7PU9xalITM7OUZMrTQZyFTw8XhqOU%2FXatfWUAwaTHFeLJ1BX22YRxdB4MtR%2F4VKSnExMj%2BIwTR9E6odCmzjXE6f64kT%2F6KsplWeRjBQ8SjeHWPLSA%3D%3D&csid=929588f0-98ae-4d0e-9ec2-71777eed1775'
    res = request_s(url,cookie,0)   
    one_click_water(cookie)    


def add_uptask(cookie):
    msg('累计完成3次任务领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=ssrVTNTtGEJnJGJARRXPVqmXUkPqsEI2j67JTqKSzcfZsSDTPDBWQG6Vpvo2O0f3O5MCYmWS%2BFG9AK6fcXvT5iHoslqDEgEWggKy%2FhxqFHG9VJnKLslBkOU48hLMfXSb0pSpRSw8JZfkZzt0EGBpJd6Wy5lRnP%2FQUN5Aeyxmc9OCvRRuZKRdCKZlD31s2ar12zlxJU%2BojH63tVHqFiQxv2PdgcSxq26%2BQxuACEefaa1FuqxwTluGKoNAhWY%2BKQ%2BemFB%2B9mUYOWfVae3B3I766TOYA6Xpeo92YgZwjXhUL7HD4hf0CkCUbE02q72wg%2FZVQMePWhXi6xe4XPA2bWlyLYX1dvIfzqj95RBTySpydA15%2Bvc%2BEbCVgT%2F8CuxtNLwu9CQkiaokQhIdla1BSlnXoVnwn8BaNIXZbDaX7VuifHaJrRbxcuYa6W8VL6nqKh35KtvkPw1mWclya3JVSOBCpnX4msHfXleBdgWZe5XChb7NMYQgg%2BT1Fwje14okldF6fZtYcl%2BrPY%2FA6kOBTQ%2FYBpadHFphpIom5OXyL2IhTvxTGTPUyZFhQZfvU6gkpZgA8GwkN%2BAwqzDdgK4qr6IuxMZ0tj0hudEdZur5njOmuDmaKtd29hAdrd8%2Bs9GJTERI0o%2FEldaSB%2Fts8SwDe0amzxZPjijNV3rNOdtBzxZfbfViQNFbGaz0udxWktGzCi24iOppZUIe7OVTltEAePWWOUioYOlFp46%2FLtQpkWwWQsSeGwe3DjO%2BYrpYS8NSV5k7Sx6T%2FRgOQBYmYNAX0AXaAwC1Q81Ba3vliuDsFMQPjFM2XUO5XlXG43jQOfHNc7qFERlEPekfTOPQZ8QOHkpozYpN8xCRD5ybujhQg2wY%2F0ppsqLvIJ6JAEquwiA354kmQBlutq149q%2BdxeagvQgjgdQ3kDwRk9iqwZ3Z2YzSRO5H%2F%2BufzYosz5OGvk%2BxG3tTnpC1YYPVt%2FDMOoVANtoIZzn1kcRGpnRhKFkfIQ%3D%3D&csid=29e839de-be53-4ebf-bec6-6fc3bcebb1af'
    res = request_s(url,cookie)
    msg('累计完成7次任务领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=NPiUf37K9Z%2FW%2BtTRotG3s6TjwT91dS6vw4MAsA9qY1ffPiOmEqzpaw%2Fre83OPEjHlMcRWy4PIzHYOWtmFNo8jzPz91hzSCb0xg4Dqqt5KdbG9gfDptf9EM%2BHCDDeG74nvJPplAmYGvPPY5gQg0n7k52XXGzP%2BGMVMP6bXxBXax2FL0TnFomcZmP8qI5EHTDM%2FwEWtolLQTmZN0IlEg3A0TC29zsbGuzLI4WXOzgoi6yvpiJLqjxdJf8Zte4g1gwqaZ5zhLRbeByzQbAdZCxt0SeNEUlR4vR%2BMO0dghr91TvEcn1JDki4XnyrFsIgFXtpQeF4NrxKrGU7zkThrk6rQC5iibk2vOEI5XutD03FFT54IPWy4yBYX%2F61Wr9lSkiFYmEYuEHwPjkeOaftOOP3Obky%2BlYvCIXmF7cszmPLBPDU5uHVLzIiILr4eh5OKX%2BIndIEZsfbep%2FLn8ciZlrzVe9lsXWJwwcPE8RZuAoGqbOEvVJx%2B1cqbG01ONX7XC8utiwhEuLF8JJyXmv%2BKhNAe5ybnwKT7u09vvI6f50jt%2FyWQDeY0zw4c%2FWcR6zCID2lJ8MAVf8Ew0BzVhPNtnDEX%2BVRYxyzriP9%2BnUVJa5LyZLJnnn3e7RsCYBik%2BJ6%2FmLeczIKNwMrgBxZi1BB4j0wptg8wzkMCeK%2Bb7QsM9%2FM6a22cpvy04CI062ZILMP6rwUol5Z12W1i4xjPwMxNQL4lEnHhjg2dumDc25unxtyWOX5PWLwzaB3TpgiLjKWygDOUHWbcP3ATm%2BWXvyv%2FaEbrvjDowPJNkGMrisAlLJJ4rIi5Lr2HjcYi5mV7JlAT3D%2BZ829HnjIIqRa6eyI8ljuXZR6s3fJmCBeeQyiD42s4G9eiaVTul38roEvvzGjHNy%2BgWbcDUvvxvPYFhxqDXcDxQ7a2pKi6pBLLgBxD9oqce2x2VVbPDABKC0eG23%2FPzloKLc2cLTnjE06EXvgyXTvq5YxUdFhHuPjamNYskfmZkUfyup%2FhE4FETM4tM9V5CHc&csid=87f938b3-b3cd-4dc4-b279-e0b02f8c2f9e'
    res = request_s(url,cookie)  
    one_click_water(cookie) 


def one_click_water(cookie):
    # msg('一键领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_batch_reward?ent=2&in=mZjHCmSauK2hCMxfcYCvIiiWiC%2BhyqSdoQU3Jj%2BV4h1U9ydh6uC%2F4fRNhlMIwxpAMuJs4jrzvkXzjgPA5Ov6g%2FC0sPfnaiythSyh%2B6annrXR%2FNeAMuPFXy8yrO1v0DghlyhbsiXxYplsRCu7hYWIkpjcbCggcvskk%2FpleL7FhcznTdrnpZ0Y2O5HhnRelkw2JUbhSjlHKsNwT%2FaxqzZtNSo6PqU%2Fj2R0EZWJTzni8jMN1l1lfilTiFLmg0Mvkx9gBeonZ0y%2BkWXjr1ClaPoRDpCeBh3xhWGF70HPEpey5NwtYr%2FDRrqNDTCQq1ia5SMWMe7QRwMjX8O3NoN09OKkRzzBrmaZbhJXe6Tc%2F%2BKDO5IpH%2FW3gryeAE%2Bf%2FKbbHIX6fKKt7a31AMfJQOYyeILb3g8ARszRSduHMoedxGauWA7Js2EepvLHsSRM1zfDGnF%2Fe2nKY5o2m7IrN5b%2B6GHTrsIgFOcc%2Fkt6ms6DNdinevX2JzpLMOM04aCzOfe3zqccAVG3U18ora6REsHLJ8iurKq3BbrVBM3pDo7DmSt19pd296NSmAahV%2Fli4Y7UsenpQhBAbuor14PqjiZ8057hnsA0NWyLv5IC5%2Bh4sAaBy8ERKrcf8KZ4pjZBk6DNrOoDDTttHunqPlfe2ublbOlb72ynE3jiO2gQT5RiazlNdet5h3gDqKa6CmnZNsPpFzUgbDXae1ozlfLpcCqLDbROyZh7t5UnV3Ous3wt5I4eVbP6wTKMpc%2BKETdhseb35R04ey2CJ3XxuVolU1mLnNmvxMpHLRQAQC9CtIaUfTpi%2FOdotyQYlFTaMXvE%2FLpbQI6USVNPNZc3b2H9Noy5oNss97jgZBLD7stwtoFGkEbwEcPC%2BhJVHD%2FwvhtJBZcvhjF%2B3aEaBe5bVGZyasJQ0PkbyyMUJmuVCO%2F5DZmnyZSgP1AGi9QVt0V7YHYLbkKK4fI3ZV27BE7xnCcRuKrAroZEPRMo160guBi7&csid=9eebeb6f-1855-499c-aa80-c22e50baa628'
    res = request_s(url,cookie)


# 热门活动领水滴
def hotDoing(cookie):
    msg('开始热门活动领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=ZmMrPwrxz0vBdqlRUi9tqfIg8ZOUChXs07wTrtEzJW9YrtO0FGjs%2FPf2n8%2BaXWxAhdpq0pfGQBdIjeMKDmtwn2BNZevgzIcR29g0wJoFLxlqYzDqe%2B%2F7d9tp0hAeEATfG312HBG9YJ1nE8V1gg%2FOXMb11CngLSgLby%2FPkFNDAFRwfyWkJXnCQM%2Fty8wJXmqlikA03zDKoH1oRfWM16ExLs%2BTBmFajrBhvmoUs40hTd0fox2eUXmEffsiM1tcBZfmLpMq9RQ1UmFc%2FMbAASZmu%2Fe2vfP46JKYV4tvjORnRn6oRUVhTtfKeMrQRzXYJy%2F753c1t%2FQT2yNTI3IJBHWQRVdMsDkb9etIhtjGi8SqgClKcdNqUa41OYzE5TyTEnDmKpM1noMW%2BPFoVHVosSfKkimX0OZEqyaKoFqAzr7LGxM8dsk0Uy5jk9FW%2BId9ZTRr0XAVZdDyunCo%2F%2FgLgTB%2BgVGmlezGo3b2cwOjCP%2BeSjecDqqXvYEPI%2F6zTLZJ0uRle2JEXgB7a1iGSJPAKKHwMLo1tdoGkKuDmlPP%2FJ3GL1mx%2BlXXWie8lfGp47JOG5G9jRKGdUuftlhT5%2BJezz39GQVOLf4fbtAcK%2FGPCNGYU6vj7LILOO%2FWt16QeJpasT9r6O4iQRYQ4iw4GLy34TvM1toskUC8Bej9jDc%2B82CUadB73rjmw%2FE3Wq4O6LI%2F4xABCmFq6Gs6R6%2FXkqU3Xt4HZ0MUM0QNu90ZYN6ruEjygIMvRQetFPmKU%2BU1DFY7tYMqQrMWx%2B%2FAcUimKryeUc5RdOXfIKweYSo%2BnL6tMYeVxLFE5fnZmVrrcUz%2BuDddA%2B2A%2FbZ484lTOk8bJA2jCugNxUO4W1RkMWX1GEgEVt%2B2fOVyvAfR4GSiJqC8bF%2BjbHLHbrvmRZIGBMEKvky2Mp4USsUC1VkeA5oiDOWpZ7hADg0Fh5NPcnSNzXgRDvNsqa3Iw4KY0IZGqGZ5HmfbQ8zvIzqgSj%2BVFyQHZYFlU27dYR3uyXcPUbn5MD6aszS2mIJcKwAyJk7sdmGNVkTqZFb4a2m%2FEIc%3D&csid=c05640c3-e554-4a09-b0a7-f7f6d559e9cf'
    res = request_s(url,cookie)


# 一日三餐领水滴
def threeWater(cookie):
    msg('开始一日三餐领水滴')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=RVBgMC3rDAa%2B6rKrqxx3mPMSgMilMHIQKu5zhIwvqo28R3TDPFE8QGO9AS9ZO4lOinpol5USg%2FpjTLDTDYk7fbuFVZgMUfB%2BM8yBZffQPeg4EnBJnVa7AD4kMs7%2B5PEMfRWzL7uTY0S%2B8ZYFubEkDX%2FxkxTY2SakfJy2PMMMdr%2F3JH3ZNy09Xrk9UuYUhfr30AgB%2B8eRv80KkH1qiMp8E6RkGCsr0w7v6rrkGdjZJerR%2BgjN3UNIKj3ZXUQegOX7FUURkapkHuKo%2Bcma693CzUmtci%2FqE1GdgLhNftISsBBIhW%2F720x%2Bi3mSwG2Ze4IlERzfHqUE1w2YPQ2iYhRNftCx2FLTRszkMJ1K%2BHi1pUNioSYIAHNDtRt4EAwsEe37vas2jRcWyGopDgh8qnvzrK%2FfRjSXtA6KlsN%2BgKmcIMeOVPL5gE7KhrTPBOv06OTNwJ%2BZ0R4BaVmvALTZPKTCVBY875o2GUhRXE4BK5aB%2BunGx7dSe0imCjv%2FWFAVLI3aUZaKhGdqS%2FrxCf6jpCK4byqgCaVRRyTFYNJmxbEJwsZtGRx1FXgPVAXBEkZlmwuMw7JO7i5oY1CgFXzeZEr%2BtxXhgkIGysqlnlZEND8sjMWg%2BQcKSfuk4H7Ugic1%2BiG9onKWzuAbBgeuaGfK4sDvcyoivLZsux6%2Bu8DGC1TdIPlr8Zqgf0dD%2B9ypZwMbzRPBzZH0m9HvdDXQzfx5AOgljulAdvijo68xURHVtCKAP%2Fqg3dJjlGcIb6jH8yOu4MuuPMMk%2FY%2FppmqKTHUcSQqt4aQpWZ7s24YlfcaZmJcPal%2FUJpR5OstOTXABM%2FcYLqssN3CgrmywMKv6Nd%2FA6yg%2F6L7lOSlf7qZ5slWLKjvooLAlmhqyAPKV7h6UqchlVFEd04cEjOPPZ6B%2BklTM3PKtNBMLUgMWTRCHVUqDQ9iTC27wdRmmn8bhoQnX%2BzY4gL7WL6j%2Bo6OW22BOYhlPEQV7%2FKpE52VTcSvxcQEaAbZXYQVkYHOgKTQdxIpGgmxgKgS1gYcOKBR3Ee5kpTsx&csid=880aa606-c566-4871-a5c4-bbc520c6616b'
    res = request_s(url,cookie)

# 签到
def keepSign(cookie):
    msg('开始签到')
    url='https://sns.amap.com/ws/activity/xiaode_garden/task_rewards?ent=2&in=bdEfO5l9%2B1IceQTpZXkY83y3PGoGZIw%2BftEv3p6yVrYRwtu%2FOjHK7GuvVSkeGwPWEIYs%2F34WiMUMSt2UPjmm07LzSWpbx%2FosUNaRrkXuk1Dagl9a2CtNfiv5B9dxfj0phhz7dJBf6BnCloWnuAuMUCdz5JmkJ4yn%2BxilINb5lYXExsmsKr1ADVtPp%2FXjOK1FoUcQw0D%2FSM%2B1t0FuhM%2BPjPUQB4OodPtns3nZN2cvPIe7UcfwOW4%2FNGf7ES50z13Bm%2BGFFuSKYZXR2bOMUtBaZq51yjvUFSu3OSItQKf6GKnC6TxO9pUrHf5e03JQ4UWIa9lFi9z8hwWcyDCAqEYJu5UEqAJGajcwx6LyzWlRsevNlySBqiuDck3cqXaYQTsyRFxwOqjkvt1RmWVKfoOroaDLieh1b%2FkeIKjknvy%2BCC3DFuHOe0U9EapCFWWpOpCybmXL%2Fey%2FE5WJbWP8jvgwKYidEHTZssaZQxxi59RV%2BuBX9otM5yfxuhu3TxAGfQBnvZBEbene4EfOGKVmqcQ%2F2wtSkdBgzv1hzT4gHRaWlt8ddcRNgVSt49gbMB2K4P7z9XK9mvzKyjQldaJYmGX%2BnUcgB1D5KThTb%2BTdzFlR7JQ%2F0Ew69h%2BTOcNagw4dMp%2BKQVLkaQ1Q5ke%2FtMN7D6CcTGLzc0WbUljj10q5P2pTBkBDvHGy1t%2Bs9IpJbuuOQIJa0VnD%2BmrSacX3ABfFV0cyUM7r19Ij%2BDcFx6OmrivkGH9EYWUrB6ducrL42svivJXA1%2Fhx18OSWX1Mac7NH8GChCE2XkV4nQ5hr9876xXntBqfiZPkPL7OW3Lohc8t6FUV3lIXrflRHOyrouL6Uy2DisQCNutzbDgZsP3G3WldJAsJkYYevXRb7QS2PlfONCznG2nqGU2qyInIDJkhpT9aZt5wYHn8WTYjjdJyQXsulhA1cHTYan2o%2FbOSxxN%2FPH2VsH3J%2BfEES3asqLVCnRaFOXF%2B8HRDVP1fura9cCvC9ON3R%2Buncux4eML%2BRaF5fjICMz0nEMzaVNzr9U6%2Fpdgd9cir3OM%3D&csid=820e3549-594f-4923-8949-ac416eec4618'
    res = request_s(url,cookie)


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
    pug_map(cookie)
    visit_hotel(cookie)
    scan_nearby(cookie)
    share(cookie)
    add_uptask(cookie)
    watering(cookie)
    msg('一键领水滴')
    one_click_water(cookie)
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
    msg('🔔小德果园，开始！\n')
    ua=ua_random()
    cookie_list=Judge_env().main_run()
    msg(f'====================共{len(cookie_list)}高德地图个账号Cookie=========\n')
    for e,cookie in enumerate(cookie_list,start=1):
        msg(f'******开始【账号 {e}】 做任务*********\n')
        doTask(cookie)
    send('### 小德果园 ###', msg_info)   # 启用通知服务

