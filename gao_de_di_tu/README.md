### 小德果园    
入口>高德地图   
脚本功能为自动浇水，签到等等功能，还在完善   
### 脚本
```
36 */8 * * * xiaode_orchard.py    # 签到，浏览，做任务，浇水等等
7 6-22/1 * * * three_meals.py   # 一日三餐打卡领水滴

```
### 环境变量
#### 填写
环境变量wy_xdgy，多账号用&分割   
```
export wy_xdgy="你的cookie1&你的cookie2"    
```
#### 获取高德地图cookie
打开高德地图，打开小黄鸟，开启抓包进入小德果园
随便点点
搜索'sns.amap.com',复制cookie,填入环境变量中   
### 小黄鸟
HttpCanary ：[点我](https://www.sogou.com/web?ie=UTF-8&query=%E5%B0%8F%E9%BB%84%E9%B8%9F)
### 通知推送
[点我查看](https://github.com/wuye999/myScripts/blob/main/send.md)
