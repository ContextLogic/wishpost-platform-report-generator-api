from wish_flask.exceptions.errors import Errors as FlaskErrors

class Error(FlaskErrors):
    DUPLICATE_REPORT_NAME = 1001
    DUPLICATE_REPORT_VERSION = 1002
    INVALID_GOOGLE_URL = 1003
    REPORT_NAME_NOT_FOUND = 1004