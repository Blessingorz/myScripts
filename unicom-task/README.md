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
钉钉、Tg、push+,微信等推送运行结果                    

### 环境变量
#### 填写
详细变量请查看脚本内说明             
           
```
export unicom_config_1="手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫<<<沃邮箱登陆Url1（可留空）<<<沃邮箱密码（可留空）"
export unicom_config_2="手机号2<<<服务密码2<<<appId2<<<抽奖次数(0-30)中奖几率渺茫<<<沃邮箱登陆Url2（可留空）<<<沃邮箱密码（可留空）"  
export unicom_config_3="自然数顺序类推..."
```
#### 获取变量         
appId：手机文件夹 unicom 里的appid文件，以文本格式打开              
沃邮箱登陆Url： 微信公众号联通沃邮箱 https://nyan.mail.wo.cn/cn/sign/index/index?mobile 开头的 URL                         
### 通知推送
[点我查看](https://github.com/wuye999/myScripts/blob/main/send.md)          
### 使用方法            
#### 青龙等    
将文件unicom_index.py和文件夹task 放入/ql/scripts 里                        
![image](https://user-images.githubusercontent.com/79479594/142781422-9a616278-1b32-4a42-ac52-9615c047e6f4.png)                                
添加定时                             
![image](https://user-images.githubusercontent.com/79479594/142781440-8f795296-e1a7-44b6-a4ae-f22505b33065.png)                     

#### 云函数               
函数类型:事件函数                        
运行环境:python3.6                   
提交方法：本地上传zip包                    
执行方法：unicom_index.main_handler              
自行把将文件unicom_index.py和文件夹task压缩成zip上传                  
![image](https://user-images.githubusercontent.com/79479594/142782021-79a1719c-e45f-473d-a51b-d83d846a6d40.png)                     

![image](https://user-images.githubusercontent.com/79479594/142781789-503e6713-6448-4139-ad67-a9a466f38e53.png)                   

高级配置
执行超时时间：900
环境变量：key填unicom_config_1  ,value填 手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫<<<沃邮箱登陆Url1（可留空）<<<沃邮箱密码（可留空），不用加引号                      
或者填在脚本内直接压缩上传                    
![image](https://user-images.githubusercontent.com/79479594/142781853-1c07d670-4cd5-467a-8a39-39efadc7df07.png)                   

触发器配置                 
触发方式:定时触发                        
触发周期：自定义                 
Cron表达式：5 6,16 * * *
然后点完成                 
![image](https://user-images.githubusercontent.com/79479594/142781995-566bcae2-30f7-4714-ada1-e16ab2e232a9.png)                                  



