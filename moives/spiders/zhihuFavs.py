import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
# from scrapy.http import Request, FormRequest
from moives.spiders.zhihuitem import ZhihuItem
import time
import requests
from PIL import Image
import mysql.connector
import re

session = requests.session()

cnx = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='zhihu')


# 知乎某个收藏夹                              
                              
class ZhihuSpiderFav(CrawlSpider):
    name = "zhihu_collection"
    allowed_domains = ["www.zhihu.com"]
    host = 'https://www.zhihu.com/'
    
    start_urls = [
        "https://www.zhihu.com/collection/123354652"
    ]
    
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Referer": "https://www.zhihu.com/collections",
    "Upgrade-Insecure-Requests": "1",
    "authority": "www.zhihu.com",
    ## 自己更新
    "cookie":'_zap=c937abaa-b6c5-4c00-9e26-de1bd7ff55ca; _xsrf=34a47769-a9d9-480c-a7ec-e8b91f877c8d; d_c0="AIAnNzOWDQ6PTi6ADWQ-IsM9yURiR_UtwQA=|1534209957"; l_n_c=1; n_c=1; gsScrollPos-2626=; q_c1=0044fbbf126b47c782a6ce17e653555c|1537171263000|1534209997000; __utmc=51854390; __utmv=51854390.100-1|2=registration_date=20110530=1^3=entry_date=20110530=1; gsScrollPos-687660391=; gsScrollPos-687653795=0; tgw_l7_route=69f52e0ac392bb43ffb22fc18a173ee6; gsScrollPos-687661826=; capsion_ticket="2|1:0|10:1538301895|14:capsion_ticket|44:ZWFiN2U0OWZlOWI0NGQ2ZDg2Y2QyY2UyYTJjMDAwNTE=|c6884d5feb177cd3aa939d55414bb0e01f4dda212fdec69b1fe5b59c82ed815b"; z_c0="2|1:0|10:1538301915|4:z_c0|92:Mi4xSW80QUFBQUFBQUFBZ0NjM001WU5EaVlBQUFCZ0FsVk4yLTJkWEFBMlNTclQ3UkNMUTBoWENwTG5TbTZiWmVGUWhB|0cf7aa65f562015aa1afa8271af1c26091f5144701a5419017128aae43320f20"; __utma=51854390.458243456.1537963987.1538014365.1538301925.3; __utmb=51854390.0.10.1538301925; __utmz=51854390.1538301925.3.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/'
    }

    def start_requests(self):
        # return [Request("https://www.zhihu.com", headers=self.headers, meta = {'cookiejar' : 1}, callback = self.post_login)]
        yield scrapy.Request(url='https://www.zhihu.com/question/272253499', headers=self.headers, meta = {'cookiejar' : 1}, callback=self.parse_page)
            
    def parse_page(self, response):
        print("parse_page")
        # print(response.text)
        divs = response.xpath('//div[@id=$val]/text()',val='data')#.re(r'https://.*zhimg.com/.*')
        # problem = Selector(response)

        m = re.findall(r'(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?', response.text)

        # title = problem.css('img').xpath('@src').extract()
        print(m)