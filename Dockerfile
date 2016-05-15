# Docker 1.5.0
FROM ubuntu:trusty
MAINTAINER Yongwen Zhuang <zhuangyw.thu@gmail.com>

# Usual update / upgrade
RUN apt-get update && \
        apt-get install -y  python     \
                            python-dev \
                            python-pip \
                            git-core\
        && apt-get clean \
        && apt-get autoclean \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Working enviroment
ENV BOTDIR /bot
WORKDIR ${BOTDIR}


# git clone wechat-bot
RUN git clone https://github.com/zYeoman/wechat-bot .
RUN pip install itchat

# Entrypoint
ENTRYPOINT ["/usr/bin/python2", "wechat_bot.py"]
