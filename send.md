### 通知环境变量
在脚本内或环境变量中填写，如果是脚本内，需要去掉export 后填写                         
#### 1. Server酱
https://sct.ftqq.com    
填写 SCHKEY 值或 SendKey 值     
export SCKEY=""    

#### 2. BARK
bark服务,自行搜索                                 
export BARK=""                    

#### 3. Telegram            
填写自己申请@BotFather的Token，如10xxx4:AAFcqxxxxgER5uw         
export TG_BOT_TOKEN=""          
填写 @getuseridbot 中获取到的纯数字ID           
export TG_USER_ID=""        
Telegram 代理IP（选填）     
填写代理IP地址，代理类型为 http，比如您代理是 http://127.0.0.1:1080，则填写 "127.0.0.1"     
如需使用，请自行解除下一行的注释        
export TG_PROXY_IP=""     
Telegram 代理端口（选填）       
填写代理端口号，代理类型为 http，比如您代理是 http://127.0.0.1:1080，则填写 "1080"      
如需使用，请自行解除下一行的注释        
export TG_PROXY_PORT=""     
Telegram 代理的认证参数（选填）     
export TG_PROXY_AUTH=""
Telegram api自建反向代理地址（选填）        
教程：https://www.hostloc.com/thread-805441-1-1.html        
如反向代理地址 http://aaa.bbb.ccc 则填写 aaa.bbb.ccc        
如需使用，请赋值代理地址链接，并自行解除下一行的注释        
export TG_API_HOST=""       

#### 4. 钉钉 
官方文档：https://developers.dingtalk.com/document/app/custom-robot-access      
填写token后面的内容，只需 https://oapi.dingtalk.com/robot/send?access_token=XXX 等于=符号后面的XXX即可      
export DD_BOT_TOKEN=""      
export DD_BOT_SECRET=""     

#### 5. qq机器人·   
qq机器人的QQ_SKEY                    
export QQ_SKEY=""                
qq机器人的QQ_MODE                    
export QQ_MODE=""                                  

#### 6. 企业微信应用消息推送的值，文档：https://work.weixin.qq.com/api/doc/90000/90135/90236         
依次填上corpid的值,corpsecret的值,touser的值,agentid,media_id的值，注意用,号隔开，例如："wwcff56746d9adwers,B-791548lnzXBE6_BWfxdf3kSTMJr9vFEPKAbh6WERQ,mingcheng,1000001,2COXgjH2UIfERF2zxrtUOKgQ9XklUqMdGSWLBoW_lSDAdafat"                       
export QYWX_AM=""              

#### 7. Push Plus
官方文档：http://www.pushplus.plus/                                    
PUSH_PLUS_TOKEN：微信扫码登录后一对一推送或一对多推送下面的token(您的Token)，不提供PUSH_PLUS_USER则默认为一对一推送                                           
PUSH_PLUS_USER： 一对多推送的“群组编码”（一对多推送下面->您的群组(如无则新建)->群组编码，如果您是创建群组人。也需点击“查看二维码”扫描绑定，否则不能接受群组消息推送）                          
let PUSH_PLUS_TOKEN = '';                              
let PUSH_PLUS_USER = '';                               
let PUSH_PLUS_TOKEN_hxtrip = '';                       
let PUSH_PLUS_USER_hxtrip = '';                                   
           
