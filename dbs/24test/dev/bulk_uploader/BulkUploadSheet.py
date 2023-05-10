from openpyxl.cell import Cell, MergedCell
from openpyxl import load_workbook
import json, uuid, re, urllib.request, warnings

class BulkUploadSheet:

	def count(self):

		return len(self.__data)

	def data(self, index):

		return self.__data[index]

	def columns(self):

		return self.__headers

	def error(self, ref, error, hint):

		self.__errors.append([ref, error, hint])

	def errors(self):

		ret = []
		for item in self.__errors:
			ret.append(item)
		return ret

	def pre_parse(self, index, columns, exclude=[]):

		unparsed = self.__data[index]

		ret = []
		pre_ret = []
		for item in unparsed:
			retitem = {}
			for column in columns:
				if not(column in item):
					retitem[column] = ['']
					continue
				if column in exclude:
					retitem[column] = [item[column]]
				else:
					retitem[column] = item[column].split('|')
			pre_ret.append(retitem)

		for item in pre_ret:
			row_count = 1
			for column in columns:
				c = len(item[column])
				if c > row_count:
					row_count = c
			for i in range(0, row_count):
				retitem = {}
				for column in columns:
					if i >= len(item[column]):
						retitem[column] = ''
					else:
						value = item[column][i].strip()
						retitem[column] = value
				ret.append(retitem)

		return ret

	def __init__(self, filename, uidkey='UNIQUEID'):

		self.__uidkey = uidkey
		self.__data = []
		self.__headers = []
		self.__errors = []

		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			wb = load_workbook(filename)
		sheet = wb.active
		headers = []
		hidden_columns = []
		for colid in sheet.column_dimensions:
			col = sheet.column_dimensions[colid]
			w = col.width
			if ((w == 0) or col.hidden):
				hidden_columns.append(str(colid))
		in_headers = True
		row_dict = {}
		last_id = ''
		skipped_rows = 0
		for row in sheet.rows:
			if skipped_rows > 100: # We have over 100 empty rows, it's pretty safe to assume the rest of the sheet is empty.
				break
			rowlist = []
			last = ''
			colid = ''
			for cell in row:
				if isinstance(cell, Cell):
					last = ''
					colid = cell.column_letter
					if cell.value:
						last = str(cell.value)
				if colid in hidden_columns:
					rowlist.append('')
				else:
					rowlist.append(last)
			if in_headers:
				headers = rowlist
				if uidkey in rowlist:
					in_headers = False
				continue
			if len(''.join(rowlist)) == 0:
				skipped_rows = skipped_rows + 1
				continue
			skipped_rows = 0 # Reset skipped row count to 0
			item = {}
			for i in range(0, len(rowlist)):
				header_key = headers[i]
				if header_key != uidkey:
					header_key = re.sub(r'[^A-Z_]+', '_', header_key.replace(' ', '_').upper().strip('_'))
				item[header_key] = rowlist[i]
				if not(header_key in self.__headers):
					self.__headers.append(header_key)
			if uidkey in item:
				if item[uidkey] == '':
					item[uidkey] = last_id
				else:
					last_id = item[uidkey]
			else:
				item[uidkey] = last_id
			if not(item[uidkey] in row_dict):
				row_dict[item[uidkey]] = []
			row_dict[item[uidkey]].append(item)
		for row_key in row_dict.keys():
			key = str(row_key)
			item = row_dict[key]
			#if uidkey in item:
				#del item[uidkey]
			self.__data.append(item)
