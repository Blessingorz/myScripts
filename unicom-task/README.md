### unicom      
在以下仓库的基础上稍作调整 ，感谢两位大佬                                                                 
[srcrs/unicom-task](https://github.com/srcrs/unicom-task)                        
[rhming/UnicomDailyTask](https://github.com/rhming/UnicomDailyTask)                     
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
天天抽红包                      
年终亿元回馈活动                
转盘抽奖                           
沃阅读                      
钉钉、Tg、push+,微信等推送运行结果                                     

### 环境变量
#### 填写
详细变量请查看脚本内说明             
           
```
export unicom_config_1="手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫<<<手机的imei（可留空）"
export unicom_config_2="手机号2<<<服务密码2<<<appId2<<<抽奖次数(0-30)中奖几率渺茫<<<手机的imei（可留空）"
export unicom_config_3="自然数顺序类推..."
export unicom_womail_1="沃邮箱登陆Url1<<<手机号1(可留空)<<<沃邮箱密码（可留空）"
export unicom_womail_2="沃邮箱登陆Url2<<<手机号2(可留空)<<<沃邮箱密码（可留空）"
export unicom_womail_3="自然数顺序类推..."
export PUSH_PLUS_TOKEN="微信推送Plus+(通知服务示例，可留空或不填)"
```         

appId：手机文件夹 unicom 里的appid文件，以文本格式打开                      
imei: 设备ID(通常是获取手机的imei) 联通判断是否登录多台设备 不能多台设备同时登录 填写常用的设备ID
沃邮箱登陆Url： 微信公众号联通沃邮箱 https://nyan.mail.wo.cn/cn/sign/index/index?mobile 开头的 URL    
                     
### 通知推送
[点我查看](https://github.com/wuye999/myScripts/blob/main/send.md)          
### 使用方法     
### docker                  
为解决依赖问题，更新docker使用方式          
```
docker run -dit \
  -v /unicom-task/config:/root/config \
  -v /unicom-task/log:/root/log \
  -v /unicom-task/unicom-task:/root/unicom-task \
  --name unicom-task \
  --restart always \
  wuye9999/unicom-task
```  
在  /unicom-task/config/config.sh里填写环境变量：               
```
export unicom_config_1="手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫<<<手机的imei（可留空）"
export unicom_config_2="手机号2<<<服务密码2<<<appId2<<<抽奖次数(0-30)中奖几率渺茫<<<手机的imei（可留空）"
export unicom_config_3="自然数顺序类推..."
export unicom_womail_1="沃邮箱登陆Url1<<<手机号1(可留空)<<<沃邮箱密码（可留空）"
export unicom_womail_2="沃邮箱登陆Url2<<<手机号2(可留空)<<<沃邮箱密码（可留空）"
export unicom_womail_3="自然数顺序类推..."
export PUSH_PLUS_TOKEN="微信推送Plus+(通知服务示例，可留空或不填)"
```         
[通知推送点我查看](https://github.com/wuye999/myScripts/blob/main/send.md)                  

每天6:15自动更新脚本                        
每天6:35, 18:35 自动运行任务                            
### 青龙
    
联通日常任务 青龙拉取命令                                            
```
cron: 28 20 * * *               
ql repo https://ghproxy.com/https://github.com/wuye999/myScripts.git "unicom_index" "" "unicom-task"                                        
```
青龙需要安装的依赖：PyExecJS, pycryptodomex, pytz, requests, rsa                    
安装方法：pip3 install xxx                  
搞不定，不会安装依赖的同学，**手动下载**一次 文件夹 tenscf_rely 放入 /ql/scripts/unicom-task或/ql/scripts/wuye999_myScripts/unicom-task                                        
**手动下载和青龙拉取的文件夹tenscf_rely文件夹是不一样的**                                 
青龙最新版是放入/ql/scripts/wuye999_myScripts/unicom-task                                                
没更新的是放入/ql/scripts/unicom-task                                          
![image](https://user-images.githubusercontent.com/79479594/144328277-b7547b28-0e6d-4058-81bc-e4d0234c2f72.png)                                
                        
### 云函数               
不再支持                                


