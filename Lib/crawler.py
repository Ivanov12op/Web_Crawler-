import os
import re
import requests
#from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from urllib.parse import urljoin



BASE_URL = "https://mobile.bg"


try:
	# when run 'crawler.py':
	from constants import DATA_PATH
	from db import DB
except:
	# when run 'app.py'
	from Lib.constants import DATA_PATH
	from Lib.db import DB



class Crawler():
	def __init__(self):
		self.current_page = 1

		# starting url, to which self.current_page wil be appended
		self.url = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qlxaxc&f1="

		# list of urls to be scraped
		self.seed = []

		# indicates that crwler is not finished it's job. We'll set it to 1 after sucessfull crawl.
		self.status = 0

	def write_to_file(self,filename, content):
		""" Write string to given filename
				:param filename: string
				:param content: sring
		"""

		with open(DATA_PATH+filename, 'w') as f:
			f.write(content)

	def get_html(self, url):


		try:
			r = requests.get(url)
		except requests.RequestException:
			r = requests.get(url,verify=False)
		except Exception as e:
			print(f'Cant not get url: {url}: {str(e)}! ')
			exit(-1)
		r.encoding = "windows-1251"
		

		if r.ok:
			return r.text
		else:
			print( 'The server did not return sucsess response....')

			exit
 




	def get_seed(self):
		page_links = []
		page_url = self.url + str(self.current_page)
		html = self.get_html(str(page_url))
		

		soup = BeautifulSoup(html, 'html.parser')
		form_search = soup.select_one('form[name="search"]')
		tables = form_search.find_all ('table', class_ = "tablereset")[1:-3]
		
		
		#td_links = tables.find_all('td',class_="valgtop")

		

		#set_a = tables.find_all('td',class_="volgtop")  


		for link in tables:
		#	if sity == re.findall(r"\София"):
			a = link .find('a', href = True )
			print(a['href'])
			
			page_links.append(a(a[ 'href' ]))
			
		

		if page_links:
			self.seed = [ *self.seed, *page_links ]
			self.current_page+=1
			self.get_seed()

	def get_page_data(self,html):
        
		
		soup = BeautifulSoup( html, 'html.parser' )

		car_data = soup.select('div', style="width:300px; display:inline-block; float:left; margin-top:18px; overflow: hidden;")
		title = car_data.find ('strong' , style="font-size:18px;color:#333;").getText()

		car_data = car_data.find ( 'ul', class_="dilarData") 

		# get title:
		car_data_items = car_data.find_all('li')

		Car_year = car_data_items.find('li',string="Дата на производство")
		Engine_type = car_data_items.find('li',string=" Тип двигател ")
		Аccumulated_km  = car_data_items.find('li',string="Пробег [км] ")

		Car_price = soup.select ('div',style="width:360px; margin-left:0; display:inline-block; margin-top:15px; margin-left:20px;")

		Price = Car_price.find('span',id="details_price").getText
		

		return { 
			'title': title,
			'Car_year': Car_year, 
			'Engine_type': Engine_type,
			'Price': Price,
			'Аccumulated_km': Аccumulated_km,
		}	
	
		

		

	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request
		"""
		db = DB()
		# db.truncate_radiotheaters_table()

		### get seed (get pages for radiotheater publiched in last 10 days)
		self.get_seed()

		### process page data
		for url in self.seed:
			print(f'Process page: {url}')
			page_html = self.get_html(url)

			data = self.get_page_data(page_html)

			###  write data to db
			db.insert_row( tuple(data.values()) )

		self.status = 1
		print('Crowler finish its job!')


if __name__ == "__main__":
	crawler = Crawler()
	crawler.run()