# VerifyBot
一个用于人肉验证码识别的 Telegram BOT 后端

# 工作方式

- 提供HTTP接口，将验证码以文件形式(multipart/form-data)POST到机器人服务程序，即可使用机器人将验证码发送到你的手机上/发布到群中
- HTTP 连接 在 POST 之后阻塞
- 在 Telegram 界面中直接**选中**图片**回复(Reply)**即可完成验证码识别
- 一旦你回复图片，HTTP请求即刻返回你的输入值
- 如果长时间没有人完成识别，返回 404 和 TimeoutError
- 基于`Tornado`实现, 未识别的验证码不会阻塞后续的识别请求

# 安装

本项目依赖Python3

> git clone git@github.com:comzyh/LDRS.git
> virtualenv env -p python3.5
> pip install -r requirements.txt

安装完成

> python verifybot.py -h 

可以查看帮助

## Telegram 机器人创建


添加 BotFather 为联系人

https://telegram.me/BotFather

输入

> /start  
> /newbot

按照提示输入你的 BOT 的name 和 username ，BOT 创建完成，然后你会得到一个BOT 的 token

**这个 Toekn 非常重要**，不过如果你忘记了，你可以随时使用 `/token` 向 BotFather 查询

然后向 BOT 添加命令，在 BotFather 中键入:

> /setcommands

选择你的BOT， 将 以下内容粘贴进去

```
subscribe - Subscribe for recognition request
unsubscribe - Unsubscribe for recognition request
```

命令配置成功

## WebHook配置

本项目提供WebHook配置功能，要求

- Telegram 的 WebHook 要求必须为HTTPS 协议，你必须拥有一个能以HTTPS方式访问的网站

> source env/bin/active  
> python verifybot.py -t <your_token> --set-web-hook --hostname <your_host_name> --url-prefix <your_url_prefix>

比如你的 token 是 111111111:YYYYYYYYY-XXXXXXXXXXXXXXXXXXXXXXXXX, 你的 HTTP 接口为 http://foo.com/bar/, 那你应该输入

> python verifybot.py -t 111111111:YYYYYYYYY-XXXXXXXXXXXXXXXXXXXXXXXXX --set-web-hook --hostname foo.com --url-prefix /bar


## 启动

本项目可以直接使用 tornado 裸奔，但是考虑到 Telegram 接口必须为 HTTPS，建议使用 Nginx

假设你的HTTP接口地址为 `http://foo.com/bar/`

在nginx server 项中加入如下内容

```
location /bar/ {
        proxy_read_timeout 300;
        proxy_pass http://127.0.0.1:8888/;
}
```

设置 proxy_read_timeout 是因为由于本程序在输入验证码之前阻塞时间比较长，所以超时时间设为5分钟,即300秒

启动服务端

> python verifybot.py -t 111111111:YYYYYYYYY-XXXXXXXXXXXXXXXXXXXXXXXXX  -d -p 8888

后台运行推荐使用 supervisor,  当然不追求稳定性的话可以随意点:

> nohup python verifybot.py -t 111111111:YYYYYYYYY-XXXXXXXXXXXXXXXXXXXXXXXXX  -d -p 8888 &

# 使用

使用方法参见源码中的 `example.py`

Enjoy!
