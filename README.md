1.输入关键字
2.登录知乎 - done
3.保存数据 - done
4.清洗数据 
5.解析主页问题（过滤广告）
6.搜索
7.展示阅读

# 描述

从zhuixinfan上抓取今日更新的列表，通过命令行菜单选择要下载的剧集，获取磁力链接，调用webtorrent-cli下载资源，同时通过mpv播放



```
pip install -r requirements.txt
```

# 追新番
 ```
 scrapy runspider moives/spiders/zhuixinfan.py
 ```

 # 知乎
  ```
 scrapy runspider moives/spiders/zhihu.py
 ```
