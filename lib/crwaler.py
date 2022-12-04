import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://www.mobile.bg"

try:
#from db import DB
	from constants import DATA_PATH
except:
	
	from Lib.constants import DATA_PATH
#	from Lib.db import DB





class Crawler():
	def __init__(self):
		self.curent_page = 1
		self.url = 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qgyawr&f'
		self.seed = [ ]
		self.status = 0

		


	def write_to_file(self,filename, content):
		""" Write string to given filename
				:param filename: string
				:param content: sring
		"""
		with open( DATA_PATH+filename, 'w') as f:
			f.write(content)
			

	def get_html(self, url):
		""" Make GET request and save content to file
			First try with SSL verification (default),
			if error => disable SSL verification

			:param url: string
		"""

		
		r = requests.get(url)
		
		if r.ok:
			r.encoding ='windows-1251'
		return r.text

	def get_seed (self):
		page_links = []

		page_url = self.url+str(self.curent_page) 
		html = self.get_html(page_url)
		

		soup = BeautifulSoup(html,'html.parser')
		table = soup.find( """ div  class="page" """)
		rows= table .find_all(""" div _ngcontent-my-app-c52= """)

		for info in rows:
			sity_info = info.find_all(""" 'advertl'  "class=results" """)
			sity_info = info.get_text()
			if sity_info == re.compile (r'([София])'):
				a = sity_info .find_all("""'di _ngcontent-my-app-c50=""  class="listItem" """)

			self.seed.append(urljoin(BASE_URL, a['id']))

		if page_links:
			self.seed = [ *self.seed, *page_links]
			self.curent_page+1 
			self.get_seed()
	


	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request

		"""

		
		self.get_seed()
		print(self.seed)
		


		print('Crowler finish its job!')

#if __name__ == '__main__':
#	crawler = Crawler("https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qdz07i&f1=1")
#	crawler.run()
