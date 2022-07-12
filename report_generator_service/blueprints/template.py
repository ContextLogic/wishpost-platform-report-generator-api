from wish_flask.base.blueprint import WishBlueprint
from wish_flask.lib.instance_manager import InstanceManager

from report_generator_service.schemas.report import AddReportTemplateRequest, AddReportTemplateRequestRS
from report_generator_service.services.template_service import TemplateService

template_blp = WishBlueprint(
    'template', __name__, url_prefix='/api/template',
    # micro=True,
    description='Operations on template'
)

template_service: TemplateService = InstanceManager.find_obj_proxy(instance_type='template_service')

@template_blp.route('/add', methods=['POST'])
@template_blp.arguments(AddReportTemplateRequest)
@template_blp.unified_rsp(data_clz=AddReportTemplateRequestRS)
def add_report_template(request: AddReportTemplateRequest):
    response = template_service.add_report_template(request.report_name, request.version, request.google_sheet_url)
    return response

def set_template_active():
    raise NotImplementedError


@template_blp.route('/generate', methods=['GET'])
def generate_report_by_template():
    raise NotImplementedError


@template_blp.route('/list-all', methods=['GET'])
def get_report_template_list_all():
    raise NotImplementedError