from enum import Enum


class UrlSource(Enum):
    # URL_36kr = "https://36kr.com/feed"
    URL_36kr = "https://36kr.com/feed-newsflash"
    # URL_36kr = "https://36kr.com/feed-article"
    URL_BLOG_GOOGLE = "https://blog.google/products/android/rss/"
    URL_MEITUAN = "https://tech.meituan.com/feed/"
    URL_TECHWEB = "http://www.techweb.com.cn/rss/hotnews.xml"

class UrlInfo(object):

    def __init__(self, sourceType, rss, allowedDomains, dateFormat):
        self.sourceType = sourceType
        self.rss = rss
        self.allowedDomains = allowedDomains
        self.dateFormat = dateFormat

NORMAL_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S +%f"
URL_LIST = {
        UrlSource.URL_36kr: UrlInfo(
            UrlSource.URL_36kr,
            UrlSource.URL_36kr.value,
            "36kr.com",
            # 2023-04-14 16:05:18  +0800
            "%Y-%m-%d %H:%M:%S  +%f"
        ),
        UrlSource.URL_BLOG_GOOGLE: UrlInfo(
            UrlSource.URL_BLOG_GOOGLE,
            UrlSource.URL_BLOG_GOOGLE.value,
            "blog.google",
            # Tue, 15 Nov 2022 14:00:00 +0000
            NORMAL_DATE_FORMAT
        ),
        UrlSource.URL_MEITUAN: UrlInfo(
            UrlSource.URL_MEITUAN,
            UrlSource.URL_MEITUAN.value,
            "tech.meituan.com",
            # Tue, 15 Nov 2022 14:00:00 +0000
            NORMAL_DATE_FORMAT
        ),
        UrlSource.URL_TECHWEB: UrlInfo(
            UrlSource.URL_TECHWEB,
            UrlSource.URL_TECHWEB.value,
            "www.techweb.com.cn",
            # Tue, 15 Nov 2022 14:00:00 +0000
            NORMAL_DATE_FORMAT
        )
    }
        

def test_url():
    assert(len(URL_LIST) > 0)

def test_find_url():
    url = "https://36kr.com/feed"
    source = UrlSource(url)
    urlInfo = URL_LIST[source]
    assert(urlInfo.sourceType is UrlSource.URL_36kr)

if __name__ == '__main__':
    test_url()
    test_find_url()
