import configparser

class config:

    config_file_path = 'config.conf'

    def __init__(self,config_file_path) -> None:
        
        config = configparser.ConfigParser()
        config.read(config_file_path)

        self.name = config.get('Settings', 'appName')

