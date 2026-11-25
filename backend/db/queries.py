"""API 와 크롤러(알림)에서 공통으로 쓰는 Elasticsearch 쿼리 빌더."""
from config import FILTER_KEYWORDS, MINIMUM_PRICE

SEARCH_FIELDS = ["title^2", "desc", "keyword"]


def _excluded():
    # 설명에는 '케이스 포함' 같은 문구가 흔하므로 제목만 검사한다
    return [{"match_phrase": {"title": kw}} for kw in FILTER_KEYWORDS]


def product_query(text=None, date_gte=None, date_lt=None, price_lte=None, exclude_title=()):
    """본품 매물만 검색하는 bool 쿼리.

    text 가 있으면 검색어의 모든 토큰이 제목에 들어간 매물만 찾는다
    (예: '아이폰 15 프로' -> 아이폰, 15, 프로 를 모두 포함).
    """
    must = (
        # 모델명은 제목에서만 확인한다 (설명의 '에어팟 프로2 증정' 같은 문구로 다른 제품이 섞이지 않도록)
        {"multi_match": {"query": text, "fields": ["title"], "operator": "and"}}
        if text
        else {"match_all": {}}
    )

    price_range = {"gte": MINIMUM_PRICE}
    if price_lte is not None:
        price_range["lte"] = price_lte

    filters = [{"range": {"price": price_range}}]
    if date_gte is not None or date_lt is not None:
        date_range = {}
        if date_gte is not None:
            date_range["gte"] = int(date_gte)
        if date_lt is not None:
            date_range["lt"] = int(date_lt)
        filters.append({"range": {"date": date_range}})

    must_not = _excluded() + [{"match": {"title": term}} for term in exclude_title]
    return {"bool": {"must": must, "must_not": must_not, "filter": filters}}


def catalog_query(key, **kwargs):
    """카탈로그 키(예: 'iPhone 15 Pro')로 해당 모델 매물만 찾는 쿼리."""
    from catalog import PRODUCTS, exclusion_terms

    return product_query(PRODUCTS[key], exclude_title=exclusion_terms(key), **kwargs)
