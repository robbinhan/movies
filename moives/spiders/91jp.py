
import scrapy


class JpSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://www.loldytt.com/Zuixinriju/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
    	lastestMoviesHome = response.xpath('//div[@class="gengxin"]/ul/li/a').extract()
    # 	print(lastestMoviesHome)

    # 	for movieHome in lastestMoviesHome:
    # 		sel = Selector(movieHome)
    # 		title = sel.xpath('/a/text()')
    # 		url = sel.xpath('/a/@href')
    # 		print(url)
    # #         # yield scrapy.Request(url=url, callback=self.parseMovieHome)

    # def parseMovieHome(self, response):