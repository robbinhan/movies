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

session = requests.session()

cnx = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='zhihu')
                              
class ZhihuSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    host = 'https://www.zhihu.com/'
    
    start_urls = [
        "https://www.zhihu.com"
    ]
    
    rules = (
        Rule(LinkExtractor(allow = ('/question/\d+#.*?', )), callback = 'parse_page', follow = True),
        Rule(LinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),
    )
    
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Referer": "https://www.zhihu.com/",
    "Host": "www.zhihu.com",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1"
    }

    def start_requests(self):
        # return [Request("https://www.zhihu.com", headers=self.headers, meta = {'cookiejar' : 1}, callback = self.post_login)]
        yield scrapy.Request(url='https://www.zhihu.com/', headers=self.headers, meta = {'cookiejar' : 1}, callback=self.post_login)
        
        
    def get_gif(self): ##获取验证码
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login&lang=en'##知乎最新验证码为文字倒立，老版未被屏蔽，这里是老版
        r2 = session.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r2.content)
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
        num = input("请输入验证码：")
        return num
        
    def post_login(self,response):
        print('Preparing login')
        print(response.headers.getlist('Set-Cookie'))
        
        cookies = []
        for value in response.headers.getlist('Set-Cookie'):
            array = str(value,'utf-8').split(';')
            cookies.append(array[0])
        cookies_string = '; '.join(cookies)
        
        print(cookies_string)
        
        #下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print(xsrf)
        print(response.meta['cookiejar'])
        
        self.headers['Accept'] = '*/*'
        self.headers['Origin'] = 'https://www.zhihu.com'
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['X-Xsrftoken'] = xsrf
        self.headers['Cookie'] = cookies_string
        
        print(self.headers)
        num = self.get_gif()
        
        # return
        #登陆成功后, 会调用after_login回调函数
        return [scrapy.FormRequest(url='https://www.zhihu.com/login/email',  
                            meta = {'cookiejar' : response.meta['cookiejar']}, #注意这里cookie的获取
                            headers = self.headers,
                            formdata = {
                            '_xsrf': xsrf,
                            'email': '',
                            'password': '',
                            # 'captcha_type': 'cn'
                            'captcha': num
                            },
                            callback = self.after_login
                            )]

    def after_login(self, response):
        print("Login success")
        print(response.text)
        print(response.headers.getlist('Set-Cookie'))
        # return 
        for url in self.start_urls :
            yield scrapy.Request(url=url, headers=self.headers, meta = {'cookiejar' : 1}, callback=self.save_content, dont_filter = True)
            
    def save_content(self, response):
        print("save_content")
        cursor = cnx.cursor()
        add_data_sql = "INSERT INTO `20171218` (html) VALUES ('%s')" % (response.text)
        cursor.execute(add_data_sql)
        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()
            
    def parse_page(self, response):
        print("parse_page")
        print(response.text)
        problem = Selector(response)
        # print(problem.text())
        item = ZhihuItem()
        item['url'] = response.url
        item['name'] = problem.css('.Feed-title').extract()
        print(item['name'])
        # item['title'] = problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        # item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
        # item['answer']= problem.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract()
        return item