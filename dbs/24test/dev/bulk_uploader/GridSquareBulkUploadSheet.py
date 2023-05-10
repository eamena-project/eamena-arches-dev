from eamena.bulk_uploader import BulkUploadSheet
import json, uuid, re, urllib.request, sys

class GridSquareBulkUploadSheet(BulkUploadSheet):

	def data(self, index):

		return super().data(index)

	def __boolean_cast(self, text):
		t = str(text).lower()
		if t == 'yes':
			return True
		if t == '1':
			return True
		if t == 'true':
			return True
		if t == 'y':
			return True
		return False

	def __init__(self, filename, uidkey='Grid ID'):

		super().__init__(filename, uidkey)
		self.__required_fields = ["Grid ID", "GRID_SQUARE_GEOMETRIC_PLACE_EXPRESSION"]
		for i in range(0, len(self._BulkUploadSheet__data)):
			for row in range(0, len(self._BulkUploadSheet__data[i])):
				for field in self.__required_fields:
					if field in self._BulkUploadSheet__data[i][row]:
						continue
					self._BulkUploadSheet__data[i][row][field] = ''
