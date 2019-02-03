# -*- coding: UTF-8 -*-
# conn = MongoClient('localhost', 27017)
# 连接mydb数据库，没有则自动创建
# db = conn.db_comic
# 使用test_set集合，没有则自动创建
# my_set = db.set_comic
# set_comic_list = db.set_comic_list
import os

import time
from pymongo import MongoClient


class UtilMongoDB:
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = str(port)
        self.conn = MongoClient(host, port)

    def get_conn(self):
        return self.conn

    def run_backup(self, host=None, port=None, username=None, password=None, output_dir=os.getcwd(), output_name=None):
        command = "mongodump"

        if host is not None:
            command += " --host " + host
        else:
            command += " --host " + self.host

        if port is not None:
            command += " --port " + port
        else:
            command += " --port " + self.port

        if username is not None:
            command += " --username " + username

        if password is not None:
            command += " --password " + password

        if output_name is None:
            output_name = output_dir + '/backup/' + time.strftime("%d-%m-%Y-%H-%M-%S")
        else:
            output_name = output_dir + '/' + output_name

        command += " --out " + output_name
        print(command)
        os.system(command)
