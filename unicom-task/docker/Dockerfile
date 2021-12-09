FROM python:alpine
ARG SCRIPT_URL=https://github.com.cnpmjs.org/wuye999/myScripts.git/ \
    pip3_url=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    PS1="\u@\h:\w\$ " \
    TZ=Asia/Shanghai \
    SCRIPT_BRANCH=main \
    SCRIPT_DIR=/myScripts
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk --no-cache add -f bash \
                             git \
                             tzdata \
                             g++ \
                             gcc \
                             libxslt-dev \
                             libxml2-dev \
                             nodejs \
                             npm \
                             vim \
    && git clone -b ${SCRIPT_BRANCH} ${SCRIPT_URL} ${SCRIPT_DIR} \
    && pip3 config set global.index-url ${pip3_url} \
    && pip3 install --no-cache-dir -r ${SCRIPT_DIR}/unicom-task/requirements.txt \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && rm -rf /var/cache/* \
    && chmod +x /myScripts/unicom-task/docker/docker-entrypoint.sh 
    
ENTRYPOINT /myScripts/unicom-task/docker/docker-entrypoint.sh
