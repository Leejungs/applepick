"""당근 크롤러 (비활성화).

2022년에 쓰던 www.daangn.com/search/... 페이지는 사라졌고, 현재 당근 웹은 자동화된 요청을
CloudFront 에서 차단(403)한다. 차단을 우회하는 방식은 쓰지 않는다.

당근이 허용하는 데이터 제공 방식(제휴, 공식 API 등)이 생기면 이 클래스의 crawl_data 를
구현하고 crawler.py 의 SOURCES 에 등록하면 된다. 반환 형식은 BunjangCrawler 와 같다.
"""
import logging

from itembase import ItemBase

log = logging.getLogger(__name__)


class DaangnItem(ItemBase):
    market = "Daangn"


class DaangnCrawler:
    name = "daangn"

    def crawl_data(self, keyword, pages):
        log.warning("당근은 현재 자동 수집이 차단되어 있어 건너뜁니다. (crawler/daangn.py 참고)")
        return []
