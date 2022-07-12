import imp
from exceptions.errors import Error
from wish_flask.exceptions.api_exception import ApiException
from wish_flask.i18n import _

class DuplicateTemplateException(ApiException):
     def __init__(self, data=None, **kwargs):
        super().__init__(Error.DUPLICATE_TEMPLATE, msg=_('Template Duplicated'), data=data, **kwargs)
