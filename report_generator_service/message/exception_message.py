from wish_flask.lib.py_enum import PyEnumMixin

class ExceptionMessage(PyEnumMixin):
    DuplicateReportName = "Report Name Duplicated."
    DuplicateReportVersion = "Report Version Duplicated."
    InvalidGoogleSheetUrl = "Invalid Google Sheet Url."