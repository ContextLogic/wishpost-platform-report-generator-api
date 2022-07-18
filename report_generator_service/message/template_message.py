from wish_flask.lib.py_enum import PyEnumMixin

class TemplateMessage(PyEnumMixin):
    NewReportAdded = "New Report [{0}] with version [{1}] Created."
    NewTemplateAdded = "Report template [{0}] with version [{1}] added."
    TemplateActivated = "Report template [{0}] activated."
    VersionActivated = "Report template [{0}] with version [{1}] activated."
    TemplateArchived = "Report template [{0}] archived."
    VersionArchived = "Report template [{0}] with version [{1}] archived."