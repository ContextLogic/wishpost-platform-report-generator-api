from pydoc import resolve
from urllib import response
from httplib2 import Authentication
import oauthlib
from wish_flask.base.blueprint import WishBlueprint
from wish_flask.lib.instance_manager import InstanceManager

from report_generator_service.schemas.general import GeneralMessageResponse
from report_generator_service.schemas.template import TemplateStatusRequest, AddReportTemplateRequest
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



@template_blp.route('/activiate-report', methods=['POST'])
@template_blp.arguments(TemplateStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def set_template_active(request: TemplateStatusRequest):
    return template_service.activate_report(request.report_id, request.version_id)


@template_blp.route('/activiate-template', methods=['POST'])
@template_blp.arguments(TemplateStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def set_template_active(request: TemplateStatusRequest):
    response = template_service.activate_report_template(request.template_id)
    raise response

@template_blp.route('/archive-report', methods=['POST'])
@template_blp.arguments(TemplateStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def set_template_archive(request: TemplateStatusRequest):
    response = template_service.archive_report_template(request.template_id)
    return response

@template_blp.route('/archive-template', methods=['POST'])
@template_blp.arguments(TemplateStatusRequest)
@template_blp.response(data_clz=GeneralMessageResponse)
def set_template_archive(request: TemplateStatusRequest):
    response = template_service.archive_report_template(request.template_id)
    return response

@template_blp.route('/list/archived-report', methods=['GET'])
def get_report_template_active_list():
    raise NotImplementedError

@template_blp.route('/list/report', methods=['GET'])
def get_report_template_active_list():
    raise NotImplementedError

@template_blp.route('/get-report-detail', methods=['GET'])
def get_report_template_list_all():
    raise NotImplementedError