import scrapy
import subprocess

class YyestOneMovieSpider(scrapy.Spider):
    name = "yyest_one_movie"

    def __init__(self, url):
        super(YyestOneMovieSpider, self).__init__()
        self.url = url

    def start_requests(self):
        print(self.url)
        yield scrapy.Request(url=self.url, callback=self.parse_download_page)
            

    def parse_download_page(self, response):
        downloadPageLink = response.xpath('/html/body/div/div/div/div/div/div[@class="tc view-res-tips view-res-nouser"]/h3/a/@href').extract()[0]
        yield scrapy.Request(url=downloadPageLink, callback=self.parse_download_page)
        

    def parse_movie_home(self, response):
        
        if "magnet:?" in downloadLink: 
            command = 'npm run webtorrent-cli -- download "' + downloadLink + '" --mpv'
            (status) = subprocess.call(command, shell=True)
            print(status)


            