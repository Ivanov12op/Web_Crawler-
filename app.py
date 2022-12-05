import os
from urllib.parse import urljoin
from Lib.crwaler import Crawler
from Lib.constants import DATA_PATH
from urllib.parse import urljoin

import requests
import sys

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from Lib.crwaler import Crawler
from Lib.pyqt_table import TableViewWidget
from Lib.db import DB


class MainWindow(qtw.QMainWindow):
	def __init__(self , *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.crawler = Crawler()

		self.setWindowTitle('BNR Crawler')


		### Main layout
		mainLayout = qtw.QVBoxLayout()

		### Table Caption part:
		lblTableCaption = qtw.QLabel('Radiotheaters Data')
		lblTableCaption.setObjectName('lblTableCaption')
		lblTableCaption.setAlignment(qtc.Qt.AlignCenter)
		mainLayout.addWidget(lblTableCaption)

		### Buttons
		btnsLayout = qtw.QHBoxLayout()
		btnCrawlerRun = qtw.QPushButton('Run Crawler')
		self.btnShowData = qtw.QPushButton('Show Data')
		self.btnShowData.setEnabled(False)

		btnsLayout.addWidget(btnCrawlerRun)
		btnsLayout.addWidget(self.btnShowData)
		mainLayout.addLayout(btnsLayout)

		### Status
		## will be hiddin on start
		statusLayout = qtw.QVBoxLayout()
		self.lblStatus = qtw.QLabel('Crawler Working...')
		self.lblStatus.hide()
		statusLayout.addWidget(self.lblStatus)
		mainLayout.addLayout(statusLayout)

		### Actions on buttons click:
		self.btnShowData.clicked.connect(self.show_data)
		btnCrawlerRun.clicked.connect(self.run_crawler)

		# add spacer or just fixed spacing
		mainLayout.addSpacing(10)
		# mainLayout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

		mainWidget = qtw.QWidget()
		mainWidget.setLayout(mainLayout)

		self.setCentralWidget(mainWidget)

		self.show()

	def show_data(self):
		self.tableViewWidget = TableViewWidget(parent=self)
		self.tableViewWidget.show()

	def run_crawler(self):
		print('Crawler started')

		# change cursor to wait icon:
		self.setCursor(qtc.Qt.WaitCursor)

		# show status label
		self.lblStatus.show()
		qtw.QApplication.processEvents()  # needed to force processEvents

		# start crawler
		self.crawler.run()

		# if crawler ready:
		if self.crawler.status:
			self.lblStatus.setText('Ready!')
			self.btnShowData.setEnabled(True)

		self.setCursor(qtc.Qt.ArrowCursor)


if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)

	window = MainWindow()

	sys.exit(app.exec_())
#BASE_URL = "https://www.mobile.bg"
#MAIN_PATH = "/results?pubtype=1&model=120&marka=BMW&sort=3&currency=Р»РІ.&nup=0~1&slink=qgyawr"

#if __name__ == '__main__':
    #r = requests.get(BASE_URL)
  #  crawler = Crawler( )
 #   crawler.run()