from pyramid.config import Configurator
import pyramid_beaker

from syops.lib.application import Application
from syops.ui.modules.default import add_routes as add_default_routes
from syops.ui.modules.apiv1 import add_routes as add_apiv1_routes

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
    Application.bootstrap(settings)
    Application.di()

    # Add modules
    add_default_routes(config)
    add_apiv1_routes(config)

    return config.make_wsgi_app()
