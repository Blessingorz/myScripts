### tg相关脚本   
青龙获取登录凭证：    
```
docker exec -it qinglong bash                # 进入容器    
cd /ql/scripts                               # 必须进入这个目录    
python3 /ql/scripts/xxxxxx.py             # 脚本在哪儿，就怎么写    
```
出现 Please enter your phone (or bot token） 的时候输入手机号获取验证码，【验证码在tg内查看！】 例如： +86188788878888         
接着输入验证码     
登录完成会生成一个凭证 anon.session ,这个凭证必须在/ql/scripts，因为青龙运行脚本默认这个目录，不然读不到登录凭证。      
如果你是其他环境，也是类似的操作。    
接下来可以添加定时了。需要科学上网。
### 脚本
```
* * * * * tg_send_messages.py               # tg定时发送消息
```
### 环境变量
详细变量脚本内有说明  
#### 填写
```
export tg_api_id="12345"    
export tg_api_hash="0123456789abcdef0123456789abcdef"  
```   
#### 获取api_id
申请api_id、api_hash： [点我申请](https://my.telegram.org/auth?to=apps)       
不懂如何申请的自行谷歌        
### 多账户
如需要使用多账户，则复制多个脚本，在每个脚本内部填写各自的变量                   
然后修改修改脚本内凭证名称，各个账号的凭证名称不相同即可，例如：                    
![image](https://user-images.githubusercontent.com/79479594/138139994-9ecb633e-4236-4190-98e8-4561cc9f7abb.png)
接着依次运行每个账号脚本，登录获取凭证             
例如3个账号都获取完成后的凭证：        
![image](https://user-images.githubusercontent.com/79479594/138140771-ed4be9b5-8e22-4b4e-add5-6f9e42e076d3.png)
然后分别添加定时即可        

