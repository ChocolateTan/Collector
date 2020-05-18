# -*- coding: utf-8 -*-


import pymysql
import json
import datetime
import os

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
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        # cursor = self.conn.cursor()
        # 使用execute方法执行SQL语句
        cursor.execute("select * from tb_post limit 5")

        # 使用 fetchone() 方法获取一条数据
        # data = cursor.fetchone()
        data = cursor.fetchall()                   # 查询结果给data。如果执行：print data 显示结果：（（第一行内容），（第二行内容），（第三行内容），（第四行内容））
        # fields = cursor.description

        with open('data.json', 'w') as f:
            json.dump(data, f, cls=DateEncoder)

        f.close()         
        # 关闭数据库连接
        self.conn.close()
    
    def create_md(self, month):
        page = 1
        path = '../output/' + month
        if os.path.exists(path) == False:
            os.makedirs(path)
        self.create_md_file(path, month, page)
    
    def create_md_file(self, path, month, page):
        page_size = 50
        idx_start = (page - 1) * page_size
        # 使用cursor()方法获取操作游标 
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 使用execute方法执行SQL语句
        sql = "select * from tb_post where DATE_FORMAT(pub_date,'%Y-%m') = '" + month + "' order by pub_date desc limit " + str(idx_start) + "," + str(page_size)
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        if data is None or len(data) == 0:
            return

        md_name = str(page) + '.md'
        cur_path = path + '/page/'
        if os.path.exists(cur_path) == False:
            os.makedirs(cur_path)
        filename = cur_path + '/' + md_name

        with open(filename, 'w') as f:
            for item in data:
                print(item['title'])
                link = item['link']
                date_str = ''
                if item['pub_date'] != '0000-00-00 00:00:00':
                    date_str = item['pub_date'].strftime('%Y-%m-%d %H:%M:%S') + ' '
                f.write('## <a href="' + link + '" target="_blank">' + item['title'].strip()+'</a>\n')
                f.write(date_str + '\n')
                # f.write(date_str + '  ' + '<a href="#" id="a_' + item['postid'] + '" onclick="onClickAction(\''+month+'\',\'' + item['postid'] + '\')">[收起]</a>\n')
                # f.write('<div class="collector_content" id="div_'+ item['postid'] +'" onclick="onClickAction(\''+month+'\',\'' + item['postid']+'\')">\n')
                # # f.write(item['description'].strip() + '\n')
                # f.write('</div>\n')
                # f.write('<script src="../../collectorjs.js"></script>\n')
                # f.write('<script>\n')
                # f.write('window.onload=function(){\n')
                # f.write('    let storage = window.localStorage;\n')
                # f.write('    var local = JSON.parse(storage.getItem(\'month_' + month + '\'));\n')
                # f.write('    if (local) {\n')
                # f.write('        var div_list = document.getElementsByClassName("collector_content");\n')
                # f.write('        for (i = 0; i < div_list.length; i++) {\n')
                # f.write('            var item = div_list[i];\n')
                # f.write('            var id = item.id.replace(\'div_\', \'\');\n')
                # f.write('            if(local.indexOf(id) > -1){\n')
                # f.write('                var eObject = document.getElementById(\'div_\'+id);\n')
                # f.write('                var aObject = document.getElementById(\'a_\'+id);\n')
                # f.write('                eObject.style.display = \'none\';\n')
                # f.write('                aObject.innerHTML = \'[收起]\';\n')
                # f.write('                eObject.innerHTML = item[\'description\'].strip();\n')
                # f.write('            }\n')
                # f.write('        }\n')
                # f.write('    }\n')
                # f.write('}\n')
                # f.write('</script>\n')

        f.close()         
        page = page + 1
        self.create_md_file(path, month, page)
        # 关闭数据库连接
        # self.conn.close()

if __name__ == "__main__":
    create = CreateJson()
    today = datetime.date.today()
    today = today.strftime('%Y-%m')
    create.create_md(today)
    # create.create_md('0000-00')
    # create.create_md('2016-04')
    # create.create_md('2016-07')
    # create.create_md('2016-08')
    # create.create_md('2016-10')
    # create.create_md('2016-11')
    # create.create_md('2017-02')
    # create.create_md('2017-03')
    # create.create_md('2017-05')
    # create.create_md('2017-11')
    # create.create_md('2017-12')
    # create.create_md('2018-03')
    # create.create_md('2018-04')
    # create.create_md('2018-05')
    # create.create_md('2018-06')
    # create.create_md('2018-07')
    # create.create_md('2018-08')
    # create.create_md('2018-09')
    # create.create_md('2018-10')
    # create.create_md('2018-11')
    # create.create_md('2018-12')
    # create.create_md('2019-01')
    # create.create_md('2019-02')
    # create.create_md('2019-03')
    # create.create_md('2019-04')
    # create.create_md('2019-05')
    # create.create_md('2019-06')
    # create.create_md('2019-07')
    # create.create_md('2019-08')
    # create.create_md('2019-09')
    create.conn.close()
    
