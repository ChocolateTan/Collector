#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys

import pymongo
from bson import ObjectId
from dateutil.parser import parse

sys.path.append("..")
from ezpython import UtilMongoDB, UtilFileIO

reload(sys)
sys.setdefaultencoding('utf-8')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



def create_index():
    # pc = crypt()
    db = UtilMongoDB.UtilMongoDB().get_conn().collections
    collection_list = list(db.collection_names())

    for collection in collection_list:
        result = db[collection].find().sort("pubDate", pymongo.DESCENDING)
        result = list(result)

        item_list = ""
        for post in result:
            # print type(JSONEncoder().encode(post))
            source = map(ord, post["description"])

            po = '''
        <a class="weui-cell weui-cell_access" onclick="showDetail(this)" href="#" data-title="%s" data-description="%s" data-pubDate="%s" data-guid="%s" data-category="%s">
        %s %s
        </a>
''' % (post["title"], source,
       parse(str(post["pubDate"])).strftime('%Y-%m-%d %H:%M:%S'),
       post["guid"], post["category"], parse(str(post["pubDate"])).strftime('%Y-%m-%d'),
       post["title"])
            item_list = item_list + po
        # print 'chardet.detect(s)',chardet.detect(post["description"])
        post_content = '''---
layout: null
---
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=0">
        <title>Collector</title>
        <!-- 引入 WeUI -->
        {%% include head %%}
    </head>
<body>
    {%% include dialogdetail.html %%}
    <div class="weui-cells">
        %s
    </div>
</body>
</html>
''' % item_list
        UtilFileIO.write_file(file_name=collection + ".html", save_dir=os.path.abspath(os.path.join(os.getcwd(), "..")),
                              write_content=post_content)


create_index()
