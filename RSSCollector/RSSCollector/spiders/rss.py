import scrapy
from scrapy.spiders import XMLFeedSpider
import re
from datetime import datetime

from rssconfig.urlinfo import URL_LIST
from rssconfig.urlinfo import UrlSource
from models.rssitem import RssItem


class RssSpider(XMLFeedSpider):
    name = "rss"
    allowed_domains = [URL_LIST[item].allowedDomains for item in list(UrlSource)]
    itertag = 'item'

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/75.0.3770.100 Safari/537.36',
        'Content-Type': 'application/xml'
    }
    cookies = {'_T_WM': '98075578786', 'WEIBOCN_WM': '3349', 'H5_wentry': 'H5', 'backURL': 'https%3A%2F%2Fm.weibo.cn%2Fdetail%2F4396824548695177', 'ALF': '1568417075', 'SCF': 'Ap5VqXy_BfNHBEUteiYtYDRa04jqF4QPJBULzWo7c1c_noO0GpnJW3BqhIkH7JXJSwWhL0qSg69_Vici5P7NbmY.', 'SUB': '_2A25wUOt6DeRhGeFM41AT9y3LyDSIHXVTuvUyrDV6PUJbktANLVXzkW1NQL_2tT4ZmobAs5b6HbIQwSRXHjjiRkzj', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWyDsTszIBJPBJ6gn7ccSM5JpX5K-hUgL.FoME1hzES0eNe0n2dJLoI0YLxK-L1K.L1KMLxK-L1KzLBoeLxK-L12BLBK2LxK-LBK-LB.BLxK-LBK-LB.BLxKnLB-qLBoBLxKnLB-qLBoBt', 'SUHB': '0S7CWHWuRz1aWf', 'SSOLoginState': '1565825835'}

    def start_requests(self):
        urls = [item.value for item in list(UrlSource)]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers,)

    def adapt_response(self, response):
        page = response.url.split("/")[-2]
        filename = 'rsssource/quotes-%s.xml' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        return response

    def parse_node(self, response, node):
        urlSource = URL_LIST[UrlSource(response.url)]

        title = node.xpath("title/text()").extract_first()
        link = node.xpath("link/text()").extract_first()
        pubDate = node.xpath("pubDate/text()").extract_first()

        self.logger.debug(title)
        self.logger.debug(link)
        resultPubDate = datetime.strftime(datetime.strptime(pubDate, urlSource.dateFormat), "%Y-%m-%d %H:%M:%S")
        self.logger.debug(resultPubDate)

        # desc = node.xpath("description/text()").extract_first()
        # pattern = re.compile(r'<[^>]+>',re.S)
        # resultDesc = pattern.sub('', desc)
        # self.logger.debug(resultDesc)
        
        item = RssItem()
        item["title"] = title
        item["link"] = link
        item["pubDate"] = resultPubDate
        yield item

# class RssSpider(scrapy.Spider):
#     name = "rss"
#     allowed_domains = ["36kr.com", "blog.google"]
#     # start_urls = ["https://36kr.com/feed", "https://blog.google/products/android/rss/"]

#     headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/75.0.3770.100 Safari/537.36',
#         'Content-Type': 'application/xml'
#     }
#     cookies = {'_T_WM': '98075578786', 'WEIBOCN_WM': '3349', 'H5_wentry': 'H5', 'backURL': 'https%3A%2F%2Fm.weibo.cn%2Fdetail%2F4396824548695177', 'ALF': '1568417075', 'SCF': 'Ap5VqXy_BfNHBEUteiYtYDRa04jqF4QPJBULzWo7c1c_noO0GpnJW3BqhIkH7JXJSwWhL0qSg69_Vici5P7NbmY.', 'SUB': '_2A25wUOt6DeRhGeFM41AT9y3LyDSIHXVTuvUyrDV6PUJbktANLVXzkW1NQL_2tT4ZmobAs5b6HbIQwSRXHjjiRkzj', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWyDsTszIBJPBJ6gn7ccSM5JpX5K-hUgL.FoME1hzES0eNe0n2dJLoI0YLxK-L1K.L1KMLxK-L1KzLBoeLxK-L12BLBK2LxK-LBK-LB.BLxK-LBK-LB.BLxKnLB-qLBoBLxKnLB-qLBoBt', 'SUHB': '0S7CWHWuRz1aWf', 'SSOLoginState': '1565825835'}

#     def start_requests(self):
#         urls = [
#             "https://36kr.com/feed", 
#             "https://blog.google/products/android/rss/"
#             ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse, headers=self.headers,)

#     def parse(self, response):
#         self.logger.info("aaa")
#         self.logger.info(response.body.decode("utf-8"))
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)
