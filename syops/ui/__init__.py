from pyramid.config import Configurator
from pyramid.events import NewRequest
import pyramid_beaker

from syops.ui.modules.default import add_routes as add_default_routes
from syops.ui.modules.apiv1 import add_routes as add_apiv1_routes
from syops.ui.plugins import Acl

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application
    """
    # Basic setup
    config = Configurator()
    config.include('pyramid_chameleon') # templating
    config.include('pyramid_beaker') # sessions
    config.add_static_view('public', 'public', cache_max_age=3600)

    # Sessions
    factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(factory)

    # Bootstrap the application
    from syops.lib.application import Application
    Application.bootstrap(settings)

    # Add modules
    add_default_routes(config)
    add_apiv1_routes(config)

    # Add plugins
    config.add_subscriber(Acl(), NewRequest)

    return config.make_wsgi_app()
