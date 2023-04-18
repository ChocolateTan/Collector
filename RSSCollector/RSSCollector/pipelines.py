# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
from time import strftime, localtime
import json


class RsscollectorPipeline:

    def __init__(self):
        self.ids_seen = set()
        self.itemList = []

    def process_item(self, item, spider):
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。

        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line)
        if item["link"] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        
        if item["pubDate"] < strftime("%Y/%m/%d/ 00:00:00", localtime()):
            raise DropItem("Not today item found: %s" % item)

        self.ids_seen.add(item["link"])
        self.itemList.append(dict(item))
        return item

    def open_spider(self, spider):
        # spider (Spider 对象) – 被开启的spider
        # 可选实现，当spider被开启时，这个方法被调用。
        pass

    def close_spider(self, spider):
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用
        self.itemList
        line = json.dumps(self.itemList, ensure_ascii=False)
        fileName = "./output/items-%s.json" % strftime('%Y-%m-%d',localtime())
        with open(fileName, "w", encoding="utf8") as text_file:
            text_file.write(line)

