"""상품 카탈로그 (백엔드 API, 크롤러, 프론트엔드가 공유하는 단일 소스).

- key       : API/URL 에서 쓰는 영문 키 (예: "iPhone 15 Pro")
- query     : Elasticsearch 검색에 쓰는 한글 검색어
- base_price: 샘플 데이터 생성 시 기준이 되는 대략적인 중고 시세 (원)

프론트엔드는 GET /api/products 로 이 목록을 받아서 화면을 구성한다.
"""

CATEGORIES = [
    {
        "param": "mac",
        "name": "Mac",
        "products": [
            ("Mac mini", "맥미니", 550000),
            ("Mac Studio", "맥스튜디오", 1900000),
            ("Mac Pro", "맥프로", 3500000),
            ("iMac", "아이맥", 900000),
        ],
    },
    {
        "param": "macbook",
        "name": "MacBook",
        "products": [
            ("MacBook Air", "맥북 에어", 800000),
            ("MacBook Pro", "맥북 프로", 1500000),
        ],
    },
    {
        "param": "iphone",
        "name": "iPhone",
        "products": [
            ("iPhone 11", "아이폰 11", 220000),
            ("iPhone 11 Pro", "아이폰 11 프로", 280000),
            ("iPhone 11 Pro Max", "아이폰 11 프로 맥스", 320000),
            ("iPhone 12 mini", "아이폰 12 미니", 250000),
            ("iPhone 12", "아이폰 12", 300000),
            ("iPhone 12 Pro", "아이폰 12 프로", 380000),
            ("iPhone 12 Pro Max", "아이폰 12 프로 맥스", 430000),
            ("iPhone 13 mini", "아이폰 13 미니", 350000),
            ("iPhone 13", "아이폰 13", 400000),
            ("iPhone 13 Pro", "아이폰 13 프로", 500000),
            ("iPhone 13 Pro Max", "아이폰 13 프로 맥스", 580000),
            ("iPhone 14", "아이폰 14", 500000),
            ("iPhone 14 Plus", "아이폰 14 플러스", 550000),
            ("iPhone 14 Pro", "아이폰 14 프로", 650000),
            ("iPhone 14 Pro Max", "아이폰 14 프로 맥스", 750000),
            ("iPhone 15", "아이폰 15", 650000),
            ("iPhone 15 Plus", "아이폰 15 플러스", 700000),
            ("iPhone 15 Pro", "아이폰 15 프로", 850000),
            ("iPhone 15 Pro Max", "아이폰 15 프로 맥스", 950000),
            ("iPhone 16", "아이폰 16", 800000),
            ("iPhone 16 Plus", "아이폰 16 플러스", 850000),
            ("iPhone 16 Pro", "아이폰 16 프로", 1050000),
            ("iPhone 16 Pro Max", "아이폰 16 프로 맥스", 1200000),
            ("iPhone 16e", "아이폰 16e", 600000),
            ("iPhone 17", "아이폰 17", 1000000),
            ("iPhone Air", "아이폰 에어", 1150000),
            ("iPhone 17 Pro", "아이폰 17 프로", 1350000),
            ("iPhone 17 Pro Max", "아이폰 17 프로 맥스", 1550000),
            ("iPhone SE Gen2", "아이폰 SE 2세대", 120000),
            ("iPhone SE Gen3", "아이폰 SE 3세대", 220000),
        ],
    },
    {
        "param": "ipad",
        "name": "iPad",
        "products": [
            ("iPad", "아이패드", 300000),
            ("iPad Air", "아이패드 에어", 500000),
            ("iPad mini", "아이패드 미니", 400000),
            ("iPad Pro", "아이패드 프로", 800000),
            ("iPad Pro(12.9)", "아이패드 프로 12.9", 950000),
            ("iPad Pro(13)", "아이패드 프로 13", 1300000),
        ],
    },
    {
        "param": "applewatch",
        "name": "Apple Watch",
        "products": [
            ("Series 6", "애플워치 6", 150000),
            ("Series 7", "애플워치 7", 200000),
            ("Series 8", "애플워치 8", 250000),
            ("Series 9", "애플워치 9", 320000),
            ("Series 10", "애플워치 10", 400000),
            ("Series 11", "애플워치 11", 480000),
            ("SE", "애플워치 SE", 180000),
            ("Ultra", "애플워치 울트라", 500000),
            ("Ultra 2", "애플워치 울트라 2", 700000),
            ("Ultra 3", "애플워치 울트라 3", 900000),
        ],
    },
    {
        "param": "airpods",
        "name": "AirPods",
        "products": [
            ("AirPods 2Gen", "에어팟 2세대", 60000),
            ("AirPods 3Gen", "에어팟 3세대", 100000),
            ("AirPods 4", "에어팟 4", 130000),
            ("AirPods Pro", "에어팟 프로", 100000),
            ("AirPods Pro 2", "에어팟 프로 2", 180000),
            ("AirPods Pro 3", "에어팟 프로 3", 260000),
            ("AirPods Max", "에어팟 맥스", 400000),
        ],
    },
]

# 영문 키 -> 한글 검색어
PRODUCTS = {key: query for cat in CATEGORIES for key, query, _ in cat["products"]}

# 영문 키 -> 기준 시세 (샘플 데이터용)
BASE_PRICES = {key: price for cat in CATEGORIES for key, _, price in cat["products"]}

# 영문 키 -> 카테고리 param
PRODUCT_CATEGORY = {key: cat["param"] for cat in CATEGORIES for key, _, _ in cat["products"]}


def catalog_for_client():
    """프론트엔드에 내려줄 형태로 변환."""
    return [
        {
            "param": cat["param"],
            "name": cat["name"],
            "products": [{"key": key, "label": label(key, cat["param"])} for key, _, _ in cat["products"]],
        }
        for cat in CATEGORIES
    ]


def label(key, category):
    """화면에 보여줄 이름. 애플워치는 'Series 9' 대신 'Apple Watch Series 9'."""
    if category == "applewatch":
        return f"Apple Watch {key}"
    return key


# 검색어가 겹치는 다른 제품군 (예: '맥 프로' 검색에 '맥북 프로' 가 섞이지 않도록)
EXTRA_EXCLUSIONS = {
    "Mac Pro": ["맥북", "아이맥"],
    "Mac Studio": ["맥북"],
}


def exclusion_terms(key):
    """상위 모델 매물이 섞이지 않도록 제목에서 제외할 단어.

    예) 'iPhone 15'(아이폰 15) -> 플러스, 프로 / 'iPhone 15 Pro' -> 맥스
    """
    base = PRODUCTS[key]
    terms = set(EXTRA_EXCLUSIONS.get(key, []))
    for other in PRODUCTS.values():
        if other == base or not other.startswith(base):
            continue
        rest = other[len(base) :]
        if rest.startswith(" "):
            terms.add(rest.split()[0])  # '아이폰 15' + ' 프로'
        elif not rest[0].isdigit():
            terms.add(rest.split()[0])  # '아이폰 16' + 'e' (형태소 분석 시 16 / e 로 분리됨)
    return sorted(terms)
