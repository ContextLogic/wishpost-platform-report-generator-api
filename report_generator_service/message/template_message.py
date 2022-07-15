from wish_flask.lib.py_enum import PyEnumMixin

class TemplateMessage(PyEnumMixin):
    NewReportAdded = "New Report {0} with version {1} Created."
    NewTemplateAdded = "{0} with version {1} added."