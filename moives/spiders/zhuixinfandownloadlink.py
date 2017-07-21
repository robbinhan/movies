import scrapy
import subprocess

class ZhuixinfanDownloadLinkSpider(scrapy.Spider):
	name = "zhuixinfan_downloadlink"

	def __init__(self, url):
		super(ZhuixinfanDownloadLinkSpider, self).__init__()
		self.url = url

	def start_requests(self):
		print(self.url)
		yield scrapy.Request(url=self.url, callback=self.parse_movie_home)
			

	def parse_movie_home(self, response):
		downloadLink = response.xpath('//dd[@id="torrent_url"]/text()').extract()[0]
		print(downloadLink)
		if "magnet:?" in downloadLink: 
			command = 'npm run webtorrent-cli -- download "' + downloadLink + '" --mpv'
			(status) = subprocess.call(command, shell=True)
			print(status)


			