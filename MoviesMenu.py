import os
from moives.spiders import zhuixinfandownloadlink
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class MoviesMenu():
	"""docstring for MoviesMenu"""
	def __init__(self, movies):
		super(MoviesMenu, self).__init__()
		self.movies = movies
		
	def create_menu(self):
		os.system('clear')

		menuString = '''
			请选择要下载的剧集：\n
		'''

		for index, moive in enumerate(self.movies):
			print(str(index) + " " + moive['title'])
		
		choice = input(" >>  ")
		self.exec_menu(choice)
			 
		return

	def exec_menu(self, choice):
		os.system('clear')
		ch = choice.lower()
		if ch == '':
			self.create_menu()
		else:
			try:
				# zhuixinfandownloadlink.ZhuixinfanDownloadLinkSpider().start_requests(self.movies[int(ch)]['url'])
				process = CrawlerProcess(get_project_settings())
				process.crawl('zhuixinfan_downloadlink',url=self.movies[int(ch)]['url'])
				process.start()
			except KeyError:
				print("Invalid selection, please try again.\n")
				self.create_menu()
		return