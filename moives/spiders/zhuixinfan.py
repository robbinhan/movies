import scrapy
from scrapy import Selector
import MoviesMenu

class ZhuixinfanSpider(scrapy.Spider):
	name = "zhuixinfan"
	host = 'http://www.zhuixinfan.com/'

	def start_requests(self):
		urls = [
			'http://www.zhuixinfan.com/main.php'
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		lastestMoviesHome = response.xpath('/html/body/div[@id="wp"]/table[@class="top-list-data"][1]/tr').extract()[1:]
		if not lastestMoviesHome:
  			print("今日最新列表未更新")
		print(lastestMoviesHome)

		moivesList = []

		for movieHomeText in lastestMoviesHome:
			print(movieHomeText)
			sel = Selector(text=movieHomeText)
			title = sel.xpath('//tr/td[2]/a[2]/text()').extract()[0]
			url = sel.xpath('//tr/td[2]/a[2]//@href').extract()[0]
			url = self.host + url
			print(title)
			print(url)
			moive = {'url':url,'title':title}
			print(moive)
			moivesList.append(moive)

		moviesMenu = MoviesMenu.MoviesMenu(moivesList)
		yield moviesMenu.create_menu()