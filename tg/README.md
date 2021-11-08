### **脚本 tg_toolbox.py** 
青龙获取登录凭证：         
先填写变量tg_api_id，tg_api_hash，然后         
```
docker exec -it qinglong bash             # 进入容器    
cd /ql/scripts                            # 必须进入这个目录    
python3 /ql/scripts/xxxxxx.py             # 脚本在哪儿，就怎么写    
```
出现 Please enter your phone (or bot token） 的时候输入手机号获取验证码，【验证码在tg内查看！】 例如： +86188788878888         
接着输入验证码     
登录完成会生成一个凭证 anon.session ,这个凭证必须在/ql/scripts，因为青龙运行脚本默认这个目录，不然读不到登录凭证。      
如果你是其他环境，也是类似的操作。    
接下来可以添加定时了。需要科学上网。
### 脚本
```
* * * * * tg_toolbox.py               # tg工具箱                    
```
### 变量
脚本内填写或者环境变量填写，环境变量优先  
脚本内填写则不需要export ，环境变量则是export xxx="xxx"
必须变量 api_id，api_hash [点我申请](https://my.telegram.org/auth?to=apps)         
必填变量        
```
export tg_api_id="12345"    
export tg_api_hash="0123456789abcdef0123456789abcdef"  
```
以下为选填变量         
代理          
```
tg_proxy_type="http"                           # socks4 或 socks5 或 http 不填则为不用代理
tg_proxy_add="1.15.14.11"                      # 代理ip
tg_proxy_port="7778"                           # 代理端口
tg_proxy_auth="代理账户<<<代理密码"              # 有就写，没有就留空 ""
```
发送消息        
```
tg_send_messages_1="@某群<<<长大了就不要笑得那么开心"
tg_send_messages_2="@某机器人<<</help"
tg_send_messages_n="@某用户<<<需要发送的消息"    #按自然数顺序填写，最多999条
```  
发送语音消息        
```
tg_send_voice_1="@某群<<<http://xxxx/1.mp3"
tg_send_voice_2="@某机器人<<</ql/config/本地目录/1.mp3"
tg_send_voice_n="@某用户<<<语音文件地址"         #按自然数顺序填写，最多999条
```
发送文件
```
tg_send_file_1="@某频道<<</ql/config/xxx.txt<<<文件备注"        # 文件备注可以不写,例如："@某频道<<<https://xxxxx/xxx.txt"
tg_send_file_2="@xiao_bot<<<https://docs.xtaolabs.com/_static/xtaothon.png<<<这是你要的文件"
tg_send_file_n="@某用户<<<文件地址<<<文件备注"   #按自然数顺序填写，最多999条 
```
下载一个 用户/频道/机器人 最近10条消息里的第一个文件        
```
tg_download_media_1="@xiao_bot<<</ql/config"
tg_download_media_2="@iKuuuu_VPN<<</ql/scripts"
tg_download_media_n="@某人<<<文件保存地址"       #按自然数顺序填写，最多999条 
```
没啥用的监控    
**启用监控后，只运行监控内容**                
**两种监控内容只能启用其中一种**            
**只能监控一个目标，目标可以是聊天群，用户，机器人，频道**          
```
tg_monitor="no"                                          # 是否启用监控 yes 或 no，不填则为no
tg_stop="18"                                             # 启用监控后，如果 18 分钟后收到消息，则结束脚本，不填则永不结束，除非杀进程        
tg_download_media_1="@iKuuuu_VPN<<</ql/config"           # 监控内容：监控iKuuuu_VPN频道，如果该频道有人发文件了，则保存到"/ql/config" 
tg_forward_messages_1="@转发目标<<<@iKuuuu_VPN<<<色图"    # 监控内容：监控iKuuuu_VPN频道，如果该频道有人发带关键字'色图'的东西，则转发给转发目标
```
#### 获取api_id
申请api_id、api_hash： [点我申请](https://my.telegram.org/auth?to=apps)                          
不懂如何申请的自行谷歌        
### 示例        
如果要发送消息，则变量这么填          
![image](https://user-images.githubusercontent.com/79479594/138205703-e79dd0da-8e2d-43d2-a214-68cf20b3bad7.png)                
                
即发送消息，又发送文件，则：              
![image](https://user-images.githubusercontent.com/79479594/138205878-78534481-7759-499c-af07-3103c217607f.png)                 
发语音也是差不多的填法，多任务也是差不多的填法           
下载你和目标最近10条消息里的第一个文件文件               
![image](https://user-images.githubusercontent.com/79479594/138205942-a4e66257-a360-4115-bf38-580c0debf5db.png)               
        
监控频道，把带关键字的消息转发到我的收藏夹                   
运行120分钟以后，一旦监听到消息，就算不带关键字，也会结束脚本         
![image](https://user-images.githubusercontent.com/79479594/138206171-9944c605-1b4d-4525-9606-09234ae960bf.png)                           
监控频道，把文件下载到本地           
运行120分钟以后，一旦监听到消息，就算不是文件，也会结束脚本          
![image](https://user-images.githubusercontent.com/79479594/138206240-e203f933-1dd6-4b63-afea-54995b960dce.png)                           
使用socks5代理        
![image](https://user-images.githubusercontent.com/79479594/138214888-5b461f88-d6d8-4be4-9927-5a260c848e43.png)           
![image](https://user-images.githubusercontent.com/79479594/138215012-ccc21ac5-7f74-4513-959a-311a220beb77.png)                      

### 多账户
如需要使用多账户，则复制多个脚本，在每个脚本内部填写各自的变量                   
然后修改修改脚本内凭证名称，各个账号的凭证名称不相同即可，例如：                    
![image](https://user-images.githubusercontent.com/79479594/138206696-8d9855bc-08ea-498d-97a4-b07aa7412a11.png)                           
接着依次运行每个账号脚本，登录获取凭证             
例如3个账号都获取完成后的凭证：        
![image](https://user-images.githubusercontent.com/79479594/138140771-ed4be9b5-8e22-4b4e-add5-6f9e42e076d3.png)         
然后分别添加定时即可        

