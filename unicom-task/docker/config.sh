# 通知推送服务环境变量请查看：https://github.com/wuye999/myScripts/blob/main/send.md
# 环境变量示例：
export unicom_config_1="手机号1<<<服务密码1<<<appId1<<<抽奖次数(0-30)中奖几率渺茫<<<手机的imei（可留空）"
export unicom_womail_1="沃邮箱登陆Url1<<<手机号1(可留空)<<<沃邮箱密码（可留空）"
export PUSH_PLUS_TOKEN="微信推送Plus+(通知服务示例，可留空或不填)"



###----------------------------------------------------------------------
# 执行开始时间
time=$(date "+%Y-%m-%d %H:%M:%S")
startTime_s=`date +%s`
echo "## 开始执行... ${time}"
crontab /root/config/crontab.list
# cd /myScripts && git pull --force origin ${SCRIPT_BRANCH}
cp -rf /myScripts/unicom-task/ /root/ && cd /root/unicom-task && python3 unicom_index.py
# 执行结束时间
time=$(date "+%Y-%m-%d %H:%M:%S")
endTime_s=`date +%s`
# 执行用时
sumTime=$[ $endTime_s - $startTime_s ]
echo "## 执行结束... ${time} 耗时 ${sumTime} 秒"
