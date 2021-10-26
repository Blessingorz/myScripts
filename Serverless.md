### 云函数使用
#### 创建自定义云函数
[创建自定义云函数](https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default&functionName=helloworld-1621082690&createType=empty)              
名称随意，地区随意       
运行环境： python3.6       
提交方法： 在线编辑        
执行方法： index.main_handler        
![image](https://user-images.githubusercontent.com/79479594/137999218-9978d63e-2d98-4dd7-8aaa-8636837fc0a4.png)
然后复制Serverless.py中所有代码            
填入index.py        
[点我查看Serverless.py](https://github.com/wuye999/myScripts/blob/main/Serverless.py)           
![image](https://user-images.githubusercontent.com/79479594/137999805-84d2c251-3e80-46be-92e1-97870b027e88.png)
#### 环境变量
点击高级配置，将执行时间改成900         
![image](https://user-images.githubusercontent.com/79479594/138000046-57536607-7dd8-4303-aa14-46ec9954d7b1.png)
填写环境变量script_add ，script_update                   
script_add一定要加https://ghproxy.com/                     
```
| key               | value                                 | 说明              
| script_add        | https://ghproxy.com/https://raw.githubusercontent.com/xxx/xxx.py   | 需要运行的脚本地址，仅支持我的库的一部分脚本      |           
| script_update     | no                                    | 每次运行时是否强制更新脚本，yes或no,不填则为no    |          
```
![image](https://user-images.githubusercontent.com/79479594/138000369-5280b3b7-6a3d-4459-9c0b-8ec0a24581d6.png)         
接着填写你需要运行的xxx.py脚本所需要的环境变量          
例如你需要运行的脚本的环境变量为          
```
export womail_account="88488848@wo.cn"          
```
则改为         
```
| key               | value            |        
| womail_account    | 88488848@wo.cn   |        
```
不需要再加双引号        
[点我查看推送通知变量](https://github.com/wuye999/myScripts/blob/main/send.md)            
#### 定时     
点击触发器配置，        
创建触发器：自定义创建       
触发方式：定时触发       
触发周期：自定义触发周期          
Cron表达式：你需要什么时间运行         
例如每天8：30运行，Cron表达式：30 8 * * *           
![image](https://user-images.githubusercontent.com/79479594/138001054-03099538-177c-472a-bb38-f5cd2e510e6d.png)           
点击完成即可          












