"""번개장터 크롤러 (2026년 기준 웹 API).

번개장터 웹(m.bunjang.co.kr)이 사용하는 API 를 호출한다. 공식 공개 API 가 아니므로
응답 구조가 바뀌면 이 파일만 수정하면 된다.

- 검색: GET /api/search/v8/web/search?q=...&policyKey=pw.product.keyword&sort=latest&size=..&cursor=..
- 상세: GET /api/pms/v1/products/{pid}/detail/web
"""
import datetime
import logging
import time

import requests

from itembase import ItemBase

log = logging.getLogger(__name__)

API = "https://api.bunjang.co.kr"
PAGE_SIZE = 60
IMAGE_RES = "400"
REQUEST_DELAY = 0.3  # 상세 조회 사이 간격 (초). 서버에 부담을 주지 않도록 유지할 것
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; used-price-research/1.0)", "Accept": "application/json"}


class BunjangItem(ItemBase):
    market = "Bunjang"


class BunjangCrawler:
    name = "bunjang"

    def __init__(self, fetch_detail=True):
        self.fetch_detail = fetch_detail
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def crawl_data(self, keyword, pages):
        items = []
        cursor = None
        for _ in range(pages):
            products, cursor = self._search(keyword, cursor)
            for product in products:
                item = self._from_search(product, keyword)
                if self.fetch_detail:
                    self._fill_detail(item)
                    time.sleep(REQUEST_DELAY)
                items.append(item)
            if not cursor:
                break
        return items

    def _search(self, keyword, cursor):
        params = {"q": keyword, "policyKey": "pw.product.keyword", "sort": "latest", "size": PAGE_SIZE}
        if cursor:
            params["cursor"] = cursor
        res = self.session.get(f"{API}/api/search/v8/web/search", params=params, timeout=15)
        res.raise_for_status()
        grid = res.json()["data"]["responses"]["mainGrid"]["searchResponse"]
        products = [
            p
            for p in grid.get("data", [])
            if p.get("type") == "PRODUCT" and not p.get("ad") and p.get("status", "SELLING") == "SELLING"
        ]
        return products, grid.get("nextCursor")

    def _from_search(self, product, keyword):
        item = BunjangItem()
        item.keyword = keyword
        item.pid = str(product["pid"])
        item.url = f"https://m.bunjang.co.kr/products/{item.pid}"
        item.title = product.get("name", "")
        item.price = int(product.get("price") or 0)
        item.date = _parse_time(product.get("updatedAt"))
        if product.get("productImage"):
            item.pictures = [product["productImage"].replace("{res}", IMAGE_RES)]
        return item

    def _fill_detail(self, item):
        try:
            res = self.session.get(f"{API}/api/pms/v1/products/{item.pid}/detail/web", timeout=15)
            res.raise_for_status()
            p = res.json()["data"]["product"]
        except Exception as e:  # 상세가 실패해도 검색 결과만으로 저장
            log.debug("상세 조회 실패 pid=%s: %s", item.pid, e)
            return

        item.title = p.get("name", item.title)
        item.desc = p.get("description", "")
        item.price = int(p.get("price") or item.price)
        item.views = int((p.get("metrics") or {}).get("viewCount") or 0)
        item.date = _parse_time(p.get("updatedAt")) or item.date
        template, count = p.get("imageUrl"), int(p.get("imageCount") or 0)
        if template and count:
            item.pictures = [
                template.replace("{cnt}", str(i)).replace("{res}", IMAGE_RES) for i in range(1, count + 1)
            ]
        item.region = _region(p.get("trade") or {})


def _parse_time(value):
    if not value:
        return int(time.time())
    return int(datetime.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())


def _region(trade):
    """직거래 지역이 있으면 첫 번째 지역명."""
    for key in ("tradeLocations", "locations"):
        locations = trade.get(key) or []
        if locations and isinstance(locations[0], dict):
            return locations[0].get("name") or locations[0].get("address") or ""
    return ""
