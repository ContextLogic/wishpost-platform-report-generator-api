# Service layer for user. To access DAO layer.
from report_generator_service.models.user import FakeUser as User
from wish_flask.base.service import BaseService


class UserService(BaseService):
    # Auto init a singleton instance.
    # You can get the instance by:
    # >> InstanceManager.find_obj_proxy(instance_type='user_service')
    # where instance_type is the snake case of class name.
    auto_init = True

    def find_user(self, name):
        user = User.find_one(
            {"username": name},
        )
        return user
