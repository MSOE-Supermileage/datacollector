from __future__ import print_function

import ConfigParser


class ConfigManager:
    def __init__(self, ini_path='datacollector.cfg'):
        self.ini_path = ini_path
        self.configs = dict()
        config = ConfigParser.ConfigParser()
        config.read(ini_path)
        for section in config.sections():
            for name, value in config.items(section):
                if name == 'sensors':
                    self.configs[name] = value.split(',')
                else:
                    self.configs[name] = value

    def __str__(self):
        """
        for debugging
        """
        return str(self.configs)

    def __getitem__(self, index):
        return self.configs[index]

    def get_adb_path(self):
        return self.configs['adbpath']

    def get_log_dir(self):
        path = self.configs['logpath']
        import os
        if not os.path.exists(path):
            os.makedirs(path)
        return path if path.endswith('/') else path + '/'

    def get_car_type(self):
        return self.configs['cartype']

    def get_sensors(self):
        return self.configs['sensors']

    def get_android_inet_address(self):
        return self.configs['host'], int(self.configs['port'])


if __name__ == "__main__":
    cm = ConfigManager()
    print(cm.get_log_dir())
    print(cm.get_adb_path())
    print(cm.get_car_type())
    print(cm.get_sensors())

