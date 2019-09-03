# -*- coding: utf-8 -*-


import pymysql
import json
import datetime

from configs_creator import ConfigsCreator


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

class CreateJson(object):
    def __init__(self):
        configs = ConfigsCreator('.conf')
        host = configs.get_value('MYSQL', 'HOST')
        port = configs.get_value('MYSQL', 'PORT')
        user = configs.get_value('MYSQL', 'USER')
        password = configs.get_value('MYSQL', 'PASSWORD')
        dbname = configs.get_value('MYSQL', 'DBNAME')
        charset = configs.get_value('MYSQL', 'CHARSET')

        # 打开数据库连接
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    passwd=password,
                                    db=dbname,
                                    charset=charset,
                                    port=int(port))
        print('connect success')
        
    def create_json(self):
        # 使用cursor()方法获取操作游标 
        cursor = self.conn.cursor()
        # 使用execute方法执行SQL语句
        cursor.execute("select * from tb_post limit 5")

        # 使用 fetchone() 方法获取一条数据
        # data = cursor.fetchone()
        data = cursor.fetchall()                   # 查询结果给data。如果执行：print data 显示结果：（（第一行内容），（第二行内容），（第三行内容），（第四行内容））
        fields = cursor.description

        with open('data.json', 'w') as f:
            json.dump(data, f, cls=DateEncoder)

        f.close()         
        # 关闭数据库连接
        self.conn.close()

if __name__ == "__main__":
    create = CreateJson()
    create.create_json()
