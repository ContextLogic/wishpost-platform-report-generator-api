from bson.objectid import ObjectId
from report_generator_service.enums.report_template_status_enum import ReportTemplateStatus, ReportStatus
from flask_mongoengine import Document
from mongoengine import ObjectIdField, IntField, DateField, ListField, EnumField, StringField, EmbeddedDocument, EmbeddedDocumentField
from wish_flask.extensions.mongo.operation import MongoOperation

class TemplateVersion(EmbeddedDocument, MongoOperation):
    _id = ObjectIdField(required=True, default=ObjectId)
    version = StringField(required=True)
    google_sheet_url = StringField(required=True)
    s3_url = StringField()
    status = EnumField(ReportTemplateStatus, default=ReportTemplateStatus.NORMAL)
    added_by = StringField(required=True)
    report_generated = IntField(default=0)
    last_generated_time_stamp = DateField()

    @classmethod
    def create_new_version(cls, version: str, google_sheet_url: str, user: str, s3_url: str=None):
        return cls(
            version = version,
            google_sheet_url = google_sheet_url,
            s3_url = s3_url,
            added_by = user
        )

class ReportTemplate(Document, MongoOperation):
    report_name = StringField(required=True)
    created_by = StringField(required=True)
    updated_by = StringField()
    active_version = ObjectIdField(required=True)
    version_list = ListField(EmbeddedDocumentField(TemplateVersion), required=True)
    status = EnumField(ReportStatus, default=ReportStatus.NORMAL)
    last_generated_time_stamp = DateField()
    
    @classmethod
    def save_new_report_template(cls, report_name: str, version: str, google_sheet_url: str, user: str, s3_url: str=None):
        new_version = TemplateVersion.create_new_version(version, google_sheet_url, user, s3_url)
        cls(
            report_name = report_name,
            created_by = user,
            active_version = new_version._id,
            version_list = [new_version]
        ).save()

    @classmethod
    def save_new_template_version(cls, report_name: str, version: str, google_sheet_url: str, user: str, s3_url: str=None):
        template = cls.find_one({"report_name": report_name})
        new_version = TemplateVersion.create_new_version(version, google_sheet_url, user, s3_url)
        version_list = template.version_list
        version_list.append(new_version)
        template.update_one({"$set" : {"version_list" : version_list}})

    @classmethod
    def check_duplicate_report_name(cls, report_name: str):
        template = cls.find_one({"report_name": report_name})
        if template:
            return True
        return False

    @classmethod
    def check_duplicate_version(cls, report_name: str, version: str):
        template = cls.find_one({"report_name": report_name})
        if not template:
            return False
        for existing_version in template.version_list:
            if existing_version.version == version:
                return True
        return False

    @classmethod
    def activiate_report(report_id:str, version_id:str):
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
