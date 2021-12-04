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
### 青龙
    
联通日常任务 青龙拉取命令                                            
```
cron: 28 20 * * *               
ql repo https://ghproxy.com/https://github.com/wuye999/myScripts.git "unicom_index" "" "unicom-task"                                        
```

搞不定，不会安装依赖的同学，**手动下载**一次 文件夹 tenscf_rely 放入 /ql/scripts/unicom-task或/ql/scripts/wuye999_myScripts/unicom-task                        
**手动下载和青龙拉取的文件夹tenscf_rely文件夹是不一样的**                       
青龙最新版是/ql/scripts/wuye999_myScripts/unicom-task                             
没更新的是/ql/scripts/unicom-task                       
**需要删除安装失败的依赖**，大部分依赖安装失败都是没升级pip,建议老实升级pip后安装依赖，免得出现各种莫名其妙的问题                                 
升级pip: pip3 install --upgrade pip             
安装依赖：pip3 install xxx              
![image](https://user-images.githubusercontent.com/79479594/144328277-b7547b28-0e6d-4058-81bc-e4d0234c2f72.png)                                
                        
### 云函数               
##### 压缩
将 tenscf_rely文件夹，utils文件夹， task文件夹， unicom_index.py文件， 压缩成zip         


![image](https://user-images.githubusercontent.com/79479594/144328517-c3e6392f-56a0-4ff4-9116-883ca2d9c405.png)                                           
                             
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
```                       
环境变量示例:               
     
     
|  key  |   value    |    
|  ----  | ----  |
|  unicom_config_1  | 手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫<<<手机的imei（可留空） |               
|  unicom_womail_1  | 沃邮箱登陆Url1<<<沃邮箱对应手机号(可留空)<<<沃邮箱密码（可留空） |   
|  PUSH_PLUS_TOKEN  | 微信推送Plus+(通知服务示例，可留空或不填)  |       


appId：手机文件夹 unicom 里的appid文件，以文本格式打开                          
imei: 设备ID(通常是获取手机的imei) 联通判断是否登录多台设备 不能多台设备同时登录 填写常用的设备ID                               
沃邮箱登陆Url： 微信公众号联通沃邮箱 https://nyan.mail.wo.cn/cn/sign/index/index?mobile 开头的 URL              

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


