import datetime
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from Lib.db import DB



class TableView(qtw.QTableView):
	def __init__(self, *args, **kwargs):
		super().__init__()

		self.db = DB()

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
		self.resizeColumnToContents(0)
		self.resizeColumnToContents(1)
		# set width of separate columns:
		self.setColumnWidth(3, 300)


		### streach table:
		# self.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
		# self.horizontalHeader().setStretchLastSection(True)
		# self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
		self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)

		### enable columns sort
		self.setSortingEnabled(True)
		# set default sorting by column 0:
		self.sortByColumn(0,qtc.Qt.AscendingOrder)

	def setup_model(self):
		model = qtg.QStandardItemModel()
		model.setHorizontalHeaderLabels(self.column_names)

			# [
			# 	['title1', dateobj,'....']
			# ]

		for i, row in enumerate(self.data):

			# items = [qtg.QStandardItem(str(item)) for item in row]

			items = []
			for field in row:

				item = qtg.QStandardItem()

				##	field = field.strftime('%d.%m.%Y')
				#elif isinstance(field, str) and len(field)>100:
				#	# set full string with ToolTipRole:
				#	item.setData(field, qtc.Qt.ToolTipRole)
				#	# trim string for display
				#	field = field[0:50]+'...'

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
	def __init__(self, parent, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parent = parent

		self.setup_gui()

	def setup_gui(self):
		### init table view:
		self.tableView = TableView()

		### make label
		lblTitle = qtw.QLabel()
		label_msg = f'Radiotheaters publications as crawlled on {self.tableView.get_last_updated_date()}'
		lblTitle.setText(label_msg)
		lblTitle.setStyleSheet('''
			font-size: 30px;
			margin:20px auto;
			color: purple;

		''')
		lblTitle.setAlignment(qtc.Qt.AlignCenter)

		### filter box layout:
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

		### close button
		btnClose = qtw.QPushButton('Close')
		btnClose.clicked.connect(self.close_all)

		### main layout
		layout = qtw.QVBoxLayout()
		layout.addWidget(lblTitle)
		layout.addLayout(filterBoxLayout)
		layout.addWidget(self.tableView)
		layout.addWidget(btnClose)

		self.setLayout(layout)

		### set Table Widget size:
		# tableViewWidth = self.tableView.frameGeometry().width()
		# tableViewHeight = self.tableView.frameGeometry().height()
		# self.setFixedWidth(tableViewWidth)
		# self.setFixedHeight(tableViewHeight)

	def close_all(self):
		self.parent.close()
		self.close()

	@qtc.pyqtSlot(int)
	def on_comboBox_currentIndexChanged(self,index):
		self.tableView.filter_proxy_model.setFilterKeyColumn(index)


	def get_current_datetime(self):
		return datetime.datetime.now().strftime('%d.%m.%y, %H:%M:%S')