from pyramid.config import Configurator
import pyramid_beaker

import syopsui.modules.default as default_module

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

    # Add modules
    default_module.add_routes(config)

    return config.make_wsgi_app()
