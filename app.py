import sys
from time import strftime
import datetime
#from urllib.parse import urljoin
from Lib.crawler import Crawler
from Lib.constants import DATA_PATH
from Lib.db import DB
from urllib.parse import urljoin

BASE_URL = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qkn957&f1="



from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


from Lib.pyqt_table import TableViewWidget

class TableView(qtw.QTableView):
	def __init__(self, *args, **kwargs):
		super().__init__()

		self.db = DB()

		if not self.db.conn:
			qtw.QMessageBox.critical(
							None,
							"Database Error!",
							#"Database Error: %s" % con.lastError().databaseText(),
			)
			return False

		self.data = self.db.select_all_data()
		self.column_names = self.db.get_column_names()

		model = self.setup_model()

		self.filter_proxy_model = qtc.QSortFilterProxyModel()
		self.filter_proxy_model.setSourceModel(model)
		self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)
		self.filter_proxy_model.setFilterKeyColumn(1)

		self.setModel(self.filter_proxy_model)

		self.setup_gui()

		# self.showColumn(2)

	def setup_gui(self):
		### set table dimensions:
		# get rows and columns count from model:
		rows_count = self.model().rowCount()
		cols_count = self.model().columnCount()

		self.setMinimumWidth(cols_count*230)
		self.setMinimumHeight(rows_count*40)

		### resize cells to fit the content:
		# self.resizeRowsToContents()
		# self.resizeColumnsToContents()
		# set width of separate columns:
		self.resizeColumnToContents(0)
		self.resizeColumnToContents(1)
		self.setColumnWidth(3, 300)


		# streach table:
		# self.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
		# self.horizontalHeader().setStretchLastSection(True)
		# self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
		self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)


		# set all cells hight
		# header = self.verticalHeader()
		# header.setDefaultSectionSize(50)
		# header.setSectionResizeMode(qtw.QHeaderView.Fixed)

		# enable columns move
		# self.horizontalHeader().setSectionsMovable(True)

		# enable columns sort
		self.setSortingEnabled(True)
		self.sortByColumn(0,qtc.Qt.AscendingOrder)

	def ___setup_model_SQL_table_model(self):
			model =QSqlTableModel(self)
			model.setTable("Car_search")
			model.setEditStrategy(QSqlTableModel.OnFieldChange)
			model.setHorizontalHeaderLabels(self.column_names)
			model.select()

	def setup_model(self):
		model = qtg.QStandardItemModel()
		model.setHorizontalHeaderLabels(self.column_names)

		for i, row in enumerate(self.data):
			items = []
			for field in row:
				item = qtg.QStandardItem()
				if isinstance(field, datetime.date):
					field = field.strftime('%d.%m.%Y')
					pass
				elif isinstance(field, str) and len(field)>100:
					# set full string with UserRole for later use:
					item.setData(field, qtc.Qt.UserRole)
					# trim string for display
					field = field[0:50]+'...'

				item.setData(field, qtc.Qt.DisplayRole)
				items.append(item)

			model.insertRow(i, items)

		return model

	@qtc.pyqtSlot(int)
	def set_filter_column(self,index):
		self.filter_proxy_model.setFilterKeyColumn(index)
	
	def get_last_updated_date(self):
			last_updated_date=self.db.get_last_updated_date()
			return last_updated_date.strftime('%d.%m.%y, %H:%M:%S')	



class TableViewWidget(qtw.QWidget):
	def __init__(self, parent, *args,**kwargs):
		super().__init__(*args, **kwargs)

		self.parant = parent
		self.setup_qui()

	def setup_gui(self):
		#tsble view:
		self.tableView = TableView()
		TableViewWidget = self.tableView.frameGeometry().width()
		TableViewWidget = self.tableView.frameGeometry().height()

		#label
		lbTitle = qtw.Qlabel()
		label_msg = f"""Car publication in Mobile as crawlled on{self.tableView. get_last_update_date()}"""
		lbTitle.setText(label_msg)
		lbTitle.setStyleSheet('''
					front-size: 30px;
					margin: 20px auto;
					coror: purple;
					''')
		lbTitle.setAligment(qtc.Qt.AlignCenter)
		# filter box layout:
		filterLabel = qtw.QLabel('Filter by column: ')
		filterLineEdit = qtw.QLineEdit()
		filterLineEdit.textChanged.connect(self.tableView.filter_proxy_model.setFilterRegExp)

		comboBox = qtw.QComboBox()
		comboBox.addItems(["{0}".format(col) for col in self.tableView.column_names])
		comboBox.setCurrentText('title')
		comboBox.currentIndexChanged.connect(lambda idx:self.tableView.set_filter_column(idx))

		filterBoxLayout = qtw.QHBoxLayout()
		filterBoxLayout.addWidget(filterLabel)
		filterBoxLayout.addWidget(comboBox)
		filterBoxLayout.addWidget(filterLineEdit)

		# close button
		btnClose = qtw.QPushButton('Close')
		# btnClose.clicked.connect(self.close_all)
		# or with lambda syntax
		btnClose.clicked.connect( lambda _:self.close() and self.parent.close() )

		# main layout
		layout = qtw.QVBoxLayout()
		layout.addWidget('lblTitle')
		layout.addLayout(filterBoxLayout)
		layout.addWidget(self.tableView)
		layout.addWidget(btnClose)

		self.setLayout(layout)

		self.setFixedWidth('tableViewWidth')
		# self.setFixedHeight(tableViewHeight)

	def close_all(self):
			self.parent.close()
			self.close()	

	@qtc.pyqtSlot(int)
	def on_comboBox_currentIndexChanged(self,index):
		self.tableView.filter_proxy_model.setFilterKeyColumn(index)

		def get_current_datetime(self):
			return datetime.datetime.now().strftime('%d.%m.%y, %H:%M:%S')


class MainWindow(qtw.QMainWindow):
	def __init__(self , *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.crawler = Crawler()

		self.setWindowTitle('Car_search Crawler')


		### Main layout
		mainLayout = qtw.QVBoxLayout()

		### Table Caption part:
		lblTableCaption = qtw.QLabel('Car_search Data')
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
		#self.lblStatus.show()
		#qtw.QApplication.processEvents()  # needed to force processEvents

		# start crawler
		self.crawler.run()
		self.setCursor(qtc.Qt.ArrowCursor)

		# if crawler ready:
		if self.crawler.status:
			self.lblStatus.setText('Ready!')
			self.btnShowData.setEnabled(True)

		self.setCursor(qtc.Qt.ArrowCursor)


if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())


