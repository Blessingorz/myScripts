### tg相关脚本   
详细变量脚本内有说明 
首先需要获取登录凭证：    
```
docker exec -it qinglong bash # 进入容器    
cd /ql/scripts # 必须进入这个目录    
python3 /ql/scripts/detg_code.py # 脚本在哪儿，就怎么写    
Please enter your phone (or bot token）# 这个时候输入手机号获取验证码，【验证码在tg内查看！】 例如： +86188788878888    
#接着输入验证码  
```
登录完成会生成一个凭证 anon.session ,这个凭证必须在/ql/scripts，因为青龙运行脚本默认这个目录，不然读不到登录凭证。      
如果你是其他环境，也是类似的操作。    
接下来可以添加定时了。需要科学上网。      
### 环境变量
#### 填写
```
export tg_api_id="12345"    
export tg_api_hash="0123456789abcdef0123456789abcdef"  
```
#### 获取api_id
申请api_id、api_hash： [点我申请](https://my.telegram.org/auth?to=apps)       
不懂如何申请的自行谷歌     

