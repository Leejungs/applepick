import logging

from bunjang import BunjangCrawler
from daangn import DaangnCrawler
from sample import SampleCrawler

log = logging.getLogger(__name__)

# 사용 가능한 수집 소스. 새 마켓을 추가하면 여기에 등록한다.
SOURCES = {
    "bunjang": BunjangCrawler,
    "daangn": DaangnCrawler,
    "sample": SampleCrawler,
}


class Crawler:
    def __init__(self):
        self.crawlers = []

    def add_crawler(self, crawler):
        self.crawlers.append(crawler)

    def crawl(self, keyword, pages):
        data = []
        for crawler in self.crawlers:
            try:
                data += crawler.crawl_data(keyword, pages)
            except Exception as e:  # 한 소스가 실패해도 나머지는 계속
                log.error("[%s] '%s' 수집 실패: %s", crawler.name, keyword, e)
        return data
