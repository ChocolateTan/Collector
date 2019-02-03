#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
# import warnings
import socket
# import sys
import time
import traceback

# from importlib import reload
import feedparser
import pymongo
import bson
from bson import json_util
from dateutil.parser import parse

from ezpython import UtilFileIO
from ezpython import UtilMongoDB

# from app.ezpython import UtilMongoDB

# warnings.filterwarnings("ignore", category=UnicodeWarning)
# reload(sys)
# sys.setdefaultencoding('utf-8')

socket.setdefaulttimeout(10)

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)

def get_articles(collect_rss_url):
    # while True:
    # print u'start from', collect_rss_url
    # 获得订阅
    feeds = feedparser.parse(collect_rss_url)
    db = UtilMongoDB.UtilMongoDB().get_conn()
    for post in feeds.entries:
        try:
            set_content = {
                "rss_title": feeds['feed']['title'],
                "rss_link": feeds['feed']['link'],
                "title": post.title,
                "link": post.link,
                "description": post.description,
                # "published": post.published,
                "modify_date": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            }
            print(post.title)
            if 'published' in feeds['feed']:
                set_content["published"] = parse(str(feeds['feed']['published'])).strftime('%Y-%m-%d %H:%M:%S')
            elif 'updated' in feeds['feed']:
                set_content["published"] = parse(str(feeds['feed']['updated'])).strftime('%Y-%m-%d %H:%M:%S')

            if 'published' in feeds['feed']:
                set_content["rss_published"] = parse(str(feeds['feed']['published'])).strftime('%Y-%m-%d %H:%M:%S')
            elif 'lastBuildDate' in feeds['feed']:
                set_content["rss_published"] = parse(str(feeds['feed']['lastBuildDate'])).strftime('%Y-%m-%d %H:%M:%S')
            else:
                set_content["rss_published"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            if 'guid' in post:
                set_content["guid"] = post.guid
            elif 'id' in post:
                set_content["guid"] = post.id
            else:
                set_content["guid"] = post.link

            if 'category' in post:
                set_content["category"] = post.category
            else:
                set_content["category"] = ""

            if 'pubDate' in post:
                # print 'published', post.published
                set_content["pubDate"] = parse(str(post.pubDate)).strftime('%Y-%m-%d %H:%M:%S')
                # set_content["pubDate"] = parse(str(post.published)).strftime('%Y-%m-%d %H:%M:%S')
            elif 'published' in post:
                # print 'pubDate', post.pubDate
                set_content["pubDate"] = parse(str(post.published)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                set_content["pubDate"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            # time.strptime(a, "%Y-%m-%d %H:%M:%S")
            time_array = time.strptime(set_content["pubDate"], "%Y-%m-%d %H:%M:%S")
            # print time.mktime(timeArray)
            # 一週內的內容
            # print time.time(), int(time.mktime(time_array)), time.time() - int(time.mktime(time_array)) <= 3600 * 24
            if time.time() - int(time.mktime(time_array)) > 3600 * 24 * 7:
                continue
            # 实现更新数据，如果一些需要更新的，就用$set设置，如果有些如创建日期这种字段，那么使用$setOnInsert更新
            # print 'dd'
            year = parse(set_content["pubDate"]).strftime('%Y')
            month = parse(set_content["pubDate"]).strftime('%m')
            day = parse(set_content["pubDate"]).strftime('%d')

            set_name = 'articles_' + year + "_" + month
            collection = db.collections[set_name]
            collection.update_one({"guid": set_content["guid"]},
                              {
                                  "$set": set_content,
                                  "$setOnInsert":
                                      {
                                          "create_date": time.strftime('%Y-%m-%d %H:%M:%S',
                                                                       time.localtime(time.time()))
                                      }
                              }, upsert=True)
        except Exception as e:
            # print u"post=", post.title
            traceback.print_exc()

    # print u'collect finish', collect_rss_url
    db.close()
    # time.sleep(60)


scrapy_list = (
    # 'http://www.ifanr.com/feed',  # 爱范儿
    {'name':'微软亚洲研究院','url':'http://blog.sina.com.cn/rss/1286528122.xml'},  # 微软亚洲研究院
    {'name':'极客公园','url':'http://www.geekpark.net/rss'},  # 极客公园
    # 'http://www.51cto.com/php/rss.php?typeid=1073',  # 51cto安全频道-新闻
    # 'http://www.51cto.com/php/rss.php?typeid=512',  # 51cto安全频道-全部原创
    # 'http://www.51cto.com/php/rss.php?typeid=552',  # 51cto网络频道-新闻
    # 'http://www.51cto.com/php/rss.php?typeid=481',  # 51cto网络频道-全部原创
    # 'http://www.51cto.com/php/rss.php?typeid=1533',  # 51ctoWeb开发频道-热点推荐
    # 'http://www.51cto.com/php/rss.php?typeid=1553',  # 51cto开发频道-业界资讯
    # 'http://www.51cto.com/php/rss.php?typeid=15',  # 51cto云计算频道-所有原创
    # 'http://www.51cto.com/php/rss.php?typeid=384',  # 51cto云计算频道-新闻
    # 'http://www.51cto.com/php/rss.php?typeid=101',  # 51cto虚拟化频道-技术透析
    # 'http://www.51cto.com/php/rss.php?typeid=39',  # 51cto虚拟化频道-新闻
    # 'http://www.51cto.com/php/rss.php?typeid=548',  # 51cto服务器频道-新闻
    # 'http://www.51cto.com/php/rss.php?typeid=402',  # 51cto数据中心频道-所有文章
    {'name':'51cto','url':'http://www.51cto.com/php/rss.php?typeid=1549'},  # 51cto移动开发频道-热点推荐
    # 'http://www.51cto.com/php/rss.php?typeid=583',  # 51cto移动开发频道-所有原创
    # 'http://www.51cto.com/php/rss.php?typeid=545',  # 51cto操作系统频道-运维经验与工具
    # 'http://www.51cto.com/php/rss.php?typeid=460',  # 51cto操作系统频道-所有原创
    {'name':'google','url':'https://www.blog.google/rss/'},  # google
    {'name':'google android','url':'https://www.blog.google/products/android/rss/'},  # google android
    {'name':'apple','url':'https://developer.apple.com/news/rss/news.rss'},  # apple
    {'name':'oschina','url':'http://www.oschina.net/news/rss'},  # oschina
    # 'https://www.ithome.com/rss/',  # it之家
    {'name':'36kr','url':'http://36kr.com/feed'},  # 36kr
    {'name':'最美應用','url':'http://zuimeia.com/feed/'}#最美應用
)

def get_title_text_style(source, pubDate, guid, category, pubDate_simp, title):
    return '''
<a class="weui-cell weui-cell_access" target="_blank" href="%s" data-title="%s" data-description="%s" data-pubDate="%s" data-guid="%s" data-category="%s">
%s %s
</a>
''' % (guid, title, source, pubDate, guid, category, pubDate_simp, title)


def get_content_text_style():
    return '''---
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
'''


def create_index():
    # pc = crypt()
    db = UtilMongoDB.UtilMongoDB().get_conn().collections
    collection_list = list(db.collection_names())
    collection_list.sort(reverse=True)

    index = 0
    save_dir = os.path.abspath(os.path.join(os.getcwd(), "."))
    for collection_index, collection in enumerate(collection_list):
        # print 'collection=', collection, 'index=', index
        print('collection='+collection)
        result = db[collection].find().sort("pubDate", pymongo.DESCENDING)
        result = list(result)

        for post in result:
            # print u'ggiid', post["pubDate"]
            post["pubDate"] = parse(str(post["pubDate"])).strftime('%Y-%m-%d %H:%M:%S')

        result.sort(key=lambda x: x["pubDate"], reverse=True)

        item_list = ""
        api_post = []
        page_index = 0
        for index,post in enumerate(result):
            try:
                source = map(ord, post["description"])
                # source, pubDate, guid, category, pubDate_simp, title
                po = get_title_text_style(title=post["title"], source=source,
                                          pubDate=parse(str(post["pubDate"])).strftime('%Y-%m-%d %H:%M:%S'),
                                          guid=post["guid"], category=post["category"],
                                          pubDate_simp=parse(str(post["pubDate"])).strftime('%Y-%m-%d')
                                          )
                item_list = item_list + po
                tr_post = post
                import html
                tr_post['description'] = html.escape(tr_post['description'])
                api_post.append(tr_post)
                # 只生成前 1 個月
                if(index % 100 == 0 or index == len(result) - 1) and index != 0 and collection_index == 0:
                    page_index = page_index + 1
                    json_file_name = 'json_'+collection+'_'+ str(page_index) + '.json'
                    api_post = json_util.dumps(api_post)
                    # api_post = bson.BSON.decode(api_post)
                    # import json
                    # api_post = json.dumps(api_post)
                    UtilFileIO.write_file(file_name=json_file_name, save_dir=save_dir+'/api', write_content=api_post)
                    api_post=[]
                    cmd_str = u"git add -A %s" % (save_dir+'/api' + "/" + json_file_name)
                    print(cmd_str)
                    os.system(cmd_str)
                    cmd_str = u'git commit -m "update %s"' % (
                        json_file_name + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    print(cmd_str)
                    os.system(cmd_str)

            except:
                # print u"post=", post.title
                traceback.print_exc()

        # print 'chardet.detect(s)',chardet.detect(post["description"])
        post_content = get_content_text_style() % item_list
        file_name = collection + ".html"
        UtilFileIO.write_file(file_name=file_name, save_dir=save_dir, write_content=post_content)
        cmd_str = u"git add -A %s" % (save_dir + "/" + file_name)
        print(cmd_str)
        os.system(cmd_str)
        cmd_str = u'git commit -m "update %s"' % (
            file_name + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print(cmd_str)
        os.system(cmd_str)

        # print 'len(collection_list)', len(collection_list)
        if collection_index == 0:
            UtilFileIO.write_file(file_name="index.html", save_dir=save_dir, write_content=post_content)
            cmd_str = u"git add -A %s" % (save_dir + "/index.html")
            print(cmd_str)
            os.system(cmd_str)

            cmd_str = u'git commit -m "update %s"' % (
                u"index.html " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            print(cmd_str)
            os.system(cmd_str)

        index = index + 1

def create_index_api():
    api_dir = os.path.abspath(os.path.join(os.getcwd(), "."))
    files = os.listdir(api_dir+'/api')
    apis = []
    
    def char2int(s): 
       return int(s.replace('json_articles_', '').replace('.json', '').replace('_', ''))

    files = sorted(files, key = char2int, reverse=True)

    for item in files:
        url = 'https://chocolatetan.github.io/Collector/api/'+item
        print(url)
        apis.append(url)

    file_name = 'api.html'
    UtilFileIO.write_file(file_name=file_name, save_dir=api_dir, write_content=json_util.dumps(apis))
    cmd_str = u"git add -A %s" % (api_dir + "/" + file_name)
    print(cmd_str)
    os.system(cmd_str)
    cmd_str = u'git commit -m "update %s"' % (file_name + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(cmd_str)
    os.system(cmd_str)

def back_data():
    backup_dir = os.path.abspath(os.path.join(os.getcwd(), ".")) + '/backup'
    backup_name = time.strftime("%Y-%m-%d")
    UtilMongoDB.UtilMongoDB().run_backup(output_dir=backup_dir,
                                         output_name=backup_name)

    cmd_str = u"git add -A %s" % (backup_dir + '/' + backup_name)
    print(cmd_str)
    os.system(cmd_str)


def run():
    print(u"Main thread doing an infinite wait loop...")
    delay_time = 60 * 60 * 1
    file_name = 'collection.html'
    save_dir = os.path.abspath(os.path.join(os.getcwd(), "."))
    UtilFileIO.write_file(file_name, save_dir, json_util.dumps(scrapy_list))
    cmd_str = u"git add -A %s" % (save_dir + "/" + file_name)
    print(cmd_str)
    os.system(cmd_str)
    cmd_str = u'git commit -m "update %s"' % (
                u"collection.html " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(cmd_str)
    os.system(cmd_str)
    while True:
        for item in scrapy_list:
            # print "Thread %s is runing..." % url
            # t = threading.Thread(name='thread_' + url, target=get_articles, args=(url,))
            # t.start()
            # try:
            # thread.start_new_thread(get_articles, (url,))
            # timer = threading.Timer(5, get_articles, (url,))
            # timer.start()
            url = item['url']
            print(str(url))
            get_articles(collect_rss_url=url)
            print(str(url))
            time.sleep(1)
            # except Exception as e:
            #     print u"url=" + url + u"\nError: unable to start thread : ", e

        create_index()
        create_index_api()
        # back_data()
        cmd_str = u"git push"
        print(cmd_str)
        os.system(cmd_str)

        # UtilMongoDB.UtilMongoDB().run_backup(output_dir=os.path.abspath(os.path.join(os.getcwd(), ".")),output_name=)
        time.sleep(delay_time)


# create_index_api()
# create_index()
run()
# UtilMongoDB.UtilMongoDB().run_backup()

# def create_index():
    # pc = crypt()

# db = UtilMongoDB.UtilMongoDB().get_conn().collections
# collection_list = list(db.collection_names())
# collection_list.sort(reverse=True)

# index = 0
# for collection in collection_list:
#     # print 'collection=', collection, 'index=', index
#     result = db[collection].find().sort("pubDate", pymongo.DESCENDING)
#     result = list(result)
#     for post in result:
#         post["pubDate"] = parse(str(post["pubDate"])).strftime('%Y-%m-%d %H:%M:%S')
#     # result.sort(key=lambda x: x["pubDate"], reverse=True)
#
#     item_list = ""
#     index = 0
#     for post in result:
#         if index == 1:
#             break
#         print 'post', post['pubDate']
#         # break
#         index = index + 1
