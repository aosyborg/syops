from ConfigParser import ConfigParser

from syopsui.library.datamanager import DataManager
from syopsui.models import Abstract as model_abstract

class Application(object):
    SALT = ''
    PROD_PKG_DIR = ''
    QA_PKG_DIR = ''
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    def bootstrap(self, settings={}):
        # Parse the config
        config_path = settings.get('config_path', '/opt/syops/config.ini')
        parser = ConfigParser()
        parser.read(config_path)

        # Setup data manager
        data_manager = DataManager(parser)
        model_abstract.data_manager = data_manager

        # Define packge destinations
        Application.PROD_PKG_DIR = parser.get('misc', 'production_pkgs')
        Application.QA_PKG_DIR = parser.get('misc', 'qa_pkgs')

        # Define salt
        Application.SALT = parser.get('misc', 'salt')

        # AWS
        Application.AWS_ACCESS_KEY_ID = parser.get('aws', 'access_key_id')
        Application.AWS_SECRET_ACCESS_KEY = parser.get('aws', 'secret_access_key')
