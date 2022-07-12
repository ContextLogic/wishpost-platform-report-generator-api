from wish_flask.base.service import BaseService
from wish_flask.extensions.s3.instance import s3

from report_generator_service.exceptions.api_exception import DuplicateTemplateException
from report_generator_service.models.report_template import ReportTemplate
from report_generator_service.proxy.google_api_proxy.google_api_proxy import GoogleApiProxy
from report_generator_service.s3 import key_folders
from report_generator_service.s3.buckets import Buckets

class ReportService(BaseService):
    auto_init = True


    