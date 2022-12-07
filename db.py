import mysql.connector as mc

try:
	from Lib.read_config import read_db_config
except:
	from read_config import read_db_config

class DB ():
	def __init__(self):
		mysql_config = read_db_config('config.ini', 'mysql')
		print(mysql_config)
		try:
			self.conn = mc.connect(**mysql_config)

		except mc.Error as e:
			print(e)


	def create_car_table(self):
		sql = """
			CREATE TABLE IF NOT EXISTS car_search (
				id INT AUTO_INCREMENT PRIMARY KEY,
				title VARCHAR(100) NOT NULL,
				Car_year  NOT NULL,
				Engine_type TEXT,
				Price ,
				Аccumulated_km   NOT NULL  ,

				CONSTRAINT title_date UNIQUE (title, Car_year , Engine_type, Price,Аccumulated_km)
			);
		"""

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			self.conn.commit()

	def drop_car_table(self):
		sql = "DROP TABLE IF EXISTS car_search"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			self.conn.commit()

	def truncate_car_table(self):
		sql = "truncate car_search"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			self.conn.commit()


	def insert_row(self, row_data):
		sql = """
			INSERT IGNORE INTO car_search
				(title, Car_year, Engine_type, Price, Аccumulated_km)
				VALUES ( %s, %s, %s, %s, %s)
		"""

		with self.conn.cursor(prepared=True) as cursor:
			cursor.execute(sql, tuple(row_data.values()))
			self.conn.commit()

	def select_all_data(self):
		sql = "SELECT id, title, Car_year, Engine_type, Price, Аccumulated_km FROM  car_search"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchall()

		return result

	def get_last_updated_date(self):
		sql = 'SELECT MAX(updated_at) AS "Max Date" FROM car_search;'
		with self.conn.cursor() as cursor:
	
			cursor.execute(sql)
			result = cursor.fetchone()

		if result:
			return result[0]
		else:
			raise ValueError('No data in table')

	def get_column_names(self):
		sql = "SELECT id, title, Car_year, Engine_type, Price, Аccumulated_km FROM  car_search LIMIT 1;"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchone()

		return cursor.column_names

if __name__ == '__main__':
	db = DB()

	 # db.get_column_names()
	res = db.select_all_data()
	print(res)


