from syops.ui.modules.apiv1.views.app import App
from syops.ui.modules.apiv1.views.team import Team
from syops.ui.modules.apiv1.views.admin import Admin
from pyramid import httpexceptions

def add_routes(config):
    # App
    config.add_route('apiv1:app:edit', '/v1/app/edit')
    config.add_view(App,
                    route_name='apiv1:app:edit',
                    attr='edit',
                    renderer='json')
    config.add_route('apiv1:app:delete', '/v1/app/delete')
    config.add_view(App,
                    route_name='apiv1:app:delete',
                    attr='delete',
                    renderer='json')
    config.add_route('apiv1:app:new_release', '/v1/app/new_release')
    config.add_view(App,
                    route_name='apiv1:app:new_release',
                    attr='new_release',
                    renderer='json')

    # Team
    config.add_route('apiv1:team:list_repos', '/v1/team/list_repos')
    config.add_view(Team,
                    route_name='apiv1:team:list_repos',
                    attr='list_repos',
                    renderer='json')
    config.add_route('apiv1:team:list_orgs', '/v1/team/list_orgs')
    config.add_view(Team,
                    route_name='apiv1:team:list_orgs',
                    attr='list_orgs',
                    renderer='json')

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
