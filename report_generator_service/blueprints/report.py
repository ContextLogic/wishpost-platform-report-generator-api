from wish_flask.base.blueprint import WishBlueprint
from wish_flask.lib.instance_manager import InstanceManager

from report_generator_service.services.report_service import ReportService

report_blp = WishBlueprint(
    'report', __name__, url_prefix='/api/report',
    # micro=True,
    description='Operations on report'
)

report_service: ReportService = InstanceManager.find_obj_proxy(instance_type='report_service')

def generate_report():
    raise NotImplementedError

def generate_op_report():
    raise NotImplementedError