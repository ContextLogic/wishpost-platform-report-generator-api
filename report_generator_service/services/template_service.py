from email import message
from wish_flask.base.service import BaseService
from wish_flask.lib.s3.abstract_s3 import BaseS3Abstraction
from wish_flask.extensions.s3.instance import s3_real as s3
s3: BaseS3Abstraction
from wish_flask.log.meta import LoggingMixin

from report_generator_service.schemas.general import GeneralMessageResponse
from report_generator_service.enums.report_template_status_enum import TemplateVersionStatus, ReportTemplateStatus
from report_generator_service.exceptions.api_exception import DuplicateReportNameException, DuplicateReportVersionException, UserException
from report_generator_service.message.template_message import TemplateMessage
from report_generator_service.models.report_template import ReportTemplate
from report_generator_service.proxy.google_api_proxy.google_api_proxy import GoogleApiProxy
from report_generator_service.s3.key_folders import KeyFolders
from report_generator_service.s3.buckets import Buckets

class TemplateService(BaseService, LoggingMixin):
    auto_init = True

    def add_new_report_template(self, report_name:str, version:str, google_sheet_url:str, user:str):
        try:
            if ReportTemplate.check_duplicate_report_name(report_name):
                raise DuplicateReportNameException()

            filename = report_name + "-" + version + ".xlsx"
            byte_data = GoogleApiProxy.download_google_sheet(google_sheet_url)
            s3_url = self.save_template_to_s3(filename, byte_data)
            ReportTemplate.save_new_report_template(report_name, version, google_sheet_url, user, s3_url=s3_url)  
        except UserException as user_exception:
            raise user_exception
        except Exception as ex:
            self.logger.error(ex)
            raise ex
            
        return GeneralMessageResponse(message=TemplateMessage.NewReportAdded.format(report_name, version))

    def add_template_version(self, report_name:str, version:str, google_sheet_url:str, user:str):
        try:
            if ReportTemplate.check_duplicate_version(report_name, version):
                raise DuplicateReportVersionException()

            filename = report_name + "-" + version + ".xlsx"
            byte_data = GoogleApiProxy.download_google_sheet(google_sheet_url)
            s3_url = self.save_template_to_s3(filename, byte_data)
            ReportTemplate.save_new_template_version(report_name, version, google_sheet_url, user, s3_url=s3_url)
        except UserException as user_exception:
            raise user_exception
        except Exception as ex:
            self.logger.error(ex)
            raise ex
        
        return GeneralMessageResponse(message=TemplateMessage.NewTemplateAdded.format(report_name, version))
    
    def activate_template(self, template_id:str, user:str):
        try:
            ReportTemplate.set_template_status(template_id, ReportTemplateStatus.NORMAL, user)   
            template = ReportTemplate.get_template_by_id(template_id)
        except UserException as user_exception:
            raise user_exception
        except Exception as ex:
            self.logger.error(ex)
            raise ex
        
        return GeneralMessageResponse(message=TemplateMessage.TemplateActivated.format(template.report_name))

    def archive_template(self, template_id:str, user:str):
        try:
            report_name = ReportTemplate.set_template_status(template_id, ReportTemplateStatus.ARCHIVE, user)   
        except UserException as user_exception:
            raise user_exception
        except Exception as ex:
            self.logger.error(ex)
            raise ex
        
        return GeneralMessageResponse(message=TemplateMessage.TemplateArchived.format(report_name))

    def activate_template_version(self, template_id:str, version_id:str, user:str):
        try:
            report_name, version = ReportTemplate.activate_template_version(template_id, version_id, user)
        except UserException as user_exception:
            raise user_exception
        except Exception as ex:
            self.logger.error(ex)
            raise ex

        return GeneralMessageResponse(message=TemplateMessage.VersionActivated.format(report_name, version))

    def archive_template_version(self, template_id:str, version_id:str, user:str):
        try:
            report_name, version = ReportTemplate.archive_template_version(template_id, version_id, user)
        except UserException as user_exception:
            raise user_exception
        except Exception as ex:
            self.logger.error(ex)
            raise ex
        
        return GeneralMessageResponse(message=TemplateMessage.VersionArchived.format(report_name, version))

    def find_report_template_by_name(self, template_name: str):
        raise NotImplementedError

    def save_template_to_s3(self, filename: str, byte_data):
        file_path = KeyFolders.REPORT_TEMPLATE.key(filename)
        if not s3.exists(Buckets.FINANCE_DATA, file_path):
            s3.save(Buckets.FINANCE_DATA, file_path, byte_data)
        return s3.generate_fetching_url(Buckets.FINANCE_DATA, file_path)