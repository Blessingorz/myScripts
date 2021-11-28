### unicom      
在[原仓库](https://github.com/srcrs/unicom-task)的基础上稍作调整更新                                                   
本仓库脚本只是因为兴趣学习而而写的，如果您使用了，则代表您认可了脚本有可能带来的风险，本人概不负责                                       
如果你想搬运脚本，请不要修改任何内容，本人很怕麻烦         
### 功能
详细介绍请查看脚本内说明        
沃之树领流量、浇水(12M日流量)       
每日签到(1积分+翻倍4积分+第七天1G流量日包)       
天天抽奖，每天三次免费机会(随机奖励)       
游戏中心每日打卡(连续打卡，积分递增至最高7，第七天1G流量日包)       
每日领取100定向积分       
积分抽奖，每天最多抽30次(中奖几率渺茫)       
冬奥积分活动(第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底)        
获取每日1G流量日包(截止日期暂时不知道)         
沃邮箱签到，连续签到可获得话费奖励（需绑定沃邮箱公众号）,完成任务得积分          
天天领现打卡
年终亿元回馈活动
转盘抽奖            
钉钉、Tg、push+,微信等推送运行结果                    

### 环境变量
#### 填写
详细变量请查看脚本内说明             
           
```
export unicom_config_1="手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫"
export unicom_config_2="手机号2<<<服务密码2<<<appId2<<<抽奖次数(0-30)中奖几率渺茫"
export unicom_config_3="自然数顺序类推..."
export unicom_womail_1="<<<沃邮箱登陆Url1<<<手机号1(可留空)<<<沃邮箱密码（可留空）"
export unicom_womail_2="<<<沃邮箱登陆Url2<<<手机号2(可留空)<<<沃邮箱密码（可留空）"
export unicom_womail_3="自然数顺序类推..."
export PUSH_PLUS_TOKEN="微信推送Plus+(通知服务示例，可留空或不填)"
```
#### 获取变量         
appId：手机文件夹 unicom 里的appid文件，以文本格式打开              
沃邮箱登陆Url： 微信公众号联通沃邮箱 https://nyan.mail.wo.cn/cn/sign/index/index?mobile 开头的 URL                         
### 通知推送
[点我查看](https://github.com/wuye999/myScripts/blob/main/send.md)          
### 使用方法            
### 青龙
    
联通日常任务 青龙拉取命令                                            
```
cron: 28 20 * * *               
ql repo https://ghproxy.com/https://github.com/wuye999/myScripts.git "unicom_index" "" "unicom-task"                                        
```
                        
### 云函数               
##### 压缩
将 tenscf_rely文件夹，unicom_index.py文件， task文件夹 压缩成zip         


![image](https://user-images.githubusercontent.com/79479594/143088148-aa05ef3b-fb25-431d-ba85-6a39858e43ec.png)                              
[自定义创建函数](https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default&createType=empty)               
##### 基础配置                             
```
函数类型： 事件函数
运行环境: python3.6 
```
![image](https://user-images.githubusercontent.com/79479594/143089468-58791b20-24cb-4359-ba64-d8284311bade.png)                                

##### 函数代码
```
提交方法: 本地上传zip包                              
执行方法：unicom_index.main_handler                         
```
上传你的zip包      


![image](https://user-images.githubusercontent.com/79479594/143089499-7872bc8f-4f4b-4544-913b-58633d0984a6.png)                                

                        
##### 高级配置                             
```
执行超时时间:900                       
环境变量示例，[具体点击查看](https://github.com/wuye999/myScripts/blob/f829758de2dd1c7e1d90e25462785d6713d59d63/unicom-task/README.md#L22):                            
key填       unicom_config_1                 
value填     手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫          
```
key和value不用加引号，多账号则unicom_config_2，unicom_config_3，自然数顺序类推                            


![image](https://user-images.githubusercontent.com/79479594/143090708-655fe96a-bb47-4a6c-a581-7ef03d3eb545.png)
                     

##### 触发器配置                            
```
触发方式: 定时触发                       
触发周期: 自定义触发周期                               
Cron表达式: 6 6,16 * * *                       
```
![image](https://user-images.githubusercontent.com/79479594/143089660-1ebd7de8-d3a9-4fd5-9027-6c64cb089bc3.png)         



点击 完成                            


