import logging
from ConfigParser import ConfigParser

from syops.lib.datamanager import DataManager

class Application(object):
    SALT = ''
    PROD_PKG_DIR = ''
    QA_PKG_DIR = ''
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    DATA_MANAGER = None

    @staticmethod
    def bootstrap(settings={}):
        # Parse the config
        config_path = settings.get('config_path', '/opt/syops/config.ini')
        parser = ConfigParser()
        parser.read(config_path)

        # Setup logger
        log_level = parser.get('misc', 'log_level').upper()
        log_level = getattr(logging, log_level, None)
        logging.basicConfig(
            filename='/var/log/syops.log',
            format='%(asctime)s %(message)s',
            level=log_level)

        # Setup data manager
        data_manager = DataManager(parser)
        Application.DATA_MANAGER = data_manager

        # Define packge destinations
        Application.PROD_PKG_DIR = parser.get('misc', 'production_pkgs')
        Application.QA_PKG_DIR = parser.get('misc', 'qa_pkgs')

        # Define salt
        Application.SALT = parser.get('misc', 'salt')

        # AWS
        Application.AWS_ACCESS_KEY_ID = parser.get('aws', 'access_key_id')
        Application.AWS_SECRET_ACCESS_KEY = parser.get('aws', 'secret_access_key')

    @staticmethod
    def di():
        from syops.ui.models import Abstract as model_abstract
        model_abstract.data_manager = Application.DATA_MANAGER
