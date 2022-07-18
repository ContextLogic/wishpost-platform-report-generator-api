from exceptions.errors import Error
from wish_flask.exceptions.api_exception import ApiException
from wish_flask.i18n import _

from report_generator_service.message.exception_message import ExceptionMessage

class UserException(ApiException):
   def __init__(self, code, msg, data=None, **kwargs):
      super().__init__(code=code, msg=msg, data=data, **kwargs)

class DuplicateReportNameException(UserException):
   def __init__(self, data=None, **kwargs):
      super().__init__(Error.DUPLICATE_REPORT_NAME, msg=_(ExceptionMessage.DuplicateReportName), data=data, **kwargs)

class DuplicateReportVersionException(UserException):
   def __init__(self, data=None, **kwargs):
      super().__init__(Error.DUPLICATE_REPORT_VERSION, msg=_(ExceptionMessage.DuplicateReportVersion), data=data, **kwargs)

class InvalidGoogleSheetUrlException(UserException):
   def __init__(self, data=None, **kwargs):
      super().__init__(Error.INVALID_GOOGLE_URL, msg=_(ExceptionMessage.InvalidGoogleSheetUrl), data=data, **kwargs)

class TemplateNotFound(UserException):
   def __init__(self, data=None, **kwargs):
      super().__init__(Error.TEMPLATE_NOT_FOUND, msg=_(ExceptionMessage.TemplateNotFound), data=data, **kwargs)

class VersionNotFound(UserException):
   def __init__(self, data=None, **kwargs):
      super().__init__(Error.VERSION_NOT_FOUND, msg=_(ExceptionMessage.VersionNotFound), data=data, **kwargs)

class VersionArchived(UserException):
   def __init__(self, data=None, **kwargs):
      super().__init__(Error.VERSION_ARCHIVED, msg=_(ExceptionMessage.VersionArchived), data=data, **kwargs)

class VersionActivated(UserException):
   def __init__(self, data=None, **kwargs):
      super().__init__(Error.VERSION_ACTIVE, msg=_(ExceptionMessage.VersionActivated), data=data, **kwargs)
