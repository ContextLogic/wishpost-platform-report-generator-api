import datetime
import typing
from marshmallow import validates_schema
from wish_flask.base.dataclasses import dataclass, field
from wish_flask.base.field_validators import NotBlank
from marshmallow.exceptions import ValidationError

from report_generator_service.enums.report_template_status_enum import ReportTemplateStatus, TemplateVersionStatus

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
    version: str
    user: str

    @validates_schema
    def validate_request(self, data, **kwargs):
        if not data.get('report_id') or not data.get('version'):
            raise ValidationError('Either of report_id or version must not be blank', self.__class__.__name__)

@dataclass
class TemplateVersionDTO(object):
    version: str
    google_sheet_url: str
    s3_url: str
    status: TemplateVersionStatus
    added_by: str
    report_generated: int
    last_generated_time_stamp: datetime.datetime

@dataclass
class TemplateReportDTO(object):
    report_name: str
    created_by: str
    updated_by: str
    active_version: str
    version_list: typing.List[TemplateVersionDTO]
    status: ReportTemplateStatus
    last_generated_time_stamp: datetime.datetime

@dataclass
class ListTemplateResponse(object):
    total: int
    template_list: typing.List[TemplateReportDTO]

@dataclass
class TemplateQueryByIdReuest(object):
    template_id: str = field(validate=NotBlank())

@dataclass
class TemplateDetailResponse(object):
    report_name: str
    created_by: str
    updated_by: str
    active_version: str
    version_list: typing.List[TemplateVersionDTO]
    status: ReportTemplateStatus
    last_generated_time_stamp: datetime.datetime

@dataclass
class GenerateReportByTemplateRequest(object):
    report_name: str
    data_source_url: str
    version: str

@dataclass
class GenerateReportByTemplateRequestRS(object):
    message: str
    url: str