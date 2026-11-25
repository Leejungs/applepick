"""샘플 데이터 생성기.

실제 마켓 크롤링 없이도 검색, 시세, 가격 추이 차트, 인기 매물, 알림 기능을 모두 확인할 수 있도록
카탈로그의 모든 모델에 대해 최근 4주치 가짜 매물을 만든다. market 이 "Sample" 이라 실제 데이터와 구분된다.

    python crawler/main.py --sources sample
    python crawler/main.py --sources sample --reset   # 기존 샘플 삭제 후 다시 생성
"""
import random
import time

from catalog import BASE_PRICES, CATEGORIES, PRODUCTS
from itembase import ItemBase

REGIONS = ["서울 강남구", "서울 마포구", "서울 송파구", "서울 성북구", "경기 성남시", "경기 수원시", "인천 연수구", "부산 해운대구", "대전 유성구"]
STORAGE = {
    "iphone": ["128GB", "256GB", "512GB"],
    "ipad": ["64GB", "128GB", "256GB"],
    "macbook": ["M2 256GB", "M3 512GB", "M4 512GB"],
    "mac": ["M2 512GB", "M4 1TB"],
}
COLORS = ["블랙", "화이트", "실버", "블루", "스페이스그레이", "미드나이트"]
CONDITIONS = ["S급", "A급", "깨끗합니다", "생활기스 약간", "풀박스", "미개봉급"]
TITLE_TEMPLATES = [
    "{query} {opt} {color} 팝니다",
    "{query} {opt} {cond}",
    "[급처] {query} {opt}",
    "{query} {color} {cond} 판매",
    "{query} {opt} 직거래 택배 가능",
]
DESC_TEMPLATES = [
    "{cond} 입니다. 배터리 효율 좋고 기능 이상 없습니다. 구성품 전부 있어요.",
    "개인 사용하던 제품입니다. 케이스 끼고 사용해서 외관 깨끗합니다. 직거래 우선.",
    "업그레이드로 판매합니다. 박스 포함, 네고는 정중히 사양합니다.",
    "선물받고 몇 번 안 썼습니다. 상태 매우 좋아요. 택배비 별도.",
]


class SampleItem(ItemBase):
    market = "Sample"


class SampleCrawler:
    name = "sample"

    def __init__(self, per_product=30, days=28, seed=2026):
        self.per_product = per_product
        self.days = days
        self.rng = random.Random(seed)

    def crawl_data(self, keyword=None, pages=1):
        """keyword 와 무관하게 카탈로그 전체 샘플을 만든다 (main.py 에서 한 번만 호출)."""
        now = int(time.time())
        items = []
        for cat in CATEGORIES:
            for key, query, _ in cat["products"]:
                for i in range(self.per_product * max(pages, 1)):
                    items.append(self._make(key, query, cat["param"], i, now))
        return items

    def _make(self, key, query, category, i, now):
        rng = self.rng
        age = rng.uniform(0, self.days * 86400)
        weeks_ago = age / (7 * 86400)
        # 오래된 매물일수록 약간 비싸게 (시세 하락 추세) + ±12% 편차
        price = BASE_PRICES[key] * (1 + 0.015 * weeks_ago) * rng.uniform(0.88, 1.12)
        if rng.random() < 0.05:  # 가끔 이상치 (z-score 필터 확인용)
            price *= rng.choice([0.45, 1.8])
        price = max(int(round(price, -3)), 10000)

        fmt = {
            "query": query,
            "opt": rng.choice(STORAGE.get(category, ["정품"])),
            "color": rng.choice(COLORS),
            "cond": rng.choice(CONDITIONS),
        }
        item = SampleItem()
        item.pid = f"{key.replace(' ', '_')}_{i}"
        item.keyword = PRODUCTS[key]
        item.title = rng.choice(TITLE_TEMPLATES).format(**fmt)
        item.desc = rng.choice(DESC_TEMPLATES).format(**fmt)
        item.price = price
        item.date = int(now - age)
        item.views = int(rng.paretovariate(1.5) * 20)
        item.region = rng.choice(REGIONS)
        item.pictures = []  # 프론트엔드가 카테고리 기본 이미지를 보여준다
        item.url = ""
        return item
