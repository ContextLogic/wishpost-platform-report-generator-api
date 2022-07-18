from marshmallow import validates_schema
from wish_flask.base.dataclasses import dataclass
from marshmallow.exceptions import ValidationError

@dataclass
class AddReportTemplateRequest(object):
    report_name: str
    version: str
    google_sheet_url: str
    user: str

    @validates_schema
    def validate_request(self, data, **kwargs):
        if not data.get('report_name') or not data.get('version') or not data.get('google_sheet_url'):
            raise ValidationError('Either of report_name or version or google_sheet_url must not be blank', self.__class__.__name__)

@dataclass
class TemplateStatusRequest(object):
    report_id: str
    user: str

    @validates_schema
    def validate_request(self, data, **kwargs):
        if not data.get('report_id'):
            raise ValidationError('report_id must not be blank', self.__class__.__name__)

@dataclass
class VersionStatusRequest(object):
    report_id: str
    version_id: str
    user: str

    @validates_schema
    def validate_request(self, data, **kwargs):
        if not data.get('report_id') or not data.get('version_id'):
            raise ValidationError('Either of report_id or version_id must not be blank', self.__class__.__name__)

@dataclass
class GenerateReportByTemplateRequest(object):
    report_name: str
    data_source_url: str
    version: str

@dataclass
class GenerateReportByTemplateRequestRS(object):
    message: str
    url: str