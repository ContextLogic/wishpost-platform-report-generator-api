from bson.objectid import ObjectId
from flask_mongoengine import Document
from mongoengine import ObjectIdField, IntField, DateField, ListField, EnumField, StringField, EmbeddedDocument, EmbeddedDocumentField
from wish_flask.extensions.mongo.operation import MongoOperation

from report_generator_service.exceptions.api_exception import TemplateNotFound, VersionActivated, VersionArchived, VersionNotFound
from report_generator_service.enums.report_template_status_enum import ReportTemplateStatus, TemplateVersionStatus

class TemplateVersion(EmbeddedDocument, MongoOperation):
    _id = ObjectIdField(required=True, default=ObjectId)
    version = StringField(required=True)
    google_sheet_url = StringField(required=True)
    s3_url = StringField()
    status = EnumField(TemplateVersionStatus, default=TemplateVersionStatus.NORMAL)
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
    status = EnumField(ReportTemplateStatus, default=ReportTemplateStatus.NORMAL)
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
    def save_new_template_version(cls, report_name:str, version:str, google_sheet_url:str, user:str, s3_url:str=None):
        template = cls.find_one({"report_name": report_name})
        new_version = TemplateVersion.create_new_version(version, google_sheet_url, user, s3_url)
        version_list = template.version_list
        version_list.append(new_version)
        template.update_one({"$set" : {"version_list" : version_list}})

    @classmethod
    def check_duplicate_report_name(cls, report_name:str):
        template = cls.find_one({"report_name": report_name})
        if template:
            return True
        return False

    @classmethod
    def check_duplicate_version(cls, report_name:str, version:str):
        template = cls.find_one({"report_name": report_name})
        if not template:
            raise TemplateNotFound()
        for existing_version in template.version_list:
            if existing_version.version == version:
                return True
        return False

    @classmethod
    def get_template_by_id(cls, template_id:str):
        template = cls.find_one({"id": template_id})
        if not template:
            raise TemplateNotFound()
        return template

    @classmethod
    def set_template_status(cls, template_id:str, status:ReportTemplateStatus, user:str):
        template = cls.get_template_by_id(template_id)
        if template.status != status:
            template.update_one({"$set" : {"status": status, "updated_by": user}})
            return template.report_name
    
    @classmethod
    def activate_template_version(cls, template_id:str, version_id:str, user:str):
        template = cls.get_template_by_id(template_id)
        if template.active_version == version_id:
            return
        for version in template.version_list:
            if str(version._id) == version_id:
                if version.status == TemplateVersionStatus.ARCHIVE:
                    raise VersionArchived()
                template.update_one({"$set" : {"active_version": version._id, "updated_by": user}})
                return template.report_name, version.version
        raise VersionNotFound()

    @classmethod
    def archive_template_version(cls, template_id:str, version_id:str, user:str):
        template = cls.get_template_by_id(template_id)
        if template.active_version == version_id:
            raise VersionActivated()
        ReportTemplate.update_doc({"id":template_id, "version_list._id":version_id},{"$set" : {"version_list.$.status":TemplateVersionStatus.ARCHIVE}})
        # for version in template.version_list:
        #     if str(version._id) == version_id and version.status != TemplateVersionStatus.ARCHIVE:
        #         TemplateVersion.update_doc({"_id":version_id},{"$set" : {"status": TemplateVersionStatus.ARCHIVE}})
        #         return template.report_name, version.version
        raise VersionNotFound()
