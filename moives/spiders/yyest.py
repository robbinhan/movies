import scrapy
from scrapy import Selector
import MoviesMenu

class YyestSpider(scrapy.Spider):
    name = "yyest"
    host = 'http://www.zimuzu.tv'

    def start_requests(self):
        urls = [
            'http://www.zimuzu.tv/fresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        lastestMoviesHome = response.xpath('//div[@class="resource-showlist has-point"]/ul/li').extract();
        if not lastestMoviesHome:
            print("今日最新列表未更新")
        print(lastestMoviesHome)

        moivesList = []

        for movieHomeText in lastestMoviesHome:
            #<li class="clearfix">\n                            <div class="fl-img">\n                                <a href="/resource/27972" target="_blank"><img src="http://tu.zmzjstu.com/ftp/2017/0206/m_75a781fb09bd779b3b7659fbcd9727e0.jpg"><span class="point"><em>8.</em>8</span></a>\n                            </div>\n                            <div class="fl-info">\n                                <dl>\n                                    <dt><span class="fr f3 dateline" time="1500614974"></span><h3 class="f14"><a href="/resource/27972" target="_blank"><strong class="tag tv">美剧</strong>【美国】《下一站歌后》(Nashville)2012</a><font class="f4">[第5季连载中]</font></h3></dt>\n                                    <dd>\n                                        <p>【说明】 【原创翻译双语字幕】【更新S05E18】</p>                                        <p>【类型】 剧情/偶像/青春</p> \n                                        <p>【人气】 566492次浏览| 978次收藏 | 2012-10-11 首播</p>\n                                        <p class="f14"><strong class="ranking">本站排名 <font class="f1">1144</font></strong></p>\n                                    </dd>\n                                </dl> \n                            </div>\n                        </li>
            print(movieHomeText)
            sel = Selector(text=movieHomeText)
            title = sel.xpath('//a/text()').extract()[0]
            url = sel.xpath('//a//@href').extract()[0]
            url = self.host + url
            print(title)
            print(url)
            moive = {'url':url,'title':title}
            print(moive)
            moivesList.append(moive)

        moviesMenu = MoviesMenu.MoviesMenu(moivesList, 'yyest_one_movie')
        yield moviesMenu.create_menu()