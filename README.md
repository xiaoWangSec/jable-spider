# jable爬虫 jable-spider
jable.tv(fs1.app)爬虫, 包含所有番号


## 使用方法

* 确保网络环境是科学的 (Clash可以打开TUN模式, 或者连接VPN)
* 直接运行`main.py` (python main.py)
* 会自动更新最新番号至`AV.db`中
* 你可以手动修改`for i in tqdm(range(1, 35), colour='green', desc='进度: '):`中的范围以实现修改爬取页面


## 数据库设计

|  car   | title  | url  | img |
|  ----  | ----  | ----  | ----  |
| 车牌  | 标题 | 链接 | 封面图 |


## 说明

直接对jable.tv进行请求会遇到cloudflare五秒盾, 可以用[https://github.com/VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper)绕过

但是也可以换个思路, 对fs1.app进行请求, 实测不会遇到cloudflare五秒盾

## TODO

* 把封面爬下来转base64存到另一张表
