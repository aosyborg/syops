from syopsui.modules.apiv1.views.admin import Admin
from pyramid import httpexceptions

def add_routes(config):
    # Admin
    config.add_route('apiv1:admin:edit-user', '/v1/admin/user/edit')
    config.add_view(Admin,
                    route_name='apiv1:admin:edit-user',
                    attr='edit_user',
                    renderer='json')
    config.add_route('apiv1:admin:delete-user', '/v1/admin/user/delete')
    config.add_view(Admin,
                    route_name='apiv1:admin:delete-user',
                    attr='delete_user',
                    renderer='json')
    config.add_route('apiv1:admin:edit-team', '/v1/admin/team/edit')
    config.add_view(Admin,
                    route_name='apiv1:admin:edit-team',
                    attr='edit_team',
                    renderer='json')
    config.add_route('apiv1:admin:delete-team', '/v1/admin/team/delete')
    config.add_view(Admin,
                    route_name='apiv1:admin:delete-team',
                    attr='delete_team',
                    renderer='json')
