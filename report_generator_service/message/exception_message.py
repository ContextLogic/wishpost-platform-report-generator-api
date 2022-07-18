from wish_flask.lib.py_enum import PyEnumMixin

class ExceptionMessage(PyEnumMixin):
    DuplicateReportName = "Report Name Duplicated."
    DuplicateReportVersion = "Report Version Duplicated."
    InvalidGoogleSheetUrl = "Invalid Google Sheet Url."
    ReportNotFound = "Report Not Found."
    TemplateNotFound = "Template Not Found."
    VersionNotFound = "Version Not Found."
    VersionArchived = "Version is set to archived."
    VersionActivated = "Version is activated, active another version first."
