from wish_flask.exceptions.errors import Errors as FlaskErrors

class Error(FlaskErrors):
    DUPLICATE_TEMPLATE = 1001