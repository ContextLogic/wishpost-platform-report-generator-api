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
      super().__init__(Error.INVALIDGOOGLEURL, msg=_(ExceptionMessage.InvalidGoogleSheetUrl), data=data, **kwargs)
