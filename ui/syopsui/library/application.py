from ConfigParser import ConfigParser

from syopsui.library.datamanager import DataManager
from syopsui.models import Abstract as model_abstract

class Application(object):
    SALT = None

    def bootstrap(self, settings={}):
        # Parse the config
        config_path = settings.get('config_path', '/opt/syops/config.ini')
        parser = ConfigParser()
        parser.read(config_path)

        # Setup data manager
        data_manager = DataManager(parser)
        model_abstract.data_manager = data_manager

        # Define salt
        Application.SALT = parser.get('misc', 'salt')
