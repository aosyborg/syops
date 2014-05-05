from syopsui.modules.default.views.index import Index
from syopsui.modules.default.views.user import User
from syopsui.modules.default.views.error import Error
from pyramid import httpexceptions

def add_routes(config):
    config.add_route('default:index:index', '/')
    config.add_view(Index, route_name='default:index:index', attr='index')
    config.add_route('default:user:login', '/login')
    config.add_view(User, route_name='default:user:login', attr='login')

    # Error handling
    config.add_view(Error, context=httpexceptions.HTTPNotFound, attr='not_found')
