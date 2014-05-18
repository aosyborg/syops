from pyramid import httpexceptions

from syops.ui.modules.default.views.index import Index
from syops.ui.modules.default.views.user import User
from syops.ui.modules.default.views.teams import Teams
from syops.ui.modules.default.views.admin import Admin
from syops.ui.modules.default.views.error import Error
from syops.ui.modules.default.views.apps import Apps

def add_routes(config):
    # User
    config.add_route('default:user:login', '/login')
    config.add_view(User, route_name='default:user:login', attr='login')

    # Dashboard
    config.add_route('default:index:index', '/')
    config.add_view(Index, route_name='default:index:index', attr='index')

    # Teams
    config.add_route('default:teams:index', '/teams')
    config.add_view(Teams, route_name='default:teams:index', attr='overview')

    # Apps
    config.add_route('default:apps:index', '/apps')
    config.add_view(Apps, route_name='default:apps:index', attr='overview')

    # Admin
    config.add_route('default:admin:manage-teams', '/admin/teams')
    config.add_view(Admin, route_name='default:admin:manage-teams', attr='manage_teams')
    config.add_route('default:admin:manage-users', '/admin/users')
    config.add_view(Admin, route_name='default:admin:manage-users', attr='manage_users')

    # Error handling
    config.add_view(Error, context=httpexceptions.HTTPNotFound, attr='not_found')
