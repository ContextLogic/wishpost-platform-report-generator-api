from wish_flask.base.service import BaseService
from wish_flask.extensions.s3.instance import s3_real as s3

from report_generator_service.exceptions.api_exception import DuplicateTemplateException
from report_generator_service.models.report_template import ReportTemplate
from report_generator_service.proxy.google_api_proxy.google_api_proxy import GoogleApiProxy
from report_generator_service.s3 import key_folders
from report_generator_service.s3.buckets import Buckets

class TemplateService(BaseService):
    auto_init = True

    def add_report_template(self, report_name: str, version: str, google_sheet_url: str):
        if ReportTemplate.check_duplicate(report_name, version):
            raise DuplicateTemplateException()

        try:
            filename = report_name + "-" + version + ".xlsx"
            print(filename)
            byte_date = GoogleApiProxy.download_google_sheet(google_sheet_url)
            file_path = key_folders.REPORT_TEMPLATE.key(filename)
            s3.save(Buckets.DATA, file_path, byte_date)
            url = s3.generate_fetching_url(Buckets.DATA, file_path)
            ReportTemplate.save_new_template(report_name, version, google_sheet_url, s3_url=url)
        except Exception as ex:
            print(str(ex.message))
        
    
    def find_report_template_by_name(self, template_name: str):
        raise NotImplementedError

    def save_template_to_s3(self):
        raise NotImplementedError

    def download_template_from_google(self):
        raise NotImplementedError

    def download_template_from_s3(self):
        raise NotImplementedError