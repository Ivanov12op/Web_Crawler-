import requests
import os

from constants import DATA_PATH


class Crawler():
	def __init__(self, base_url):
		self.seed = [base_url]

	def write_to_file(self,filename, content):
		""" Write string to given filename
				:param filename: string
				:param content: sring
		"""
		with open(DATA_PATH+filename, 'w') as f:
			f.write(content)
			

	def get_html(self, url):
		""" Make GET request and save content to file
			First try with SSL verification (default),
			if error => disable SSL verification

			:param url: string
		"""
		r = requests.get(url)
		
		if r.ok:
			r.encoding = 'windows-1251'
		return r.text


	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request

		"""
		for url in self.seed:
			html = self.get_html(url)
			self.write_to_file('mobile.bg.html', html)


		print('Crowler finish its job!')

if __name__ == '__main__':
	crawler = Crawler("https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qdz07i&f1=1")
	crawler.run()
