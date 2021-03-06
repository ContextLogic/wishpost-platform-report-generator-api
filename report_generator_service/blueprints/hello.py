from collections import defaultdict

from wish_flask.base.view import WishMethodView
from wish_flask.base.blueprint import WishBlueprint
from wish_flask.lib.instance_manager import InstanceManager

from report_generator_service.schemas.hello import NameQuerySchema, HelloMsgSchema
from report_generator_service.services.user_service import UserService


hello_blp = WishBlueprint(
    'hello', __name__, url_prefix='/api/hello',
    description='Operations on hello'
)

user_service: UserService = InstanceManager.find_obj_proxy(instance_type='user_service')


@hello_blp.route('/')
class Hello(WishMethodView):

    @hello_blp.arguments(NameQuerySchema, location='query')
    @hello_blp.unified_rsp(data_clz=HelloMsgSchema)
    def get(self, name_query: NameQuerySchema):
        name = name_query.name
        user = user_service.find_user(name)
        if user:
            message = f'Hello {user.username} ({user.email})'
        else:
            message = f'No such user {name}'
        return {'message': message}


record = defaultdict(lambda : 0)

# We can decorate a function directly.
@hello_blp.route('/record', methods=['POST'])
@hello_blp.arguments(NameQuerySchema)
@hello_blp.unified_rsp(data_clz=HelloMsgSchema)
def update_pets(query):
    """Record call times"""
    name = query.name
    record[name] += 1
    return {'message': f'{name} called {record[name]} times'}
