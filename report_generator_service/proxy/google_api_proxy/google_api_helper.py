from collections import namedtuple
from wish_flask.lib.py_enum import PyEnumMixin

class GoogleApiName(PyEnumMixin):
	SHEETS = "sheets"
	DRIVE = "drive"

class GoogleApiScpoes(PyEnumMixin):
	SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	DRIVE_SCOPE = ['https://www.googleapis.com/auth/drive']

class GoogleApiVersion(PyEnumMixin):
	API_VERSION_V4 = "v4"
	API_VERSION_V3 = "v3"

class GoogleApiMemeType(PyEnumMixin):
	SPREADSHEET = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

class GoogleSheetsHelper:
	# --> spreadsheets().batchUpdate()
	Paste_Type = namedtuple('_Paste_Type', 
					('normal', 'value', 'format', 'without_borders', 
					 'formula', 'date_validation', 'conditional_formatting')
					)('PASTE_NORMAL', 'PASTE_VALUES', 'PASTE_FORMAT', 'PASTE_NO_BORDERS', 
					  'PASTE_FORMULA', 'PASTE_DATA_VALIDATION', 'PASTE_CONDITIONAL_FORMATTING')

	Paste_Orientation = namedtuple('_Paste_Orientation', ('normal', 'transpose'))('NORMAL', 'TRANSPOSE')

	Merge_Type = namedtuple('_Merge_Type', ('merge_all', 'merge_columns', 'merge_rows')
					)('MERGE_ALL', 'MERGE_COLUMNS', 'MERGE_ROWS')

	Delimiter_Type = namedtuple('_Delimiter_Type', ('comma', 'semicolon', 'period', 'space', 'custom', 'auto_detect')
						)('COMMA', 'SEMICOLON', 'PERIOD', 'SPACE', 'CUSTOM', 'AUTODETECT')

	# --> Types
	Dimension = namedtuple('_Dimension', ('rows', 'columns'))('ROWS', 'COLUMNS')

	Value_Input_Option = namedtuple('_Value_Input_Option', ('raw', 'user_entered'))('RAW', 'USER_ENTERED')

	Value_Render_Option = namedtuple('_Value_Render_Option',["formatted", "unformatted", "formula"]
							)("FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA")
                            
	@staticmethod
	def define_cell_range(
		sheet_id, 
		start_row_number=1, end_row_number=0, 
		start_column_number=None, end_column_number=0):
		"""GridRange object"""
		json_body = {
			'sheetId': sheet_id,
			'startRowIndex': start_row_number - 1,
			'endRowIndex': end_row_number,
			'startColumnIndex': start_column_number - 1,
			'endColumnIndex': end_column_number
		}
		return json_body

	@staticmethod
	def define_dimension_range(sheet_id, dimension, start_index, end_index):
		json_body = {
			'sheetId': sheet_id,
			'dimension': dimension,
			'startIndex': start_index,
			'endIndex': end_index
		}
		return json_body

class GoogleCalendarHelper:
	...

class GoogleDriverHelper:
	...

if __name__ == '__main__':
	g = GoogleSheetsHelper()
	print(g.Delimiter_Type)