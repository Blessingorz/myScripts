### 美团
此脚本只是搬运修改，方便青龙，v4，云函数等使用        
此脚本只是搬运修改，方便青龙，v4，云函数等使用        
请支持脚本作者：https://github.com/fuguiKz/meituan-shenquan             
请支持脚本作者：https://github.com/fuguiKz/meituan-shenquan         
美团token获取教程：https://github.com/fuguiKz/meituan-shenquan             
变量解释：https://github.com/fuguiKz/meituan-shenquan                  
### 脚本
详细介绍请查看脚本内说明              
```
0 11,14,17,21,0,1,2,3 * * * meituanshenquan.py   # 美团 
```

### 腾讯云函数
据说美团限制了云函数ip，不知真假                            
[查看腾讯云函数方法](https://github.com/wuye999/myScripts/blob/main/Serverless.md)


### 环境变量
#### 填写
脚本内或环境变量填写        
填了环境变量就不用填脚本内的，都填了则优先使用环境变量         
脚本内填写请去掉export          
```
export meituan_token=""     # 美团token       
export meituan_wm_latitude=""       # 去除小数点的纬度(如30657401)
export meituan_wm_longitude=""      # 去除小数点的经度(如104065827)
export meituan_propId=""        # 所需要兑换道具的propId(推荐填写5)
export meituan_exchangeCoinNumber=""        # propId对应某类必中符所需的豆子数量(推荐填写1800)   
```
#### 通知推送
在原脚本的基础上支持了多种推送方式         
[点我查看推送服务填写](https://github.com/wuye999/myScripts/blob/main/send.md) 
#### 获取tokon
[美团token获取教程](https://github.com/fuguiKz/meituan-shenquan)          
         

