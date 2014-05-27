from syops.ui.modules.apiv1.views.app import App
from syops.ui.modules.apiv1.views.team import Team
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
    config.add_route('apiv1:app:list_branches', '/v1/app/list_branches')
    config.add_view(App,
                    route_name='apiv1:app:list_branches',
                    attr='list_branches',
                    renderer='json')
    config.add_route('apiv1:app:new_release', '/v1/app/new_release')
    config.add_view(App,
                    route_name='apiv1:app:new_release',
                    attr='new_release',
                    renderer='json')
    config.add_route('apiv1:app:release', '/v1/app/release')
    config.add_view(App,
                    route_name='apiv1:app:release',
                    attr='release',
                    renderer='json')
    config.add_route('apiv1:app:console', '/v1/app/console')
    config.add_view(App,
                    route_name='apiv1:app:console',
                    attr='build_console',
                    renderer='string')

    # Team
    config.add_route('apiv1:team:edit', '/v1/team/edit')
    config.add_view(Team,
                    route_name='apiv1:team:edit',
                    attr='edit',
                    renderer='json')
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
