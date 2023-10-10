# jable爬虫 jable-spider
jable.tv(fs1.app)爬虫, 包含所有番号

![](https://github.com/xiaoWangSec/jable-spider/blob/master/img.jpg)

## 使用方法

* 确保网络环境是科学的 (Clash可以打开TUN模式, 或者连接VPN) 
* 或者直接Fork一份代码然后在Codespace中打开
* 安装依赖`pip install -r requirements.txt`
* 运行爬虫`python main.py`
* 会自动更新最新番号至`avdb_images`中
* 你可以手动修改`for i in tqdm(range(1, 35), colour='green', desc='进度: '):`中的范围以实现修改爬取页面


## 数据库设计

见sql文件


## 说明

<s>直接对jable.tv进行请求会遇到cloudflare五秒盾, 可以用cloudscraper绕过</s>

<s>但是也可以换个思路, 对fs1.app进行请求, 实测不会遇到cloudflare五秒盾</s>

站点改动, jable.tv用了Cloudflare version 2 Captcha challenge, cloudscraper免费版无法绕过

fs1.app也不能直接爬了, 需要使用[https://github.com/VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper)绕过

## TODO

<s>把封面爬下来转base64存到另一张表</s>
