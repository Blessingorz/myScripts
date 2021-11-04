### 京东 
京东类型脚本       
### 脚本
详细介绍请查看脚本内说明    
```
9 9 * * * jd_sign_miandan.py            # 签到免单  
17 */6 * * * jd_wabao.py                # 京东极速版发财挖宝
17 */6 * * * jd_xdz.py                  # 星店长 
58 59 * * * * jd_jxcfd_cash111.py       # 京喜财富岛抢111红包
0,1 0,1 * * * jd_angryKoi.py            # 愤怒的锦鲤修复
17 */6 * * * jd_ghwzjd.py               # 逛好物，赚京豆
17 15 * * * jd_jxnnfls.py               # 京喜 牛牛福利社
```
### 环境变量
#### 填写
详细变量请查看脚本内说明      
环境变量JD_COOKIE，多账号用&分割       
```
export JD_COOKIE="你的cookie1&你的cookie2"    
```
#### 获取京东cookie
自行解决    
### 通知推送
[点我查看](https://github.com/wuye999/myScripts/blob/main/send.md)



