from pyramid import httpexceptions

from syops.ui.modules.default.views.index import Index
from syops.ui.modules.default.views.user import User
from syops.ui.modules.default.views.teams import Teams
from syops.ui.modules.default.views.error import Error
from syops.ui.modules.default.views.apps import Apps

def add_routes(config):
    # User
    config.add_route('default:user:login', '/login')
    config.add_view(User, route_name='default:user:login', attr='login')
    config.add_route('default:user:logout', '/logout')
    config.add_view(User, route_name='default:user:logout', attr='logout')
    config.add_route('default:oauth:callback', '/oauth/callback')
    config.add_view(User, route_name='default:oauth:callback', attr='oauth_callback')

    # Dashboard
    config.add_route('default:index:index', '/')
    config.add_view(Index, route_name='default:index:index', attr='index')

    # Teams
    config.add_route('default:teams:index', '/teams')
    config.add_view(Teams, route_name='default:teams:index', attr='overview')

    # Apps
    config.add_route('default:apps:index', '/apps')
    config.add_view(Apps, route_name='default:apps:index', attr='overview')
    config.add_route('default:app:edit', '/app/edit')
    config.add_view(Apps, route_name='default:app:edit', attr='edit')

    # Error handling
    config.add_view(Error, context=httpexceptions.HTTPNotFound, attr='not_found')
