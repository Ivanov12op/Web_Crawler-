import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#base_url = "https://mobile.bg"
try:
	from Lib.constants import DATA_PATH
	from Lib.db import DB
except:
	from constants import DATA_PATH
	from db import DB

class Crawler():
	def __init__(self, base_url, data_path='./data/'):
		self.base_url = base_url
		self.seed = []
		self.visited = []
		self.url = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qkn957&f1="
		self.data_path = DATA_PATH
		self.current_page = 1

		self.db = DB()
		# self.db.drop_radiotheaters_table()
		# self.db.create_radiotheaters_table()

	def make_filename(self,url):
		""" Extracts domain from a url.
			Prepend data_path and append '.html'
			:param url: string
			return <domain>.html string
		"""
		rx = re.compile(r'^https?:\/\/(?:www.)?([^\/]+)\/?')
		m = rx.search(url)
		if m:
			filename = self.data_path + m[1]  + '.html'
			# print(filename)
			return filename
		else:
			print(f'Can not get domain from {url}')
			exit(-1)

	def write_to_file(self,filename, content):
		""" Write string to given filename
				:param filename: string
				:param content: sring
		"""
		try:
			with open(filename, 'w',encoding='windows-1251') as f:
				f.write(content)
		except FileNotFoundError:
			print(f'File {filename} does not exists!')
		except Exception as e:
			print(f'Can not write to file: {filename}: {str(e)}')
			exit(-1)

	def get_html(self,url):
		# GET request without SSL verification:
		try:
			r = requests.get(url)
		except requests.RequestException:
			# try with SSL verification disabled.
			# this is just a dirty workaraound
			# check https://levelup.gitconnected.com/solve-the-dreadful-certificate-issues-in-python-requests-module-2020d922c72f
			r = requests.get(url,verify=False)
		except Exception as e:
			print(f'Can not get url: {url}: {str(e)}!')
			exit(-1)

		# set content encoding explicitely
		r.encoding="windows-1251"

		if r.ok:
			return r.text
		else:
			print('The server did not return success response. Bye...')
			exit


	def get_seed(self,url ):
		print(f'Crawling main page {self.current_page}:{url}')
		page_links = []

		page_url = self.url+ str(self.current_page)  ### тук нещо нее както трябва
		html = self.get_html(page_url)
		
		soup = BeautifulSoup(html.content, 'html.parser')
		table = soup.find_all ('table',  class_="tablereset" )
		set_a = table.find ('td', colspan= "3" ).getText()

		for sity in set_a:
			if sity == re.findall(r"\София", sity):
				a = table .find_all("a", href = True )

			page_links.append( urljoin (base_url, a['hre']))



			if page_links:
				self.seed = [ *self.seed, *page_links]
				self.current_page+1 
				self.get_seed()

			

		
	def get_data(self, html):
		
		soup = BeautifulSoup( html, 'html.parser')
		modul = soup.find ( 'div', style_="width:300px; display:inline-block;  float:left; margin-top:18px; overflow: hidden;"  ) 

		title = modul.find('strong', style_="font-size:18px;color:#333;" ).getText()
	
		modul2= modul.find ('ul', class_="dilarData")(2).getTex()   # !!!!!!!!!!!!
	
		Car_year = modul2.(2)getText()
		Engine_type = modul2.getText()
		Аccumulated_km  =

		return { 
			'title': title,
			'Car_year': Car_year,
			'Engine_type': Engine_type,
			'Price': Price,
			'Аccumulated_km': Аccumulated_km,
		}	
	
		


	def run(self):
		# get all URLs to be scraped from base_url
		#	""" run the crawler for each url in seed
		#	Use multithreading for each GET request
		#"""

		self.get_seed(self.base_url)

		for url in self.seed:
			page_html = self.get_html(url)
			data = self.get_data(page_html)

			DB.insert_row(tuple(data.values()))
		


if __name__ == '__main__':

	base_url = 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qkn957&f1='
	crawler = Crawler()
	crawler.run()
	bd = DB()


