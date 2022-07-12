from marshmallow import validates_schema
from wish_flask.base.dataclasses import dataclass
from marshmallow.exceptions import ValidationError

@dataclass
class AddReportTemplateRequest(object):
    report_name: str
    version: str
    google_sheet_url: str

    @validates_schema
    def validate_request(self, data, **kwargs):
        if not data.get('report_name') or not data.get('version') or not data.get('google_sheet_url'):
            raise ValidationError('Either of report_name or version or google_sheet_url must be not blank', self.__class__.__name__)


@dataclass
class AddReportTemplateRequestRS(object):
    message: str

@dataclass
class GenerateReportByTemplateRequest(object):
    report_name: str
    data_source_url: str
    version: str

@dataclass
class GenerateReportByTemplateRequestRS(object):
    message: str
    url: str