# -*- coding: utf-8 -*-

from configparser import ConfigParser


class ConfigsCreator(object):

    def __init__(self, filename='path+filename'):
        self.path = filename
        config = ConfigParser()
        config.read(filename)
        self.config = config

    def get_value(self, section, key):
        return self.config.get(section, key)

if __name__ == "__main__":
    configs = ConfigsCreator('.conf')
    host = configs.get_value('MYSQL', 'HOST')
    print(host)
