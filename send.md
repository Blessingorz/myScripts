##### 通知环境变量
##### 在脚本内或环境变量中填写，如果是脚本内，需要去掉export 后填写   


#### 通知环境变量
#### 1. Server酱
#### https://sct.ftqq.com
#### 下方填写 SCHKEY 值或 SendKey 值
export PUSH_KEY=""              


#### 2. BARK
#### 下方填写app提供的设备码，例如：https://api.day.app/123 那么此处的设备码就是123
export BARK_PUSH=""             
#### 下方填写推送声音设置，例如choo，具体值请在bark-推送铃声-查看所有铃声
export BARK_SOUND=""                
#### 下方填写推送消息分组，默认为"QingLong"
export BARK_GROUP="QingLong"                                                    


#### 3. Telegram 
#### 下方填写自己申请@BotFather的Token，如10xxx4:AAFcqxxxxgER5uw
export TG_BOT_TOKEN=""                                                 
#### 下方填写 @getuseridbot 中获取到的纯数字ID
export TG_USER_ID=""                                            
#### Telegram 代理IP（选填）
#### 下方填写代理IP地址，代理类型为 http，比如您代理是 http://127.0.0.1:1080，则填写 "127.0.0.1"
#### 如需使用，请自行解除下一行的注释
export TG_PROXY_HOST=""                                                             
#### Telegram 代理端口（选填）
#### 下方填写代理端口号，代理类型为 http，比如您代理是 http://127.0.0.1:1080，则填写 "1080"
#### 如需使用，请自行解除下一行的注释
export TG_PROXY_PORT=""                                                 
#### Telegram 代理的认证参数（选填）
export TG_PROXY_AUTH=""                                                             
#### Telegram api自建反向代理地址（选填）
#### 教程：https://www.hostloc.com/thread-805441-1-1.html
#### 如反向代理地址 http://aaa.bbb.ccc 则填写 aaa.bbb.ccc
#### 如需使用，请赋值代理地址链接，并自行解除下一行的注释
export TG_API_HOST=""                                                           


#### 4. 钉钉 
#### 官方文档：https://developers.dingtalk.com/document/app/custom-robot-access
#### 下方填写token后面的内容，只需 https://oapi.dingtalk.com/robot/send?access_token=XXX 等于=符号后面的XXX即可
export DD_BOT_TOKEN=""                                                       
export DD_BOT_SECRET=""                                             


#### 5. 企业微信机器人
#### 官方说明文档：https://work.weixin.qq.com/api/doc/90000/90136/91770
#### 下方填写密钥，企业微信推送 webhook 后面的 key
export QYWX_KEY=""                                                                                                  


#### 6. 企业微信应用
#### 参考文档：http://note.youdao.com/s/HMiudGkb
#### 下方填写素材库图片id（corpid,corpsecret,touser,agentid），素材库图片填0为图文消息, 填1为纯文本消息
export QYWX_AM=""                                                                               


#### 7. iGot聚合
#### 参考文档：https://wahao.github.io/Bark-MP-helper
#### 下方填写iGot的推送key，支持多方式推送，确保消息可达
export IGOT_PUSH_KEY=""                                                         


#### 8. Push Plus
#### 官方网站：http://www.pushplus.plus
#### 下方填写您的Token，微信扫码登录后一对一推送或一对多推送下面的token，只填 PUSH_PLUS_TOKEN 默认为一对一推送
export PUSH_PLUS_TOKEN=""                                                                               
#### 一对一多推送（选填）
#### 下方填写您的一对多推送的 "群组编码" ，（一对多推送下面->您的群组(如无则新建)->群组编码）
####  1需订阅者扫描二维码 2、如果您是创建群组所属人，也需点击“查看二维码”扫描绑定，否则不能接受群组消息推送
export PUSH_PLUS_USER=""                                                                


#### 9. go-cqhttp
#### gobot_url 推送到个人QQ: http://127.0.0.1/send_private_msg  群：http://127.0.0.1/send_group_msg 
#### gobot_token 填写在go-cqhttp文件设置的访问密钥
#### gobot_qq 如果GOBOT_URL设置 /send_private_msg 则需要填入 user_id=个人QQ 相反如果是 /send_group_msg 则需要填入 group_id=QQ群 
#### go-cqhttp相关API https://docs.go-cqhttp.org/api
export GOBOT_URL=""                                     
export GOBOT_TOKEN=""                                                   
export GOBOT_QQ=""                                      


#### 10. gotify
#### gotify_url 填写gotify地址,如https://push.example.de:8080
#### gotify_token 填写gotify的消息应用token
#### gotify_priority 填写推送消息优先级,默认为0
export GOTIFY_URL=""                                                                 
export GOTIFY_TOKEN=""                                                                               
export GOTIFY_PRIORITY=0                                                                                   



#### 11. qmsg 酱·   
#### qmsg 酱的 QMSG_KEY                                                                                       
export QMSG_KEY=""                                                                       
#### qmsg 酱的 QMSG_TYPE                                                                                       
export QMSG_TYPE=""                                                                                                             


#### 12. 飞书机器人


#### 飞书机器人的 FSKEY                                                              
export FSKEY=""                                                                                                                                 


