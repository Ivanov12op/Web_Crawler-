import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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
		self.url = "https://m.mobile.bg/results?pubtype=1&currency=%D0%A0%C2%BB%D0%A0%D0%86.&marka=BMW&model=120&sort=3&nup=0~1&slink=qgy2t8&page="
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


	def get_seed(self,html ):
		page_links = []

		page_url = self.url+ str(self.current_page) 
		html = self.get_html(page_url)
		
		soup = BeautifulSoup(html,'html.parser')
		table = soup.find ( 'div',  class_="page" )
		# get  publicat list
		rows= table.find ( 'div', class_="ng-star-inserted")
		
		
		for info in rows:
			sity_info = info.find( 'advertl' , class_="results" ).getText()
			
			if sity_info == re.compile (r'([София])'):
		        
				a = sity_info .find_all('div',  class_="listItem")

			page_links.append( urljoin (base_url, a['id']))
		    
			
			#if page_links:
			#	self.seed = [ *self.seed, *page_links]
			#	self.current_page+1 
			#	self.get_seed()

		
	def get_data(self, html):
		
		soup = BeautifulSoup( html, 'html.parser') 
		modul = soup.find('div',id='callButtonsOffset',class_="page")
		
		Price = modul.find( "div", class_="price" ).getText
		title = modul.find('h1').getText(strip=True) 
		#### !!!!!!!!!!
		modul2 = modul.find('div', class_='oPanel oMainData ng-star-inserted')
		
		Car_year = modul2.find_all('div',clas_='oPanel oMainData ng-star-inserted')[0].getText()
		Engine_type =modul2.find_all('div',clas_='oPanel oMainData ng-star-inserted')[1].getText()
		Аccumulated_km = modul2.find_all('div',clas_='oPanel oMainData ng-star-inserted')[6].getText()

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


		print('Crawler finished its job!')


if __name__ == '__main__':

	base_url = 'https://m.mobile.bg/results?pubtype=1&currency=%D0%A0%C2%BB%D0%A0%D0%86.&marka=BMW&model=120&sort=3&nup=0~1&slink=qgy2t8'
	crawler = Crawler(base_url)
	crawler.run()



