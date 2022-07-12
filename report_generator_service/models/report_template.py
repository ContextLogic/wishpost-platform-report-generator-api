from sqlalchemy import false, true
from report_generator_service.enums.report_template_status_enum import ReportTemplateStatus
from report_generator_service.exceptions.api_exception import DuplicateTemplateException

try:
    # Try import mongo in case that it is not installed.
    from flask_mongoengine import Document
except:
    Document = None

if Document:
    from mongoengine import ObjectIdField, StringField, EnumField
    from wish_flask.extensions.mongo.operation import MongoOperation

    class ReportTemplate(Document, MongoOperation):

        report_name = StringField(required=True)
        version = StringField(required=True)
        google_sheet_url = StringField(required=True)
        s3_url = StringField()
        status = EnumField(ReportTemplateStatus, default=ReportTemplateStatus.INACTIVE)

        @classmethod
        def save_new_template(cls, report_name: str, version: str, google_sheet_url: str, s3_url: str=None, status=ReportTemplateStatus.INACTIVE):
            cls(
                report_name=report_name,
                version=version,
                google_sheet_url=google_sheet_url,
                s3_url=s3_url,
                status=status
            ).save()

        @classmethod
        def check_duplicate(cls, report_name: str, version: str):
            templates = cls.find({"report_name": report_name, "version": version})
            if len(templates) > 0:
                return True
            return False

        @classmethod
        def get_active_template_by_name():
            pass

        @classmethod
        def get_template_by_name():
            pass
        
        @classmethod
        def save_new_active_template():
            pass

        @classmethod
        def activiate_template():
            pass

        @classmethod
        def update_template_s3_url():
            pass