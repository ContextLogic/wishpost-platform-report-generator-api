from pydoc import resolve
from urllib import response
from httplib2 import Authentication
import oauthlib
from wish_flask.base.blueprint import WishBlueprint
from wish_flask.lib.instance_manager import InstanceManager

from report_generator_service.schemas.general import GeneralMessageResponse
from report_generator_service.schemas.template import ListTemplateResponse, TemplateDetailResponse, TemplateQueryByIdReuest, TemplateStatusRequest, AddReportTemplateRequest, VersionStatusRequest
from report_generator_service.services.template_service import TemplateService

template_blp = WishBlueprint(
    'template', __name__, url_prefix='/api/template',
    # micro=True,
    description='Operations on template'
)

template_service: TemplateService = InstanceManager.find_obj_proxy(instance_type='template_service')

@template_blp.route('/add', methods=['POST'])
@template_blp.arguments(AddReportTemplateRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def add_new_report_template(request: AddReportTemplateRequest):
    return template_service.add_new_report_template(request.report_name, request.version, request.google_sheet_url, request.user)

@template_blp.route('/add-version', methods=['POST'])
@template_blp.arguments(AddReportTemplateRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def add_report_template(request: AddReportTemplateRequest):
    return template_service.add_template_version(request.report_name, request.version, request.google_sheet_url, request.user)

@template_blp.route('/activiate-template', methods=['POST'])
@template_blp.arguments(TemplateStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def activate_report(request: TemplateStatusRequest):
    return template_service.activate_template(request.report_id, request.user)

@template_blp.route('/archive-template', methods=['POST'])
@template_blp.arguments(TemplateStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def archive_report(request: TemplateStatusRequest):
    return template_service.archive_template(request.report_id, request.user)


@template_blp.route('/activate-version', methods=['POST'])
@template_blp.arguments(VersionStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def activate_version(request:VersionStatusRequest):
    return template_service.activate_template_version(request.report_id, request.version, request.user)

@template_blp.route('/archive-version', methods=['POST'])
@template_blp.arguments(VersionStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def activate_version(request:VersionStatusRequest):
    return template_service.archive_template_version(request.report_id, request.version, request.user)

@template_blp.route('/list/archived-template', methods=['GET'])
@template_blp.response(data_clz=ListTemplateResponse)
def get_report_template_archive_list():
    return template_service.get_archive_report_templates()

@template_blp.route('/list', methods=['GET'])
@template_blp.response(data_clz=ListTemplateResponse)
def get_report_template_active_list():
    return template_service.get_active_report_templates()

@template_blp.route('/get-template-detail', methods=['GET'])
@template_blp.arguments(TemplateQueryByIdReuest, location='query')
@template_blp.response(data_clz=TemplateDetailResponse)
def get_report_template_by_id(request:TemplateQueryByIdReuest):
    return template_service.get_report_template_by_id(request.template_id)